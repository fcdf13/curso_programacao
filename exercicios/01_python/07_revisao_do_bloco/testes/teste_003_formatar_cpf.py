"""Testes de A07-003 · Formatar CPF.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_cpf_normal():
    verificar(ex.resolver("12345678901"), "123.456.789-01")


def teste_cpf_de_zeros():
    verificar(ex.resolver("00000000000"), "000.000.000-00")


def teste_curto_demais():
    verificar(ex.resolver("123"), "invalido")


def teste_vazio():
    verificar(ex.resolver(""), "invalido")


def teste_longo_demais():
    verificar(ex.resolver("123456789012"), "invalido")
