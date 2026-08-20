"""
Devolva quantos números da lista são maiores que o limite.

Exemplos:

    resolver([10, 5, 20], 8)   ->  2
    resolver([1, 2], 100)      ->  0
    resolver([], 0)            ->  0

Mesmo esqueleto do acumulador, mas somando 1 em vez do valor —
e só quando a condição bate.
"""

META = {
    "id": "A06-004",
    "titulo": "Contar quantos passam",
    "nivel": 2,
    "tempo_min": 7,
    "tags": ["for", "contador", "if"],
    "requer": ["A06-003"],
    "dicas": [
        "Um contador que começa em 0, fora do laço.",
        "Dentro do laço, um if decide se o contador cresce.",
        "quantos += 1 acrescenta um ao contador.",
    ],
}


def resolver(numeros: list, limite) -> int:
    ...
