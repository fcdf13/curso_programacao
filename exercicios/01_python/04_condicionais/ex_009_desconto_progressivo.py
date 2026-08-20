"""
A loja dá desconto conforme o valor da compra:

    a partir de R$ 500   ->  15%
    a partir de R$ 200   ->  10%
    a partir de R$ 100   ->  5%
    abaixo de R$ 100     ->  sem desconto

Devolva o **valor final** já com o desconto aplicado, arredondado
para duas casas.

Exemplos:

    resolver(600)  ->  510.0
    resolver(200)  ->  180.0
    resolver(150)  ->  142.5
    resolver(50)   ->  50.0
"""

META = {
    "id": "A04-009",
    "titulo": "Desconto progressivo",
    "nivel": 3,
    "tempo_min": 9,
    "tags": ["elif", "aritmetica", "regra-de-negocio"],
    "requer": ["A04-003"],
    "dicas": [
        "Primeiro descubra a taxa de desconto; só depois aplique no valor.",
        "Aplicar 15% de desconto é multiplicar por (1 - 0.15).",
        'Guarde a taxa numa variável dentro dos if/elif e faça um único\\nreturn round(valor * (1 - taxa), 2) no fim.',
    ],
}


def resolver(valor: float) -> float:
    ...
