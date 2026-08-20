"""
Listas respondem a `+` e a `*` como as strings:

    [1, 2] + [3]   ->  [1, 2, 3]
    [0] * 3        ->  [0, 0, 0]

Devolva a tupla `(as duas listas juntas, a primeira repetida 2 vezes)`.

Exemplos:

    resolver([1], [2, 3])   ->  ([1, 2, 3], [1, 1])
    resolver([], ["a"])     ->  (["a"], [])
"""

META = {
    "id": "A05-010",
    "titulo": "Juntar e repetir",
    "nivel": 2,
    "tempo_min": 6,
    "tags": ["concatenacao", "repeticao"],
    "dicas": [
        "+ concatena duas listas numa terceira.",
        "* repete os itens de uma lista.",
        "return a + b, a * 2",
    ],
}


def resolver(a: list, b: list) -> tuple[list, list]:
    return a + b, a * 2
