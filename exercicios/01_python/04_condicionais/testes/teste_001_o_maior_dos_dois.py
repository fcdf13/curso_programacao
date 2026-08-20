"""Testes de A04-001 · O maior dos dois.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_primeiro_maior():
    verificar(ex.resolver(10, 3), 10)


def teste_segundo_maior():
    verificar(ex.resolver(3, 10), 10)


def teste_iguais():
    verificar(ex.resolver(5, 5), 5)


def teste_negativos():
    verificar(ex.resolver(-2, -9), -2)
