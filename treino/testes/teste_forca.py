"""A equação de 1RM conferida contra o paper.

Os valores da primeira classe saíram do texto de arXiv:2603.17495v1. Eles estão
aqui para que uma refatoração futura não mexa na conta sem avisar — é o tipo de
erro que não quebra nenhum teste de rota e sai como carga errada na academia.
"""

from __future__ import annotations

import math

import pytest

from jf.forca import (
    ALFA,
    CARGA_MINIMA_PROPOSTA,
    Equacao,
    CargaInvalida,
    ForaDoDominio,
    K_MINIMO,
    arredondar_para_anilha,
    carga_para,
    estimar,
    estimar_1rm,
    fator_de_conversao,
    percentual_do_1rm,
    tabela_de_cargas,
    tonelagem,
)


# ------------------------------------------------------- os números do paper


def teste_fator_de_conversao_em_12kg():
    """O paper: "k(12) ≈ 8,8"."""
    assert fator_de_conversao(12) == pytest.approx(8.8, abs=0.05)


def teste_rosca_de_13kg_por_10_reps():
    """O paper: "cerca de 22 kg" pela proposta, "cerca de 17 kg" pelo Brzycki."""
    assert estimar_1rm(13, 10) == pytest.approx(22, abs=0.5)
    assert estimar_1rm(13, 10, Equacao.BRZYCKI) == pytest.approx(17, abs=0.5)


def teste_12kg_por_15_reps():
    """O paper: proposta "roughly 25 kg", clássicas agrupadas em 19–20 kg."""
    assert estimar_1rm(12, 15) == pytest.approx(25, abs=0.5)
    assert 19 <= estimar_1rm(12, 15, Equacao.BRZYCKI) <= 20
    assert 18 <= estimar_1rm(12, 15, Equacao.EPLEY) <= 20


def teste_guard_ativa_abaixo_de_dois_quilos():
    """O paper: o guard pega apenas séries "abaixo de 2 kg"."""
    limite = math.exp((K_MINIMO + 2.55) / 4.58)
    assert limite == pytest.approx(1.95, abs=0.01)
    assert fator_de_conversao(limite * 0.5) == K_MINIMO
    assert fator_de_conversao(limite * 1.5) > K_MINIMO


def teste_as_equacoes_convergem_no_pesado_e_divergem_no_leve():
    """O achado central: o desacordo é maior nas cargas leves."""
    leve = abs(estimar_1rm(12, 15) - estimar_1rm(12, 15, Equacao.BRZYCKI))
    pesado = abs(estimar_1rm(150, 5) - estimar_1rm(150, 5, Equacao.BRZYCKI))
    assert leve / 12 > pesado / 150


def teste_k_cresce_com_a_carga():
    valores = [fator_de_conversao(w) for w in (5, 12, 30, 60, 100, 200)]
    assert valores == sorted(valores)
    # E fica bem abaixo do k fixo das clássicas (30 no Epley, ≈36 no Brzycki),
    # que é por que elas subestimam o peso de cada repetição.
    assert max(valores) < 30


# --------------------------------------------------------------- propriedades


@pytest.mark.parametrize("equacao", list(Equacao))
@pytest.mark.parametrize("carga", [2.5, 13, 60, 137.5])
def teste_uma_repeticao_devolve_a_propria_carga(equacao, carga):
    assert estimar_1rm(carga, 1, equacao) == carga


@pytest.mark.parametrize("equacao", list(Equacao))
def teste_cresce_com_as_repeticoes(equacao):
    estimativas = [estimar_1rm(80, r, equacao) for r in range(1, 13)]
    assert estimativas == sorted(estimativas)


@pytest.mark.parametrize("equacao", list(Equacao))
def teste_cresce_com_a_carga(equacao):
    """Monotonicidade em `w` — é o que faz a bisseção de `carga_para` convergir."""
    cargas = [w for w in range(1, 250) if w >= CARGA_MINIMA_PROPOSTA]
    estimativas = [estimar_1rm(w, 8, equacao) for w in cargas]
    assert estimativas == sorted(estimativas)


# ------------------------------------------- o domínio da equação proposta
#
# Achado nosso, não do paper: o guard k(w) >= 0,5 impede a divisão por zero,
# mas não impede a equação de inverter de sentido nas cargas muito leves.


def teste_a_equacao_proposta_inverte_de_sentido_abaixo_do_piso():
    """O comportamento que motiva o piso, registrado para não se perder.

    Sem o piso, 2 kg por 8 reps estimaria 18,7 kg de 1RM e 3 kg pelas mesmas
    8 reps estimaria 9,3 kg — mais carga, menos força.
    """
    def sem_piso(w, r):
        return w * (1 + (r - 1) ** ALFA / fator_de_conversao(w))

    assert sem_piso(2, 8) > sem_piso(3, 8)
    assert CARGA_MINIMA_PROPOSTA == pytest.approx(4.74, abs=0.01)


def teste_o_piso_e_onde_k_alcanca_b():
    """k(w) >= b é a condição que garante a derivada positiva para todo r."""
    assert fator_de_conversao(CARGA_MINIMA_PROPOSTA) == pytest.approx(4.58, abs=1e-6)


def teste_carga_leve_demais_e_recusada_pela_proposta():
    with pytest.raises(ForaDoDominio):
        estimar_1rm(3, 8, Equacao.PROPOSTA)


def teste_uma_repeticao_passa_mesmo_com_carga_leve():
    """Sem termo de repetição não há o que inverter de sentido."""
    assert estimar_1rm(3, 1, Equacao.PROPOSTA) == 3


def teste_as_classicas_aceitam_carga_leve():
    """Epley e Brzycki são monótonas em todo o domínio."""
    assert estimar_1rm(3, 8, Equacao.EPLEY) > 0
    assert estimar_1rm(3, 8, Equacao.BRZYCKI) > 0


def teste_estimar_cai_para_epley_e_avisa():
    """A troca acontece, mas nunca calada."""
    resultado = estimar(3, 8, Equacao.PROPOSTA, rir=0)
    assert resultado.equacao is Equacao.EPLEY
    assert not resultado.confiavel
    assert "Epley" in resultado.ressalva
    assert resultado.um_rm == pytest.approx(estimar_1rm(3, 8, Equacao.EPLEY))


def teste_carga_para_recusa_alvo_fora_do_dominio():
    with pytest.raises(ForaDoDominio):
        carga_para(5, 12, Equacao.PROPOSTA)


def teste_tabela_omite_as_linhas_fora_do_dominio():
    """Num exercício leve as faixas altas somem em vez de virar número inventado."""
    tabela = tabela_de_cargas(um_rm=9, incremento_kg=2.0)
    assert tabela, "as faixas baixas ainda precisam sair"
    assert all(s.carga_kg >= CARGA_MINIMA_PROPOSTA for s in tabela)
    assert len(tabela) < 8


@pytest.mark.parametrize("equacao", list(Equacao))
@pytest.mark.parametrize("reps", [1, 3, 5, 8, 10, 15, 20])
@pytest.mark.parametrize("carga", [5, 22.5, 60, 180])  # todas >= o piso
def teste_inverter_volta_para_a_carga_original(equacao, reps, carga):
    alvo = estimar_1rm(carga, reps, equacao)
    assert carga_para(alvo, reps, equacao) == pytest.approx(carga, rel=1e-6)


def teste_a_estimativa_nunca_fica_abaixo_da_carga():
    for reps in range(1, 21):
        assert estimar_1rm(45, reps) >= 45


def teste_expoente_sublinear():
    """α < 1: o salto de 1 para 2 reps pesa mais que o de 14 para 15."""
    assert ALFA < 1
    primeiro = estimar_1rm(60, 2) - estimar_1rm(60, 1)
    ultimo = estimar_1rm(60, 15) - estimar_1rm(60, 14)
    assert primeiro > ultimo


# ------------------------------------------------------------------ domínio


@pytest.mark.parametrize("carga,reps", [(0, 5), (-10, 5), (60, 0), (60, -1), (60, 31)])
def teste_entrada_invalida_e_recusada(carga, reps):
    with pytest.raises(CargaInvalida):
        estimar_1rm(carga, reps)


def teste_carga_para_recusa_alvo_invalido():
    with pytest.raises(CargaInvalida):
        carga_para(0, 5)


# --------------------------------------------------------------- percentuais


def teste_o_percentual_por_reps_depende_da_carga():
    """O argumento contra a tabela impressa de %1RM.

    Dez repetições não são uma fração fixa do 1RM: numa rosca leve são bem
    menos que num supino pesado. Uma tabela única não pode servir aos dois.
    """
    rosca = carga_para(estimar_1rm(13, 10), 10)
    supino = carga_para(estimar_1rm(86, 10), 10)

    pct_rosca = percentual_do_1rm(rosca, estimar_1rm(13, 10))
    pct_supino = percentual_do_1rm(supino, estimar_1rm(86, 10))

    assert pct_rosca == pytest.approx(59, abs=1)
    assert pct_supino == pytest.approx(73, abs=1)
    assert pct_supino - pct_rosca > 10


def teste_tabela_de_cargas_desce_com_as_reps():
    tabela = tabela_de_cargas(um_rm=120, incremento_kg=2.5)
    cargas = [s.carga_kg for s in tabela]
    assert cargas == sorted(cargas, reverse=True)
    # A primeira linha é 1 rep, que por definição é o próprio 1RM.
    assert tabela[0].reps == 1
    assert tabela[0].carga_kg == pytest.approx(120)
    assert tabela[0].percentual == pytest.approx(100)


def teste_tabela_respeita_o_incremento():
    for sugestao in tabela_de_cargas(um_rm=100, incremento_kg=2.5):
        assert sugestao.carga_arredondada_kg % 2.5 == pytest.approx(0, abs=1e-9)


# ------------------------------------------------------------ arredondamento


@pytest.mark.parametrize(
    "carga,incremento,esperado",
    [
        (63.7, 2.5, 62.5),
        (64.0, 2.5, 65.0),
        (63.0, 2.5, 62.5),
        (21.4, 2.0, 22.0),
        (47.0, 5.0, 45.0),
        (48.0, 5.0, 50.0),
    ],
)
def teste_arredonda_para_a_anilha(carga, incremento, esperado):
    assert arredondar_para_anilha(carga, incremento) == pytest.approx(esperado)


def teste_arredondamento_nunca_devolve_zero():
    """Arredondar 1 kg para baixo num incremento de 2,5 seria a barra vazia."""
    assert arredondar_para_anilha(1.0, 2.5) == 2.5
    assert arredondar_para_anilha(0.1, 5.0) == 5.0


def teste_incremento_invalido_e_recusado():
    with pytest.raises(CargaInvalida):
        arredondar_para_anilha(60, 0)


# ------------------------------------------------------------------ volume


def teste_tonelagem():
    assert tonelagem(4, 10, 60) == 2400


def teste_tonelagem_nao_substitui_o_1rm():
    """Volume alto com carga leve não indica força; a métrica é outra."""
    leve = tonelagem(3, 15, 40)
    pesado = tonelagem(1, 3, 140)
    assert leve > pesado
    assert estimar_1rm(140, 3) > estimar_1rm(40, 15)


# ------------------------------------------------------------- as ressalvas


def teste_estimativa_confiavel_nao_tem_ressalva():
    resultado = estimar(100, 5, rir=1)
    assert resultado.confiavel
    assert resultado.ressalva is None
    assert resultado.nome_da_equacao == "Marzagão (2026)"


def teste_reserva_demais_derruba_a_confianca():
    resultado = estimar(100, 5, rir=4)
    assert not resultado.confiavel
    assert "reserva" in resultado.ressalva


def teste_reps_demais_derruba_a_confianca():
    resultado = estimar(40, 18, rir=0)
    assert not resultado.confiavel
    assert "precisão" in resultado.ressalva


def teste_tecnica_que_distorce_derruba_a_confianca():
    """Cluster de 3×3 não é uma série de 9 reps."""
    resultado = estimar(100, 9, rir=0, tecnica_distorce=True)
    assert not resultado.confiavel
    assert "técnica" in resultado.ressalva.lower()


def teste_a_tecnica_pesa_mais_que_as_outras_ressalvas():
    """Com tudo errado ao mesmo tempo, a técnica é a que precisa aparecer:
    as outras enviesam o número, a técnica invalida a comparação."""
    resultado = estimar(100, 20, rir=5, tecnica_distorce=True)
    assert "técnica" in resultado.ressalva.lower()


# ------------------------------------------- a equação que vem do banco


def teste_a_equacao_aceita_a_string_que_o_banco_guarda():
    """`Periodizacao.equacao` é coluna de texto, não enum.

    Com comparação por identidade, `"proposta"` não casava com nenhum ramo e
    caía calada na última equação do arquivo — a estimativa saía de Brzycki
    achando que era a proposta, e ninguém tinha como perceber. É o tipo de erro
    que não quebra teste de rota nenhum e sai como carga errada na academia.
    """
    for membro in Equacao:
        assert estimar_1rm(70, 8, membro.value) == estimar_1rm(70, 8, membro)

    assert estimar_1rm(70, 8, "proposta") == pytest.approx(91.6, abs=0.05)
    assert estimar_1rm(70, 8, "brzycki") == pytest.approx(86.9, abs=0.05)


def teste_equacao_desconhecida_falha_em_vez_de_escolher_outra():
    with pytest.raises(ValueError):
        estimar_1rm(70, 8, "a-que-eu-inventei")

    with pytest.raises(ValueError):
        carga_para(100, 8, "a-que-eu-inventei")


def teste_carga_para_tambem_aceita_a_string():
    assert carga_para(100, 8, "epley") == pytest.approx(carga_para(100, 8, Equacao.EPLEY))
