"""Testes de A03-003 · Um pedaço do texto.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_palavra_longa():
    verificar(ex.resolver("Eletrônicos"), "Ele")


def teste_palavra_de_quatro():
    verificar(ex.resolver("Casa"), "Cas")


def teste_texto_curto_demais():
    verificar(ex.resolver("SP"), "SP")
