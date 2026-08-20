"""
Devolva uma tupla `(primeiro item, último item, quantidade de itens)`.

Exemplos:

    resolver([10, 20, 30])  ->  (10, 30, 3)
    resolver(["a"])         ->  ("a", "a", 1)

Pode contar com a lista nunca estar vazia.
"""

META = {
    "id": "A05-002",
    "titulo": "Primeiro, último e quantos",
    "nivel": 1,
    "tempo_min": 5,
    "tags": ["indexacao", "len"],
    "dicas": [
        "Índice 0 é o primeiro; -1 é o último.",
        "len(itens) diz quantos são.",
        "return itens[0], itens[-1], len(itens)",
    ],
}


def resolver(itens: list) -> tuple:
    return itens[0], itens[-1], len(itens)
