"""Testes de A05-014 · Os três maiores.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_lista_grande():
    verificar(ex.resolver([5, 1, 9, 3, 7]), [9, 7, 5])


def teste_menos_de_tres():
    verificar(ex.resolver([2, 8]), [8, 2])


def teste_lista_vazia():
    verificar(ex.resolver([]), [])


def teste_com_repetidos():
    verificar(ex.resolver([4, 4, 4, 1]), [4, 4, 4])


def teste_exatamente_tres():
    verificar(ex.resolver([1, 3, 2]), [3, 2, 1])
