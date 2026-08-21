"""Os sinais que colocam um aluno no topo da lista do João.

Cada regra precisa dar para explicar numa frase: um alerta que ninguém entende
por que disparou é um alerta que se aprende a ignorar. Os testes conferem tanto
o disparo quanto o silêncio — o silêncio importa tanto quanto o alerta, porque
é ele que evita o João aprender a ignorar a tela.
"""

from __future__ import annotations

from datetime import date, timedelta

from jf.alertas import (
    Alerta,
    aderencia_caindo,
    avaliar,
    forca_caindo,
    peso_subindo_no_corte,
    pontuacao,
    sem_checkin,
    sono_baixo,
)

HOJE = date(2026, 8, 21)


# ------------------------------------------------------------ sem check-in


def teste_nunca_fez_checkin():
    alerta = sem_checkin(None, HOJE)
    assert alerta is not None
    assert alerta.gravidade == 3


def teste_checkin_recente_nao_alerta():
    assert sem_checkin(HOJE - timedelta(days=3), HOJE) is None


def teste_dez_dias_e_o_limite():
    assert sem_checkin(HOJE - timedelta(days=9), HOJE) is None
    alerta = sem_checkin(HOJE - timedelta(days=10), HOJE)
    assert alerta is not None
    assert alerta.gravidade == 2


def teste_o_dobro_do_limite_e_grave():
    alerta = sem_checkin(HOJE - timedelta(days=20), HOJE)
    assert alerta is not None
    assert alerta.gravidade == 3
    assert "semana" in alerta.mensagem


# ----------------------------------------------------------------- sono


def teste_sono_baixo_alerta():
    alerta = sono_baixo(5.5)
    assert alerta is not None
    assert "5.5" in alerta.mensagem or "5,5" in alerta.mensagem


def teste_sono_normal_nao_alerta():
    assert sono_baixo(7.5) is None


def teste_sem_dado_de_sono_nao_alerta():
    """Silêncio é a resposta certa quando não há o que avaliar."""
    assert sono_baixo(None) is None


# ------------------------------------------------------------------ peso


def teste_peso_subindo_no_corte_alerta():
    alerta = peso_subindo_no_corte(em_corte=True, tendencia_kg=[80.0, 80.3, 80.7])
    assert alerta is not None
    assert alerta.tipo == "peso_subindo"


def teste_peso_subindo_fora_do_corte_nao_alerta():
    """Subir de peso é o esperado fora de déficit — alertar seria ruído."""
    assert peso_subindo_no_corte(em_corte=False, tendencia_kg=[80.0, 80.3, 80.7]) is None


def teste_oscilacao_pequena_nao_alerta():
    """Água e sal não é sinal; só a subida que passa do limiar conta."""
    assert peso_subindo_no_corte(em_corte=True, tendencia_kg=[80.0, 80.1, 80.2]) is None


def teste_peso_caindo_no_corte_nao_alerta():
    assert peso_subindo_no_corte(em_corte=True, tendencia_kg=[82.0, 81.0, 80.0]) is None


def teste_sem_tendencia_suficiente_nao_alerta():
    assert peso_subindo_no_corte(em_corte=True, tendencia_kg=[80.0]) is None
    assert peso_subindo_no_corte(em_corte=True, tendencia_kg=[]) is None


# ------------------------------------------------------------------ força


def teste_duas_quedas_seguidas_alertam():
    alerta = forca_caindo("Supino", [100.0, 95.0, 90.0])
    assert alerta is not None
    assert "Supino" in alerta.mensagem


def teste_uma_queda_so_nao_alerta():
    """Um dia fraco não é tendência — precisa de dois seguidos."""
    assert forca_caindo("Supino", [90.0, 95.0, 100.0]) is None
    assert forca_caindo("Supino", [100.0, 95.0, 96.0]) is None


def teste_forca_subindo_nao_alerta():
    assert forca_caindo("Supino", [90.0, 95.0, 100.0]) is None


def teste_poucos_pontos_nao_alertam():
    assert forca_caindo("Supino", [100.0, 95.0]) is None
    assert forca_caindo("Supino", []) is None


# -------------------------------------------------------------- aderência


def teste_queda_grande_de_aderencia_alerta():
    alerta = aderencia_caindo(atual=60, anterior=90)
    assert alerta is not None
    assert "30" in alerta.mensagem


def teste_queda_pequena_nao_alerta():
    assert aderencia_caindo(atual=85, anterior=90) is None


def teste_aderencia_subindo_nao_alerta():
    assert aderencia_caindo(atual=95, anterior=80) is None


def teste_sem_dois_pontos_nao_alerta():
    assert aderencia_caindo(atual=60, anterior=None) is None
    assert aderencia_caindo(atual=None, anterior=90) is None


# -------------------------------------------------------------- avaliar


def teste_avaliar_junta_tudo_ordenado_por_gravidade():
    alertas = avaliar(
        hoje=HOJE,
        ultimo_checkin=HOJE - timedelta(days=20),  # grave
        horas_de_sono=5.0,  # atenção
        em_corte=False,
        tendencia_de_peso_kg=[],
        forca_por_exercicio={},
        aderencia_dieta_atual=None,
        aderencia_dieta_anterior=None,
    )
    assert [a.gravidade for a in alertas] == sorted(
        (a.gravidade for a in alertas), reverse=True
    )
    assert alertas[0].tipo == "sem_checkin"


def teste_avaliar_sem_nenhum_sinal_devolve_lista_vazia():
    assert (
        avaliar(
            hoje=HOJE,
            ultimo_checkin=HOJE - timedelta(days=1),
            horas_de_sono=8.0,
            em_corte=True,
            tendencia_de_peso_kg=[80.0, 79.5],
            forca_por_exercicio={"Supino": [90.0, 95.0, 100.0]},
            aderencia_dieta_atual=95,
            aderencia_dieta_anterior=90,
        )
        == []
    )


def teste_avaliar_inclui_forca_caindo_por_exercicio():
    alertas = avaliar(
        hoje=HOJE,
        ultimo_checkin=HOJE,
        horas_de_sono=8.0,
        em_corte=False,
        tendencia_de_peso_kg=[],
        forca_por_exercicio={
            "Supino": [100.0, 95.0, 90.0],
            "Agachamento": [100.0, 110.0, 120.0],
        },
        aderencia_dieta_atual=None,
        aderencia_dieta_anterior=None,
    )
    assert len(alertas) == 1
    assert "Supino" in alertas[0].mensagem


# ------------------------------------------------------------- pontuação


def teste_pontuacao_soma_as_gravidades():
    assert pontuacao([Alerta("a", 3, ""), Alerta("b", 1, "")]) == 4


def teste_pontuacao_vazia_e_zero():
    assert pontuacao([]) == 0
