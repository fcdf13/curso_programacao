"""Testes de C01-001 · Clientes de São Paulo.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar_sql, verificar  # noqa: F401
from curso import teste as t  # noqa: F401
import pandas as pd

ex = carregar_sql(__file__)


def teste_resultado_bate_com_a_tabela():
    clientes = t.tabela("clientes")
    esperado = (
        clientes[clientes["uf"] == "SP"]
        .sort_values("cliente_id")
        .head(10)[["cliente_id", "nome", "cidade"]]
        .reset_index(drop=True)
    )
    verificar(t.consultar(ex), esperado)


def teste_traz_exatamente_dez_linhas():
    verificar(len(t.consultar(ex)), 10, nome="número de linhas",
              dica="Faltou o LIMIT 10, ou ele veio antes do ORDER BY.")


def teste_apenas_colunas_pedidas():
    verificar(list(t.consultar(ex).columns), ["cliente_id", "nome", "cidade"],
              nome="nome das colunas",
              dica="SELECT * traria as 8 colunas — liste só as três pedidas.")
