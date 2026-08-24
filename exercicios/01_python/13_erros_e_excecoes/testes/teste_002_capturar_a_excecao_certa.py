"""Testes de A13-002 · Capturar a exceção certa.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_texto_valido():
    verificar(ex.resolver("42"), 42)


def teste_texto_invalido():
    verificar(ex.resolver("abc"), None)


def teste_texto_vazio():
    verificar(ex.resolver(""), None)


def teste_numero_negativo_em_texto():
    verificar(ex.resolver("-7"), -7)
