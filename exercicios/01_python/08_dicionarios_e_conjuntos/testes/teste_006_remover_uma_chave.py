"""Testes de A08-006 · Remover uma chave.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_remove_existente():
    verificar(ex.resolver({"Fone": 99.9, "Capa": 25.0}, "Capa"), {"Fone": 99.9})


def teste_remove_inexistente_nao_quebra():
    verificar(ex.resolver({"Fone": 99.9}, "Mouse"), {"Fone": 99.9},
              dica="del estouraria KeyError aqui — use .pop(produto, None).")
