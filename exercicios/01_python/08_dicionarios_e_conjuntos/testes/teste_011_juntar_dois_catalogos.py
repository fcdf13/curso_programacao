"""Testes de A08-011 · Juntar dois catálogos.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_chave_repetida_o_segundo_vence():
    verificar(
        ex.resolver({"Fone": 99.9, "Capa": 25.0}, {"Capa": 20.0, "Mouse": 45.0}),
        {"Fone": 99.9, "Capa": 20.0, "Mouse": 45.0},
    )


def teste_sem_sobreposicao():
    verificar(ex.resolver({"A": 1}, {"B": 2}), {"A": 1, "B": 2})


def teste_segundo_vazio():
    verificar(ex.resolver({"A": 1}, {}), {"A": 1})
