"""
O frete da Loja Aurora depende do estado:

    SP, RJ, MG, ES           ->  15.0   (Sudeste)
    PR, SC, RS               ->  22.0   (Sul)
    qualquer outro estado    ->  35.0

Exemplos:

    resolver("SP")  ->  15.0
    resolver("RS")  ->  22.0
    resolver("AM")  ->  35.0
"""

META = {
    "id": "A04-007",
    "titulo": "Frete por região",
    "nivel": 2,
    "tempo_min": 7,
    "tags": ["elif", "in", "strings"],
    "requer": ["A04-005"],
    "dicas": [
        'Testar uf == "SP" or uf == "RJ" or ... funciona, mas é longo.',
        "in com uma lista deixa cada condição em uma linha só.",
        'if uf in ["SP", "RJ", "MG", "ES"]: return 15.0 — e siga com elif.',
    ],
}


def resolver(uf: str) -> float:
    ...
