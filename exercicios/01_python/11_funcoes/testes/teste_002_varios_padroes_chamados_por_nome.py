"""Testes de A11-002 · Vários padrões, chamados por nome.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_so_produto():
    verificar(ex.resolver("Fone"), "1x Fone")


def teste_com_quantidade():
    verificar(ex.resolver("Fone", 3), "3x Fone")


def teste_pulando_quantidade_por_nome():
    verificar(ex.resolver("Fone", desconto=0.1), "1x Fone (10% de desconto)")


def teste_todos_os_argumentos():
    verificar(ex.resolver("Fone", 2, 0.2), "2x Fone (20% de desconto)")
