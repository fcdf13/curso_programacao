"""
Monte um dicionário `produto -> preço`, mas só com os produtos
cujo preço é maior ou igual a um mínimo.

Exemplo:

    resolver(["Fone", "Capa"], [150.0, 20.0], 100.0)
    ->  {"Fone": 150.0}

Igual ao exercício anterior, com um `if` no fim — o mesmo
filtro que você já usou na list comprehension.
"""

META = {
    "id": "A12-005",
    "titulo": "Dict comprehension com filtro",
    "nivel": 3,
    "tempo_min": 7,
    "tags": ["compreensao", "dict-comprehension", "filtro"],
    "requer": ["A12-004", "A12-002"],
    "dicas": [
        'O if de filtro funciona em dict comprehension do mesmo jeito\nque em list comprehension.',
        "{nome: preco for nome, preco in zip(produtos, precos) if preco >= minimo}",
        "return {nome: preco for nome, preco in zip(produtos, precos) if preco >= minimo}",
    ],
}


def resolver(produtos: list, precos: list, minimo: float) -> dict:
    return {nome: preco for nome, preco in zip(produtos, precos) if preco >= minimo}
