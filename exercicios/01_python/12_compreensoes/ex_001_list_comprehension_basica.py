"""
Dobre cada preço da lista.

Exemplo:

    resolver([10.0, 20.0, 30.0])  ->  [20.0, 40.0, 60.0]

É o mesmo resultado do laço com `.append()` que você já escreveu
no módulo A6 — só que numa linha: `[expressão for item in lista]`.
"""

META = {
    "id": "A12-001",
    "titulo": "List comprehension básica",
    "nivel": 1,
    "tempo_min": 5,
    "tags": ["compreensao", "list-comprehension"],
    "requer": ["A06-005"],
    "dicas": [
        "A forma geral é [expressao for item in lista].",
        "Aqui a expressão é preco * 2, e item é preco.",
        "return [preco * 2 for preco in precos]",
    ],
}


def resolver(precos: list) -> list:
    ...
