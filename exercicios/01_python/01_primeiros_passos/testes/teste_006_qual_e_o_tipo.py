"""Testes de A01-006 · Qual é o tipo.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_inteiro():
    verificar(ex.resolver(42), int)


def teste_decimal():
    verificar(ex.resolver(3.14), float)


def teste_texto():
    verificar(ex.resolver("Aurora"), str)


def teste_booleano():
    verificar(ex.resolver(True), bool)
