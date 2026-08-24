"""Testes de A10-005 · Só o que interessa.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_registro_completo():
    verificar(ex.resolver(("Ana", "SP", "2024-01-15")), "SP")


def teste_outro_estado():
    verificar(ex.resolver(("Bruno", "RJ", "2023-06-01")), "RJ")
