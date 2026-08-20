"""Testes de A04-011 · Que triângulo é esse.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_equilatero():
    verificar(ex.resolver(3, 3, 3), "equilatero")


def teste_isosceles():
    verificar(ex.resolver(5, 5, 3), "isosceles")


def teste_isosceles_em_outra_posicao():
    verificar(ex.resolver(3, 5, 5), "isosceles")


def teste_escaleno():
    verificar(ex.resolver(3, 4, 5), "escaleno")


def teste_invalido_por_folga():
    verificar(ex.resolver(1, 2, 10), "invalido")


def teste_invalido_no_limite():
    verificar(ex.resolver(1, 2, 3), "invalido",
              dica="A soma precisa ser MAIOR que o terceiro lado; 1+2 é igual a 3.")
