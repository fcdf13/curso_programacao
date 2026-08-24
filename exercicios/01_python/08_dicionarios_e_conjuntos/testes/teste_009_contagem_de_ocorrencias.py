"""Testes de A08-009 · Contagem de ocorrências.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_categorias_repetidas():
    verificar(ex.resolver(["Moda", "Casa", "Moda", "Moda"]), {"Moda": 3, "Casa": 1})


def teste_todas_diferentes():
    verificar(ex.resolver(["A", "B", "C"]), {"A": 1, "B": 1, "C": 1})


def teste_lista_vazia():
    verificar(ex.resolver([]), {})


def teste_um_item_repetido_varias_vezes():
    verificar(ex.resolver(["X", "X", "X"]), {"X": 3})
