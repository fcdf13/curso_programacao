"""
Devolva uma tupla `(lista com todos menos o último, último item)` —
o espelho do exercício anterior.

Exemplos:

    resolver([10, 20, 30])  ->  ([10, 20], 30)
    resolver([5])           ->  ([], 5)

O `*` também funciona no começo do desempacotamento — o que sobra
fica sempre do lado sem asterisco.
"""

META = {
    "id": "A10-007",
    "titulo": "O resto e o último",
    "nivel": 3,
    "tempo_min": 7,
    "tags": ["tupla", "desempacotamento", "star-expression"],
    "requer": ["A10-006"],
    "dicas": [
        "Desta vez o * vai na primeira variável, não na última.",
        '*inicio, ultimo = itens deixa ultimo com o último item, e\\ninicio com todo o resto.',
        "*inicio, ultimo = itens; return inicio, ultimo",
    ],
}


def resolver(itens: list) -> tuple:
    *inicio, ultimo = itens
    return inicio, ultimo
