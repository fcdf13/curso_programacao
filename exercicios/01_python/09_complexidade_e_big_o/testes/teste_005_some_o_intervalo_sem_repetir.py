"""Testes de A09-005 · Some o intervalo sem repetir a conta.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_tres_perguntas():
    verificar(
        ex.resolver([10, 20, 30, 40], [(0, 2), (1, 4), (0, 4)]),
        [30, 90, 100],
    )


def teste_intervalo_de_um_dia():
    verificar(ex.resolver([5, 10, 15], [(1, 2)]), [10])


def teste_sem_perguntas():
    verificar(ex.resolver([1, 2, 3], []), [])


def teste_muitas_perguntas_pequenas():
    vendas = [1] * 100
    perguntas = [(i, i + 1) for i in range(100)]
    verificar(ex.resolver(vendas, perguntas), [1] * 100)
