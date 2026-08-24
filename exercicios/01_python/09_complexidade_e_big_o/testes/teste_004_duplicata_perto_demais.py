"""Testes de A09-004 · Duplicata perto demais.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_distancia_igual_a_k():
    verificar(ex.resolver(["a", "b", "c", "a"], 3), True)


def teste_distancia_maior_que_k():
    verificar(ex.resolver(["a", "b", "c", "a"], 2), False)


def teste_distancia_dois():
    verificar(ex.resolver(["a", "b", "a"], 2), True)


def teste_sem_repeticao():
    verificar(ex.resolver(["a", "b", "c"], 5), False)


def teste_repeticao_distante_demais():
    verificar(ex.resolver(["a", "b", "c", "d", "a"], 2), False)


def teste_lista_vazia():
    verificar(ex.resolver([], 3), False)
