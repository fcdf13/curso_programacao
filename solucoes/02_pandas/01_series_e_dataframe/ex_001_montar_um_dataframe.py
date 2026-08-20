"""
Monte um DataFrame de duas colunas a partir de duas listas.

A coluna com os nomes deve se chamar `nome`; a com os preços, `preco`.
A ordem das colunas importa: `nome` primeiro.

Exemplo:

    resolver(["Fone", "Capa"], [49.9, 12.0])

    ->     nome  preco
        0  Fone   49.9
        1  Capa   12.0

A forma mais direta é passar um dicionário para `pd.DataFrame`:
cada chave vira o nome de uma coluna, e cada valor, o conteúdo dela.
"""

META = {
    "id": "B01-001",
    "titulo": "Montar um DataFrame",
    "nivel": 1,
    "tempo_min": 6,
    "tags": ["dataframe", "criacao"],
    "dicas": [
        "pd.DataFrame(...) aceita um dicionário de {nome_da_coluna: lista}.",
        'As chaves do dicionário são exatamente os nomes pedidos: "nome" e "preco".',
        'return pd.DataFrame({"nome": nomes, "preco": precos})',
    ],
}


import pandas as pd


def resolver(nomes: list, precos: list) -> pd.DataFrame:
    # A ordem das chaves do dicionário vira a ordem das colunas.
    return pd.DataFrame({"nome": nomes, "preco": precos})
