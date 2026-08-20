"""
Devolva os **dois primeiros** itens da lista.

Exemplos:

    resolver([10, 20, 30, 40])  ->  [10, 20]
    resolver([7])               ->  [7]
    resolver([])                ->  []

Fatiar lista é igual a fatiar texto — e o resultado é sempre uma lista nova.
"""

META = {
    "id": "A05-003",
    "titulo": "Fatiar a lista",
    "nivel": 2,
    "tempo_min": 5,
    "tags": ["fatiamento"],
    "requer": ["A03-003"],
    "dicas": [
        "Colchetes com dois-pontos: itens[inicio:fim].",
        "Para dois itens a partir do começo, o fim é 2.",
        "return itens[:2]",
    ],
}


def resolver(itens: list) -> list:
    return itens[:2]
