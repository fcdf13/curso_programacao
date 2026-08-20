"""
Devolva a posição do primeiro número negativo da lista.
Se não houver nenhum, devolva `-1`.

Exemplos:

    resolver([5, 3, -2, -8])  ->  2
    resolver([1, 2, 3])       ->  -1
    resolver([-1])            ->  0

Assim que achar, pare — não faz sentido continuar procurando.
Com `return` dentro do laço, você já sai da função de uma vez.
"""

META = {
    "id": "A06-007",
    "titulo": "Parar na primeira",
    "nivel": 2,
    "tempo_min": 7,
    "tags": ["for", "break", "busca"],
    "dicas": [
        'Você precisa da posição, não do valor — então percorra os índices,\\nou use enumerate.',
        "for posicao in range(len(numeros)) te dá as posições.",
        "Ao encontrar, return posicao na hora. O return -1 fica depois do laço.",
    ],
}


def resolver(numeros: list) -> int:
    ...
