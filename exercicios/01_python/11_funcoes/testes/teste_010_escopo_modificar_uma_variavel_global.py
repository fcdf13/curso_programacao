"""Testes de A11-010 · Escopo: modificar uma variável global.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_acumula_em_sequencia():
    verificar(ex.resolver(100.0), 100.0)
    verificar(ex.resolver(50.0), 150.0)
    verificar(ex.resolver(25.0), 175.0)


def teste_soma_exatamente_o_valor_passado():
    anterior = ex.resolver(0.0)
    verificar(ex.resolver(10.0), anterior + 10.0)
