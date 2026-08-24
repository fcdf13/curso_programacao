"""Testes de A13-001 · try/except: um plano B para o erro.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_divisao_normal():
    verificar(ex.resolver(10, 2), 5.0)


def teste_divisao_por_zero():
    verificar(ex.resolver(10, 0), None)


def teste_zero_dividido_por_numero():
    verificar(ex.resolver(0, 5), 0.0)
