"""O modo academia: o aluno registrando o que levantou de verdade.

O assunto central destes testes é a **sincronização com sinal ruim**. Subsolo
de academia derruba a conexão no meio do treino, então o celular guarda a fila
e reenvia — e reenviar não pode duplicar série, nem apagar o que ele não viu.
"""

from __future__ import annotations

from datetime import date, timedelta

import pytest
from sqlalchemy import select

from jf.dados import semear_tudo
from jf.modelos import Exercicio, Papel, Tecnica

from .conftest import SENHA


@pytest.fixture
def joao(criar_usuario):
    return criar_usuario("João Filho", "joao@exemplo.com", Papel.TREINADOR)


@pytest.fixture
def filipe(criar_aluno, joao):
    return criar_aluno("Filipe", "filipe@exemplo.com", joao)


@pytest.fixture
def catalogo(sessao_de_banco):
    semear_tudo(sessao_de_banco)
    return {
        "exercicio": sessao_de_banco.scalar(select(Exercicio)),
        "cluster": sessao_de_banco.scalar(
            select(Tecnica).where(Tecnica.nome == "Cluster set")
        ),
    }


@pytest.fixture
def treino(cliente, joao, filipe, catalogo):
    """Um bloco com um treino e um exercício de três séries prescritas."""
    treinador = cliente(joao.email)
    bloco = treinador.post(
        f"/api/alunos/{filipe.id}/periodizacoes", json={"nome": "Bloco 1"}
    ).json()
    sessao = treinador.post(
        f"/api/periodizacoes/{bloco['id']}/sessoes", json={"nome": "Treino A"}
    ).json()
    prescricao = treinador.post(
        f"/api/sessoes/{sessao['id']}/prescricoes",
        json={"exercicio_id": catalogo["exercicio"].id},
    ).json()
    prescricao = treinador.put(
        f"/api/prescricoes/{prescricao['id']}/series",
        json={
            "series": [
                {"reps": 12, "carga_kg": 60},
                {"reps": 10, "carga_kg": 70},
                {"reps": 8, "carga_kg": 80},
            ]
        },
    ).json()
    return {"sessao": sessao, "prescricao": prescricao}


@pytest.fixture
def aberto(cliente, filipe, treino):
    aluno = cliente("filipe@exemplo.com")
    resposta = aluno.post(
        f"/api/alunos/{filipe.id}/treinos-realizados",
        json={"sessao_id": treino["sessao"]["id"]},
    )
    assert resposta.status_code == 201, resposta.text
    return resposta.json()


def serie(chave, **campos):
    base = {
        "chave_local": chave,
        "ordem": 0,
        "exercicio_id": campos.pop("exercicio_id"),
        "reps": 12,
        "carga_kg": 60.0,
        "rir": 2,
    }
    base.update(campos)
    return base


# ------------------------------------------------------------- abertura


def teste_abrir_o_treino_de_hoje(aberto, treino):
    assert aberto["nome"] == "Treino A"
    assert aberto["dia"] == date.today().isoformat()
    assert aberto["encerrada"] is False
    assert aberto["series"] == []


def teste_abrir_duas_vezes_devolve_o_mesmo(cliente, filipe, treino, aberto):
    """O celular vai chamar de novo: perdeu sinal, recarregou, voltou depois."""
    de_novo = cliente("filipe@exemplo.com").post(
        f"/api/alunos/{filipe.id}/treinos-realizados",
        json={"sessao_id": treino["sessao"]["id"]},
    )
    assert de_novo.json()["id"] == aberto["id"]

    lista = cliente("filipe@exemplo.com").get(
        f"/api/alunos/{filipe.id}/treinos-realizados"
    ).json()
    assert len(lista) == 1


def teste_nao_abre_treino_do_futuro(cliente, filipe, treino):
    amanha = (date.today() + timedelta(days=1)).isoformat()
    resposta = cliente("filipe@exemplo.com").post(
        f"/api/alunos/{filipe.id}/treinos-realizados",
        json={"sessao_id": treino["sessao"]["id"], "dia": amanha},
    )
    assert resposta.status_code == 422


def teste_nao_abre_treino_de_outro_aluno(
    cliente, criar_usuario, criar_aluno, treino
):
    outro_treinador = criar_usuario("Outro", "outro@exemplo.com", Papel.TREINADOR)
    alheio = criar_aluno("Alheio", "alheio@exemplo.com", outro_treinador)

    resposta = cliente("alheio@exemplo.com").post(
        f"/api/alunos/{alheio.id}/treinos-realizados",
        json={"sessao_id": treino["sessao"]["id"]},
    )
    # A sessão é de outro aluno: para quem pergunta, ela não existe.
    assert resposta.status_code == 404


# -------------------------------------------------------- sincronização


def teste_registrar_series(cliente, filipe, treino, aberto, catalogo):
    aluno = cliente("filipe@exemplo.com")
    prescricao = treino["prescricao"]
    exercicio = catalogo["exercicio"].id

    corpo = {
        "series": [
            serie("serie-0001-abcd", exercicio_id=exercicio, prescricao_id=prescricao["id"],
                  serie_id=prescricao["series_detalhadas"][0]["id"],
                  ordem=0, reps=12, carga_kg=60),
            serie("serie-0002-abcd", exercicio_id=exercicio, prescricao_id=prescricao["id"],
                  serie_id=prescricao["series_detalhadas"][1]["id"],
                  ordem=1, reps=10, carga_kg=72.5),
        ]
    }
    resposta = aluno.put(f"/api/treinos-realizados/{aberto['id']}/series", json=corpo)
    assert resposta.status_code == 200, resposta.text

    corpo = resposta.json()
    assert [s["chave_local"] for s in corpo["series"]] == ["serie-0001-abcd", "serie-0002-abcd"]
    # 12×60 + 10×72,5 = 720 + 725
    assert corpo["tonelagem"] == pytest.approx(1445.0)


def teste_reenviar_a_mesma_fila_nao_duplica(cliente, filipe, aberto, treino, catalogo):
    """O ponto do modo academia: sinal ruim faz o celular reenviar.

    Sem a chave gerada no aparelho, cada tentativa viraria uma série nova e o
    volume da semana passaria a mentir.
    """
    aluno = cliente("filipe@exemplo.com")
    corpo = {"series": [serie("serie-0001-abcd", exercicio_id=catalogo["exercicio"].id)]}

    for _ in range(5):
        resposta = aluno.put(f"/api/treinos-realizados/{aberto['id']}/series", json=corpo)
        assert resposta.status_code == 200

    assert len(resposta.json()["series"]) == 1


def teste_reenviar_corrigido_atualiza(cliente, filipe, aberto, catalogo):
    """Digitou 60 e era 65: o aparelho reenvia a mesma chave com o valor novo."""
    aluno = cliente("filipe@exemplo.com")
    exercicio = catalogo["exercicio"].id

    aluno.put(
        f"/api/treinos-realizados/{aberto['id']}/series",
        json={"series": [serie("serie-0001-abcd", exercicio_id=exercicio, carga_kg=60)]},
    )
    corpo = aluno.put(
        f"/api/treinos-realizados/{aberto['id']}/series",
        json={"series": [serie("serie-0001-abcd", exercicio_id=exercicio, carga_kg=65)]},
    ).json()

    assert len(corpo["series"]) == 1
    assert corpo["series"][0]["carga_kg"] == 65.0


def teste_a_sincronizacao_nunca_apaga_o_que_nao_veio(cliente, filipe, aberto, catalogo):
    """Um aparelho com visão parcial não pode limpar o que outro registrou.

    O aluno registra duas séries no celular, o João corrige uma pelo
    computador, e então o celular — que ficou offline e só conhece a primeira —
    sincroniza. A segunda tem de continuar lá.
    """
    aluno = cliente("filipe@exemplo.com")
    exercicio = catalogo["exercicio"].id

    aluno.put(
        f"/api/treinos-realizados/{aberto['id']}/series",
        json={
            "series": [
                serie("serie-0001-abcd", exercicio_id=exercicio),
                serie("serie-0002-abcd", exercicio_id=exercicio, ordem=1),
            ]
        },
    )

    # O celular atrasado manda só o que conhece.
    corpo = aluno.put(
        f"/api/treinos-realizados/{aberto['id']}/series",
        json={"series": [serie("serie-0001-abcd", exercicio_id=exercicio)]},
    ).json()

    assert sorted(s["chave_local"] for s in corpo["series"]) == [
        "serie-0001-abcd",
        "serie-0002-abcd",
    ]


def teste_apagar_serie_e_explicito(cliente, filipe, aberto, catalogo):
    aluno = cliente("filipe@exemplo.com")
    exercicio = catalogo["exercicio"].id
    aluno.put(
        f"/api/treinos-realizados/{aberto['id']}/series",
        json={"series": [serie("serie-0001-abcd", exercicio_id=exercicio)]},
    )

    assert aluno.delete(
        f"/api/treinos-realizados/{aberto['id']}/series/serie-0001-abcd"
    ).status_code == 204
    assert aluno.get(f"/api/treinos-realizados/{aberto['id']}").json()["series"] == []


def teste_exercicio_desconhecido_e_recusado(cliente, filipe, aberto):
    resposta = cliente("filipe@exemplo.com").put(
        f"/api/treinos-realizados/{aberto['id']}/series",
        json={"series": [serie("serie-0001-abcd", exercicio_id=99999)]},
    )
    assert resposta.status_code == 422


def teste_prescricao_de_outro_treino_e_recusada(
    cliente, joao, filipe, aberto, treino, catalogo
):
    """Sem isto, dava para pendurar a própria série na prescrição alheia."""
    treinador = cliente(joao.email)
    outro_bloco = treinador.post(
        f"/api/alunos/{filipe.id}/periodizacoes", json={"nome": "Bloco 2"}
    ).json()
    outra_sessao = treinador.post(
        f"/api/periodizacoes/{outro_bloco['id']}/sessoes", json={"nome": "Treino B"}
    ).json()
    outra_prescricao = treinador.post(
        f"/api/sessoes/{outra_sessao['id']}/prescricoes",
        json={"exercicio_id": catalogo["exercicio"].id},
    ).json()

    resposta = cliente("filipe@exemplo.com").put(
        f"/api/treinos-realizados/{aberto['id']}/series",
        json={
            "series": [
                serie(
                    "serie-0001-abcd",
                    exercicio_id=catalogo["exercicio"].id,
                    prescricao_id=outra_prescricao["id"],
                )
            ]
        },
    )
    assert resposta.status_code == 422
    assert "não é deste treino" in resposta.text


# --------------------------------------------------------- encerramento


def teste_encerrar_e_reabrir(cliente, filipe, aberto, catalogo):
    aluno = cliente("filipe@exemplo.com")

    encerrado = aluno.post(
        f"/api/treinos-realizados/{aberto['id']}/encerrar",
        json={"observacoes": "ombro incomodou na última"},
    ).json()
    assert encerrado["encerrada"] is True
    assert encerrado["observacoes"] == "ombro incomodou na última"

    # Treino encerrado não aceita série nova sem reabrir — senão o registro de
    # ontem mudaria sozinho.
    recusado = aluno.put(
        f"/api/treinos-realizados/{aberto['id']}/series",
        json={"series": [serie("serie-0001-abcd", exercicio_id=catalogo["exercicio"].id)]},
    )
    assert recusado.status_code == 409

    reaberto = aluno.post(f"/api/treinos-realizados/{aberto['id']}/reabrir").json()
    assert reaberto["encerrada"] is False
    assert aluno.put(
        f"/api/treinos-realizados/{aberto['id']}/series",
        json={"series": [serie("serie-0001-abcd", exercicio_id=catalogo["exercicio"].id)]},
    ).status_code == 200


# ----------------------------------------------------------- permissão


def teste_o_treinador_ve_o_treino_do_aluno(cliente, joao, filipe, aberto, catalogo):
    cliente("filipe@exemplo.com").put(
        f"/api/treinos-realizados/{aberto['id']}/series",
        json={"series": [serie("serie-0001-abcd", exercicio_id=catalogo["exercicio"].id)]},
    )

    visto = cliente(joao.email).get(f"/api/treinos-realizados/{aberto['id']}").json()
    assert len(visto["series"]) == 1


def teste_aluno_alheio_nao_ve(cliente, criar_usuario, criar_aluno, aberto):
    outro = criar_usuario("Outro", "outro@exemplo.com", Papel.TREINADOR)
    criar_aluno("Alheio", "alheio@exemplo.com", outro)

    resposta = cliente("alheio@exemplo.com").get(
        f"/api/treinos-realizados/{aberto['id']}"
    )
    assert resposta.status_code == 404


def teste_sem_consentimento_nao_registra(cliente, joao, criar_aluno, treino):
    """Carga levantada é dado de saúde como o resto."""
    sem_termo = criar_aluno("Sem termo", "semtermo@exemplo.com", joao, consentiu=False)
    resposta = cliente("semtermo@exemplo.com").post(
        f"/api/alunos/{sem_termo.id}/treinos-realizados",
        json={"sessao_id": treino["sessao"]["id"]},
    )
    assert resposta.status_code == 451


def teste_sem_login_nao_registra(cliente, aberto):
    assert cliente().get(f"/api/treinos-realizados/{aberto['id']}").status_code == 401


# ------------------------------------------------------ o histórico dura


def teste_apagar_o_bloco_nao_apaga_o_que_o_aluno_levantou(
    cliente, joao, filipe, aberto, treino, catalogo, sessao_de_banco
):
    """O João reorganiza a periodização; a carga de março continua verdade.

    Se o histórico executado sumisse junto com o modelo, o app perderia
    justamente o dado que ninguém consegue recriar.
    """
    aluno = cliente("filipe@exemplo.com")
    aluno.put(
        f"/api/treinos-realizados/{aberto['id']}/series",
        json={"series": [serie("serie-0001-abcd", exercicio_id=catalogo["exercicio"].id,
                               reps=10, carga_kg=80)]},
    )

    treinador = cliente(joao.email)
    assert treinador.delete(
        f"/api/sessoes/{treino['sessao']['id']}"
    ).status_code == 204

    sessao_de_banco.expire_all()
    depois = aluno.get(f"/api/treinos-realizados/{aberto['id']}").json()
    assert depois["nome"] == "Treino A"
    assert depois["sessao_id"] is None
    assert depois["series"][0]["carga_kg"] == 80.0
    # A prescrição citada some, mas o exercício e a carga continuam.
    assert depois["series"][0]["prescricao_id"] is None
    assert depois["series"][0]["exercicio_id"] == catalogo["exercicio"].id


# ------------------------------------------------------- força e sugestão


def registrar(cliente_do_aluno, treino_id, exercicio_id, series):
    """Manda séries de um treino já aberto, com chaves distintas."""
    corpo = {
        "series": [
            {
                "chave_local": f"chave-{treino_id}-{i:03d}",
                "ordem": i,
                "exercicio_id": exercicio_id,
                "reps": reps,
                "carga_kg": carga,
                "rir": rir,
                "tipo": "valida",
            }
            for i, (reps, carga, rir) in enumerate(series)
        ]
    }
    resposta = cliente_do_aluno.put(
        f"/api/treinos-realizados/{treino_id}/series", json=corpo
    )
    assert resposta.status_code == 200, resposta.text
    return resposta.json()


@pytest.fixture
def com_historico(cliente, filipe, treino, catalogo, sessao_de_banco):
    """Dois treinos, uma semana de diferença, com o aluno mais forte no segundo."""
    from jf.modelos import SessaoRealizada

    aluno = cliente("filipe@exemplo.com")
    exercicio = catalogo["exercicio"].id
    hoje = date.today()

    dias = [hoje - timedelta(days=7), hoje]
    cargas = [[(8, 70.0, 1)], [(5, 85.0, 1)]]

    for dia, series in zip(dias, cargas):
        aberto = aluno.post(
            f"/api/alunos/{filipe.id}/treinos-realizados",
            json={"sessao_id": treino["sessao"]["id"], "dia": dia.isoformat()},
        ).json()
        registrar(aluno, aberto["id"], exercicio, series)

    assert sessao_de_banco.query(SessaoRealizada).count() == 2
    return {"exercicio_id": exercicio}


def teste_a_forca_sai_do_que_foi_levantado(cliente, filipe, com_historico):
    """8×70 estima 91,6 kg; 5×85 estima 100,5. É isso que o gráfico mostra."""
    resposta = cliente("filipe@exemplo.com").get(
        f"/api/alunos/{filipe.id}/forca/{com_historico['exercicio_id']}"
    )
    assert resposta.status_code == 200, resposta.text
    corpo = resposta.json()

    assert [p["e1rm"] for p in corpo["pontos"]] == [91.6, 100.5]
    assert corpo["atual"]["e1rm"] == 100.5
    assert corpo["variacao_kg"] == 8.9
    # O ponto diz de qual série saiu, para dar para conferir.
    assert (corpo["atual"]["reps"], corpo["atual"]["carga_kg"]) == (5, 85.0)


def teste_o_resumo_lista_os_exercicios_com_registro(cliente, filipe, com_historico):
    resumo = cliente("filipe@exemplo.com").get(f"/api/alunos/{filipe.id}/forca").json()
    assert len(resumo) == 1
    assert resumo[0]["exercicio_id"] == com_historico["exercicio_id"]
    assert resumo[0]["atual"]["e1rm"] == 100.5


def teste_sem_registro_a_forca_vem_vazia(cliente, filipe, catalogo):
    corpo = cliente("filipe@exemplo.com").get(
        f"/api/alunos/{filipe.id}/forca/{catalogo['exercicio'].id}"
    ).json()
    assert corpo["pontos"] == []
    assert corpo["atual"] is None
    assert corpo["variacao_kg"] is None


def teste_o_treinador_ve_a_forca_do_aluno(cliente, joao, filipe, com_historico):
    resposta = cliente(joao.email).get(
        f"/api/alunos/{filipe.id}/forca/{com_historico['exercicio_id']}"
    )
    assert resposta.json()["atual"]["e1rm"] == 100.5


def teste_carga_sugerida_sai_do_e1rm(cliente, joao, filipe, treino, com_historico):
    """O ciclo fechando: o João marca 80% e o número sai do treino do aluno."""
    treinador = cliente(joao.email)
    treinador.put(
        f"/api/prescricoes/{treino['prescricao']['id']}",
        json={
            "exercicio_id": com_historico["exercicio_id"],
            "percentual_1rm": 80,
        },
    )

    sugestoes = treinador.get(
        f"/api/sessoes/{treino['sessao']['id']}/cargas-sugeridas"
    ).json()

    assert len(sugestoes) == 1
    sugestao = sugestoes[0]
    assert sugestao["e1rm"] == 100.5
    assert sugestao["carga_kg"] == pytest.approx(80.4, abs=0.05)
    # Arredondada para o que dá para montar na barra.
    assert sugestao["carga_arredondada_kg"] == 80.0
    assert sugestao["confiavel"] is True


def teste_sem_percentual_nao_ha_sugestao(cliente, joao, treino, com_historico):
    """A prescrição que não pede percentual não recebe palpite."""
    sugestoes = cliente(joao.email).get(
        f"/api/sessoes/{treino['sessao']['id']}/cargas-sugeridas"
    ).json()
    assert sugestoes == []


def teste_sem_historico_nao_ha_sugestao(cliente, joao, filipe, treino, catalogo):
    """Silêncio é a resposta certa: um número inventado aqui vira carga na barra."""
    treinador = cliente(joao.email)
    treinador.put(
        f"/api/prescricoes/{treino['prescricao']['id']}",
        json={"exercicio_id": catalogo["exercicio"].id, "percentual_1rm": 80},
    )

    sugestoes = treinador.get(
        f"/api/sessoes/{treino['sessao']['id']}/cargas-sugeridas"
    ).json()
    assert sugestoes == []


def teste_aluno_alheio_nao_ve_a_forca(cliente, criar_usuario, criar_aluno, filipe, com_historico):
    outro = criar_usuario("Outro", "outro@exemplo.com", Papel.TREINADOR)
    criar_aluno("Alheio", "alheio@exemplo.com", outro)

    resposta = cliente("alheio@exemplo.com").get(
        f"/api/alunos/{filipe.id}/forca/{com_historico['exercicio_id']}"
    )
    assert resposta.status_code == 404
