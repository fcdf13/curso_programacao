"""Testes de A11-007 · Argumentos somente nomeados.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_sem_desconto():
    verificar(ex.resolver(100.0), 100.0)


def teste_com_desconto():
    verificar(ex.resolver(100.0, desconto=0.1), 90.0)


def teste_desconto_total():
    verificar(ex.resolver(50.0, desconto=1.0), 0.0)
