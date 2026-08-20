"""Testes de A06-008 · Pular os inválidos.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_ignora_um_nulo():
    verificar(ex.resolver([10, None, 5]), 15)


def teste_todos_nulos():
    verificar(ex.resolver([None, None]), 0)


def teste_sem_nulos():
    verificar(ex.resolver([1, 2]), 3)


def teste_zero_nao_e_nulo():
    verificar(ex.resolver([0, None, 0]), 0,
              dica="Zero é um valor válido — só o None deve ser pulado.")
