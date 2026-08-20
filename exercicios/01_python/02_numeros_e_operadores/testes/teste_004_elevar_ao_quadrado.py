"""Testes de A02-004 · Elevar ao quadrado.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_quadrado_inteiro():
    verificar(ex.resolver(5), 25)


def teste_quadrado_decimal():
    verificar(ex.resolver(1.5), 2.25)


def teste_quadrado_de_negativo():
    verificar(ex.resolver(-3), 9)
