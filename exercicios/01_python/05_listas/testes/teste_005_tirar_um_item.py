"""Testes de A05-005 · Tirar um item.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_remove_do_meio():
    verificar(ex.resolver([1, 2, 3], 2), [1, 3])


def teste_remove_so_a_primeira():
    verificar(ex.resolver([1, 2, 2], 2), [1, 2])


def teste_remove_texto():
    verificar(ex.resolver(["a", "b"], "a"), ["b"])
