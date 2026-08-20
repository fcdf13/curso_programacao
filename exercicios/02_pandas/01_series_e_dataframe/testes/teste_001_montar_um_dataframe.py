"""Testes de B01-001 · Montar um DataFrame.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401
import pandas as pd

ex = carregar(__file__)


def teste_duas_linhas():
    esperado = pd.DataFrame({"nome": ["Fone", "Capa"], "preco": [49.9, 12.0]})
    verificar(ex.resolver(["Fone", "Capa"], [49.9, 12.0]), esperado)


def teste_uma_linha():
    esperado = pd.DataFrame({"nome": ["Livro"], "preco": [30.0]})
    verificar(ex.resolver(["Livro"], [30.0]), esperado)


def teste_listas_vazias():
    resultado = ex.resolver([], [])
    verificar(list(resultado.columns), ["nome", "preco"], nome="nome das colunas")
    verificar(len(resultado), 0, nome="número de linhas")
