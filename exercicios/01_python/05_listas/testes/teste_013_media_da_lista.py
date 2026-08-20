"""Testes de A05-013 · Média da lista.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_media_inteira():
    verificar(ex.resolver([10, 8, 6]), 8.0)


def teste_media_quebrada():
    verificar(ex.resolver([1, 2]), 1.5)


def teste_lista_vazia():
    verificar(ex.resolver([]), 0.0,
              dica="Sem tratar a lista vazia, len() vale 0 e a divisão estoura.")


def teste_arredonda():
    verificar(ex.resolver([1, 1, 2]), 1.33)
