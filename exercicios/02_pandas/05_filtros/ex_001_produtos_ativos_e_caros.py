"""
Devolva apenas os produtos que estão **ativos** e cujo preço é
**maior ou igual** ao mínimo informado.

Mantenha todas as colunas e a ordem original das linhas.

Exemplo:

    produtos = pd.DataFrame({
        "nome":  ["Fone", "Capa", "Notebook"],
        "preco": [200.0,  30.0,   3000.0],
        "ativo": [True,   True,   False],
    })
    resolver(produtos, 100)

    ->        nome  preco  ativo
        0     Fone  200.0   True

O Notebook fica de fora por estar inativo; a Capa, por ser barata.

Lembre: em Pandas o "e" é `&`, e cada condição vai entre parênteses.
"""

META = {
    "id": "B05-001",
    "titulo": "Produtos ativos e caros",
    "nivel": 2,
    "tempo_min": 8,
    "tags": ["filtro", "mascara-booleana", "and"],
    "dicas": [
        "Cada condição vira uma máscara booleana separada.",
        "Combine as duas com & — e ponha parênteses em volta de cada uma.",
        'return produtos[(produtos["ativo"]) & (produtos["preco"] >= preco_minimo)]',
    ],
}


import pandas as pd


def resolver(produtos: pd.DataFrame, preco_minimo: float) -> pd.DataFrame:
    ...
