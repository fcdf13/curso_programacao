"""Testes de A06-009 · Achar o maior na mão.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_positivos():
    verificar(ex.resolver([3, 9, 2]), 9)


def teste_so_negativos():
    verificar(ex.resolver([-5, -1, -9]), -1,
              dica="Se veio 0, você iniciou o maior em 0 em vez do primeiro item.")


def teste_lista_vazia():
    verificar(ex.resolver([]), None)


def teste_um_item():
    verificar(ex.resolver([7]), 7)


def teste_maior_no_fim():
    verificar(ex.resolver([1, 2, 100]), 100)
