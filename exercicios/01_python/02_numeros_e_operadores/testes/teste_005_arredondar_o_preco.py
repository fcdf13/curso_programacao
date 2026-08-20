"""Testes de A02-005 · Arredondar o preço.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_arredonda_para_cima():
    verificar(ex.resolver(49.876), 49.88)


def teste_ja_esta_redondo():
    verificar(ex.resolver(10.0), 10.0)


def teste_arredonda_para_baixo():
    verificar(ex.resolver(3.14159), 3.14)
