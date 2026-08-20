"""Testes de A06-012 · Percorrer um texto.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_com_maiuscula():
    verificar(ex.resolver("Aurora"), 4)


def teste_sem_vogais():
    verificar(ex.resolver("XYZ"), 0)


def teste_texto_vazio():
    verificar(ex.resolver(""), 0)


def teste_tudo_maiusculo():
    verificar(ex.resolver("AEIOU"), 5,
              dica="Converta para minúsculas antes de comparar.")
