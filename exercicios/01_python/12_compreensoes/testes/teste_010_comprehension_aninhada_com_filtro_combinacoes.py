"""Testes de A12-010 · Comprehension aninhada com filtro: combinações.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_exclui_sp_luxo():
    verificar(
        ex.resolver(["SP", "RJ"], ["Moda", "Luxo"]),
        [("SP", "Moda"), ("RJ", "Moda"), ("RJ", "Luxo")],
    )


def teste_sem_luxo_nao_exclui_nada():
    verificar(
        ex.resolver(["SP", "RJ"], ["Moda", "Casa"]),
        [("SP", "Moda"), ("SP", "Casa"), ("RJ", "Moda"), ("RJ", "Casa")],
    )


def teste_lista_de_ufs_vazia():
    verificar(ex.resolver([], ["Moda"]), [])
