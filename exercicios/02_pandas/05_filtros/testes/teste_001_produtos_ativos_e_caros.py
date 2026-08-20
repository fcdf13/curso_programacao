"""Testes de B05-001 · Produtos ativos e caros.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401
import pandas as pd

ex = carregar(__file__)


def _amostra():
    return pd.DataFrame({
        "nome": ["Fone", "Capa", "Notebook"],
        "preco": [200.0, 30.0, 3000.0],
        "ativo": [True, True, False],
    })


def teste_filtra_por_preco_e_por_ativo():
    esperado = _amostra().iloc[[0]]
    verificar(ex.resolver(_amostra(), 100), esperado)


def teste_limite_inclui_o_valor_exato():
    esperado = _amostra().iloc[[0]]
    verificar(ex.resolver(_amostra(), 200), esperado,
              dica="O enunciado diz MAIOR OU IGUAL: o preço exato entra.")


def teste_nenhum_produto_passa():
    verificar(len(ex.resolver(_amostra(), 99999)), 0, nome="número de linhas")


def teste_mantem_todas_as_colunas():
    verificar(list(ex.resolver(_amostra(), 0).columns), ["nome", "preco", "ativo"],
              nome="nome das colunas")


def teste_na_tabela_real():
    produtos = t.tabela("produtos")
    esperado = produtos.query("ativo and preco >= 1000")
    verificar(ex.resolver(produtos, 1000), esperado)
