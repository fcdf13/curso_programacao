"""Testes de A03-006 · Trocar um pedaço.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_dois_hifens():
    verificar(ex.resolver("SP-01-A"), "SP/01/A")


def teste_sem_hifen():
    verificar(ex.resolver("SP01"), "SP01")


def teste_so_o_hifen():
    verificar(ex.resolver("-"), "/")
