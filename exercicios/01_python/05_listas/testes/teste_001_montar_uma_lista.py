"""Testes de A05-001 · Montar uma lista.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_numeros():
    verificar(ex.resolver(1, 2, 3), [1, 2, 3])


def teste_textos():
    verificar(ex.resolver("a", "b", "c"), ["a", "b", "c"])


def teste_tipos_misturados():
    verificar(ex.resolver(1, "a", True), [1, "a", True])
