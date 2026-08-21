"""Os direitos do titular, e a prova de que a exclusão apaga mesmo.

O teste que mais importa aqui é `teste_apagar_nao_deixa_nada_para_tras`. Uma
exclusão que esquece uma tabela não quebra nada, não aparece em log nenhum, e
deixa dado de saúde de alguém que pediu para ser esquecido guardado
indefinidamente.
"""

from __future__ import annotations

from datetime import date, timedelta

import pytest
from sqlalchemy import inspect, text

from jf.modelos import Papel
from jf.privacidade import versao_do_termo


@pytest.fixture
def cenario(criar_usuario, criar_aluno):
    joao = criar_usuario("João Filho", "joao@exemplo.com", Papel.TREINADOR)
    # Sem consentimento de propósito: é o que estes testes exercitam.
    return {
        "joao": joao,
        "filipe": criar_aluno("Filipe", "filipe@exemplo.com", joao, consentiu=False),
        "outro": criar_aluno("Outro Aluno", "outro@exemplo.com", joao, consentiu=False),
    }


@pytest.fixture
def consentido(cliente, cenario):
    """Um aluno que já aceitou o termo."""
    sessao = cliente("filipe@exemplo.com")
    assert sessao.post("/api/eu/consentimento").json()["consentido"] is True
    return sessao


def segunda(recuo: int = 0) -> str:
    hoje = date.today()
    return (hoje - timedelta(days=hoje.weekday(), weeks=recuo)).isoformat()


# ------------------------------------------------------------------- o termo


def teste_o_termo_e_publico(cliente, cenario):
    """Precisa dar para ler antes de aceitar — e antes de ter conta."""
    resposta = cliente().get("/api/termo")
    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["versao"] == versao_do_termo()
    assert "dado pessoal sensível" in corpo["texto"]


def teste_a_versao_e_o_hash_do_texto(monkeypatch, tmp_path):
    """Editar o termo muda a versão sozinho.

    É o que impede o caso silencioso: alguém reescreve o texto, esquece de
    incrementar um número, e consentimentos antigos passam a valer para um
    texto que ninguém leu.
    """
    from jf import privacidade

    antes = versao_do_termo()

    outro = tmp_path / "termo.md"
    outro.write_text("# Outro texto qualquer", encoding="utf-8")
    monkeypatch.setattr(privacidade, "TERMO", outro)
    privacidade.texto_do_termo.cache_clear()
    privacidade.versao_do_termo.cache_clear()

    assert privacidade.versao_do_termo() != antes

    privacidade.texto_do_termo.cache_clear()
    privacidade.versao_do_termo.cache_clear()


# ----------------------------------------------------------- o consentimento


def teste_aceitar_e_ver_o_estado(cliente, cenario):
    sessao = cliente("filipe@exemplo.com")
    assert sessao.get("/api/eu/consentimento").json()["consentido"] is False

    corpo = sessao.post("/api/eu/consentimento").json()
    assert corpo["consentido"] is True
    assert corpo["aceito_em"] is not None
    assert corpo["versao_atual"] == versao_do_termo()


def teste_aceitar_duas_vezes_nao_duplica(consentido):
    consentido.post("/api/eu/consentimento")
    dados = consentido.get("/api/eu/dados").json()
    assert len(dados["consentimentos"]) == 1


def teste_revogar_para_de_aceitar_dado_novo(consentido, cenario):
    """O ponto do consentimento: sem ele o app *recusa*, não aceita e lamenta."""
    alvo = f"/api/alunos/{cenario['filipe'].id}/checkins"
    assert consentido.post(alvo, json={"peso_kg": 84}).status_code == 201

    assert consentido.request("DELETE", "/api/eu/consentimento").json()["consentido"] is False

    recusado = consentido.post(
        alvo, json={"semana": segunda(1), "peso_kg": 83}
    )
    assert recusado.status_code == 451
    assert "termo" in recusado.json()["detail"]


def teste_revogar_nao_apaga_o_historico(consentido, cenario):
    """Revogar e eliminar são direitos diferentes (art. 18, VI e IX)."""
    consentido.post(f"/api/alunos/{cenario['filipe'].id}/checkins", json={"peso_kg": 84})
    consentido.request("DELETE", "/api/eu/consentimento")

    ainda_la = consentido.get(f"/api/alunos/{cenario['filipe'].id}/checkins").json()
    assert len(ainda_la) == 1
    assert ainda_la[0]["peso_kg"] == 84


def teste_sem_consentimento_o_aluno_ainda_le_o_treino(cliente, cenario):
    """Não consentir bloqueia o dado de saúde, não o app inteiro."""
    sessao = cliente("filipe@exemplo.com")
    assert sessao.get("/api/eu").status_code == 200
    assert sessao.get(f"/api/alunos/{cenario['filipe'].id}").status_code == 200
    assert sessao.get(f"/api/alunos/{cenario['filipe'].id}/evolucao").status_code == 200


def teste_sem_consentimento_nao_edita_o_proprio_perfil(cliente, cenario):
    """Altura e nascimento também são dado de saúde."""
    resposta = cliente("filipe@exemplo.com").patch(
        f"/api/alunos/{cenario['filipe'].id}", json={"altura_cm": 180}
    )
    assert resposta.status_code == 451


def teste_o_treinador_nao_precisa_consentir(cliente, cenario):
    """Ele é o controlador, não o titular: a base legal dele é outra."""
    joao = cliente("joao@exemplo.com")
    resposta = joao.post(
        f"/api/alunos/{cenario['filipe'].id}/checkins", json={"peso_kg": 84}
    )
    assert resposta.status_code == 201


def teste_termo_novo_derruba_o_consentimento_antigo(
    consentido, cenario, monkeypatch, tmp_path
):
    """Consentimento é específico para uma finalidade (art. 8º §4º).

    Texto novo é outra coisa, então o sim anterior não vale para ele.
    """
    from jf import privacidade

    alvo = f"/api/alunos/{cenario['filipe'].id}/checkins"
    assert consentido.post(alvo, json={"peso_kg": 84}).status_code == 201

    outro = tmp_path / "termo.md"
    outro.write_text("# Termo reescrito, com finalidade nova", encoding="utf-8")
    monkeypatch.setattr(privacidade, "TERMO", outro)
    privacidade.texto_do_termo.cache_clear()
    privacidade.versao_do_termo.cache_clear()

    try:
        estado = consentido.get("/api/eu/consentimento").json()
        assert estado["consentido"] is False
        assert estado["precisa_reaceitar"] is True

        recusado = consentido.post(alvo, json={"semana": segunda(1), "peso_kg": 83})
        assert recusado.status_code == 451
    finally:
        privacidade.texto_do_termo.cache_clear()
        privacidade.versao_do_termo.cache_clear()


# -------------------------------------------------------------------- exportar


def teste_exportar_traz_tudo(consentido, cenario):
    consentido.post(
        f"/api/alunos/{cenario['filipe'].id}/checkins",
        json={"peso_kg": 84.2, "horas_de_sono": 7, "medidas": {"cintura_cm": 86}},
    )

    dados = consentido.get("/api/eu/dados").json()
    assert dados["conta"]["email"] == "filipe@exemplo.com"
    assert dados["consentimentos"][0]["versao_do_termo"] == versao_do_termo()

    checkins = dados["aluno"]["checkins"]
    assert len(checkins) == 1
    assert checkins[0]["peso_kg"] == 84.2
    assert checkins[0]["medidas"]["cintura_cm"] == 86
    assert dados["aluno"]["perfil"]["treinador"] == "João Filho"


def teste_exportar_traz_a_dieta(consentido, cenario, cliente):
    """O termo promete "cópia completa" — a dieta é dado de saúde e entra nela."""
    aluno_id = cenario["filipe"].id
    protocolo = cliente("joao@exemplo.com").post(
        f"/api/alunos/{aluno_id}/protocolos",
        json={
            "nome": "Corte",
            "deficit_kcal": 500,
            "grupos": [
                {
                    "nome": "Carboidratos",
                    "itens": [{"descricao": "Arroz", "quantidade": 200, "unidade": "g"}],
                }
            ],
            "refeicoes": [{"nome": "Almoço", "itens": [{"descricao": "Arroz"}]}],
            "suplementos": [{"nome": "Ioimbina", "dose": "5 mg"}],
        },
    ).json()
    consentido.put(
        f"/api/refeicoes/{protocolo['refeicoes'][0]['id']}/aderencia",
        json={"seguiu": False, "observacao": "comi fora"},
    )

    dieta = consentido.get("/api/eu/dados").json()["aluno"]["dieta"]
    assert len(dieta) == 1
    assert dieta[0]["deficit_kcal"] == 500
    # A quantidade vem junto: a substituição sem ela não é o protocolo.
    assert dieta[0]["grupos_de_substituicao"][0]["itens"] == ["Arroz 200 g"]
    assert dieta[0]["refeicoes"][0]["itens"][0]["grupo"] == "Carboidratos"
    assert dieta[0]["suplementos"][0]["dose"] == "5 mg"

    marcacoes = consentido.get("/api/eu/dados").json()["aluno"]["aderencia_as_refeicoes"]
    assert marcacoes[0]["observacao"] == "comi fora"


def teste_a_exportacao_nao_leva_a_senha(consentido):
    """Nem embaralhada: ela é credencial, não dado sobre a pessoa."""
    import json

    bruto = json.dumps(consentido.get("/api/eu/dados").json())
    assert "senha" not in bruto
    assert "argon2" not in bruto.lower()


def teste_o_treinador_exporta_a_propria_conta(cliente, cenario):
    dados = cliente("joao@exemplo.com").get("/api/eu/dados").json()
    assert dados["conta"]["papel"] == "treinador"
    assert dados["aluno"] is None  # ele não é aluno de ninguém


def teste_exportar_nao_traz_dado_de_outro(consentido, cenario, cliente):
    outro = cliente("outro@exemplo.com")
    outro.post("/api/eu/consentimento")
    outro.post(f"/api/alunos/{cenario['outro'].id}/checkins", json={"peso_kg": 99})

    dados = consentido.get("/api/eu/dados").json()
    assert all(c["peso_kg"] != 99 for c in dados["aluno"]["checkins"])


# ---------------------------------------------------------------------- apagar


def teste_apagar_exige_o_email_como_confirmacao(consentido):
    """Não é segurança — é atrito, numa ação que não tem volta."""
    errado = consentido.request("DELETE", "/api/eu", params={"confirmacao": "sim"})
    assert errado.status_code == 400
    assert consentido.get("/api/eu").status_code == 200


def teste_apagar_derruba_a_sessao(consentido):
    resposta = consentido.request(
        "DELETE", "/api/eu", params={"confirmacao": "filipe@exemplo.com"}
    )
    assert resposta.status_code == 204
    assert consentido.get("/api/eu").status_code == 401


def teste_apagar_nao_deixa_nada_para_tras(consentido, cenario, sessao_de_banco, cliente):
    """A prova de que "apagar" apaga.

    Enche o banco com todos os tipos de registro que pendem de um aluno,
    apaga a conta, e confere **tabela por tabela** que nada com o id dele
    sobreviveu — inclusive as tabelas de associação, que são justamente as que
    se esquece.
    """
    aluno_id = cenario["filipe"].id
    usuario_id = cenario["filipe"].usuario_id

    # Check-in com medidas.
    consentido.post(
        f"/api/alunos/{aluno_id}/checkins",
        json={"peso_kg": 84, "medidas": {"cintura_cm": 86}},
    )

    # Um treino completo, com técnica na prescrição e nas séries.
    from jf.dados import semear_tudo

    semear_tudo(sessao_de_banco)
    from sqlalchemy import select

    from jf.modelos import Exercicio, Tecnica

    exercicio = sessao_de_banco.scalar(select(Exercicio))
    cluster = sessao_de_banco.scalar(
        select(Tecnica).where(Tecnica.nome == "Cluster set")
    )

    joao = cliente("joao@exemplo.com")
    bloco = joao.post(
        f"/api/alunos/{aluno_id}/periodizacoes", json={"nome": "Bloco 1"}
    ).json()
    treino = joao.post(
        f"/api/periodizacoes/{bloco['id']}/sessoes", json={"nome": "Treino A"}
    ).json()
    prescricao = joao.post(
        f"/api/sessoes/{treino['id']}/prescricoes",
        json={"exercicio_id": exercicio.id, "tecnica_ids": [cluster.id]},
    ).json()
    joao.put(
        f"/api/prescricoes/{prescricao['id']}/series",
        json={"series": [{"reps": 10, "carga_kg": 60, "tecnica_ids": [cluster.id]}]},
    )

    # Um protocolo alimentar com refeição marcada.
    protocolo = joao.post(
        f"/api/alunos/{aluno_id}/protocolos",
        json={
            "grupos": [{"nome": "Carboidratos", "itens": [{"descricao": "Arroz"}]}],
            "refeicoes": [{"nome": "Almoço", "itens": [{"descricao": "Arroz"}]}],
            "suplementos": [{"nome": "Ioimbina"}],
        },
    ).json()
    consentido.put(
        f"/api/refeicoes/{protocolo['refeicoes'][0]['id']}/aderencia", json={}
    )

    # O outro aluno fica, para provar que a exclusão é cirúrgica.
    outro = cliente("outro@exemplo.com")
    outro.post("/api/eu/consentimento")
    outro.post(f"/api/alunos/{cenario['outro'].id}/checkins", json={"peso_kg": 99})

    resposta = consentido.request(
        "DELETE", "/api/eu", params={"confirmacao": "filipe@exemplo.com"}
    )
    assert resposta.status_code == 204

    sessao_de_banco.expire_all()
    inspetor = inspect(sessao_de_banco.get_bind())
    sobras: list[str] = []

    for tabela in inspetor.get_table_names():
        colunas = {c["name"] for c in inspetor.get_columns(tabela)}
        for coluna, valor in (("aluno_id", aluno_id), ("usuario_id", usuario_id)):
            if coluna not in colunas:
                continue
            quantos = sessao_de_banco.execute(
                text(f"SELECT COUNT(*) FROM {tabela} WHERE {coluna} = :valor"),
                {"valor": valor},
            ).scalar_one()
            if quantos:
                sobras.append(f"{tabela}.{coluna} = {valor}: {quantos} linha(s)")

    assert sobras == [], "sobrou dado do aluno apagado: " + "; ".join(sobras)

    # E as tabelas que pendem indiretamente também foram junto.
    for tabela in ("sessao_modelo", "prescricao", "serie_da_prescricao",
                   "prescricao_tecnica", "serie_tecnica", "medida_corporal",
                   "grupo_de_substituicao", "item_de_substituicao", "refeicao",
                   "item_da_refeicao", "suplemento"):
        assert sessao_de_banco.execute(
            text(f"SELECT COUNT(*) FROM {tabela}")
        ).scalar_one() == 0, f"{tabela} não ficou vazia"

    # O outro aluno continua inteiro.
    restantes = outro.get(f"/api/alunos/{cenario['outro'].id}/checkins").json()
    assert len(restantes) == 1 and restantes[0]["peso_kg"] == 99


def teste_o_treinador_com_aluno_nao_se_apaga(cliente, cenario):
    """Apagar a conta dele levaria o histórico dos alunos junto."""
    resposta = cliente("joao@exemplo.com").request(
        "DELETE", "/api/eu", params={"confirmacao": "joao@exemplo.com"}
    )
    assert resposta.status_code == 409
    assert "aluno" in resposta.json()["detail"]


def teste_treinador_sem_aluno_se_apaga(cliente, criar_usuario):
    sozinho = criar_usuario("Sozinho", "sozinho@exemplo.com", Papel.TREINADOR)
    assert sozinho is not None
    resposta = cliente("sozinho@exemplo.com").request(
        "DELETE", "/api/eu", params={"confirmacao": "sozinho@exemplo.com"}
    )
    assert resposta.status_code == 204


def teste_sem_login_nada_de_privacidade(cliente, cenario):
    anonimo = cliente()
    assert anonimo.get("/api/eu/dados").status_code == 401
    assert anonimo.post("/api/eu/consentimento").status_code == 401
    assert anonimo.request(
        "DELETE", "/api/eu", params={"confirmacao": "filipe@exemplo.com"}
    ).status_code == 401
