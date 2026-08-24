"""Testes de A12-002 · List comprehension com filtro.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_alguns_passam():
    verificar(ex.resolver([10.0, 200.0, 50.0], 100.0), [200.0])


def teste_nenhum_passa():
    verificar(ex.resolver([10.0, 20.0], 100.0), [])


def teste_todos_passam():
    verificar(ex.resolver([200.0, 300.0], 100.0), [200.0, 300.0])


def teste_lista_vazia():
    verificar(ex.resolver([], 100.0), [])
