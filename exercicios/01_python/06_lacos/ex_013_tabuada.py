"""
Devolva uma lista com todos os produtos da tabuada, de `1 x 1` até
`n x n`, lidos linha por linha.

Exemplos:

    resolver(2)  ->  [1, 2, 2, 4]
    resolver(3)  ->  [1, 2, 3, 2, 4, 6, 3, 6, 9]
    resolver(1)  ->  [1]

Para n=2 a leitura é: 1x1, 1x2, 2x1, 2x2.

Isso pede um laço **dentro** do outro. O de fora anda nas linhas,
o de dentro anda nas colunas — e o de dentro roda inteiro a cada
volta do de fora.
"""

META = {
    "id": "A06-013",
    "titulo": "Tabuada",
    "nivel": 3,
    "tempo_min": 9,
    "tags": ["for", "laco-aninhado", "range"],
    "dicas": [
        "Dois for encaixados, cada um com seu range(1, n + 1).",
        "A lista de resultados é criada antes dos dois laços.",
        "O append fica no laço de dentro, com a multiplicação das duas variáveis.",
    ],
}


def resolver(n: int) -> list:
    ...
