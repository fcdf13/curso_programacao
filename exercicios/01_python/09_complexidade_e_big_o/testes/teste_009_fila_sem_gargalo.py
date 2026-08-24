"""Testes de A09-009 · Fila sem gargalo.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401
import time  # noqa: F401  (t.cronometrar já cuida da medição)
from collections import deque

ex = carregar(__file__)


def teste_uma_rodada_mantem_a_ordem():
    verificar(ex.resolver(["p1", "p2", "p3"], 1), ["p1", "p2", "p3"])


def teste_duas_rodadas():
    verificar(ex.resolver(["p1", "p2", "p3"], 2), ["p1", "p2", "p3"])


def teste_fila_vazia():
    verificar(ex.resolver([], 3), [])


def teste_grande_e_rapido():
    def round_robin_referencia(pedidos, rodadas):
        # Implementação de referência, independente da solução do exercício —
        # existe só para calcular o esperado, não para servir de gabarito.
        fila = deque(pedidos)
        restam = {p: rodadas for p in pedidos}
        concluidos = []
        while fila:
            atual = fila.popleft()
            restam[atual] -= 1
            if restam[atual] == 0:
                concluidos.append(atual)
            else:
                fila.append(atual)
        return concluidos

    pedidos = [f"p{i}" for i in range(80_000)]
    esperado = round_robin_referencia(pedidos, 3)

    with t.cronometrar() as tempo:
        obtido = ex.resolver(pedidos, 3)

    verificar(obtido, esperado, nome="ordem de conclusão")
    t.verificar_tempo(
        tempo["segundos"], limite=0.5,
        dica="troque a lista por collections.deque, e pop(0) por popleft().",
    )
