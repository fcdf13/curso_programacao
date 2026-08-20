"""Testes de A01-011 · Média de três notas.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_media_simples():
    verificar(ex.resolver(10, 8, 6), 8.0)


def teste_media_de_iguais():
    verificar(ex.resolver(5, 5, 5), 5.0)


def teste_media_com_dizima():
    verificar(ex.resolver(4, 5, 5), 14 / 3,
              dica="Sem parênteses, o Python divide c por 3 antes de somar.")
