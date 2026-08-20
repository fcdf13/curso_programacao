"""Testes de A05-011 · Quantas vezes aparece.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_duas_ocorrencias():
    verificar(ex.resolver(["SP", "RJ", "SP"], "SP"), 2)


def teste_nenhuma():
    verificar(ex.resolver([1, 2, 3], 9), 0)


def teste_lista_vazia():
    verificar(ex.resolver([], "a"), 0)
