"""Testes de A04-008 · Faixa etária.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_crianca():
    verificar(ex.resolver(15), "menor")


def teste_limite_da_maioridade():
    verificar(ex.resolver(18), "adulto")


def teste_ultimo_ano_de_adulto():
    verificar(ex.resolver(59), "adulto")


def teste_limite_da_terceira_idade():
    verificar(ex.resolver(60), "idoso")


def teste_recem_nascido():
    verificar(ex.resolver(0), "menor")
