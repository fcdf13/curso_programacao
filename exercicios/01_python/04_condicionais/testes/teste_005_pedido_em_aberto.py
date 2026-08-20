"""Testes de A04-005 · Pedido em aberto.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_processando():
    verificar(ex.resolver("processando"), True)


def teste_enviado():
    verificar(ex.resolver("enviado"), True)


def teste_entregue():
    verificar(ex.resolver("entregue"), False)


def teste_cancelado():
    verificar(ex.resolver("cancelado"), False)


def teste_status_desconhecido():
    verificar(ex.resolver("devolvido"), True)
