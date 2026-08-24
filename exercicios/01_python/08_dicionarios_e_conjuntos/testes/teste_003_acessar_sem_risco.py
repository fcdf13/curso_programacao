"""Testes de A08-003 · Acessar sem risco.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_produto_existe():
    verificar(ex.resolver({"Fone": 99.9}, "Fone"), 99.9)


def teste_produto_nao_existe():
    verificar(ex.resolver({"Fone": 99.9}, "Mouse"), 0.0,
              dica="precos[produto] estouraria KeyError; use .get(produto, 0.0).")


def teste_catalogo_vazio():
    verificar(ex.resolver({}, "Fone"), 0.0)
