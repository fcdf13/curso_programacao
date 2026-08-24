"""
Remova o produto do catálogo, se ele existir, e devolva o dicionário.
Se o produto não existir, devolva o dicionário sem alterar nada — sem
estourar erro.

Exemplos:

    resolver({"Fone": 99.9, "Capa": 25.0}, "Capa")  ->  {"Fone": 99.9}
    resolver({"Fone": 99.9}, "Mouse")               ->  {"Fone": 99.9}

`del precos[produto]` estouraria `KeyError` no segundo caso.
`.pop(chave, None)` não estoura.
"""

META = {
    "id": "A08-006",
    "titulo": "Remover uma chave",
    "nivel": 2,
    "tempo_min": 5,
    "tags": ["dict", "pop"],
    "requer": ["A08-005"],
    "dicas": [
        "del estoura erro se a chave não existir; existe uma alternativa que não estoura.",
        "precos.pop(produto, None) remove se existir, e não faz nada (sem erro) se não existir.",
        "precos.pop(produto, None), e depois return precos.",
    ],
}


def resolver(precos: dict, produto: str) -> dict:
    precos.pop(produto, None)
    return precos
