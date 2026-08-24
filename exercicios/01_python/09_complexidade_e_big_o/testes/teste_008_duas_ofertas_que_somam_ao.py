"""Testes de A09-008 · Duas ofertas que somam ao vale-presente.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401
import time  # noqa: F401  (t.cronometrar já cuida da medição)

ex = carregar(__file__)


def teste_par_no_comeco():
    verificar(ex.resolver([2, 7, 11, 15], 9), (0, 1))


def teste_par_no_fim():
    verificar(ex.resolver([2, 7, 11, 15], 26), (2, 3))


def teste_sem_par():
    verificar(ex.resolver([2, 7, 11, 15], 99), None)


def teste_grande_e_rapido():
    precos = list(range(0, 120_000, 10))  # 12.000 preços, nenhum par soma ao vale
    vale = -999_999

    with t.cronometrar() as tempo:
        obtido = ex.resolver(precos, vale)

    verificar(obtido, None, nome="resultado")
    t.verificar_tempo(
        tempo["segundos"], limite=0.4,
        dica="troque os dois for aninhados por um dict de {preço: índice}.",
    )
