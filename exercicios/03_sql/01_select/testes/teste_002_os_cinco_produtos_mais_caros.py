"""Testes de C01-002 · Os cinco produtos mais caros.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar_sql, verificar  # noqa: F401
from curso import teste as t  # noqa: F401
import pandas as pd

ex = carregar_sql(__file__)


def teste_resultado_bate_com_a_tabela():
    produtos = t.tabela("produtos")
    esperado = (
        produtos[produtos["ativo"]]
        .sort_values("preco", ascending=False)
        .head(5)[["nome", "preco"]]
        .rename(columns={"nome": "produto", "preco": "preco_atual"})
        .reset_index(drop=True)
    )
    verificar(t.consultar(ex), esperado)


def teste_colunas_renomeadas():
    verificar(list(t.consultar(ex).columns), ["produto", "preco_atual"],
              nome="nome das colunas",
              dica="Use AS para renomear: SELECT nome AS produto, preco AS preco_atual.")


def teste_ordem_decrescente():
    precos = t.consultar(ex)["preco_atual"].tolist()
    verificar(precos, sorted(precos, reverse=True), nome="ordem dos preços",
              dica="Faltou o DESC no ORDER BY.")
