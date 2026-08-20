"""
Você recebe as vendas diárias do mês. Devolva o tamanho da **maior
sequência de dias seguidos com zero vendas**.

Exemplos:

    resolver([5, 0, 0, 3, 0])        ->  2
    resolver([0, 0, 0])              ->  3
    resolver([1, 2, 3])              ->  0
    resolver([])                     ->  0
    resolver([0, 1, 0, 0, 0, 1, 0])  ->  3

Este é o problema que em SQL se chama *gaps and islands*, e você vai
reencontrá-lo no Bloco C. Aqui ele sai com dois contadores.

A armadilha: se a maior sequência terminar no último dia, é fácil
esquecer de contabilizá-la.
"""

META = {
    "id": "A07-007",
    "titulo": "Maior sequência sem vendas",
    "nivel": 4,
    "tempo_min": 12,
    "tags": ["laco", "acumulador", "maximo", "revisao"],
    "requer": ["A06-009", "A06-004"],
    "dicas": [
        "Você precisa de duas variáveis: a sequência atual e a maior já vista.",
        "Dia com zero: a atual cresce. Dia com venda: a atual volta a zero.",
        'Atualize a maior a CADA volta, e não só quando a sequência quebra —\\nsenão a sequência que termina no último dia se perde.',
    ],
}


def resolver(vendas_por_dia: list) -> int:
    ...
