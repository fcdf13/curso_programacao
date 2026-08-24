"""Testes de A08-012 · Inverter um dicionário.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_duas_siglas():
    verificar(ex.resolver({"SP": "São Paulo", "RJ": "Rio de Janeiro"}),
              {"São Paulo": "SP", "Rio de Janeiro": "RJ"})


def teste_dicionario_vazio():
    verificar(ex.resolver({}), {})


def teste_um_par_so():
    verificar(ex.resolver({"A": 1}), {1: "A"})
