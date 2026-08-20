"""Testes de A04-007 · Frete por região.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_sudeste():
    verificar(ex.resolver("SP"), 15.0)


def teste_outro_do_sudeste():
    verificar(ex.resolver("ES"), 15.0)


def teste_sul():
    verificar(ex.resolver("RS"), 22.0)


def teste_demais_estados():
    verificar(ex.resolver("AM"), 35.0)


def teste_estado_do_nordeste():
    verificar(ex.resolver("BA"), 35.0)
