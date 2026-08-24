"""Testes de A10-003 · Tupla não muda — cria outra.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_atualiza_preco():
    verificar(ex.resolver(("Fone", 99.9), 79.9), ("Fone", 79.9))


def teste_preco_para_zero():
    verificar(ex.resolver(("Amostra", 10.0), 0.0), ("Amostra", 0.0))
