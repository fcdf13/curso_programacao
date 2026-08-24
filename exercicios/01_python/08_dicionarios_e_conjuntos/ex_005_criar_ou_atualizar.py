"""
Registre o preço de um produto no dicionário — funciona tanto para um
produto novo quanto para atualizar um preço existente — e devolva o
dicionário.

Exemplos:

    resolver({"Fone": 99.9}, "Fone", 89.9)   ->  {"Fone": 89.9}
    resolver({"Fone": 99.9}, "Capa", 25.0)   ->  {"Fone": 99.9, "Capa": 25.0}

A mesma linha resolve os dois casos: não existe diferença de sintaxe
entre criar e atualizar uma chave.
"""

META = {
    "id": "A08-005",
    "titulo": "Criar ou atualizar",
    "nivel": 2,
    "tempo_min": 5,
    "tags": ["dict", "mutacao"],
    "dicas": [
        "Atribuir a uma chave que já existe substitui o valor.",
        "Atribuir a uma chave que não existe cria a entrada.",
        "precos[produto] = novo_preco, e depois return precos.",
    ],
}


def resolver(precos: dict, produto: str, novo_preco: float) -> dict:
    ...
