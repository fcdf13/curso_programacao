"""
Devolva uma tupla com a primeira e a última letra do texto.

Exemplos:

    resolver("Aurora")  ->  ("A", "a")
    resolver("SP")      ->  ("S", "P")
    resolver("x")       ->  ("x", "x")

A posição do último caractere é `-1` — assim você não precisa
calcular `len(texto) - 1`.
"""

META = {
    "id": "A03-002",
    "titulo": "Primeira e última letra",
    "nivel": 2,
    "tempo_min": 5,
    "tags": ["indexacao"],
    "dicas": [
        "A contagem começa no 0, então o primeiro caractere é texto[0].",
        "Índices negativos contam de trás para frente: -1 é o último.",
        "return texto[0], texto[-1]",
    ],
}


def resolver(texto: str) -> tuple[str, str]:
    return texto[0], texto[-1]
