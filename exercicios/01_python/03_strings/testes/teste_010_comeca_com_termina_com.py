"""Testes de A03-010 · Começa com, termina com.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_bate_nos_dois():
    verificar(ex.resolver("aurora.pro@loja.com", "aurora", ".com"), (True, True))


def teste_nao_bate_em_nenhum():
    verificar(ex.resolver("teste@loja.org", "aurora", ".com"), (False, False))


def teste_bate_so_no_comeco():
    verificar(ex.resolver("aurora@loja.org", "aurora", ".com"), (True, False))
