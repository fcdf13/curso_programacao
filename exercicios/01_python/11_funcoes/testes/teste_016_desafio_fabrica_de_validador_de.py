"""Testes de A11-016 · Desafio: fábrica de validador de desconto.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_teto_padrao():
    validar = ex.resolver()
    verificar(validar(0.1, 0.6, 0.3), [0.1, 0.3])


def teste_teto_customizado():
    validar_rigido = ex.resolver(teto=0.2)
    verificar(validar_rigido(0.1, 0.6, 0.3), [0.1])


def teste_nenhum_desconto_passa():
    validar = ex.resolver(teto=0.05)
    verificar(validar(0.1, 0.2), [])


def teste_sem_nenhum_desconto_informado():
    validar = ex.resolver()
    verificar(validar(), [])
