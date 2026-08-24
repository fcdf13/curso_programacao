"""Testes de A08-008 · Pares chave-valor.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_dois_produtos():
    verificar(ex.resolver({"Fone": 99.9, "Capa": 25.0}),
              ["Fone: 99.90", "Capa: 25.00"])


def teste_dicionario_vazio():
    verificar(ex.resolver({}), [])
