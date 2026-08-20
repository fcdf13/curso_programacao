"""Testes de A01-009 · Nome completo.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_nome_e_sobrenome():
    verificar(ex.resolver("Ana", "Souza"), "Ana Souza")


def teste_outro_nome():
    verificar(ex.resolver("Carlos", "Oliveira"), "Carlos Oliveira")
