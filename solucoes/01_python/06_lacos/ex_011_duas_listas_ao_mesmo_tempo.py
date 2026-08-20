"""
Você recebe os nomes dos produtos e seus preços, em duas listas alinhadas.
Devolva uma lista de textos no formato `"nome: preço"`, com duas casas.

Exemplos:

    resolver(["Fone", "Capa"], [99.9, 25])  ->  ["Fone: 99.90", "Capa: 25.00"]
    resolver([], [])                        ->  []

`zip` anda nas duas listas em paralelo e para na mais curta.
"""

META = {
    "id": "A06-011",
    "titulo": "Duas listas ao mesmo tempo",
    "nivel": 2,
    "tempo_min": 8,
    "tags": ["zip", "for"],
    "dicas": [
        "for nome, preco in zip(nomes, precos): pega um par por volta.",
        "A formatação de duas casas é {preco:.2f} dentro da f-string.",
        'Acrescente f"{nome}: {preco:.2f}" numa lista de resultados.',
    ],
}


def resolver(nomes: list, precos: list) -> list:
    linhas = []
    for nome, preco in zip(nomes, precos):
        linhas.append(f"{nome}: {preco:.2f}")
    return linhas
