"""
Devolva os valores distintos da lista, como um **conjunto**.

Exemplo:

    resolver(["SP", "RJ", "SP", "MG", "RJ"])  ->  {"SP", "RJ", "MG"}

`set(lista)` remove as repetições de uma vez — não importa a ordem.
"""

META = {
    "id": "A08-013",
    "titulo": "Sem repetir",
    "nivel": 1,
    "tempo_min": 4,
    "tags": ["set", "criacao", "dedup"],
    "dicas": [
        "Existe uma função que transforma qualquer sequência em conjunto.",
        "set(...) remove as repetições automaticamente.",
        "return set(itens)",
    ],
}


def resolver(itens: list) -> set:
    ...
