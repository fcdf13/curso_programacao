"""
Fechando o módulo com algo que a loja realmente faria.

Você recebe três listas alinhadas: preços unitários, quantidades e
descontos (em fração, `0.1` = 10%). Devolva o total do carrinho,
arredondado para duas casas.

O total de cada item é: `preço × quantidade × (1 - desconto)`.

Exemplos:

    resolver([100, 50], [1, 2], [0, 0.1])  ->  190.0
    resolver([10], [3], [0])               ->  30.0
    resolver([], [], [])                   ->  0.0

Confira o primeiro: 100×1×1 = 100, mais 50×2×0.9 = 90, dá 190.
"""

META = {
    "id": "A06-016",
    "titulo": "Total do carrinho",
    "nivel": 3,
    "tempo_min": 10,
    "tags": ["zip", "acumulador", "arredondamento", "composicao"],
    "requer": ["A06-011", "A06-003"],
    "dicas": [
        "zip aceita mais de duas listas: zip(a, b, c) entrega trios.",
        "Acumule o total item a item, e arredonde só no fim.",
        'Arredondar dentro do laço acumula erro de centavos — deixe o round\\npara a linha do return.',
    ],
}


def resolver(precos: list, quantidades: list, descontos: list) -> float:
    ...
