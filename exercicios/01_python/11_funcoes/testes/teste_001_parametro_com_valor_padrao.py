"""Testes de A11-001 · Parâmetro com valor padrão.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_saudacao_padrao():
    verificar(ex.resolver("Ana"), "Olá, Ana!")


def teste_saudacao_customizada():
    verificar(ex.resolver("Ana", "Bem-vindo"), "Bem-vindo, Ana!")


def teste_saudacao_por_nome():
    verificar(ex.resolver("Bruno", saudacao="E aí"), "E aí, Bruno!")
