"""Testes de A08-002 · Acessar com risco.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_acha_o_preco():
    verificar(ex.resolver({"Fone": 99.9, "Capa": 25.0}, "Fone"), 99.9)


def teste_outro_produto():
    verificar(ex.resolver({"Fone": 99.9, "Capa": 25.0}, "Capa"), 25.0)
