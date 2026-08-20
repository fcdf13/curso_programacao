"""Testes de C05-001 · Resumo do catálogo.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar_sql, verificar  # noqa: F401
from curso import teste as t  # noqa: F401
import pandas as pd

ex = carregar_sql(__file__)


def teste_resumo_completo():
    produtos = t.tabela("produtos")
    esperado = pd.DataFrame({
        "total_produtos": [len(produtos)],
        "categorias": [produtos["categoria"].nunique()],
        "preco_medio": [produtos["preco"].mean()],
        "preco_maximo": [produtos["preco"].max()],
    })
    verificar(t.consultar(ex), esperado, tolerancia=1e-6)


def teste_uma_linha_so():
    verificar(len(t.consultar(ex)), 1, nome="número de linhas",
              dica="Agregação sem GROUP BY sempre devolve exatamente uma linha.")


def teste_categorias_sao_distintas():
    produtos = t.tabela("produtos")
    verificar(int(t.consultar(ex)["categorias"].iloc[0]),
              produtos["categoria"].nunique(), nome="total de categorias",
              dica="Sem o DISTINCT, você contaria 400 — uma por produto.")
