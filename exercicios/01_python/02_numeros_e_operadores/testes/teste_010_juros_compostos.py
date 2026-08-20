"""Testes de A02-010 · Juros compostos.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_dois_periodos():
    verificar(ex.resolver(1000, 10, 2), 1210.0)


def teste_sem_periodo_nao_rende():
    verificar(ex.resolver(1000, 10, 0), 1000.0)


def teste_um_por_cento_ao_ano():
    verificar(ex.resolver(500, 1, 12), 563.41)


def teste_taxa_zero():
    verificar(ex.resolver(250, 0, 5), 250.0)
