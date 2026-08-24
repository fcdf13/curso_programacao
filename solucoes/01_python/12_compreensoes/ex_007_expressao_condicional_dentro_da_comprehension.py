"""
Rotule cada preço como `"caro"` (maior ou igual ao limite) ou
`"barato"` (menor que o limite).

Exemplo:

    resolver([10.0, 500.0, 5.0], 100.0)  ->  ["barato", "caro", "barato"]

Isto é diferente do `if` de filtro dos exercícios anteriores:
aqui **todo** item continua no resultado — só muda qual dos
dois valores entra. A forma é
`valor_a if condicao else valor_b`, no lugar da expressão.
"""

META = {
    "id": "A12-007",
    "titulo": "Expressão condicional dentro da comprehension",
    "nivel": 3,
    "tempo_min": 7,
    "tags": ["compreensao", "ternario"],
    "requer": ["A12-001"],
    "dicas": [
        'Isto não é filtro — a lista de saída tem o mesmo tamanho da\nde entrada, um rótulo para cada preço.',
        'A expressão inteira é "caro" if preco >= limite else "barato".',
        'return ["caro" if preco >= limite else "barato" for preco in precos]',
    ],
}


def resolver(precos: list, limite: float) -> list:
    # O if aqui faz parte da EXPRESSÃO (antes do for) — o if de filtro fica depois do for. São dois usos diferentes do mesmo palavra-chave.
    return ["caro" if preco >= limite else "barato" for preco in precos]
