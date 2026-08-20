"""Testes de A01-010 · A mesma frase com f-string.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_frase_montada():
    verificar(ex.resolver("Ana", 3), "Ana fez 3 pedidos")


def teste_outro_cliente():
    verificar(ex.resolver("Bruno", 12), "Bruno fez 12 pedidos")
