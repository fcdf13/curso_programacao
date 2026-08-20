"""
Devolva uma lista nova com os itens na ordem inversa, **sem alterar**
a lista recebida.

Exemplos:

    resolver([1, 2, 3])  ->  [3, 2, 1]
    resolver([])         ->  []

`lista.reverse()` inverteria a original — não é o que queremos aqui.
"""

META = {
    "id": "A05-007",
    "titulo": "De trás para frente",
    "nivel": 2,
    "tempo_min": 5,
    "tags": ["fatiamento", "inversao"],
    "requer": ["A03-012"],
    "dicas": [
        "O fatiamento com passo -1 funciona igual ao das strings.",
        "itens[::-1] devolve uma cópia invertida.",
        "return itens[::-1]",
    ],
}


def resolver(itens: list) -> list:
    ...
