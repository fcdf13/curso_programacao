"""Testes de A01-004 · Guardar em uma variável.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_devolve_o_nome_da_loja():
    verificar(ex.resolver(), "Aurora")
