"""
Devolva só os preços que são maiores ou iguais a um mínimo.

Exemplo:

    resolver([10.0, 200.0, 50.0], 100.0)  ->  [200.0]

Um `if` no fim da comprehension filtra: só os itens que passam
nele viram parte do resultado. `[item for item in lista if condicao]`.
"""

META = {
    "id": "A12-002",
    "titulo": "List comprehension com filtro",
    "nivel": 2,
    "tempo_min": 6,
    "tags": ["compreensao", "filtro"],
    "requer": ["A12-001"],
    "dicas": [
        "O if vai depois do for, dentro dos mesmos colchetes.",
        "[preco for preco in precos if preco >= minimo]",
        "return [preco for preco in precos if preco >= minimo]",
    ],
}


def resolver(precos: list, minimo: float) -> list:
    return [preco for preco in precos if preco >= minimo]
