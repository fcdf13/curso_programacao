"""Testes de A07-008 · Fechamento do mês.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_duas_categorias():
    verificar(
        ex.resolver(["moda", "casa"], [1000.0, 500.0], [10, 5]),
        ["MODA: R$ 1000.00 em 10 pedidos (ticket R$ 100.00)",
         "CASA: R$ 500.00 em 5 pedidos (ticket R$ 100.00)",
         "TOTAL: R$ 1500.00 em 15 pedidos"],
    )


def teste_ignora_categoria_sem_pedidos():
    verificar(
        ex.resolver(["moda", "vazia"], [100.0, 0.0], [2, 0]),
        ["MODA: R$ 100.00 em 2 pedidos (ticket R$ 50.00)",
         "TOTAL: R$ 100.00 em 2 pedidos"],
        dica="Categoria com 0 pedidos sai do relatório e não entra no total.",
    )


def teste_tudo_vazio():
    verificar(ex.resolver([], [], []), ["TOTAL: R$ 0.00 em 0 pedidos"])


def teste_todas_sem_pedidos():
    verificar(ex.resolver(["a"], [0.0], [0]), ["TOTAL: R$ 0.00 em 0 pedidos"])


def teste_ticket_quebrado():
    verificar(
        ex.resolver(["livros"], [100.0], [3]),
        ["LIVROS: R$ 100.00 em 3 pedidos (ticket R$ 33.33)",
         "TOTAL: R$ 100.00 em 3 pedidos"],
    )
