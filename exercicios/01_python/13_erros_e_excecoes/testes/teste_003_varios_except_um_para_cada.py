"""Testes de A13-003 · Vários except, um para cada erro.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_divisao_valida():
    verificar(ex.resolver("10", "2"), "5.0")


def teste_divisao_por_zero():
    verificar(ex.resolver("10", "0"), "Erro: divisão por zero")


def teste_primeiro_valor_invalido():
    verificar(ex.resolver("dez", "2"), "Erro: valor inválido")


def teste_segundo_valor_invalido():
    verificar(ex.resolver("10", "dois"), "Erro: valor inválido")
