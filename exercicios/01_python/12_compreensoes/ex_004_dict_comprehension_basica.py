"""
Monte um dicionário `produto -> preço`, a partir de duas listas
alinhadas.

Exemplo:

    resolver(["Fone", "Capa"], [99.9, 25.0])
    ->  {"Fone": 99.9, "Capa": 25.0}

Dict comprehension é a mesma ideia da list comprehension, com
`{chave: valor for ... in ...}` no lugar de colchetes.
"""

META = {
    "id": "A12-004",
    "titulo": "Dict comprehension básica",
    "nivel": 2,
    "tempo_min": 6,
    "tags": ["compreensao", "dict-comprehension", "zip"],
    "requer": ["A12-001", "A06-011"],
    "dicas": [
        "A forma geral é {chave: valor for item in iteravel}.",
        "zip(produtos, precos) entrega os pares (nome, preco) de uma vez.",
        "return {nome: preco for nome, preco in zip(produtos, precos)}",
    ],
}


def resolver(produtos: list, precos: list) -> dict:
    ...
