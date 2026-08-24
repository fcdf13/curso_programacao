"""Testes de A11-008 · A armadilha do argumento padrão mutável.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_uma_chamada():
    verificar(ex.resolver("Fone"), ["Fone"])


def teste_historico_explicito_acumula():
    verificar(ex.resolver("Capa", ["Fone"]), ["Fone", "Capa"])


def teste_duas_chamadas_sem_historico_nao_compartilham():
    ex.resolver("Fone")
    segunda = ex.resolver("Capa")
    verificar(segunda, ["Capa"])
