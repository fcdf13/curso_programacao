"""Testes de A08-005 · Criar ou atualizar.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_atualiza_existente():
    verificar(ex.resolver({"Fone": 99.9}, "Fone", 89.9), {"Fone": 89.9})


def teste_cria_novo():
    verificar(ex.resolver({"Fone": 99.9}, "Capa", 25.0),
              {"Fone": 99.9, "Capa": 25.0})


def teste_dicionario_vazio():
    verificar(ex.resolver({}, "Fone", 99.9), {"Fone": 99.9})
