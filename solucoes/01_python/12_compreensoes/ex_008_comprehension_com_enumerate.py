"""
Devolva as posições (a partir de 0) dos preços maiores que um
limite.

Exemplo:

    resolver([10.0, 500.0, 5.0, 800.0], 100.0)  ->  [1, 3]

`enumerate` entrega posição e item ao mesmo tempo, como no
módulo A6 — dentro da comprehension funciona igual:
`for posicao, preco in enumerate(precos)`.
"""

META = {
    "id": "A12-008",
    "titulo": "Comprehension com enumerate",
    "nivel": 3,
    "tempo_min": 7,
    "tags": ["compreensao", "enumerate", "filtro"],
    "requer": ["A12-002", "A06-010"],
    "dicas": [
        'for posicao, preco in enumerate(precos) desempacota os dois,\ndentro da comprehension.',
        "A expressão é só a posicao; o filtro é if preco > limite.",
        "return [posicao for posicao, preco in enumerate(precos) if preco > limite]",
    ],
}


def resolver(precos: list, limite: float) -> list:
    return [posicao for posicao, preco in enumerate(precos) if preco > limite]
