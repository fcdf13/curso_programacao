"""Testes de A04-009 · Desconto progressivo.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_faixa_de_quinze():
    verificar(ex.resolver(600), 510.0)


def teste_limite_de_duzentos():
    verificar(ex.resolver(200), 180.0)


def teste_faixa_de_cinco():
    verificar(ex.resolver(150), 142.5)


def teste_sem_desconto():
    verificar(ex.resolver(50), 50.0)


def teste_limite_de_quinhentos():
    verificar(ex.resolver(500), 425.0)


def teste_logo_abaixo_de_cem():
    verificar(ex.resolver(99.99), 99.99)
