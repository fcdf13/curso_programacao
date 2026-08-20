"""Testes de A05-010 · Juntar e repetir.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_junta_e_repete():
    verificar(ex.resolver([1], [2, 3]), ([1, 2, 3], [1, 1]))


def teste_primeira_vazia():
    verificar(ex.resolver([], ["a"]), (["a"], []))


def teste_duas_com_itens():
    verificar(ex.resolver(["x", "y"], ["z"]),
              (["x", "y", "z"], ["x", "y", "x", "y"]))
