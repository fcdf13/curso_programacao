"""Testes de A08-013 · Sem repetir.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_com_repetidos():
    verificar(ex.resolver(["SP", "RJ", "SP", "MG", "RJ"]), {"SP", "RJ", "MG"})


def teste_ja_sem_repeticao():
    verificar(ex.resolver(["A", "B"]), {"A", "B"})


def teste_lista_vazia():
    verificar(ex.resolver([]), set())
