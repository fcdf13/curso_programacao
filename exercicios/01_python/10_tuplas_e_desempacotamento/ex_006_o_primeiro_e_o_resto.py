"""
Devolva uma tupla `(primeiro item, lista com os demais)`.

Exemplos:

    resolver([10, 20, 30])  ->  (10, [20, 30])
    resolver([5])           ->  (5, [])

`*resto` no desempacotamento junta "tudo que sobrou" numa lista —
mesmo que a entrada seja só um item.
"""

META = {
    "id": "A10-006",
    "titulo": "O primeiro e o resto",
    "nivel": 3,
    "tempo_min": 7,
    "tags": ["tupla", "desempacotamento", "star-expression"],
    "requer": ["A10-005"],
    "dicas": [
        "O desempacotamento aceita um * na frente de uma das variáveis.",
        "primeiro, *resto = itens separa o primeiro do restante.",
        "primeiro, *resto = itens; return primeiro, resto",
    ],
}


def resolver(itens: list) -> tuple:
    ...
