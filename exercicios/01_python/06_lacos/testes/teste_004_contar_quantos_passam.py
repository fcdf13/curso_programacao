"""Testes de A06-004 · Contar quantos passam.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_dois_passam():
    verificar(ex.resolver([10, 5, 20], 8), 2)


def teste_nenhum_passa():
    verificar(ex.resolver([1, 2], 100), 0)


def teste_lista_vazia():
    verificar(ex.resolver([], 0), 0)


def teste_igual_ao_limite_nao_conta():
    verificar(ex.resolver([8, 9], 8), 1,
              dica="O enunciado diz MAIORES que o limite — o 8 não entra.")
