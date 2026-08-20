"""Testes de A04-010 · Ano bissexto.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_ano_comum_bissexto():
    verificar(ex.resolver(2024), True)


def teste_ano_normal():
    verificar(ex.resolver(2023), False)


def teste_seculo_nao_bissexto():
    verificar(ex.resolver(1900), False,
              dica="1900 é divisível por 100 e não por 400 — logo, não é bissexto.")


def teste_seculo_bissexto():
    verificar(ex.resolver(2000), True,
              dica="2000 é divisível por 400, então a regra do 100 não vale.")


def teste_outro_ano_par():
    verificar(ex.resolver(2022), False)


def teste_ano_zero():
    verificar(ex.resolver(0), True)
