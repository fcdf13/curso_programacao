"""Testes de A10-007 · O resto e o último.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_tres_itens():
    verificar(ex.resolver([10, 20, 30]), ([10, 20], 30))


def teste_um_item_so():
    verificar(ex.resolver([5]), ([], 5))


def teste_dois_itens():
    verificar(ex.resolver(["a", "b"]), (["a"], "b"))
