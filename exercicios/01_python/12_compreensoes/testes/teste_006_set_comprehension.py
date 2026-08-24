"""Testes de A12-006 · Set comprehension.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_com_repeticao():
    verificar(ex.resolver(["moda", "casa", "moda"]), {"MODA", "CASA"})


def teste_sem_repeticao():
    verificar(ex.resolver(["moda", "casa"]), {"MODA", "CASA"})


def teste_lista_vazia():
    verificar(ex.resolver([]), set())
