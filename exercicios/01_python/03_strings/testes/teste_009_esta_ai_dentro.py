"""Testes de A03-009 · Está aí dentro?.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_encontra():
    verificar(ex.resolver("Fone Aurora Pro", "Aurora"), True)


def teste_caixa_diferente_nao_encontra():
    verificar(ex.resolver("Fone Aurora Pro", "aurora"), False)


def teste_texto_vazio_sempre_existe():
    verificar(ex.resolver("Fone", ""), True)
