"""
Devolva o preço do produto informado, buscando direto no dicionário.

Exemplo:

    resolver({"Fone": 99.9, "Capa": 25.0}, "Fone")  ->  99.9

Pode assumir que o produto sempre existe no dicionário — este exercício
é só sobre o acesso direto. O que fazer quando ele pode não existir é o
próximo.
"""

META = {
    "id": "A08-002",
    "titulo": "Acessar com risco",
    "nivel": 1,
    "tempo_min": 4,
    "tags": ["dict", "acesso"],
    "requer": ["A08-001"],
    "dicas": [
        "Acesso direto em dicionário usa colchetes, como em lista — mas com a chave.",
        "precos[produto]",
        "return precos[produto]",
    ],
}


def resolver(precos: dict, produto: str) -> float:
    ...
