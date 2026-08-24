"""Testes de A09-001 · Quantas vezes o laço roda.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_tres():
    verificar(ex.resolver(3), 9)


def teste_um():
    verificar(ex.resolver(1), 1)


def teste_zero():
    verificar(ex.resolver(0), 0)


def teste_cresce_ao_quadrado():
    # dobrar n de 5 para 10 deve multiplicar o resultado por 4, não por 2.
    verificar(ex.resolver(10), ex.resolver(5) * 4,
              dica="Se isso não bater, o laço de dentro não está indo até n.")
