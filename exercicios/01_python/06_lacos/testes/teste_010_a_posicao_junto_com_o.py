"""Testes de A06-010 · A posição junto com o item.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_dois_itens():
    verificar(ex.resolver(["Moda", "Casa"]), ["1. Moda", "2. Casa"])


def teste_um_item():
    verificar(ex.resolver(["Livros"]), ["1. Livros"],
              dica="A numeração começa em 1, não em 0.")


def teste_lista_vazia():
    verificar(ex.resolver([]), [])
