"""
Devolva os três maiores valores da lista, do maior para o menor.
Se a lista tiver menos de três itens, devolva todos os que houver
(ainda em ordem decrescente).

Exemplos:

    resolver([5, 1, 9, 3, 7])  ->  [9, 7, 5]
    resolver([2, 8])           ->  [8, 2]
    resolver([])               ->  []

Combine ordenação com fatiamento. `sorted` aceita `reverse=True`
para ordenar do maior para o menor.
"""

META = {
    "id": "A05-014",
    "titulo": "Os três maiores",
    "nivel": 3,
    "tempo_min": 9,
    "tags": ["sorted", "fatiamento", "reverse", "composicao"],
    "requer": ["A05-006", "A05-003"],
    "dicas": [
        "Ordene primeiro; depois é só pegar os três primeiros.",
        "sorted(numeros, reverse=True) ordena do maior para o menor.",
        "Fatiar com [:3] já lida sozinho com listas menores que três.",
    ],
}


def resolver(numeros: list) -> list:
    # O fatiamento nunca estoura: com 2 itens ele devolve 2, sem precisar de if.
    return sorted(numeros, reverse=True)[:3]
