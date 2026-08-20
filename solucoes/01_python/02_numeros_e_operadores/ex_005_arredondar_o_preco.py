"""
Dinheiro tem duas casas decimais. Devolva o valor arredondado para centavos.

Exemplos:

    resolver(49.876)   ->  49.88
    resolver(10.0)     ->  10.0
    resolver(3.14159)  ->  3.14
"""

META = {
    "id": "A02-005",
    "titulo": "Arredondar o preço",
    "nivel": 2,
    "tempo_min": 5,
    "tags": ["round", "dinheiro"],
    "dicas": [
        "round(valor) arredonda para inteiro; ele aceita um segundo argumento.",
        "O segundo argumento é quantas casas decimais manter.",
        "return round(valor, 2)",
    ],
}


def resolver(valor: float) -> float:
    return round(valor, 2)
