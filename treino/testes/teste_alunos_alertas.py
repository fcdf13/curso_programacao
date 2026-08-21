"""O painel de alertas: os alunos do João, ordenados por quem precisa de
atenção primeiro — não por ordem alfabética.

Os testes passam pela API de verdade em vez de só chamar `jf.alertas.avaliar`
diretamente: o que importa aqui é que os dados certos (o check-in mais recente,
a tendência de peso, a força por exercício) cheguem até a função pura.
"""

from __future__ import annotations

from datetime import date, timedelta

import pytest

from jf.dados import semear_tudo
from jf.modelos import Exercicio, Papel


@pytest.fixture
def joao(criar_usuario):
    return criar_usuario("João Filho", "joao@exemplo.com", Papel.TREINADOR)


def registrar_checkin(cliente_do_aluno, aluno_id, semana, peso=None, sono=None, aderencia=None):
    corpo = {"semana": semana.isoformat()}
    if peso is not None:
        corpo["peso_kg"] = peso
    if sono is not None:
        corpo["horas_de_sono"] = sono
    if aderencia is not None:
        corpo["aderencia_dieta"] = aderencia
    resposta = cliente_do_aluno.post(f"/api/alunos/{aluno_id}/checkins", json=corpo)
    assert resposta.status_code in (200, 201), resposta.text
    return resposta.json()


def segunda(recuo_semanas: int) -> date:
    hoje = date.today()
    inicio_da_semana = hoje - timedelta(days=hoje.weekday())
    return inicio_da_semana - timedelta(weeks=recuo_semanas)


# --------------------------------------------------------------- básico


def teste_lista_vazia_sem_alunos(cliente, joao):
    resposta = cliente(joao.email).get("/api/alunos/alertas")
    assert resposta.status_code == 200
    assert resposta.json() == []


def teste_aluno_sem_nenhum_sinal_fica_com_lista_vazia(cliente, joao, criar_aluno):
    aluno = criar_aluno("Filipe", "filipe@exemplo.com", joao)
    cliente(aluno.usuario.email).post(
        f"/api/alunos/{aluno.id}/checkins",
        json={"semana": segunda(0).isoformat(), "horas_de_sono": 8},
    )

    corpo = cliente(joao.email).get("/api/alunos/alertas").json()
    assert len(corpo) == 1
    assert corpo[0]["alertas"] == []
    assert corpo[0]["pontuacao"] == 0


def teste_so_o_treinador_ve_a_propria_lista(cliente, joao, criar_aluno):
    criar_aluno("Filipe", "filipe@exemplo.com", joao)
    resposta = cliente("filipe@exemplo.com").get("/api/alunos/alertas")
    assert resposta.status_code == 403


def teste_sem_login_nao_ve(cliente):
    assert cliente().get("/api/alunos/alertas").status_code == 401


def teste_a_rota_alertas_nao_e_confundida_com_um_id(cliente, joao):
    """`/alunos/alertas` precisa vir antes de `/alunos/{aluno_id}` nas rotas."""
    resposta = cliente(joao.email).get("/api/alunos/alertas")
    assert resposta.status_code == 200
    assert isinstance(resposta.json(), list)


# ------------------------------------------------------------ sem check-in


def teste_aluno_sem_checkin_nenhum_acende_o_alerta(cliente, joao, criar_aluno):
    criar_aluno("Filipe", "filipe@exemplo.com", joao)
    corpo = cliente(joao.email).get("/api/alunos/alertas").json()
    assert corpo[0]["alertas"][0]["tipo"] == "sem_checkin"


def teste_aluno_com_checkin_atrasado_aparece_primeiro(cliente, joao, criar_aluno):
    """A ordem é o ponto: quem precisa de atenção vem antes, não por nome."""
    em_dia = criar_aluno("Ana", "ana@exemplo.com", joao)
    atrasado = criar_aluno("Zeca", "zeca@exemplo.com", joao)

    cliente("ana@exemplo.com").post(
        f"/api/alunos/{em_dia.id}/checkins", json={"semana": segunda(0).isoformat()}
    )
    cliente("zeca@exemplo.com").post(
        f"/api/alunos/{atrasado.id}/checkins", json={"semana": segunda(4).isoformat()}
    )

    corpo = cliente(joao.email).get("/api/alunos/alertas").json()
    assert [item["nome"] for item in corpo] == ["Zeca", "Ana"]


# ----------------------------------------------------------------- sono


def teste_sono_baixo_no_ultimo_checkin(cliente, joao, criar_aluno):
    aluno = criar_aluno("Filipe", "filipe@exemplo.com", joao)
    cliente(aluno.usuario.email).post(
        f"/api/alunos/{aluno.id}/checkins",
        json={"semana": segunda(0).isoformat(), "horas_de_sono": 5},
    )
    corpo = cliente(joao.email).get("/api/alunos/alertas").json()
    tipos = [a["tipo"] for a in corpo[0]["alertas"]]
    assert "sono_baixo" in tipos


# ------------------------------------------------------------------ peso


def teste_peso_subindo_com_deficit_ativo(cliente, joao, criar_aluno):
    aluno = criar_aluno("Filipe", "filipe@exemplo.com", joao)
    email = aluno.usuario.email

    cliente(joao.email).post(
        f"/api/alunos/{aluno.id}/protocolos",
        json={"deficit_kcal": 500, "grupos": [], "refeicoes": []},
    )

    pesos = [79.0, 79.8, 80.6, 81.5, 82.3]
    for i, peso in enumerate(pesos):
        registrar_checkin(cliente(email), aluno.id, segunda(len(pesos) - 1 - i), peso=peso)

    corpo = cliente(joao.email).get("/api/alunos/alertas").json()
    tipos = [a["tipo"] for a in corpo[0]["alertas"]]
    assert "peso_subindo" in tipos


def teste_peso_subindo_sem_deficit_nao_alerta(cliente, joao, criar_aluno):
    """Fora de corte, peso subindo é o esperado — não um sinal."""
    aluno = criar_aluno("Filipe", "filipe@exemplo.com", joao)
    email = aluno.usuario.email

    pesos = [80.0, 80.3, 80.6, 81.0, 81.3]
    for i, peso in enumerate(pesos):
        registrar_checkin(cliente(email), aluno.id, segunda(len(pesos) - 1 - i), peso=peso)

    corpo = cliente(joao.email).get("/api/alunos/alertas").json()
    tipos = [a["tipo"] for a in corpo[0]["alertas"]]
    assert "peso_subindo" not in tipos


# -------------------------------------------------------------- aderência


def teste_queda_de_aderencia_entre_os_dois_ultimos_checkins(cliente, joao, criar_aluno):
    aluno = criar_aluno("Filipe", "filipe@exemplo.com", joao)
    email = aluno.usuario.email

    registrar_checkin(cliente(email), aluno.id, segunda(1), aderencia=90)
    registrar_checkin(cliente(email), aluno.id, segunda(0), aderencia=50)

    corpo = cliente(joao.email).get("/api/alunos/alertas").json()
    tipos = [a["tipo"] for a in corpo[0]["alertas"]]
    assert "aderencia_caindo" in tipos


# ------------------------------------------------------------------ força


def teste_forca_caindo_no_exercicio(cliente, joao, criar_aluno, sessao_de_banco):
    from sqlalchemy import select

    aluno = criar_aluno("Filipe", "filipe@exemplo.com", joao)
    email = aluno.usuario.email

    semear_tudo(sessao_de_banco)
    exercicio = sessao_de_banco.scalar(select(Exercicio))

    treinador = cliente(joao.email)
    bloco = treinador.post(
        f"/api/alunos/{aluno.id}/periodizacoes", json={"nome": "Bloco 1"}
    ).json()
    sessao_modelo = treinador.post(
        f"/api/periodizacoes/{bloco['id']}/sessoes", json={"nome": "Treino A"}
    ).json()
    treinador.post(
        f"/api/sessoes/{sessao_modelo['id']}/prescricoes",
        json={"exercicio_id": exercicio.id},
    )

    aluno_cliente = cliente(email)
    quedas = [(8, 100.0, 1), (8, 90.0, 1), (8, 80.0, 1)]
    dias = [date.today() - timedelta(days=14), date.today() - timedelta(days=7), date.today()]
    for dia, (reps, carga, rir) in zip(dias, quedas):
        aberto = aluno_cliente.post(
            f"/api/alunos/{aluno.id}/treinos-realizados",
            json={"sessao_id": sessao_modelo["id"], "dia": dia.isoformat()},
        ).json()
        aluno_cliente.put(
            f"/api/treinos-realizados/{aberto['id']}/series",
            json={
                "series": [
                    {
                        "chave_local": f"chave-{dia.isoformat()}",
                        "exercicio_id": exercicio.id,
                        "reps": reps,
                        "carga_kg": carga,
                        "rir": rir,
                        "tipo": "valida",
                    }
                ]
            },
        )

    corpo = cliente(joao.email).get("/api/alunos/alertas").json()
    tipos = [a["tipo"] for a in corpo[0]["alertas"]]
    assert "forca_caindo" in tipos
