"""O leitor do formato que o João já escreve.

Os casos vêm dos treinos reais dele:

    Cadeira abdutora vermelha
    Up set de 40 a 100kg
    10x100kg
    12x100kg cluster set
"""

from __future__ import annotations

import pytest

from jf.leitura import ler, ler_linha
from jf.modelos import TipoDeSerie

CATALOGO = ["Cluster set", "Dead Stop", "Drop-set", "Rest-pause", "Super Slow", "Slow"]


# ------------------------------------------------------------ série simples


@pytest.mark.parametrize(
    "texto,reps,carga",
    [
        ("10x100kg", 10, 100.0),
        ("12x50kg", 12, 50.0),
        ("8x109kg", 8, 109.0),
        ("8 x 109 kg", 8, 109.0),
        ("12×22,5kg", 12, 22.5),   # vírgula decimal e o × de verdade
        ("12x22.5", 12, 22.5),      # o "kg" é opcional
        ("- 10x30kg", 10, 30.0),    # colado num marcador de lista
    ],
)
def teste_serie_simples(texto, reps, carga):
    linha = ler_linha(texto, CATALOGO)
    assert linha.entendida
    assert (linha.reps, linha.carga_kg) == (reps, carga)
    assert linha.carga_ate_kg is None
    assert linha.tipo is TipoDeSerie.VALIDA


# -------------------------------------------------------------------- rampa


@pytest.mark.parametrize(
    "texto,reps,de,ate",
    [
        ("12x50 a 92kg", 12, 50.0, 92.0),
        ("12x50 até 92kg", 12, 50.0, 92.0),
        ("12x50-92kg", 12, 50.0, 92.0),
    ],
)
def teste_serie_em_rampa(texto, reps, de, ate):
    linha = ler_linha(texto, CATALOGO)
    assert linha.entendida
    assert (linha.reps, linha.carga_kg, linha.carga_ate_kg) == (reps, de, ate)


@pytest.mark.parametrize(
    "texto,de,ate,tipo",
    [
        ("Up set de 40 a 100kg", 40.0, 100.0, TipoDeSerie.UP_SET),
        ("Up set 40 a 100kg", 40.0, 100.0, TipoDeSerie.UP_SET),
        ("up-set de 40-100", 40.0, 100.0, TipoDeSerie.UP_SET),
        ("Aquecimento 20 a 60kg", 20.0, 60.0, TipoDeSerie.AQUECIMENTO),
    ],
)
def teste_rampa_sem_repeticoes(texto, de, ate, tipo):
    """"Up set de 40 a 100kg" não tem contagem de repetições — e tudo bem."""
    linha = ler_linha(texto, CATALOGO)
    assert linha.entendida
    assert linha.reps is None
    assert (linha.carga_kg, linha.carga_ate_kg) == (de, ate)
    assert linha.tipo is tipo


# ------------------------------------------------------------------ técnicas


def teste_tecnica_no_fim_da_linha():
    linha = ler_linha("12x100kg cluster set", CATALOGO)
    assert linha.entendida
    assert (linha.reps, linha.carga_kg) == (12, 100.0)
    assert linha.tecnicas == ["Cluster set"]
    assert linha.observacao is None


def teste_tecnica_ignora_acento_e_caixa():
    assert ler_linha("10x60kg DEAD STOP", CATALOGO).tecnicas == ["Dead Stop"]
    assert ler_linha("10x60kg super slow", CATALOGO).tecnicas == ["Super Slow"]


def teste_a_tecnica_mais_longa_ganha():
    """Com "Slow" e "Super Slow" no catálogo, "super slow" não vira "Slow"."""
    assert ler_linha("10x60kg super slow", CATALOGO).tecnicas == ["Super Slow"]


def teste_tecnica_desconhecida_vira_observacao():
    linha = ler_linha("10x60kg pausa de 2s no fundo", CATALOGO)
    assert linha.entendida
    assert linha.tecnicas == []
    assert linha.observacao == "pausa de 2s no fundo"


def teste_rotulo_de_tipo_numa_serie_normal():
    linha = ler_linha("10x30kg back off", CATALOGO)
    assert linha.tipo is TipoDeSerie.BACK_OFF
    assert linha.reps == 10


# ---------------------------------------------------------- bloco inteiro


def teste_o_treino_real_do_joao():
    texto = """Up set de 40 a 100kg
10x100kg
12x100kg cluster set"""
    linhas = ler(texto, CATALOGO)
    assert len(linhas) == 3
    assert all(linha.entendida for linha in linhas)

    assert linhas[0].tipo is TipoDeSerie.UP_SET
    assert (linhas[0].carga_kg, linhas[0].carga_ate_kg) == (40.0, 100.0)
    assert (linhas[1].reps, linhas[1].carga_kg) == (10, 100.0)
    assert linhas[2].tecnicas == ["Cluster set"]


def teste_progressao_crescente_e_decrescente():
    """Os dois sentidos aparecem nos treinos dele; nenhum é uma fórmula."""
    subindo = ler("12x20kg\n10x30kg\n8x40kg", CATALOGO)
    assert [(l.reps, l.carga_kg) for l in subindo] == [(12, 20.0), (10, 30.0), (8, 40.0)]

    descendo = ler("12x20kg\n10x15kg\n8x10kg", CATALOGO)
    assert [(l.reps, l.carga_kg) for l in descendo] == [(12, 20.0), (10, 15.0), (8, 10.0)]


def teste_linhas_em_branco_somem():
    assert len(ler("10x60kg\n\n\n12x50kg\n", CATALOGO)) == 2


def teste_linha_que_nao_e_serie_volta_com_o_motivo():
    """Não some em silêncio: a tela precisa mostrar o que ficou de fora."""
    linhas = ler("Cadeira abdutora vermelha\n10x100kg", CATALOGO)
    assert len(linhas) == 2
    assert not linhas[0].entendida
    assert "12x50kg" in linhas[0].erro
    assert linhas[1].entendida


def teste_texto_vazio():
    assert ler("", CATALOGO) == []
    assert ler("   \n  \n", CATALOGO) == []
