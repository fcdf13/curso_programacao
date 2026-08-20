"""
Devolva quantas vezes o valor aparece na lista.

Exemplos:

    resolver(["SP", "RJ", "SP"], "SP")  ->  2
    resolver([1, 2, 3], 9)              ->  0
    resolver([], "a")                   ->  0
"""

META = {
    "id": "A05-011",
    "titulo": "Quantas vezes aparece",
    "nivel": 2,
    "tempo_min": 5,
    "tags": ["count"],
    "requer": ["A03-013"],
    "dicas": [
        "Listas têm o mesmo método de contagem que as strings.",
        "itens.count(valor)",
        "return itens.count(valor)",
    ],
}


def resolver(itens: list, valor) -> int:
    return itens.count(valor)
