"""Testes de A08-010 · A chave do maior valor.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_um_produto_claramente_mais_caro():
    verificar(ex.resolver({"Fone": 200.0, "Notebook": 3000.0, "Capa": 30.0}), "Notebook")


def teste_produto_unico():
    verificar(ex.resolver({"Fone": 200.0}), "Fone")


def teste_nao_e_ordem_alfabetica():
    verificar(ex.resolver({"Zebra": 1.0, "Abelha": 99.0}), "Abelha",
              dica="max(precos) sozinho compararia as chaves em ordem alfabética.")
