"""Testes de A05-006 · sorted não é sort.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_ordena_e_preserva():
    verificar(ex.resolver([3, 1, 2]), ([1, 2, 3], [3, 1, 2]),
              dica="Se a original também saiu ordenada, você usou .sort().")


def teste_ja_ordenada():
    verificar(ex.resolver([1, 2]), ([1, 2], [1, 2]))


def teste_com_repetidos():
    verificar(ex.resolver([2, 1, 2]), ([1, 2, 2], [2, 1, 2]))


def teste_a_original_nao_muda_de_fora():
    entrada = [5, 3, 9]
    ex.resolver(entrada)
    verificar(entrada, [5, 3, 9], nome="lista recebida",
              dica="Sua função não deve modificar a lista que recebeu.")
