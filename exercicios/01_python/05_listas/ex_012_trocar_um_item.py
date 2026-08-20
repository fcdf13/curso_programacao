"""
Substitua o item que está na posição indicada e devolva a lista.

Exemplos:

    resolver([1, 2, 3], 1, 99)      ->  [1, 99, 3]
    resolver(["a", "b"], 0, "z")    ->  ["z", "b"]
    resolver([1, 2, 3], -1, 0)      ->  [1, 2, 0]

Pode contar com a posição sempre ser válida.
"""

META = {
    "id": "A05-012",
    "titulo": "Trocar um item",
    "nivel": 2,
    "tempo_min": 6,
    "tags": ["indexacao", "mutacao"],
    "dicas": [
        "Diferente das strings, uma lista aceita atribuição por índice.",
        "itens[posicao] = novo altera a lista no lugar.",
        "Depois de alterar, devolva a lista numa segunda linha.",
    ],
}


def resolver(itens: list, posicao: int, novo) -> list:
    ...
