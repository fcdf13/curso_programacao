"""O check-in semanal e a evolução."""

from __future__ import annotations

from datetime import date, timedelta

import pytest

from jf.modelos import Papel


@pytest.fixture
def cenario(criar_usuario, criar_aluno):
    joao = criar_usuario("João Filho", "joao@exemplo.com", Papel.TREINADOR)
    outro = criar_usuario("Outro Treinador", "outro@exemplo.com", Papel.TREINADOR)
    return {
        "filipe": criar_aluno("Filipe", "filipe@exemplo.com", joao),
        "alheio": criar_aluno("Aluno Alheio", "alheio@exemplo.com", outro),
    }


def segunda(recuo_em_semanas: int = 0) -> str:
    hoje = date.today()
    inicio = hoje - timedelta(days=hoje.weekday(), weeks=recuo_em_semanas)
    return inicio.isoformat()


# ----------------------------------------------------------------- registrar


def teste_aluno_registra_a_semana(cliente, cenario):
    filipe = cliente("filipe@exemplo.com")
    resposta = filipe.post(
        f"/api/alunos/{cenario['filipe'].id}/checkins",
        json={
            "peso_kg": 84.2,
            "horas_de_sono": 7.5,
            "qualidade_do_sono": 4,
            "disposicao": 4,
            "recuperacao": 3,
            "passos_por_dia": 9000,
            "aderencia_dieta": 90,
            "aderencia_treino": 100,
            "observacoes": "Semana boa, dormi melhor.",
        },
    )
    assert resposta.status_code == 201, resposta.text
    corpo = resposta.json()
    assert corpo["peso_kg"] == 84.2
    assert corpo["semana"] == segunda()


def teste_qualquer_dia_cai_na_segunda_da_semana(cliente, cenario):
    """O que preenche no domingo e o que preenche na terça caem na mesma linha."""
    filipe = cliente("filipe@exemplo.com")
    hoje = date.today()
    quarta = hoje - timedelta(days=hoje.weekday()) + timedelta(days=2)

    corpo = filipe.post(
        f"/api/alunos/{cenario['filipe'].id}/checkins",
        json={"semana": quarta.isoformat(), "peso_kg": 84},
    ).json()
    assert corpo["semana"] == segunda()


def teste_duas_semanas_iguais_dao_conflito(cliente, cenario):
    """Sem isso o gráfico ganharia um degrau falso."""
    filipe = cliente("filipe@exemplo.com")
    caminho = f"/api/alunos/{cenario['filipe'].id}/checkins"
    assert filipe.post(caminho, json={"peso_kg": 84}).status_code == 201
    repetido = filipe.post(caminho, json={"peso_kg": 83})
    assert repetido.status_code == 409
    assert "Edite" in repetido.json()["detail"]


def teste_editar_troca_so_o_que_veio(cliente, cenario):
    filipe = cliente("filipe@exemplo.com")
    criado = filipe.post(
        f"/api/alunos/{cenario['filipe'].id}/checkins",
        json={"peso_kg": 84, "horas_de_sono": 7},
    ).json()

    corpo = filipe.patch(
        f"/api/checkins/{criado['id']}", json={"peso_kg": 83.5}
    ).json()
    assert corpo["peso_kg"] == 83.5
    assert corpo["horas_de_sono"] == 7  # não veio no corpo, então ficou


def teste_o_treinador_corrige_o_check_in_do_aluno(cliente, cenario):
    """Peso digitado errado não precisa virar pedido no WhatsApp."""
    criado = cliente("filipe@exemplo.com").post(
        f"/api/alunos/{cenario['filipe'].id}/checkins", json={"peso_kg": 88.2}
    ).json()
    corpo = cliente("joao@exemplo.com").patch(
        f"/api/checkins/{criado['id']}", json={"peso_kg": 84.2}
    ).json()
    assert corpo["peso_kg"] == 84.2


@pytest.mark.parametrize(
    "campo,valor",
    [
        ("peso_kg", 0),
        ("peso_kg", 500),
        ("qualidade_do_sono", 0),
        ("qualidade_do_sono", 6),
        ("horas_de_sono", 20),
        ("aderencia_dieta", 150),
    ],
)
def teste_valores_absurdos_sao_recusados(cliente, cenario, campo, valor):
    resposta = cliente("filipe@exemplo.com").post(
        f"/api/alunos/{cenario['filipe'].id}/checkins", json={campo: valor}
    )
    assert resposta.status_code == 422


# ------------------------------------------------------------------ medidas


def teste_medidas_entram_junto(cliente, cenario):
    corpo = cliente("filipe@exemplo.com").post(
        f"/api/alunos/{cenario['filipe'].id}/checkins",
        json={"peso_kg": 84, "medidas": {"cintura_cm": 86, "braco_cm": 38}},
    ).json()
    assert corpo["medidas"]["cintura_cm"] == 86
    assert corpo["medidas"]["quadril_cm"] is None


def teste_medidas_em_branco_nao_viram_linha(cliente, cenario):
    corpo = cliente("filipe@exemplo.com").post(
        f"/api/alunos/{cenario['filipe'].id}/checkins",
        json={"peso_kg": 84, "medidas": {}},
    ).json()
    assert corpo["medidas"] is None


# ----------------------------------------------------------------- evolução


@pytest.fixture
def historico(cliente, cenario):
    """Oito semanas de peso caindo, com uma semana sem resposta no meio."""
    filipe = cliente("filipe@exemplo.com")
    pesos = [86.0, 85.6, 85.4, 84.9, None, 84.4, 84.1, 83.6]
    for recuo, peso in enumerate(reversed(pesos)):
        corpo: dict = {"semana": segunda(recuo), "horas_de_sono": 7}
        if peso is not None:
            corpo["peso_kg"] = peso
        filipe.post(f"/api/alunos/{cenario['filipe'].id}/checkins", json=corpo)
    return filipe


def teste_evolucao_traz_as_series(historico, cenario):
    corpo = historico.get(f"/api/alunos/{cenario['filipe'].id}/evolucao").json()
    chaves = {s["chave"] for s in corpo["series"]}
    assert "peso_kg" in chaves and "horas_de_sono" in chaves


def teste_semana_sem_resposta_some_em_vez_de_virar_zero(historico, cenario):
    """Quem não pesou não pesa zero; uma linha caindo ao eixo seria mentira."""
    corpo = historico.get(f"/api/alunos/{cenario['filipe'].id}/evolucao").json()
    peso = next(s for s in corpo["series"] if s["chave"] == "peso_kg")
    assert len(peso["pontos"]) == 7  # oito semanas, uma em branco
    assert all(ponto["valor"] > 0 for ponto in peso["pontos"])


def teste_a_tendencia_e_media_movel_de_quatro_semanas(historico, cenario):
    corpo = historico.get(f"/api/alunos/{cenario['filipe'].id}/evolucao").json()
    peso = next(s for s in corpo["series"] if s["chave"] == "peso_kg")

    # Sete pontos, janela de quatro: quatro médias.
    assert len(peso["tendencia"]) == 4
    primeiros = [p["valor"] for p in peso["pontos"][:4]]
    assert peso["tendencia"][0]["valor"] == pytest.approx(sum(primeiros) / 4, abs=0.01)
    # E a tendência desce junto com o peso.
    assert peso["tendencia"][0]["valor"] > peso["tendencia"][-1]["valor"]


def teste_sem_pontos_suficientes_nao_ha_tendencia(cliente, cenario):
    """Duas semanas não formam tendência — é justamente o ruído a evitar."""
    filipe = cliente("filipe@exemplo.com")
    for recuo, peso in enumerate([84.0, 85.0]):
        filipe.post(
            f"/api/alunos/{cenario['filipe'].id}/checkins",
            json={"semana": segunda(recuo), "peso_kg": peso},
        )
    corpo = filipe.get(f"/api/alunos/{cenario['filipe'].id}/evolucao").json()
    peso = next(s for s in corpo["series"] if s["chave"] == "peso_kg")
    assert peso["tendencia"] == []


def teste_variacao_compara_o_primeiro_com_o_ultimo(historico, cenario):
    corpo = historico.get(f"/api/alunos/{cenario['filipe'].id}/evolucao").json()
    assert corpo["variacao"]["peso_kg"] == pytest.approx(83.6 - 86.0, abs=0.01)


def teste_serie_sem_nenhum_dado_nao_aparece(historico, cenario):
    corpo = historico.get(f"/api/alunos/{cenario['filipe'].id}/evolucao").json()
    assert "passos_por_dia" not in {s["chave"] for s in corpo["series"]}


def teste_o_treinador_ve_a_evolucao_do_aluno(historico, cliente, cenario):
    corpo = cliente("joao@exemplo.com").get(
        f"/api/alunos/{cenario['filipe'].id}/evolucao"
    ).json()
    assert corpo["aluno_id"] == cenario["filipe"].id
    assert corpo["series"]


# --------------------------------------------------------------- permissões


def teste_aluno_alheio_nao_registra_nem_le(cliente, cenario):
    alheio = cliente("alheio@exemplo.com")
    caminho = f"/api/alunos/{cenario['filipe'].id}"
    assert alheio.post(f"{caminho}/checkins", json={"peso_kg": 80}).status_code == 404
    assert alheio.get(f"{caminho}/checkins").status_code == 404
    assert alheio.get(f"{caminho}/evolucao").status_code == 404


def teste_aluno_alheio_nao_edita_check_in(cliente, cenario):
    criado = cliente("filipe@exemplo.com").post(
        f"/api/alunos/{cenario['filipe'].id}/checkins", json={"peso_kg": 84}
    ).json()
    alheio = cliente("alheio@exemplo.com")
    assert alheio.patch(f"/api/checkins/{criado['id']}", json={"peso_kg": 1}).status_code == 404
    assert alheio.request("DELETE", f"/api/checkins/{criado['id']}").status_code == 404


def teste_treinador_de_outro_nao_ve(cliente, cenario):
    resposta = cliente("outro@exemplo.com").get(
        f"/api/alunos/{cenario['filipe'].id}/evolucao"
    )
    assert resposta.status_code == 404
