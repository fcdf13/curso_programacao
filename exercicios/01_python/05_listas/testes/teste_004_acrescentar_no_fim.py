"""Testes de A05-004 · Acrescentar no fim.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_acrescenta_no_fim():
    verificar(ex.resolver([1, 2], 3), [1, 2, 3])


def teste_lista_vazia():
    verificar(ex.resolver([], "a"), ["a"])


def teste_nao_devolve_none():
    verificar(ex.resolver([1], 2), [1, 2],
              dica="Se veio None, você escreveu return itens.append(...).")
