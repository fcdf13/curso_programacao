"""Testes de A11-005 · **kwargs: os argumentos nomeados soltos.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_duas_caracteristicas():
    verificar(ex.resolver(cor="azul", tamanho="M"), {"cor": "azul", "tamanho": "M"})


def teste_sem_nenhuma():
    verificar(ex.resolver(), {})


def teste_uma_caracteristica():
    verificar(ex.resolver(cor="preto"), {"cor": "preto"})
