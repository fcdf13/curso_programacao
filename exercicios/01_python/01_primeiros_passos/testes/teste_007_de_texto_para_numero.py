"""Testes de A01-007 · De texto para número.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_soma_simples():
    verificar(ex.resolver("7", "3"), 10)


def teste_numeros_maiores():
    verificar(ex.resolver("100", "25"), 125)


def teste_devolve_numero_e_nao_texto():
    verificar(ex.resolver("2", "2"), 4,
              dica="Se o resultado for '22', você somou os textos sem converter.")
