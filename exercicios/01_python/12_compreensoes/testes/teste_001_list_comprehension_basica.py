"""Testes de A12-001 · List comprehension básica.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_tres_precos():
    verificar(ex.resolver([10.0, 20.0, 30.0]), [20.0, 40.0, 60.0])


def teste_lista_vazia():
    verificar(ex.resolver([]), [])


def teste_um_preco():
    verificar(ex.resolver([5.0]), [10.0])
