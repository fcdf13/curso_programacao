"""Testes de A04-006 · Dentro da faixa.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_no_meio():
    verificar(ex.resolver(7), True)


def teste_limite_inferior():
    verificar(ex.resolver(0), True)


def teste_limite_superior():
    verificar(ex.resolver(10), True)


def teste_abaixo():
    verificar(ex.resolver(-1), False)


def teste_acima():
    verificar(ex.resolver(10.5), False)
