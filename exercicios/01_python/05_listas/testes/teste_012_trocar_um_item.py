"""Testes de A05-012 · Trocar um item.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_troca_no_meio():
    verificar(ex.resolver([1, 2, 3], 1, 99), [1, 99, 3])


def teste_troca_no_comeco():
    verificar(ex.resolver(["a", "b"], 0, "z"), ["z", "b"])


def teste_troca_no_fim_com_indice_negativo():
    verificar(ex.resolver([1, 2, 3], -1, 0), [1, 2, 0])
