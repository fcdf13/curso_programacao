"""Testes de A11-003 · *args: uma quantidade qualquer de argumentos.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_tres_valores():
    verificar(ex.resolver(10, 20, 30), 60)


def teste_um_valor():
    verificar(ex.resolver(5), 5)


def teste_nenhum_valor():
    verificar(ex.resolver(), 0)
