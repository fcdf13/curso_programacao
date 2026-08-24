"""Testes de A11-013 · Despacho por dicionário de funções.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_soma():
    verificar(ex.resolver("soma", 4, 3), 7)


def teste_subtracao():
    verificar(ex.resolver("subtracao", 4, 3), 1)


def teste_multiplicacao():
    verificar(ex.resolver("multiplicacao", 4, 3), 12)


def teste_divisao():
    verificar(ex.resolver("divisao", 9, 3), 3.0)
