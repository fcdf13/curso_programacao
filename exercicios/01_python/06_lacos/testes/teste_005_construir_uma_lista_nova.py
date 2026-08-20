"""Testes de A06-005 · Construir uma lista nova.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_dois_precos():
    verificar(ex.resolver([100, 50]), [110.0, 55.0])


def teste_um_preco():
    verificar(ex.resolver([9.99]), [10.99])


def teste_lista_vazia():
    verificar(ex.resolver([]), [])


def teste_nao_altera_a_original():
    entrada = [100.0]
    ex.resolver(entrada)
    verificar(entrada, [100.0], nome="lista recebida")
