"""Testes de A07-001 · Padronizar a sigla do estado.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_espacos_e_minuscula():
    verificar(ex.resolver(" sp "), "SP")


def teste_caixa_mista():
    verificar(ex.resolver("Rj"), "RJ")


def teste_so_espacos():
    verificar(ex.resolver("  "), "??")


def teste_palavra_inteira():
    verificar(ex.resolver("Brasil"), "??")


def teste_uma_letra_so():
    verificar(ex.resolver("s"), "??")


def teste_ja_padronizada():
    verificar(ex.resolver("MG"), "MG")
