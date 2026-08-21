"""A evolução de força a partir do que o aluno levantou.

Módulo puro, testado contra números que dá para conferir: `estimar(70, 8)` dá
91,6 kg pela equação proposta, e é esse número que precisa aparecer no gráfico.
"""

from __future__ import annotations

from datetime import date

from jf.forca import Equacao
from jf.progresso import (
    REPS_MAXIMAS_PARA_E1RM,
    PontoDeForca,
    Registro,
    atual,
    melhor_do_dia,
    variacao,
)

SEGUNDA = date(2026, 8, 3)
TERCA = date(2026, 8, 4)
OUTRA_SEMANA = date(2026, 8, 10)


def teste_um_ponto_por_dia():
    pontos = melhor_do_dia(
        [
            Registro(SEGUNDA, reps=8, carga_kg=70),
            Registro(SEGUNDA, reps=6, carga_kg=80),
            Registro(OUTRA_SEMANA, reps=5, carga_kg=85),
        ]
    )
    assert [p.dia for p in pontos] == [SEGUNDA, OUTRA_SEMANA]


def teste_vale_a_melhor_serie_do_dia_nao_a_media():
    """A pergunta é "quanto ele consegue"; a série mais fraca não responde isso."""
    pontos = melhor_do_dia(
        [
            Registro(SEGUNDA, reps=8, carga_kg=70),   # e1RM 91,6
            Registro(SEGUNDA, reps=6, carga_kg=80),   # e1RM 97,9
            Registro(SEGUNDA, reps=12, carga_kg=50),  # bem menor
        ]
    )
    assert len(pontos) == 1
    assert pontos[0].e1rm == 97.9
    # E o ponto diz de onde veio, para dar para conferir olhando.
    assert (pontos[0].reps, pontos[0].carga_kg) == (6, 80.0)


def teste_serie_confiavel_ganha_de_estimativa_alta():
    """Estimativa com ressalva não vira o recorde do dia, nem sendo maior.

    20×60 estima 105,2 kg contra os 91,6 de 8×70 — e mesmo assim perde. Acima
    de dez repetições a precisão cai em qualquer equação, e deixar o número
    maior ganhar poria no gráfico um "progresso" que só existe na extrapolação.
    """
    pontos = melhor_do_dia(
        [
            Registro(SEGUNDA, reps=8, carga_kg=70, rir=1),
            Registro(SEGUNDA, reps=20, carga_kg=60),  # estima 105,2, não confiável
        ]
    )
    assert len(pontos) == 1
    assert pontos[0].confiavel is True
    assert pontos[0].e1rm == 91.6


def teste_a_ressalva_acompanha_o_ponto():
    pontos = melhor_do_dia([Registro(SEGUNDA, reps=12, carga_kg=60, rir=4)])
    assert pontos[0].confiavel is False
    assert "reserva" in (pontos[0].ressalva or "")


def teste_tecnica_que_distorce_fica_de_fora():
    """Um cluster de 3×3 não é uma série de 9 reps corridas."""
    pontos = melhor_do_dia(
        [
            Registro(SEGUNDA, reps=9, carga_kg=100, distorce=True),
            Registro(SEGUNDA, reps=8, carga_kg=70),
        ]
    )
    assert len(pontos) == 1
    assert pontos[0].carga_kg == 70.0


def teste_so_com_serie_que_distorce_o_dia_some():
    assert melhor_do_dia([Registro(SEGUNDA, reps=9, carga_kg=100, distorce=True)]) == []


def teste_serie_longa_demais_nao_entra():
    """Acima da faixa, a série mede resistência e a extrapolação engana."""
    demais = REPS_MAXIMAS_PARA_E1RM + 1
    assert melhor_do_dia([Registro(SEGUNDA, reps=demais, carga_kg=40)]) == []
    assert melhor_do_dia([Registro(SEGUNDA, reps=REPS_MAXIMAS_PARA_E1RM, carga_kg=40)])


def teste_carga_zerada_nao_entra():
    assert melhor_do_dia([Registro(SEGUNDA, reps=10, carga_kg=0)]) == []


def teste_variacao_entre_o_primeiro_e_o_ultimo():
    pontos = melhor_do_dia(
        [
            Registro(SEGUNDA, reps=8, carga_kg=70),        # 91,6
            Registro(OUTRA_SEMANA, reps=5, carga_kg=85),   # 100,5
        ]
    )
    assert variacao(pontos) == 8.9
    assert atual(pontos).e1rm == 100.5


def teste_um_ponto_so_nao_tem_variacao():
    """Um treino não é uma tendência, e fingir que é seria pior que calar."""
    pontos = melhor_do_dia([Registro(SEGUNDA, reps=8, carga_kg=70)])
    assert variacao(pontos) is None
    assert atual(pontos) is not None


def teste_sem_registro_nenhum():
    assert melhor_do_dia([]) == []
    assert variacao([]) is None
    assert atual([]) is None


def teste_a_equacao_escolhida_muda_o_numero():
    de_casa = melhor_do_dia([Registro(SEGUNDA, reps=8, carga_kg=70)])
    epley = melhor_do_dia(
        [Registro(SEGUNDA, reps=8, carga_kg=70)], equacao=Equacao.EPLEY
    )
    assert de_casa[0].e1rm != epley[0].e1rm
    # Epley: 70 × (1 + 8/30) = 88,7
    assert epley[0].e1rm == 88.7


def teste_dias_saem_em_ordem():
    pontos = melhor_do_dia(
        [
            Registro(OUTRA_SEMANA, reps=5, carga_kg=85),
            Registro(SEGUNDA, reps=8, carga_kg=70),
            Registro(TERCA, reps=6, carga_kg=80),
        ]
    )
    assert [p.dia for p in pontos] == [SEGUNDA, TERCA, OUTRA_SEMANA]
    assert isinstance(pontos[0], PontoDeForca)
