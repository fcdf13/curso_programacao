"""Testes de B01-002 · Cartão de visita da tabela.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401
import pandas as pd

ex = carregar(__file__)


def teste_tabela_pequena():
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4], "c": [5, 6]})
    verificar(ex.resolver(df), (2, 3, ["a", "b", "c"]))


def teste_tabela_real_de_produtos():
    produtos = t.tabela("produtos")
    verificar(
        ex.resolver(produtos),
        (400, 8, ["produto_id", "nome", "categoria", "subcategoria",
                  "preco", "custo", "peso_kg", "ativo"]),
    )


def teste_devolve_lista_e_nao_index():
    df = pd.DataFrame({"x": [1]})
    verificar(type(ex.resolver(df)[2]), list, nome="tipo do terceiro item",
              dica="df.columns é um Index; envolva em list(...).")
