"""Testes de A07-007 · Maior sequência sem vendas.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_sequencia_no_meio():
    verificar(ex.resolver([5, 0, 0, 3, 0]), 2)


def teste_mes_inteiro_sem_venda():
    verificar(ex.resolver([0, 0, 0]), 3)


def teste_sem_dias_zerados():
    verificar(ex.resolver([1, 2, 3]), 0)


def teste_lista_vazia():
    verificar(ex.resolver([]), 0)


def teste_duas_sequencias():
    verificar(ex.resolver([0, 1, 0, 0, 0, 1, 0]), 3)


def teste_sequencia_termina_no_ultimo_dia():
    verificar(ex.resolver([1, 0, 0, 0]), 3,
              dica="A maior sequência acaba junto com a lista — atualize o máximo\ndentro do laço, a cada volta.")
