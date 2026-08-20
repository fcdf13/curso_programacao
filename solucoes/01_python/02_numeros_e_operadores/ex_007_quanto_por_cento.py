"""
Devolva quantos por cento `parte` representa de `total`, arredondado
para uma casa decimal.

Exemplos:

    resolver(25, 200)   ->  12.5
    resolver(1, 3)      ->  33.3
    resolver(200, 200)  ->  100.0

Porcentagem é a fração multiplicada por 100.
"""

META = {
    "id": "A02-007",
    "titulo": "Quanto por cento",
    "nivel": 2,
    "tempo_min": 6,
    "tags": ["porcentagem", "round"],
    "dicas": [
        "Primeiro a fração (parte dividida por total), depois vezes 100.",
        "round(x, 1) deixa uma casa decimal.",
        "return round(parte / total * 100, 1)",
    ],
}


def resolver(parte, total) -> float:
    return round(parte / total * 100, 1)
