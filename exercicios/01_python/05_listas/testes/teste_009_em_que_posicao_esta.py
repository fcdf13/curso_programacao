"""Testes de A05-009 · Em que posição está.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_encontra_no_meio():
    verificar(ex.resolver(["a", "b", "c"], "b"), 1)


def teste_nao_encontra():
    verificar(ex.resolver(["a", "b"], "z"), -1)


def teste_primeira_ocorrencia():
    verificar(ex.resolver([1, 2, 1], 1), 0)


def teste_lista_vazia():
    verificar(ex.resolver([], "a"), -1)
