"""Testes de A05-002 · Primeiro, último e quantos.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_tres_itens():
    verificar(ex.resolver([10, 20, 30]), (10, 30, 3))


def teste_um_item():
    verificar(ex.resolver(["a"]), ("a", "a", 1))


def teste_lista_longa():
    verificar(ex.resolver([1, 2, 3, 4, 5, 6]), (1, 6, 6))
