"""Testes de A11-014 · Função que devolve função.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_vezes_tres():
    vezes3 = ex.resolver(3)
    verificar(vezes3(10), 30)
    verificar(vezes3(2), 6)


def teste_duas_fabricas_sao_independentes():
    vezes2 = ex.resolver(2)
    vezes5 = ex.resolver(5)
    verificar(vezes2(10), 20)
    verificar(vezes5(10), 50)
