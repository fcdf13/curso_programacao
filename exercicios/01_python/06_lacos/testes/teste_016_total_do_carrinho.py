"""Testes de A06-016 · Total do carrinho.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_dois_itens_com_desconto():
    verificar(ex.resolver([100, 50], [1, 2], [0, 0.1]), 190.0)


def teste_item_unico():
    verificar(ex.resolver([10], [3], [0]), 30.0)


def teste_carrinho_vazio():
    verificar(ex.resolver([], [], []), 0.0)


def teste_desconto_total():
    verificar(ex.resolver([100], [1], [1]), 0.0)


def teste_valores_quebrados():
    verificar(ex.resolver([19.99, 5.55], [3, 2], [0.15, 0]), 62.07)
