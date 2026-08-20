"""Testes de A04-003 · Conceito por faixa.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_conceito_a():
    verificar(ex.resolver(9.5), "A")


def teste_limite_de_a():
    verificar(ex.resolver(9), "A")


def teste_conceito_b():
    verificar(ex.resolver(7), "B")


def teste_conceito_c():
    verificar(ex.resolver(5), "C")


def teste_conceito_d():
    verificar(ex.resolver(2), "D")


def teste_nota_maxima():
    verificar(ex.resolver(10), "A")
