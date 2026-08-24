"""Testes de A09-006 · Quem comprou nas duas, rápido.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401
import time  # noqa: F401  (t.cronometrar já cuida da medição)

ex = carregar(__file__)


def teste_caso_pequeno():
    verificar(ex.resolver(["ana", "bruno"], ["bruno", "caio"]), {"bruno"})


def teste_sem_intersecao():
    verificar(ex.resolver(["ana"], ["bruno"]), set())


def teste_grande_e_rapido():
    a = [f"cliente_{i}" for i in range(10_000)]
    b = [f"cliente_{i}" for i in range(5_000, 15_000)]
    esperado = set(a) & set(b)

    with t.cronometrar() as tempo:
        obtido = ex.resolver(a, b)

    verificar(obtido, esperado, nome="conjunto de clientes em comum")
    t.verificar_tempo(
        tempo["segundos"], limite=0.3,
        dica="compare por conjuntos (&), não percorrendo uma lista dentro da outra.",
    )
