"""Testes de A05-008 · Resumo dos números.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_tres_numeros():
    verificar(ex.resolver([1, 2, 3]), (6, 1, 3))


def teste_um_numero():
    verificar(ex.resolver([10]), (10, 10, 10))


def teste_com_negativos():
    verificar(ex.resolver([-5, 0, 5]), (0, -5, 5))
