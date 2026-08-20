"""Testes de A01-008 · De número para texto.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_numero_grande():
    verificar(ex.resolver(1042), "Pedido nº 1042")


def teste_numero_pequeno():
    verificar(ex.resolver(7), "Pedido nº 7")
