"""Testes de A02-002 · Par ou ímpar.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_par():
    verificar(ex.resolver(4), True)


def teste_impar():
    verificar(ex.resolver(7), False)


def teste_zero_e_par():
    verificar(ex.resolver(0), True)


def teste_negativo_impar():
    verificar(ex.resolver(-3), False)
