"""
Você recebe os valores de venda do mês. Devolva uma tupla com quatro
informações, nesta ordem:

    (quantidade de vendas,
     total vendido,
     média por venda arredondada em 2 casas,
     quantas vendas ficaram acima da média)

Se a lista estiver vazia, devolva `(0, 0, 0.0, 0)`.

Exemplos:

    resolver([100, 200, 300])   ->  (3, 600, 200.0, 1)
    resolver([50])              ->  (1, 50, 50.0, 0)
    resolver([])                ->  (0, 0, 0.0, 0)

No primeiro caso a média é 200, e só o 300 fica acima dela.
Repare que a comparação é com a média **antes** do arredondamento —
aqui os dois valores coincidem, mas o teste tem um caso onde não.
"""

META = {
    "id": "A07-006",
    "titulo": "Estatísticas das vendas",
    "nivel": 4,
    "tempo_min": 12,
    "tags": ["laco", "lista", "media", "condicional", "revisao"],
    "requer": ["A06-004", "A05-013"],
    "dicas": [
        "Trate a lista vazia primeiro e devolva a tupla de zeros.",
        'Calcule a média em uma variável e só depois percorra de novo\\npara contar quantas passam dela.',
        'São duas passadas pela lista: uma para somar, outra para contar.\\nNão dá para fazer as duas ao mesmo tempo — você precisa da média pronta.',
    ],
}


def resolver(vendas: list) -> tuple:
    # Comparar com a média exata (e arredondar só na saída) evita erros de fronteira.
    if not vendas:
        return 0, 0, 0.0, 0

    quantidade = len(vendas)
    total = sum(vendas)
    media = total / quantidade

    acima = 0
    for venda in vendas:
        if venda > media:
            acima += 1

    return quantidade, total, round(media, 2), acima
