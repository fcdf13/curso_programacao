"""Testes de A10-002 · Desempacotar dois valores.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_produto_simples():
    verificar(ex.resolver(("Fone", 99.9)), "Fone custa R$ 99.90")


def teste_preco_redondo():
    verificar(ex.resolver(("Livro", 30.0)), "Livro custa R$ 30.00")
