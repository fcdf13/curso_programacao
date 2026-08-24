"""Testes de A11-004 · *args ao lado de um parâmetro fixo.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_soma():
    verificar(ex.resolver("soma", 1, 2, 3), 6)


def teste_produto():
    verificar(ex.resolver("produto", 2, 3, 4), 24)


def teste_produto_sem_numeros():
    verificar(ex.resolver("produto"), 1)


def teste_soma_sem_numeros():
    verificar(ex.resolver("soma"), 0)
