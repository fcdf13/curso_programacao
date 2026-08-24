"""
Aplique uma operação (`"soma"` ou `"produto"`) sobre uma
quantidade qualquer de números.

Exemplos:

    resolver("soma", 1, 2, 3)      ->  6
    resolver("produto", 2, 3, 4)   ->  24
    resolver("produto")             ->  1

`*args` pode vir depois de um parâmetro fixo — a assinatura é
`def resolver(operacao, *numeros)`.
"""

META = {
    "id": "A11-004",
    "titulo": "*args ao lado de um parâmetro fixo",
    "nivel": 2,
    "tempo_min": 7,
    "tags": ["funcoes", "args", "variadico"],
    "requer": ["A11-003"],
    "dicas": [
        "Parâmetros fixos vêm antes do *args na assinatura: def resolver(operacao, *numeros).",
        "numeros continua sendo uma tupla comum — some com sum(), multiplique com um laço.",
        'if operacao == "soma":\n        return sum(numeros)\n    total = 1\n    for n in numeros:\n        total *= n\n    return total',
    ],
}


def resolver(operacao: str, *numeros) -> float:
    # Multiplicação não tem um sum() pronto — o acumulador começa em 1 (o neutro da multiplicação), não em 0.
    if operacao == "soma":
        return sum(numeros)
    total = 1
    for n in numeros:
        total *= n
    return total
