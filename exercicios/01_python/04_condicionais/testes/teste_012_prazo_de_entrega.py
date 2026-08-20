"""Testes de A04-012 · Prazo de entrega.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_sudeste_expresso():
    verificar(ex.resolver("SP", True), 1)


def teste_sudeste_comum():
    verificar(ex.resolver("SP", False), 4)


def teste_sul_comum():
    verificar(ex.resolver("RS", False), 6)


def teste_sul_expresso():
    verificar(ex.resolver("PR", True), 2)


def teste_outros_expresso():
    verificar(ex.resolver("BA", True), 4)


def teste_outros_comum():
    verificar(ex.resolver("AM", False), 12)
