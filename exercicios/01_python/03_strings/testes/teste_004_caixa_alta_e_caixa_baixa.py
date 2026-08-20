"""Testes de A03-004 · Caixa alta e caixa baixa.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_nome_proprio():
    verificar(ex.resolver("Aurora"), ("AURORA", "aurora"))


def teste_sigla_minuscula():
    verificar(ex.resolver("sp"), ("SP", "sp"))
