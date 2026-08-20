"""Testes de A05-007 · De trás para frente.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_inverte():
    verificar(ex.resolver([1, 2, 3]), [3, 2, 1])


def teste_lista_vazia():
    verificar(ex.resolver([]), [])


def teste_nao_altera_a_original():
    entrada = [1, 2, 3]
    ex.resolver(entrada)
    verificar(entrada, [1, 2, 3], nome="lista recebida",
              dica="reverse() altera a original; o fatiamento [::-1] faz uma cópia.")
