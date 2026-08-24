"""
Devolva as categorias, em maiúsculas, sem repetir.

Exemplo:

    resolver(["moda", "casa", "moda"])  ->  {"MODA", "CASA"}

Set comprehension é a mesma ideia da list comprehension, com
`{}` no lugar de `[]` — e, como todo conjunto, remove as
repetições sozinho.
"""

META = {
    "id": "A12-006",
    "titulo": "Set comprehension",
    "nivel": 2,
    "tempo_min": 6,
    "tags": ["compreensao", "set-comprehension"],
    "requer": ["A12-001", "A08-013"],
    "dicas": [
        "A forma geral é {expressao for item in iteravel} — chaves, sem dois-pontos.",
        "A expressão é categoria.upper().",
        "return {categoria.upper() for categoria in categorias}",
    ],
}


def resolver(categorias: list) -> set:
    # Sem dois-pontos, {} vira set comprehension; com chave: valor, vira dict comprehension.
    return {categoria.upper() for categoria in categorias}
