"""
Devolva a posição do valor na lista. Se o valor não estiver lá,
devolva `-1`.

Exemplos:

    resolver(["a", "b", "c"], "b")  ->  1
    resolver(["a", "b"], "z")       ->  -1
    resolver([1, 2, 1], 1)          ->  0

`lista.index(valor)` daria erro quando o valor não existe — então
confira antes com `in`.
"""

META = {
    "id": "A05-009",
    "titulo": "Em que posição está",
    "nivel": 2,
    "tempo_min": 6,
    "tags": ["index", "in"],
    "dicas": [
        "index() devolve a posição da primeira ocorrência, mas estoura se não achar.",
        "Confira com `if valor in itens` antes de chamar index.",
        "if valor in itens: return itens.index(valor) — e um return -1 no fim.",
    ],
}


def resolver(itens: list, valor) -> int:
    # Perguntar antes de agir evita a exceção — no módulo A13 você vê a alternativa com try/except.
    if valor in itens:
        return itens.index(valor)
    return -1
