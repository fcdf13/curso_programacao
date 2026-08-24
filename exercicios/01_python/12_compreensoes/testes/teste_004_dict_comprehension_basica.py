"""Testes de A12-004 · Dict comprehension básica.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_dois_produtos():
    verificar(ex.resolver(["Fone", "Capa"], [99.9, 25.0]), {"Fone": 99.9, "Capa": 25.0})


def teste_listas_vazias():
    verificar(ex.resolver([], []), {})


def teste_um_produto():
    verificar(ex.resolver(["Livro"], [30.0]), {"Livro": 30.0})
