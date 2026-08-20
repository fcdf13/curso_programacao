"""
Um formulário sempre entrega números como **texto**: `"7"`, e não `7`.
E texto não soma — gruda:

    "7" + "3"    ->  "73"
    int("7") + int("3")  ->  10

Você recebe duas quantidades em texto. Devolva a soma delas como número.

Exemplos:

    resolver("7", "3")     ->  10
    resolver("100", "25")  ->  125
"""

META = {
    "id": "A01-007",
    "titulo": "De texto para número",
    "nivel": 2,
    "tempo_min": 5,
    "tags": ["conversao", "int"],
    "dicas": [
        'int("7") transforma o texto "7" no número 7.',
        "Converta cada um dos dois antes de somar.",
        "return int(a) + int(b)",
    ],
}


def resolver(a: str, b: str) -> int:
    # Converter na entrada é a regra: dado de fora chega como texto até prova em contrário.
    return int(a) + int(b)
