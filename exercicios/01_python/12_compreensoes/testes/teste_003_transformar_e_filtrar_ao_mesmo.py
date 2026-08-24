"""Testes de A12-003 · Transformar e filtrar ao mesmo tempo.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_um_produto_passa():
    verificar(ex.resolver(["Fone", "Livro"], [150.0, 20.0], 100.0), ["FONE"])


def teste_nenhum_produto_passa():
    verificar(ex.resolver(["Fone", "Livro"], [10.0, 20.0], 100.0), [])


def teste_todos_passam():
    verificar(ex.resolver(["Fone", "Capa"], [150.0, 200.0], 100.0), ["FONE", "CAPA"])
