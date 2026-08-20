"""Testes de A06-006 · Enquanto houver saldo.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_tres_meses():
    verificar(ex.resolver(100, 30), 3)


def teste_um_mes_exato():
    verificar(ex.resolver(100, 100), 1)


def teste_nao_da_nem_um_mes():
    verificar(ex.resolver(50, 80), 0)


def teste_sem_saldo():
    verificar(ex.resolver(0, 10), 0)
