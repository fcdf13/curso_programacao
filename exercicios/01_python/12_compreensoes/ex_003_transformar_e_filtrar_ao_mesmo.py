"""
Devolva, em maiúsculas, os nomes dos produtos cujo preço é maior
ou igual a um mínimo.

Exemplo:

    resolver(["Fone", "Livro"], [150.0, 20.0], 100.0)  ->  ["FONE"]

`zip` anda nas duas listas em paralelo, como no módulo A6 —
dentro da comprehension funciona igual: `for nome, preco in
zip(nomes, precos)`.
"""

META = {
    "id": "A12-003",
    "titulo": "Transformar e filtrar ao mesmo tempo",
    "nivel": 2,
    "tempo_min": 7,
    "tags": ["compreensao", "filtro", "zip"],
    "requer": ["A12-002", "A06-011"],
    "dicas": [
        'for nome, preco in zip(produtos, precos) desempacota os dois de\num par por vez, dentro da comprehension.',
        "A expressão é nome.upper(); o filtro é if preco >= minimo.",
        "return [nome.upper() for nome, preco in zip(produtos, precos) if preco >= minimo]",
    ],
}


def resolver(produtos: list, precos: list, minimo: float) -> list:
    ...
