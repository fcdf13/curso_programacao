"""Testes de A03-008 · Juntar palavras.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_tres_itens():
    verificar(ex.resolver(["Moda", "Casa", "Livros"]), "Moda, Casa, Livros")


def teste_um_item_so():
    verificar(ex.resolver(["Moda"]), "Moda")


def teste_lista_vazia():
    verificar(ex.resolver([]), "")
