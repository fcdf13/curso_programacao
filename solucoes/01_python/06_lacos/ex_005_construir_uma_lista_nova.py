"""
Devolva uma lista com todos os preços reajustados em 10%,
arredondados para duas casas.

Exemplos:

    resolver([100, 50])   ->  [110.0, 55.0]
    resolver([9.99])      ->  [10.99]
    resolver([])          ->  []

Mesma estrutura do acumulador, mas o que acumula é uma lista:
comece com `[]` e vá acrescentando.
"""

META = {
    "id": "A06-005",
    "titulo": "Construir uma lista nova",
    "nivel": 2,
    "tempo_min": 8,
    "tags": ["for", "append", "transformacao"],
    "requer": ["A05-004"],
    "dicas": [
        "Comece com uma lista vazia antes do laço.",
        "A cada volta, calcule o novo preço e acrescente com .append().",
        "Reajustar em 10% é multiplicar por 1.1.",
    ],
}


def resolver(precos: list) -> list:
    # Este é exatamente o padrão que a list comprehension do módulo A12 vai encurtar.
    reajustados = []
    for preco in precos:
        reajustados.append(round(preco * 1.1, 2))
    return reajustados
