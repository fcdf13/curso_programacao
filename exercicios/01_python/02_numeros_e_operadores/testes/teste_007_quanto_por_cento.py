"""Testes de A02-007 · Quanto por cento.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_fracao_simples():
    verificar(ex.resolver(25, 200), 12.5)


def teste_dizima_arredondada():
    verificar(ex.resolver(1, 3), 33.3)


def teste_cem_por_cento():
    verificar(ex.resolver(200, 200), 100.0)
