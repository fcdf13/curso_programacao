"""A escada de revisão espaçada: o intervalo cresce no acerto e desaba no erro."""

from datetime import date

from curso import srs

HOJE = date(2026, 3, 1)


def teste_qualidade_por_tentativas():
    assert srs.qualidade(1, acertou=True) == 5
    assert srs.qualidade(2, acertou=True) == 4
    assert srs.qualidade(3, acertou=True) == 3
    assert srs.qualidade(7, acertou=True) == 2
    assert srs.qualidade(1, acertou=False) == 1


def teste_quem_olhou_a_solucao_nao_ganha_nota_alta():
    assert srs.qualidade(1, acertou=True, viu_solucao=True) == 1


def teste_primeira_revisao_cai_no_dia_seguinte():
    agendamento, repeticoes = srs.agendar(5, hoje=HOJE)
    assert agendamento.intervalo_dias == 1
    assert agendamento.proxima_revisao == date(2026, 3, 2)
    assert repeticoes == 1


def teste_escada_de_quem_acerta_sempre_de_primeira():
    facilidade, intervalo, repeticoes = srs.FACILIDADE_INICIAL, 0, 0
    escada = []
    for _ in range(5):
        agendamento, repeticoes = srs.agendar(
            5, facilidade=facilidade, intervalo_dias=intervalo,
            repeticoes=repeticoes, hoje=HOJE,
        )
        facilidade, intervalo = agendamento.facilidade, agendamento.intervalo_dias
        escada.append(intervalo)

    assert escada[:3] == [1, 3, 8]
    assert escada == sorted(escada), "o intervalo nunca pode encolher em quem acerta"
    assert escada[-1] > 30


def teste_errar_devolve_o_exercicio_para_amanha():
    agendamento, repeticoes = srs.agendar(
        1, facilidade=2.5, intervalo_dias=45, repeticoes=6, hoje=HOJE,
    )
    assert agendamento.intervalo_dias == 1
    assert agendamento.proxima_revisao == date(2026, 3, 2)
    assert repeticoes == 0, "errar recomeça a escada"
    assert agendamento.facilidade < 2.5, "e deixa o exercício marcado como difícil"


def teste_facilidade_tem_piso():
    facilidade = srs.FACILIDADE_INICIAL
    for _ in range(30):
        agendamento, _ = srs.agendar(1, facilidade=facilidade, hoje=HOJE)
        facilidade = agendamento.facilidade
    assert facilidade == srs.FACILIDADE_MINIMA


def teste_intervalo_tem_teto():
    agendamento, _ = srs.agendar(
        5, facilidade=2.5, intervalo_dias=10_000, repeticoes=20, hoje=HOJE,
    )
    assert agendamento.intervalo_dias == srs.INTERVALO_MAXIMO_DIAS


def teste_nota_fora_da_escala_e_limitada():
    assert srs.agendar(99, hoje=HOJE)[0].intervalo_dias == 1
    assert srs.agendar(-5, hoje=HOJE)[0].intervalo_dias == 1
