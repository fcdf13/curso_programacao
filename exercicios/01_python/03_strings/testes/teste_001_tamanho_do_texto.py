"""Testes de A03-001 · Tamanho do texto.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_palavra():
    verificar(ex.resolver("Aurora"), 6)


def teste_texto_vazio():
    verificar(ex.resolver(""), 0)


def teste_conta_espacos():
    verificar(ex.resolver("a b"), 3)
