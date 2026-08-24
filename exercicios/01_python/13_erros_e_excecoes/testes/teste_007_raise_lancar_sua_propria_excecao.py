"""Testes de A13-007 · raise: lançar sua própria exceção.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401
import pytest

ex = carregar(__file__)


def teste_idade_valida():
    verificar(ex.resolver(25), 25)


def teste_idade_zero_e_valida():
    verificar(ex.resolver(0), 0)


def teste_idade_negativa_levanta_erro():
    with pytest.raises(ValueError):
        ex.resolver(-1)
