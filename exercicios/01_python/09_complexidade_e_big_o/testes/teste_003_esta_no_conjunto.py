"""Testes de A09-003 · Está no conjunto.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_cupom_valido():
    verificar(ex.resolver({"BEMVINDO10", "FRETEGRATIS"}, "BEMVINDO10"), True)


def teste_cupom_invalido():
    verificar(ex.resolver({"BEMVINDO10", "FRETEGRATIS"}, "XYZ"), False)


def teste_conjunto_vazio():
    verificar(ex.resolver(set(), "BEMVINDO10"), False)
