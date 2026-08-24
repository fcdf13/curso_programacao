"""
Some uma quantidade qualquer de números.

Exemplos:

    resolver(10, 20, 30)  ->  60
    resolver(5)            ->  5
    resolver()              ->  0

`*valores` na assinatura junta qualquer quantidade de argumentos
posicionais numa tupla — de zero a quantos quem chama quiser
passar.
"""

META = {
    "id": "A11-003",
    "titulo": "*args: uma quantidade qualquer de argumentos",
    "nivel": 2,
    "tempo_min": 6,
    "tags": ["funcoes", "args", "variadico"],
    "dicas": [
        "*valores junta qualquer quantidade de argumentos posicionais numa tupla.",
        "Dentro da função, valores já é uma tupla comum — soma dá para fazer com sum().",
        "return sum(valores)",
    ],
}


def resolver(*valores) -> float:
    ...
