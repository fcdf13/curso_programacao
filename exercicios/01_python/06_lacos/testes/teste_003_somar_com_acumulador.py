"""Testes de A06-003 · Somar com acumulador.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_soma_simples():
    verificar(ex.resolver([1, 2, 3]), 6)


def teste_lista_vazia():
    verificar(ex.resolver([]), 0,
              dica="Com o total iniciado em 0 antes do laço, este caso sai de graça.")


def teste_com_negativos():
    verificar(ex.resolver([-1, 1]), 0)


def teste_lista_longa():
    verificar(ex.resolver(list(range(1, 101))), 5050,
              dica="Se veio só 1, o return está dentro do laço.")
