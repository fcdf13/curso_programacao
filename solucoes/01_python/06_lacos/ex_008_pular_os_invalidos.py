"""
Some os valores da lista, **ignorando** os que são `None`.

Exemplos:

    resolver([10, None, 5])  ->  15
    resolver([None, None])   ->  0
    resolver([1, 2])         ->  3

Dados reais vêm cheios de buracos — pular o que não dá para usar é
rotina. Você pode usar `continue` ou simplesmente um `if` positivo.
"""

META = {
    "id": "A06-008",
    "titulo": "Pular os inválidos",
    "nivel": 2,
    "tempo_min": 8,
    "tags": ["for", "continue", "limpeza"],
    "dicas": [
        "Compare com None usando `is None` (e não ==).",
        "continue abandona a volta atual e vai para a próxima.",
        "if valor is None: continue — e a soma vem depois, dentro do laço.",
    ],
}


def resolver(valores: list):
    # `is None` compara identidade; para None é o jeito correto e mais rápido.
    total = 0
    for valor in valores:
        if valor is None:
            continue
        total += valor
    return total
