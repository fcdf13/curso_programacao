"""Testes de A06-007 · Parar na primeira.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_encontra_no_meio():
    verificar(ex.resolver([5, 3, -2, -8]), 2,
              dica="A resposta é a posição do PRIMEIRO negativo.")


def teste_nao_ha_negativos():
    verificar(ex.resolver([1, 2, 3]), -1)


def teste_primeiro_ja_e_negativo():
    verificar(ex.resolver([-1]), 0)


def teste_lista_vazia():
    verificar(ex.resolver([]), -1)
