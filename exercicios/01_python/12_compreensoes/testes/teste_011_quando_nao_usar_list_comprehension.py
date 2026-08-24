"""Testes de A12-011 · Quando não usar list comprehension.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401
import time  # noqa: F401  (t.cronometrar já cuida da medição)

ex = carregar(__file__)


def teste_encontra_acima_do_limite():
    verificar(ex.resolver([10.0, 5000.0, 20.0], 1000.0), True)


def teste_nenhum_acima_do_limite():
    verificar(ex.resolver([10.0, 20.0], 1000.0), False)


def teste_lista_vazia():
    verificar(ex.resolver([], 1000.0), False)


def teste_generator_para_cedo_numa_lista_enorme():
    # 5 milhões de preços, com o único valor alto logo no início: any() com
    # uma expressão geradora encontra a resposta quase na hora; any() com
    # uma list comprehension precisa montar a lista dos 5 milhões primeiro.
    precos = [10.0] * 5_000_000
    precos[0] = 999_999.0

    with t.cronometrar() as tempo:
        obtido = ex.resolver(precos, 500_000.0)

    verificar(obtido, True)
    t.verificar_tempo(
        tempo["segundos"], limite=0.5,
        dica="troque any([... for ...]) por any(... for ...), sem colchetes.",
    )
