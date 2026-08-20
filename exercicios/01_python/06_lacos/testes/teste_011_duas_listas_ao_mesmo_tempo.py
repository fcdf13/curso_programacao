"""Testes de A06-011 · Duas listas ao mesmo tempo.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_dois_produtos():
    verificar(ex.resolver(["Fone", "Capa"], [99.9, 25]),
              ["Fone: 99.90", "Capa: 25.00"])


def teste_listas_vazias():
    verificar(ex.resolver([], []), [])


def teste_para_na_mais_curta():
    verificar(ex.resolver(["Fone", "Capa"], [10]), ["Fone: 10.00"],
              dica="zip para quando a lista mais curta acaba.")
