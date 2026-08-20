"""
O exercício mais importante do módulo, porque a diferença aqui gera bug
silencioso a vida inteira:

    sorted(lista)   devolve uma lista NOVA ordenada; a original fica igual
    lista.sort()    reordena a PRÓPRIA lista e devolve None

Devolva a tupla `(lista ordenada, lista original)` — usando `sorted`,
de modo que a original chegue **intacta** no segundo item.

Exemplo:

    resolver([3, 1, 2])  ->  ([1, 2, 3], [3, 1, 2])

Se você usar `.sort()`, os dois itens da tupla vão sair ordenados e o
teste vai pegar.
"""

META = {
    "id": "A05-006",
    "titulo": "sorted não é sort",
    "nivel": 3,
    "tempo_min": 8,
    "tags": ["sorted", "sort", "imutabilidade"],
    "dicas": [
        "Só um dos dois preserva a lista original.",
        "sorted(...) é função, não método: sorted(numeros), sem ponto.",
        "return sorted(numeros), numeros",
    ],
}


def resolver(numeros: list) -> tuple[list, list]:
    ...
