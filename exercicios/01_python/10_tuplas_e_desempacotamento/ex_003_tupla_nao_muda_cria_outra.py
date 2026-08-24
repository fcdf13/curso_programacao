"""
Você recebe um produto como `(nome, preço)` e um preço novo. Devolva
uma tupla **nova** com o mesmo nome e o preço atualizado.

Exemplo:

    resolver(("Fone", 99.9), 79.9)  ->  ("Fone", 79.9)

`produto[1] = novo_preco` estouraria `TypeError` — tupla não aceita
atribuição por índice depois de criada. O jeito é montar uma tupla
nova, reaproveitando o que não mudou.
"""

META = {
    "id": "A10-003",
    "titulo": "Tupla não muda — cria outra",
    "nivel": 2,
    "tempo_min": 6,
    "tags": ["tupla", "imutabilidade"],
    "requer": ["A10-002"],
    "dicas": [
        "Tente produto[1] = novo_preco só para ver o erro — depois apague.",
        "Desempacote o produto para pegar o nome, e monte uma tupla nova.",
        "nome, _ = produto; return (nome, novo_preco)",
    ],
}


def resolver(produto: tuple, novo_preco: float) -> tuple:
    ...
