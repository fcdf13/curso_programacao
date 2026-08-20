"""
Remova da lista a primeira ocorrência do valor indicado e devolva a lista.

Exemplos:

    resolver([1, 2, 3], 2)      ->  [1, 3]
    resolver([1, 2, 2], 2)      ->  [1, 2]
    resolver(["a", "b"], "a")   ->  ["b"]

Repare no segundo exemplo: `remove` tira só a **primeira** ocorrência.
Pode contar com o valor sempre existir na lista.
"""

META = {
    "id": "A05-005",
    "titulo": "Tirar um item",
    "nivel": 2,
    "tempo_min": 6,
    "tags": ["remove", "mutacao"],
    "requer": ["A05-004"],
    "dicas": [
        "remove recebe o VALOR a tirar, não a posição.",
        "Assim como append, ele devolve None — precisa de duas linhas.",
        "itens.remove(valor) e depois return itens",
    ],
}


def resolver(itens: list, valor) -> list:
    ...
