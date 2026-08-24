"""Testes de A12-005 · Dict comprehension com filtro.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_um_produto_passa():
    verificar(ex.resolver(["Fone", "Capa"], [150.0, 20.0], 100.0), {"Fone": 150.0})


def teste_nenhum_produto_passa():
    verificar(ex.resolver(["Fone", "Capa"], [10.0, 20.0], 100.0), {})


def teste_todos_passam():
    verificar(
        ex.resolver(["Fone", "Capa"], [150.0, 200.0], 100.0),
        {"Fone": 150.0, "Capa": 200.0},
    )
