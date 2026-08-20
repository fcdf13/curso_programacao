"""
Dentro de uma f-string, dois-pontos abre o formato do valor:

    f"{1234.5:.2f}"    ->  '1234.50'

O `.2f` significa "número com vírgula, exatamente 2 casas".

Devolva o preço formatado como moeda:

    resolver(1234.5)  ->  "R$ 1234.50"
    resolver(9.999)   ->  "R$ 10.00"
    resolver(0)       ->  "R$ 0.00"
"""

META = {
    "id": "A03-011",
    "titulo": "Formatar dinheiro",
    "nivel": 2,
    "tempo_min": 6,
    "tags": ["f-string", "formatacao"],
    "requer": ["A01-010"],
    "dicas": [
        'O prefixo "R$ " é texto comum dentro da f-string.',
        "O formato vai depois de dois-pontos, dentro das chaves: {preco:.2f}.",
        'return f"R$ {preco:.2f}"',
    ],
}


def resolver(preco: float) -> str:
    ...
