"""Testes de A03-007 · Quebrar a frase em palavras.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_tres_palavras():
    verificar(ex.resolver("Fone Aurora Pro"), ["Fone", "Aurora", "Pro"])


def teste_uma_palavra():
    verificar(ex.resolver("Casa"), ["Casa"])


def teste_espacos_repetidos():
    verificar(ex.resolver("a   b"), ["a", "b"],
              dica="split() sem argumento já ignora espaços repetidos.")
