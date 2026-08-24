"""Testes de A12-007 · Expressão condicional dentro da comprehension.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_mistura():
    verificar(ex.resolver([10.0, 500.0, 5.0], 100.0), ["barato", "caro", "barato"])


def teste_exatamente_no_limite():
    verificar(ex.resolver([100.0], 100.0), ["caro"])


def teste_lista_vazia():
    verificar(ex.resolver([], 100.0), [])
