"""Testes de A09-007 · Sem repetir, na ordem, rápido.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401
import time  # noqa: F401  (t.cronometrar já cuida da medição)

ex = carregar(__file__)


def teste_caso_pequeno():
    verificar(ex.resolver([3, 1, 3, 2, 1]), [3, 1, 2])


def teste_sem_repeticao():
    verificar(ex.resolver([1, 2, 3]), [1, 2, 3])


def teste_lista_vazia():
    verificar(ex.resolver([]), [])


def teste_grande_e_rapido():
    dados = list(range(10_000)) * 3
    esperado = list(range(10_000))

    with t.cronometrar() as tempo:
        obtido = ex.resolver(dados)

    verificar(obtido, esperado)
    t.verificar_tempo(
        tempo["segundos"], limite=0.35,
        dica="troque 'if item not in resultado' por uma checagem num set à parte.",
    )
