"""Testes de A10-008 · Tupla como chave.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_tres_combinacoes():
    verificar(
        ex.resolver(["SP", "SP", "RJ"], ["Moda", "Casa", "Moda"], [100.0, 50.0, 80.0]),
        {("SP", "Moda"): 100.0, ("SP", "Casa"): 50.0, ("RJ", "Moda"): 80.0},
    )


def teste_mesma_combinacao_repetida():
    verificar(
        ex.resolver(["SP", "SP"], ["Moda", "Moda"], [100.0, 50.0]),
        {("SP", "Moda"): 150.0},
    )


def teste_listas_vazias():
    verificar(ex.resolver([], [], []), {})
