"""
Troque de lugar os itens das posições `i` e `j` de uma lista, e
devolva a lista.

Exemplo:

    resolver([10, 20, 30, 40], 0, 3)  ->  [40, 20, 30, 10]

Você já trocou duas variáveis de lugar no módulo A1
(`a, b = b, a`). A mesma ideia funciona com posições de lista —
sem precisar de uma variável temporária para guardar o valor.
"""

META = {
    "id": "A10-004",
    "titulo": "Trocar dois itens de uma lista",
    "nivel": 2,
    "tempo_min": 6,
    "tags": ["tupla", "desempacotamento", "lista"],
    "requer": ["A01-012"],
    "dicas": [
        'A troca sem variável temporária que você viu no A1 funciona\\ntambém com itens[i] e itens[j].',
        'Os dois lados da atribuição são montados antes de qualquer\\nvalor ser sobrescrito.',
        "itens[i], itens[j] = itens[j], itens[i]",
    ],
}


def resolver(itens: list, i: int, j: int) -> list:
    # Python monta a tupla (itens[j], itens[i]) inteira antes de atribuir — por isso não precisa de variável auxiliar.
    itens[i], itens[j] = itens[j], itens[i]
    return itens
