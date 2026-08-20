"""Testes de A07-005 · Relatório do estoque.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_esgotado_e_ok():
    verificar(ex.resolver(["Fone", "Capa"], [0, 25]),
              ["Fone: 0 (esgotado)", "Capa: 25 (ok)"])


def teste_critico():
    verificar(ex.resolver(["Livro"], [3]), ["Livro: 3 (critico)"])


def teste_listas_vazias():
    verificar(ex.resolver([], []), [])


def teste_limite_do_critico():
    verificar(ex.resolver(["A", "B"], [9, 10]),
              ["A: 9 (critico)", "B: 10 (ok)"],
              dica="9 ainda é crítico; 10 já é ok.")
