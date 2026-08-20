"""
Devolva a contagem regressiva de n até 1, como lista.

Exemplos:

    resolver(3)  ->  [3, 2, 1]
    resolver(1)  ->  [1]
    resolver(0)  ->  []

Use `while`. (Com `range` daria em uma linha — mas a ideia aqui é
controlar o contador na mão.)
"""

META = {
    "id": "A06-014",
    "titulo": "Contagem regressiva",
    "nivel": 2,
    "tempo_min": 7,
    "tags": ["while", "lista"],
    "requer": ["A06-006"],
    "dicas": [
        "Comece com uma lista vazia e um contador valendo n.",
        "O laço continua enquanto o contador for >= 1.",
        "Dentro: acrescente o contador na lista e depois diminua 1 dele.",
    ],
}


def resolver(n: int) -> list:
    numeros = []
    atual = n
    while atual >= 1:
        numeros.append(atual)
        atual -= 1
    return numeros
