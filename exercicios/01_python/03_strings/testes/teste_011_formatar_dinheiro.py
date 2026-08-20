"""Testes de A03-011 · Formatar dinheiro.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_valor_com_uma_casa():
    verificar(ex.resolver(1234.5), "R$ 1234.50")


def teste_arredonda_para_cima():
    verificar(ex.resolver(9.999), "R$ 10.00")


def teste_zero():
    verificar(ex.resolver(0), "R$ 0.00")
