"""Testes de A11-015 · Contador com nonlocal.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_conta_a_partir_de_um():
    contador = ex.resolver()
    verificar(contador(), 1)
    verificar(contador(), 2)
    verificar(contador(), 3)


def teste_dois_contadores_sao_independentes():
    a = ex.resolver()
    b = ex.resolver()
    a()
    a()
    verificar(b(), 1)
