"""Testes de A02-003 · As duas divisões.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_divisao_com_resto():
    verificar(ex.resolver(7, 2), (3.5, 3))


def teste_divisao_exata():
    verificar(ex.resolver(10, 5), (2.0, 2))


def teste_dividendo_menor():
    verificar(ex.resolver(3, 4), (0.75, 0))
