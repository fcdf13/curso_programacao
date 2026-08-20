"""
Devolva uma lista com os números de 1 até n, incluindo o n.

Exemplos:

    resolver(5)  ->  [1, 2, 3, 4, 5]
    resolver(1)  ->  [1]
    resolver(0)  ->  []

Lembre que `range(1, 5)` para no 4 — o fim nunca entra. Para incluir
o n, o fim precisa ser `n + 1`.
"""

META = {
    "id": "A06-002",
    "titulo": "Uma sequência de números",
    "nivel": 2,
    "tempo_min": 6,
    "tags": ["range", "lista"],
    "dicas": [
        "range(inicio, fim) vai do início até o fim MENOS UM.",
        "Para chegar até n, o fim precisa ser n + 1.",
        "list(range(1, n + 1)) transforma o range em lista.",
    ],
}


def resolver(n: int) -> list:
    ...
