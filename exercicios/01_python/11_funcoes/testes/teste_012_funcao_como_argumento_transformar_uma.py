"""Testes de A11-012 · Função como argumento: transformar uma lista.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_dobrar_cada_item():
    def dobro(x):
        return x * 2

    verificar(ex.resolver(dobro, [1, 2, 3]), [2, 4, 6])


def teste_lista_vazia():
    def dobro(x):
        return x * 2

    verificar(ex.resolver(dobro, []), [])


def teste_funcao_embutida_str():
    verificar(ex.resolver(str, [1, 2, 3]), ["1", "2", "3"])
