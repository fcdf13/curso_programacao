"""Testes de A08-014 · Clientes de duas campanhas.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_caso_geral():
    verificar(
        ex.resolver(["ana", "bruno", "caio"], ["bruno", "caio", "duda"]),
        ({"bruno", "caio"}, {"ana"}, {"duda"}),
    )


def teste_sem_sobreposicao():
    verificar(ex.resolver(["ana"], ["bruno"]), (set(), {"ana"}, {"bruno"}))


def teste_listas_identicas():
    verificar(ex.resolver(["ana", "bruno"], ["ana", "bruno"]),
              ({"ana", "bruno"}, set(), set()))


def teste_uma_lista_vazia():
    verificar(ex.resolver([], ["ana"]), (set(), set(), {"ana"}))
