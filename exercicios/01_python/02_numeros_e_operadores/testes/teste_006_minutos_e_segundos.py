"""Testes de A02-006 · Minutos e segundos.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_minutos_e_sobra():
    verificar(ex.resolver(125), (2, 5))


def teste_minuto_exato():
    verificar(ex.resolver(60), (1, 0))


def teste_menos_de_um_minuto():
    verificar(ex.resolver(45), (0, 45))


def teste_mais_de_uma_hora():
    verificar(ex.resolver(3661), (61, 1))
