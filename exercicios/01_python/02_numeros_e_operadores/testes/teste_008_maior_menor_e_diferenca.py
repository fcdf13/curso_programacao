"""Testes de A02-008 · Maior, menor e diferença.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_positivos():
    verificar(ex.resolver(10, 3, 7), (10, 3, 7))


def teste_negativos():
    verificar(ex.resolver(-5, -1, -9), (-1, -9, 8))


def teste_todos_iguais():
    verificar(ex.resolver(4, 4, 4), (4, 4, 0))
