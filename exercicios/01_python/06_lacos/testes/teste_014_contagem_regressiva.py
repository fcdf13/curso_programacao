"""Testes de A06-014 · Contagem regressiva.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_de_tres_a_um():
    verificar(ex.resolver(3), [3, 2, 1])


def teste_so_um():
    verificar(ex.resolver(1), [1])


def teste_zero_nao_conta():
    verificar(ex.resolver(0), [])


def teste_numero_maior():
    verificar(ex.resolver(5), [5, 4, 3, 2, 1])
