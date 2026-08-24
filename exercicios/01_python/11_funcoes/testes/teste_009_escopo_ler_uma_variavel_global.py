"""Testes de A11-009 · Escopo: ler uma variável global.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_aplica_a_taxa():
    verificar(ex.resolver(100.0), 105.0)


def teste_preco_zero():
    verificar(ex.resolver(0.0), 0.0)
