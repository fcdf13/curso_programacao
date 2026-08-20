"""Testes de A06-002 · Uma sequência de números.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_ate_cinco():
    verificar(ex.resolver(5), [1, 2, 3, 4, 5])


def teste_ate_um():
    verificar(ex.resolver(1), [1])


def teste_zero_devolve_vazio():
    verificar(ex.resolver(0), [])


def teste_inclui_o_ultimo():
    verificar(ex.resolver(3), [1, 2, 3],
              dica="Se faltou o 3, o fim do range precisa ser n + 1.")
