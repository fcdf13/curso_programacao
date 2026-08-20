"""Testes de A01-005 · Somar dois números.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_soma_inteiros():
    verificar(ex.resolver(2, 3), 5)


def teste_soma_com_negativo():
    verificar(ex.resolver(10, -4), 6)


def teste_soma_com_virgula():
    verificar(ex.resolver(1.5, 0.5), 2.0)


def teste_soma_zeros():
    verificar(ex.resolver(0, 0), 0)
