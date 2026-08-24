"""Testes de A13-004 · except ... as erro: a mensagem original.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_texto_valido():
    verificar(ex.resolver("3.5"), "3.5")


def teste_texto_invalido():
    verificar(ex.resolver("abc"), "Não deu: could not convert string to float: 'abc'")


def teste_texto_vazio():
    verificar(ex.resolver(""), "Não deu: could not convert string to float: ''")
