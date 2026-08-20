"""
Devolva quantos caracteres tem o texto recebido.

Exemplos:

    resolver("Aurora")  ->  6
    resolver("")        ->  0
    resolver("a b")     ->  3

Espaços contam como caractere.
"""

META = {
    "id": "A03-001",
    "titulo": "Tamanho do texto",
    "nivel": 1,
    "tempo_min": 3,
    "tags": ["len"],
    "dicas": [
        "Existe uma função pronta para medir o tamanho de qualquer sequência.",
        "É len(...), de length.",
        "return len(texto)",
    ],
}


def resolver(texto: str) -> int:
    return len(texto)
