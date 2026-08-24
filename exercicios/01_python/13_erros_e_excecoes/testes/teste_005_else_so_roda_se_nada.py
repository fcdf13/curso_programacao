"""Testes de A13-005 · else: só roda se nada deu errado.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_numero_valido():
    verificar(ex.resolver("42"), "número: 42")


def teste_nao_e_numero():
    verificar(ex.resolver("abc"), "não é número")


def teste_numero_negativo():
    verificar(ex.resolver("-5"), "número: -5")
