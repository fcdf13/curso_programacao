"""Testes de A12-008 · Comprehension com enumerate.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_duas_posicoes():
    verificar(ex.resolver([10.0, 500.0, 5.0, 800.0], 100.0), [1, 3])


def teste_nenhuma_posicao():
    verificar(ex.resolver([10.0, 20.0], 100.0), [])


def teste_lista_vazia():
    verificar(ex.resolver([], 100.0), [])
