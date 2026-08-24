"""Testes de A10-004 · Trocar dois itens de uma lista.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_pontas_opostas():
    verificar(ex.resolver([10, 20, 30, 40], 0, 3), [40, 20, 30, 10])


def teste_posicoes_vizinhas():
    verificar(ex.resolver([1, 2, 3], 0, 1), [2, 1, 3])


def teste_mesma_posicao_nao_muda_nada():
    verificar(ex.resolver([1, 2, 3], 1, 1), [1, 2, 3])
