"""Testes de A11-011 · Função como valor: guardar e passar adiante.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_com_funcao_definida_no_teste():
    def dobro(x):
        return x * 2

    verificar(ex.resolver(dobro, 5), 10)


def teste_com_funcao_embutida():
    verificar(ex.resolver(abs, -7), 7)


def teste_com_outra_funcao_embutida():
    verificar(ex.resolver(str, 42), "42")
