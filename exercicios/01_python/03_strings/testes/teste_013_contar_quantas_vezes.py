"""Testes de A03-013 · Contar quantas vezes.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_duas_ocorrencias():
    verificar(ex.resolver("aurora", "r"), 2)


def teste_nenhuma_ocorrencia():
    verificar(ex.resolver("aurora", "z"), 0)


def teste_nao_conta_sobreposicao():
    verificar(ex.resolver("aaaa", "aa"), 2)
