"""
Você recebe uma lista de pedidos, cada um com uma lista de
itens. Devolva uma única lista com todos os itens, na ordem.

Exemplo:

    resolver([["Fone", "Capa"], ["Livro"], []])
    ->  ["Fone", "Capa", "Livro"]

Uma comprehension aceita mais de um `for`, na mesma ordem em
que você escreveria os laços aninhados à mão — o de fora
primeiro: `[item for pedido in pedidos for item in pedido]`.
"""

META = {
    "id": "A12-009",
    "titulo": "Comprehension aninhada: achatar uma lista de listas",
    "nivel": 4,
    "tempo_min": 9,
    "tags": ["compreensao", "aninhada"],
    "requer": ["A12-001"],
    "dicas": [
        'Escreva primeiro com dois laços aninhados de verdade (for pedido\nin pedidos: for item in pedido: ...append(item)) — depois junte numa linha.',
        'Os dois for ficam um atrás do outro, na mesma ordem dos laços\naninhados: for pedido in pedidos for item in pedido.',
        "return [item for pedido in pedidos for item in pedido]",
    ],
}


def resolver(pedidos: list) -> list:
    ...
