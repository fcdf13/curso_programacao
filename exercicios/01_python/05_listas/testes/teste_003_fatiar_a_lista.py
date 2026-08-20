"""Testes de A05-003 · Fatiar a lista.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_lista_maior():
    verificar(ex.resolver([10, 20, 30, 40]), [10, 20])


def teste_lista_menor_que_o_pedido():
    verificar(ex.resolver([7]), [7])


def teste_lista_vazia():
    verificar(ex.resolver([]), [])
