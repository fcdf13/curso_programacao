"""
Monte uma tupla com o nome do produto e o preço, nessa ordem.

Exemplo:

    resolver("Fone", 99.9)  ->  ("Fone", 99.9)

Tupla se escreve entre parênteses, com vírgula separando os itens —
igual à lista, mas com `()` no lugar de `[]`.
"""

META = {
    "id": "A10-001",
    "titulo": "Criar e indexar uma tupla",
    "nivel": 1,
    "tempo_min": 4,
    "tags": ["tupla", "criacao"],
    "dicas": [
        "Parênteses com itens separados por vírgula criam uma tupla.",
        "A ordem dos itens na tupla é a ordem em que você escreve.",
        "return (nome, preco)",
    ],
}


def resolver(nome: str, preco: float) -> tuple:
    ...
