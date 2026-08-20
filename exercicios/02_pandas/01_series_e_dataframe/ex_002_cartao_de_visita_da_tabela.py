"""
A primeira coisa que se faz com uma tabela desconhecida é medi-la.

Devolva a tupla `(número de linhas, número de colunas, lista com os
nomes das colunas)`.

Exemplo, para a tabela de produtos da Loja Aurora:

    resolver(produtos)
    ->  (400, 8, ['produto_id', 'nome', 'categoria', 'subcategoria',
                  'preco', 'custo', 'peso_kg', 'ativo'])

`df.shape` já devolve `(linhas, colunas)` numa tupla. `df.columns`
devolve os nomes — mas num objeto Index, que você precisa converter
para lista.
"""

META = {
    "id": "B01-002",
    "titulo": "Cartão de visita da tabela",
    "nivel": 2,
    "tempo_min": 7,
    "tags": ["shape", "columns", "inspecao"],
    "requer": ["B01-001"],
    "dicas": [
        "shape é um atributo, não um método: df.shape, sem parênteses.",
        "df.shape[0] são as linhas e df.shape[1] as colunas.",
        "list(df.columns) converte o Index para uma lista de verdade.",
    ],
}


import pandas as pd


def resolver(df: pd.DataFrame) -> tuple:
    ...
