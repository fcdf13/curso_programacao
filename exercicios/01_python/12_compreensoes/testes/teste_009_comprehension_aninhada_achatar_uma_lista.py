"""Testes de A12-009 · Comprehension aninhada: achatar uma lista de listas.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_tres_pedidos():
    verificar(
        ex.resolver([["Fone", "Capa"], ["Livro"], []]),
        ["Fone", "Capa", "Livro"],
    )


def teste_lista_vazia():
    verificar(ex.resolver([]), [])


def teste_um_pedido_so():
    verificar(ex.resolver([["Mouse"]]), ["Mouse"])


def teste_todos_pedidos_vazios():
    verificar(ex.resolver([[], []]), [])
