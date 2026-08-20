"""Testes de A01-012 · Trocar dois valores de lugar.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_troca_numeros():
    verificar(ex.resolver(1, 2), (2, 1))


def teste_troca_textos():
    verificar(ex.resolver("a", "b"), ("b", "a"))


def teste_troca_tipos_diferentes():
    verificar(ex.resolver(10, "dez"), ("dez", 10))
