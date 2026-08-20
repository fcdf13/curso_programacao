"""Testes de A02-001 · Área do retângulo.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_area_inteira():
    verificar(ex.resolver(3, 4), 12)


def teste_area_com_decimal():
    verificar(ex.resolver(2.5, 4), 10.0)
