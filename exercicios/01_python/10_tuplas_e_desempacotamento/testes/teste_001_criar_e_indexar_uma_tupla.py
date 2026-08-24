"""Testes de A10-001 · Criar e indexar uma tupla.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_produto_e_preco():
    verificar(ex.resolver("Fone", 99.9), ("Fone", 99.9))


def teste_outro_produto():
    verificar(ex.resolver("Capa", 25.0), ("Capa", 25.0))
