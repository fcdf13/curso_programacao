"""
Um valor rende juros compostos quando os juros de cada período passam a
render junto no período seguinte. A fórmula é:

    montante = capital × (1 + taxa) ** periodos

A taxa vem em porcentagem (por exemplo, `10` para 10% ao mês).

Devolva o montante final arredondado para duas casas.

Exemplos:

    resolver(1000, 10, 2)   ->  1210.0
    resolver(1000, 10, 0)   ->  1000.0
    resolver(500, 1, 12)    ->  563.41
"""

META = {
    "id": "A02-010",
    "titulo": "Juros compostos",
    "nivel": 3,
    "tempo_min": 8,
    "tags": ["potencia", "financeiro"],
    "dicas": [
        "A taxa chega em porcentagem: 10 precisa virar 0.10 antes de entrar na fórmula.",
        "Dividir a taxa por 100 é o primeiro passo; o ** vem depois.",
        "Guarde a taxa convertida numa variável para a fórmula ficar legível.",
    ],
}


def resolver(capital, taxa_percentual, periodos) -> float:
    # Com 0 períodos o expoente zera e o montante é o próprio capital — bom teste de sanidade.
    taxa = taxa_percentual / 100
    montante = capital * (1 + taxa) ** periodos
    return round(montante, 2)
