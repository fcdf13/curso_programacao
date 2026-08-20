"""
Devolva os três primeiros caracteres do texto.

Exemplos:

    resolver("Eletrônicos")  ->  "Ele"
    resolver("Casa")         ->  "Cas"
    resolver("SP")           ->  "SP"

Repare no último caso: se o texto for menor que 3, o fatiamento
simplesmente devolve o que existe, sem erro.
"""

META = {
    "id": "A03-003",
    "titulo": "Um pedaço do texto",
    "nivel": 2,
    "tempo_min": 6,
    "tags": ["fatiamento"],
    "dicas": [
        "Fatiar usa dois pontos dentro dos colchetes: texto[inicio:fim].",
        "O fim é exclusivo — para pegar 3 caracteres a partir do 0, o fim é 3.",
        "return texto[:3]",
    ],
}


def resolver(texto: str) -> str:
    ...
