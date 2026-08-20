"""Testes de A03-002 · Primeira e última letra.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_palavra():
    verificar(ex.resolver("Aurora"), ("A", "a"))


def teste_duas_letras():
    verificar(ex.resolver("SP"), ("S", "P"))


def teste_uma_letra_so():
    verificar(ex.resolver("x"), ("x", "x"))
