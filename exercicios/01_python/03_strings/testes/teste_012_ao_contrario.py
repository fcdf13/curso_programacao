"""Testes de A03-012 · Ao contrário.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_palavra():
    verificar(ex.resolver("Aurora"), "aroruA")


def teste_palindromo():
    verificar(ex.resolver("ana"), "ana")


def teste_vazio():
    verificar(ex.resolver(""), "")
