"""Prescrição (séries × reps × carga), técnicas e a calculadora pela API."""

from __future__ import annotations

import pytest
from sqlalchemy import select

from jf.dados import semear_tudo
from jf.modelos import EscopoDaTecnica, Exercicio, Papel, Tecnica


@pytest.fixture
def cenario(sessao_de_banco, criar_usuario, criar_aluno):
    list(semear_tudo(sessao_de_banco))
    joao = criar_usuario("João Filho", "joao@exemplo.com", Papel.TREINADOR)
    outro = criar_usuario("Outro Treinador", "outro@exemplo.com", Papel.TREINADOR)
    return {
        "joao": joao,
        "filipe": criar_aluno("Filipe", "filipe@exemplo.com", joao),
        "alheio": criar_aluno("Aluno Alheio", "alheio@exemplo.com", outro),
        "banco": sessao_de_banco,
    }


def exercicio(banco, nome: str) -> Exercicio:
    return banco.scalar(select(Exercicio).where(Exercicio.nome == nome))


def tecnica(banco, nome: str) -> Tecnica:
    return banco.scalar(select(Tecnica).where(Tecnica.nome == nome))


@pytest.fixture
def treino(cliente, cenario):
    """Uma periodização com um treino dentro, pronta para receber exercícios."""
    joao = cliente("joao@exemplo.com")
    periodizacao = joao.post(
        f"/api/alunos/{cenario['filipe'].id}/periodizacoes",
        json={"nome": "Corte — bloco 1", "fase": "acumulacao", "semanas": 4},
    ).json()
    sessao = joao.post(
        f"/api/periodizacoes/{periodizacao['id']}/sessoes",
        json={"nome": "Treino A — peito e tríceps", "dia_da_semana": 0},
    ).json()
    return {"cliente": joao, "periodizacao": periodizacao, "sessao": sessao}


# ------------------------------------------------ séries × reps × carga


def teste_prescricao_guarda_series_reps_e_carga(treino, cenario):
    supino = exercicio(cenario["banco"], "Supino reto com barra")
    resposta = treino["cliente"].post(
        f"/api/sessoes/{treino['sessao']['id']}/prescricoes",
        json={
            "exercicio_id": supino.id,
            "series": 4,
            "reps_min": 6,
            "reps_max": 8,
            "rir_alvo": 2,
            "carga_alvo_kg": 80,
            "descanso_s": 120,
        },
    )
    assert resposta.status_code == 201, resposta.text
    corpo = resposta.json()
    assert corpo["series"] == 4
    assert (corpo["reps_min"], corpo["reps_max"]) == (6, 8)
    assert corpo["carga_alvo_kg"] == 80
    assert corpo["exercicio"]["nome"] == "Supino reto com barra"


def teste_tonelagem_e_series_vezes_reps_vezes_carga(treino, cenario):
    supino = exercicio(cenario["banco"], "Supino reto com barra")
    corpo = treino["cliente"].post(
        f"/api/sessoes/{treino['sessao']['id']}/prescricoes",
        json={
            "exercicio_id": supino.id,
            "series": 4,
            "reps_min": 6,
            "reps_max": 8,
            "carga_alvo_kg": 80,
        },
    ).json()
    # Média da faixa: 4 × 7 × 80.
    assert corpo["tonelagem_prevista"] == pytest.approx(2240)


def teste_tonelagem_do_treino_soma_as_prescricoes(treino, cenario):
    banco = treino["cliente"]
    for nome, carga in [("Supino reto com barra", 80), ("Crucifixo na máquina", 40)]:
        banco.post(
            f"/api/sessoes/{treino['sessao']['id']}/prescricoes",
            json={
                "exercicio_id": exercicio(cenario["banco"], nome).id,
                "series": 3,
                "reps_min": 10,
                "reps_max": 10,
                "carga_alvo_kg": carga,
            },
        )
    corpo = banco.get(f"/api/sessoes/{treino['sessao']['id']}").json()
    assert corpo["tonelagem_prevista"] == pytest.approx(3 * 10 * 80 + 3 * 10 * 40)
    assert corpo["prescricoes_sem_carga"] == 0


def teste_prescricao_sem_carga_e_contada_a_parte(treino, cenario):
    """O total sozinho enganaria; a tela precisa saber quantas ficaram de fora."""
    treino["cliente"].post(
        f"/api/sessoes/{treino['sessao']['id']}/prescricoes",
        json={
            "exercicio_id": exercicio(cenario["banco"], "Supino reto com barra").id,
            "series": 3,
            "reps_min": 10,
            "reps_max": 10,
        },
    )
    corpo = treino["cliente"].get(f"/api/sessoes/{treino['sessao']['id']}").json()
    assert corpo["prescricoes_sem_carga"] == 1
    assert corpo["tonelagem_prevista"] == 0
    assert corpo["prescricoes"][0]["tonelagem_prevista"] is None


def teste_faixa_de_reps_invertida_e_recusada(treino, cenario):
    resposta = treino["cliente"].post(
        f"/api/sessoes/{treino['sessao']['id']}/prescricoes",
        json={
            "exercicio_id": exercicio(cenario["banco"], "Supino reto com barra").id,
            "reps_min": 12,
            "reps_max": 6,
        },
    )
    assert resposta.status_code == 422


# ----------------------------------------------------------- técnicas


def teste_o_catalogo_cobre_os_tres_escopos(cliente, cenario):
    tecnicas = cliente("joao@exemplo.com").get("/api/tecnicas").json()
    nomes = {t["nome"] for t in tecnicas}
    assert {"Dead Stop", "Slow", "Super Slow", "Cluster set", "Bi-set", "Tri-set"} <= nomes
    assert {t["escopo"] for t in tecnicas} == {
        "execucao",
        "intra_serie",
        "agrupamento",
    }


def teste_filtrar_por_escopo(cliente, cenario):
    resposta = cliente("joao@exemplo.com").get(
        "/api/tecnicas", params={"escopo": "agrupamento"}
    )
    nomes = {t["nome"] for t in resposta.json()}
    assert "Bi-set" in nomes and "Dead Stop" not in nomes


def teste_prescricao_com_tecnica_de_execucao(treino, cenario):
    dead_stop = tecnica(cenario["banco"], "Dead Stop")
    corpo = treino["cliente"].post(
        f"/api/sessoes/{treino['sessao']['id']}/prescricoes",
        json={
            "exercicio_id": exercicio(cenario["banco"], "Supino reto com barra").id,
            "series": 4,
            "reps_min": 5,
            "reps_max": 5,
            "carga_alvo_kg": 90,
            "tecnica_ids": [dead_stop.id],
            "cadencia": "3-1-1-0",
        },
    ).json()
    assert [t["nome"] for t in corpo["tecnicas"]] == ["Dead Stop"]
    assert corpo["cadencia"] == "3-1-1-0"
    # Dead Stop não quebra a contagem de repetições.
    assert corpo["distorce_estimativa"] is False


def teste_cluster_marca_a_prescricao_como_distorcida(treino, cenario):
    cluster = tecnica(cenario["banco"], "Cluster set")
    assert cluster.distorce_estimativa
    corpo = treino["cliente"].post(
        f"/api/sessoes/{treino['sessao']['id']}/prescricoes",
        json={
            "exercicio_id": exercicio(cenario["banco"], "Supino reto com barra").id,
            "carga_alvo_kg": 90,
            "tecnica_ids": [cluster.id],
        },
    ).json()
    assert corpo["distorce_estimativa"] is True


def teste_biset_no_campo_errado_e_recusado(treino, cenario):
    """Bi-set liga exercícios; não é técnica de execução de um só."""
    biset = tecnica(cenario["banco"], "Bi-set")
    resposta = treino["cliente"].post(
        f"/api/sessoes/{treino['sessao']['id']}/prescricoes",
        json={
            "exercicio_id": exercicio(cenario["banco"], "Supino reto com barra").id,
            "tecnica_ids": [biset.id],
        },
    )
    assert resposta.status_code == 422
    assert "agrupamento" in resposta.json()["detail"]


def teste_dead_stop_nao_serve_de_agrupamento(treino, cenario):
    resposta = treino["cliente"].post(
        f"/api/sessoes/{treino['sessao']['id']}/prescricoes",
        json={
            "exercicio_id": exercicio(cenario["banco"], "Supino reto com barra").id,
            "bloco": "A",
            "agrupamento_id": tecnica(cenario["banco"], "Dead Stop").id,
        },
    )
    assert resposta.status_code == 422


def teste_agrupamento_exige_bloco(treino, cenario):
    """Sem bloco não dá para saber com quais exercícios o bi-set se liga."""
    resposta = treino["cliente"].post(
        f"/api/sessoes/{treino['sessao']['id']}/prescricoes",
        json={
            "exercicio_id": exercicio(cenario["banco"], "Supino reto com barra").id,
            "agrupamento_id": tecnica(cenario["banco"], "Bi-set").id,
        },
    )
    assert resposta.status_code == 422
    assert "bloco" in resposta.json()["detail"]


def teste_biset_liga_dois_exercicios_pelo_bloco(treino, cenario):
    biset = tecnica(cenario["banco"], "Bi-set")
    for ordem, nome in enumerate(["Crucifixo na máquina", "Supino reto com barra"]):
        resposta = treino["cliente"].post(
            f"/api/sessoes/{treino['sessao']['id']}/prescricoes",
            json={
                "exercicio_id": exercicio(cenario["banco"], nome).id,
                "ordem": ordem,
                "bloco": "A",
                "agrupamento_id": biset.id,
                "series": 3,
                "reps_min": 10,
                "reps_max": 12,
                "carga_alvo_kg": 30,
                "descanso_s": 0,
            },
        )
        assert resposta.status_code == 201, resposta.text

    corpo = treino["cliente"].get(f"/api/sessoes/{treino['sessao']['id']}").json()
    bloco_a = [p for p in corpo["prescricoes"] if p["bloco"] == "A"]
    assert len(bloco_a) == 2
    assert all(p["agrupamento"]["nome"] == "Bi-set" for p in bloco_a)


# -------------------------------------------------------------- calculadora


def teste_calculadora_reproduz_o_paper(cliente, cenario):
    resposta = cliente("joao@exemplo.com").post(
        "/api/calculadora", json={"carga_kg": 13, "reps": 10, "rir": 0}
    )
    corpo = resposta.json()
    assert corpo["um_rm"] == pytest.approx(22.1, abs=0.1)
    assert corpo["nome_da_equacao"] == "Marzagão (2026)"
    assert corpo["confiavel"] is True
    # Brzycki no mesmo caso, para o João comparar.
    assert corpo["comparacao"]["Brzycki (1993)"] == pytest.approx(17.3, abs=0.1)


def teste_a_tabela_usa_o_incremento_do_exercicio(cliente, cenario):
    halteres = exercicio(cenario["banco"], "Supino reto com halteres")
    assert halteres.incremento_kg == 2.0

    corpo = cliente("joao@exemplo.com").post(
        "/api/calculadora",
        json={"carga_kg": 30, "reps": 8, "rir": 1, "exercicio_id": halteres.id},
    ).json()
    assert corpo["incremento_kg"] == 2.0
    for linha in corpo["tabela"]:
        assert linha["carga_arredondada_kg"] % 2 == pytest.approx(0, abs=1e-9)


def teste_o_percentual_nao_e_fixo_por_reps(cliente, cenario):
    """A razão de existir da calculadora, exposta pela API."""
    sessao = cliente("joao@exemplo.com")
    leve = sessao.post("/api/calculadora", json={"carga_kg": 13, "reps": 10}).json()
    pesado = sessao.post("/api/calculadora", json={"carga_kg": 86, "reps": 10}).json()

    pct_leve = next(l["percentual"] for l in leve["tabela"] if l["reps"] == 10)
    pct_pesado = next(l["percentual"] for l in pesado["tabela"] if l["reps"] == 10)

    assert pct_leve == pytest.approx(59, abs=1)
    assert pct_pesado == pytest.approx(73, abs=1)


def teste_reserva_demais_vira_ressalva(cliente, cenario):
    corpo = cliente("joao@exemplo.com").post(
        "/api/calculadora", json={"carga_kg": 100, "reps": 8, "rir": 4}
    ).json()
    assert corpo["confiavel"] is False
    assert "reserva" in corpo["ressalva"]


def teste_tecnica_que_distorce_vira_ressalva(cliente, cenario):
    cluster = tecnica(cenario["banco"], "Cluster set")
    corpo = cliente("joao@exemplo.com").post(
        "/api/calculadora",
        json={"carga_kg": 100, "reps": 9, "rir": 0, "tecnica_ids": [cluster.id]},
    ).json()
    assert corpo["confiavel"] is False
    assert "técnica" in corpo["ressalva"].lower()


def teste_dead_stop_nao_derruba_a_confianca(cliente, cenario):
    dead_stop = tecnica(cenario["banco"], "Dead Stop")
    corpo = cliente("joao@exemplo.com").post(
        "/api/calculadora",
        json={"carga_kg": 100, "reps": 5, "rir": 1, "tecnica_ids": [dead_stop.id]},
    ).json()
    assert corpo["confiavel"] is True


def teste_carga_leve_troca_de_equacao_e_avisa(cliente, cenario):
    """Abaixo de ~4,7 kg a proposta inverte de sentido; a troca precisa aparecer."""
    corpo = cliente("joao@exemplo.com").post(
        "/api/calculadora", json={"carga_kg": 3, "reps": 12, "equacao": "proposta"}
    ).json()
    assert corpo["equacao"] == "epley"
    assert corpo["confiavel"] is False
    assert "Epley" in corpo["ressalva"]
    # A comparação omite a proposta em vez de trazer um número que não vale.
    assert "Marzagão (2026)" not in corpo["comparacao"]


def teste_entrada_absurda_e_recusada(cliente, cenario):
    resposta = cliente("joao@exemplo.com").post(
        "/api/calculadora", json={"carga_kg": 100, "reps": 60}
    )
    assert resposta.status_code == 422


# ------------------------------------------------------------- permissões


def teste_treinador_nao_monta_treino_de_aluno_alheio(cliente, cenario):
    resposta = cliente("joao@exemplo.com").post(
        f"/api/alunos/{cenario['alheio'].id}/periodizacoes", json={"nome": "Invasão"}
    )
    assert resposta.status_code == 404


def teste_aluno_le_o_proprio_treino_mas_nao_escreve(treino, cliente, cenario):
    treino["cliente"].post(
        f"/api/sessoes/{treino['sessao']['id']}/prescricoes",
        json={
            "exercicio_id": exercicio(cenario["banco"], "Supino reto com barra").id,
            "series": 4,
            "reps_min": 6,
            "reps_max": 8,
            "carga_alvo_kg": 80,
        },
    )
    filipe = cliente("filipe@exemplo.com")

    lido = filipe.get(f"/api/periodizacoes/{treino['periodizacao']['id']}")
    assert lido.status_code == 200
    assert lido.json()["sessoes"][0]["prescricoes"][0]["carga_alvo_kg"] == 80

    escrita = filipe.post(
        f"/api/sessoes/{treino['sessao']['id']}/prescricoes",
        json={"exercicio_id": exercicio(cenario["banco"], "Prancha").id},
    )
    assert escrita.status_code == 403


def teste_aluno_alheio_nao_ve_a_periodizacao(treino, cliente, cenario):
    resposta = cliente("alheio@exemplo.com").get(
        f"/api/periodizacoes/{treino['periodizacao']['id']}"
    )
    assert resposta.status_code == 404


def teste_aluno_alheio_nao_ve_o_treino_nem_a_prescricao(treino, cliente, cenario):
    prescricao = treino["cliente"].post(
        f"/api/sessoes/{treino['sessao']['id']}/prescricoes",
        json={"exercicio_id": exercicio(cenario["banco"], "Prancha").id},
    ).json()

    alheio = cliente("alheio@exemplo.com")
    assert alheio.get(f"/api/sessoes/{treino['sessao']['id']}").status_code == 404
    assert (
        alheio.request("DELETE", f"/api/prescricoes/{prescricao['id']}").status_code
        == 404
    )


def teste_apagar_periodizacao_leva_treinos_e_prescricoes(treino, cenario, sessao_de_banco):
    from jf.modelos import Prescricao, SessaoModelo

    treino["cliente"].post(
        f"/api/sessoes/{treino['sessao']['id']}/prescricoes",
        json={"exercicio_id": exercicio(cenario["banco"], "Prancha").id},
    )
    resposta = treino["cliente"].request(
        "DELETE", f"/api/periodizacoes/{treino['periodizacao']['id']}"
    )
    assert resposta.status_code == 204
    assert sessao_de_banco.scalars(select(SessaoModelo)).all() == []
    assert sessao_de_banco.scalars(select(Prescricao)).all() == []


def teste_escopo_da_tecnica_e_do_catalogo(cenario):
    """As de agrupamento estão marcadas como tal, e o cluster distorce."""
    banco = cenario["banco"]
    assert tecnica(banco, "Tri-set").escopo is EscopoDaTecnica.AGRUPAMENTO
    assert tecnica(banco, "Super Slow").escopo is EscopoDaTecnica.EXECUCAO
    assert tecnica(banco, "Cluster set").escopo is EscopoDaTecnica.INTRA_SERIE
    assert tecnica(banco, "Cluster set").distorce_estimativa
    # Série até a falha é justamente o que a estimativa de 1RM pede.
    assert not tecnica(banco, "Série até a falha").distorce_estimativa


# =========================================================== séries por linha
#
# A progressão dentro do exercício: cada série com reps e carga próprias, e a
# técnica de uma série só. Vem dos treinos reais do João.


@pytest.fixture
def prescricao(treino, cenario):
    """Uma prescrição vazia, pronta para receber as séries."""
    return treino["cliente"].post(
        f"/api/sessoes/{treino['sessao']['id']}/prescricoes",
        json={"exercicio_id": exercicio(cenario["banco"], "Cadeira flexora").id},
    ).json()


def teste_progressao_crescente(treino, prescricao):
    """12x20 / 10x30 / 8x40 — reps e carga variam entre as séries."""
    corpo = treino["cliente"].put(
        f"/api/prescricoes/{prescricao['id']}/series",
        json={
            "series": [
                {"ordem": 0, "reps": 12, "carga_kg": 20},
                {"ordem": 1, "reps": 10, "carga_kg": 30},
                {"ordem": 2, "reps": 8, "carga_kg": 40},
            ]
        },
    ).json()

    assert [(s["reps"], s["carga_kg"]) for s in corpo["series_detalhadas"]] == [
        (12, 20.0),
        (10, 30.0),
        (8, 40.0),
    ]
    assert corpo["tem_progressao"] is True
    assert corpo["tonelagem_prevista"] == pytest.approx(12 * 20 + 10 * 30 + 8 * 40)
    # O resumo acompanha a lista: 3 séries, de 8 a 12 reps, até 40 kg.
    assert corpo["series"] == 3
    assert (corpo["reps_min"], corpo["reps_max"]) == (8, 12)
    assert corpo["carga_alvo_kg"] == 40.0


def teste_progressao_decrescente(treino, prescricao):
    """A nórdica do João: 12x20 / 10x15 / 8x10, carga caindo."""
    corpo = treino["cliente"].put(
        f"/api/prescricoes/{prescricao['id']}/series",
        json={
            "series": [
                {"reps": 12, "carga_kg": 20},
                {"ordem": 1, "reps": 10, "carga_kg": 15},
                {"ordem": 2, "reps": 8, "carga_kg": 10},
            ]
        },
    ).json()
    assert [s["carga_kg"] for s in corpo["series_detalhadas"]] == [20.0, 15.0, 10.0]
    assert corpo["tem_progressao"] is True


def teste_series_iguais_nao_contam_como_progressao(treino, prescricao):
    corpo = treino["cliente"].put(
        f"/api/prescricoes/{prescricao['id']}/series",
        json={"series": [{"ordem": i, "reps": 10, "carga_kg": 60} for i in range(3)]},
    ).json()
    assert corpo["tem_progressao"] is False
    assert corpo["tonelagem_prevista"] == pytest.approx(3 * 10 * 60)


def teste_up_set_nao_entra_na_tonelagem(treino, prescricao):
    """A rampa sobe até a carga de trabalho; somá-la inflaria o volume."""
    corpo = treino["cliente"].put(
        f"/api/prescricoes/{prescricao['id']}/series",
        json={
            "series": [
                {"ordem": 0, "tipo": "up_set", "carga_kg": 40, "carga_ate_kg": 100},
                {"ordem": 1, "reps": 10, "carga_kg": 100},
            ]
        },
    ).json()

    up_set, valida = corpo["series_detalhadas"]
    assert up_set["reps"] is None and up_set["em_rampa"] is True
    assert up_set["tonelagem"] is None
    assert valida["tonelagem"] == pytest.approx(1000)
    assert corpo["tonelagem_prevista"] == pytest.approx(1000)
    # E o resumo conta só a série de trabalho.
    assert corpo["series"] == 1


def teste_rampa_com_repeticoes_conta_pelo_ponto_medio(treino, prescricao):
    """"12x50 a 92kg": a carga não é um número só, então vale a média."""
    corpo = treino["cliente"].put(
        f"/api/prescricoes/{prescricao['id']}/series",
        json={"series": [{"reps": 12, "carga_kg": 50, "carga_ate_kg": 92}]},
    ).json()
    serie = corpo["series_detalhadas"][0]
    assert serie["em_rampa"] is True
    assert serie["tonelagem"] == pytest.approx(12 * 71)
    # Rampa não serve para estimar 1RM: a carga não é única.
    assert serie["serve_para_1rm"] is False


def teste_tecnica_de_uma_serie_so(treino, prescricao, cenario):
    """"10x100kg / 12x100kg cluster set": só a segunda é cluster."""
    cluster = tecnica(cenario["banco"], "Cluster set")
    corpo = treino["cliente"].put(
        f"/api/prescricoes/{prescricao['id']}/series",
        json={
            "series": [
                {"ordem": 0, "reps": 10, "carga_kg": 100},
                {"ordem": 1, "reps": 12, "carga_kg": 100, "tecnica_ids": [cluster.id]},
            ]
        },
    ).json()

    primeira, segunda = corpo["series_detalhadas"]
    assert primeira["tecnicas"] == []
    assert primeira["serve_para_1rm"] is True
    assert [t["nome"] for t in segunda["tecnicas"]] == ["Cluster set"]
    assert segunda["serve_para_1rm"] is False
    # E o exercício inteiro fica marcado, porque uma das séries distorce.
    assert corpo["distorce_estimativa"] is True


def teste_biset_nao_cabe_numa_serie(treino, prescricao, cenario):
    resposta = treino["cliente"].put(
        f"/api/prescricoes/{prescricao['id']}/series",
        json={
            "series": [
                {
                    "reps": 10,
                    "carga_kg": 60,
                    "tecnica_ids": [tecnica(cenario["banco"], "Bi-set").id],
                }
            ]
        },
    )
    assert resposta.status_code == 422


def teste_rampa_invertida_e_recusada(treino, prescricao):
    resposta = treino["cliente"].put(
        f"/api/prescricoes/{prescricao['id']}/series",
        json={"series": [{"reps": 10, "carga_kg": 90, "carga_ate_kg": 40}]},
    )
    assert resposta.status_code == 422


def teste_redefinir_substitui_em_vez_de_acrescentar(treino, prescricao):
    caminho = f"/api/prescricoes/{prescricao['id']}/series"
    treino["cliente"].put(caminho, json={"series": [{"reps": 10, "carga_kg": 60}]})
    corpo = treino["cliente"].put(
        caminho, json={"series": [{"reps": 8, "carga_kg": 80}]}
    ).json()
    assert len(corpo["series_detalhadas"]) == 1
    assert corpo["series_detalhadas"][0]["carga_kg"] == 80.0


def teste_aluno_nao_define_series(treino, prescricao, cliente):
    resposta = cliente("filipe@exemplo.com").put(
        f"/api/prescricoes/{prescricao['id']}/series",
        json={"series": [{"reps": 10, "carga_kg": 60}]},
    )
    assert resposta.status_code == 403


def teste_prescricao_sem_series_detalhadas_usa_o_resumo(treino, cenario):
    """Quem prescreve "3 × 10 @ 60" sem detalhar continua funcionando."""
    corpo = treino["cliente"].post(
        f"/api/sessoes/{treino['sessao']['id']}/prescricoes",
        json={
            "exercicio_id": exercicio(cenario["banco"], "Leg press 45").id,
            "series": 3,
            "reps_min": 10,
            "reps_max": 10,
            "carga_alvo_kg": 60,
        },
    ).json()
    assert corpo["series_detalhadas"] == []
    assert corpo["tem_progressao"] is False
    assert corpo["tonelagem_prevista"] == pytest.approx(1800)


# ------------------------------------------------------ ler o texto colado


def teste_ler_o_treino_como_o_joao_escreve(cliente, cenario):
    corpo = cliente("joao@exemplo.com").post(
        "/api/prescricoes/ler-texto",
        json={"texto": "Up set de 40 a 100kg\n10x100kg\n12x100kg cluster set"},
    ).json()

    assert corpo["entendidas"] == 3
    assert corpo["nao_entendidas"] == 0

    up, primeira, segunda = corpo["linhas"]
    assert up["tipo"] == "up_set" and up["carga_ate_kg"] == 100.0
    assert (primeira["reps"], primeira["carga_kg"]) == (10, 100.0)
    assert segunda["tecnicas"] == ["Cluster set"]
    # Os ids vêm resolvidos, prontos para salvar sem uma segunda consulta.
    assert len(segunda["tecnica_ids"]) == 1


def teste_linha_nao_entendida_volta_com_o_motivo(cliente, cenario):
    corpo = cliente("joao@exemplo.com").post(
        "/api/prescricoes/ler-texto",
        json={"texto": "Cadeira abdutora vermelha\n10x100kg"},
    ).json()
    assert corpo["entendidas"] == 1
    assert corpo["nao_entendidas"] == 1
    assert corpo["linhas"][0]["entendida"] is False
    assert corpo["linhas"][0]["erro"] is not None


def teste_aluno_nao_usa_o_leitor(cliente, cenario):
    resposta = cliente("filipe@exemplo.com").post(
        "/api/prescricoes/ler-texto", json={"texto": "10x100kg"}
    )
    assert resposta.status_code == 403


def teste_o_que_o_leitor_devolve_serve_para_salvar(treino, prescricao, cliente):
    """O ciclo fechado: ler o texto e gravar o resultado sem tradução no meio."""
    lido = treino["cliente"].post(
        "/api/prescricoes/ler-texto",
        json={"texto": "Up set de 40 a 100kg\n10x100kg\n12x100kg cluster set"},
    ).json()

    series = [
        {
            "ordem": posicao,
            "reps": linha["reps"],
            "carga_kg": linha["carga_kg"],
            "carga_ate_kg": linha["carga_ate_kg"],
            "tipo": linha["tipo"],
            "observacao": linha["observacao"],
            "tecnica_ids": linha["tecnica_ids"],
        }
        for posicao, linha in enumerate(lido["linhas"])
        if linha["entendida"]
    ]

    corpo = treino["cliente"].put(
        f"/api/prescricoes/{prescricao['id']}/series", json={"series": series}
    ).json()

    assert len(corpo["series_detalhadas"]) == 3
    assert corpo["tonelagem_prevista"] == pytest.approx(10 * 100 + 12 * 100)
    assert corpo["distorce_estimativa"] is True
