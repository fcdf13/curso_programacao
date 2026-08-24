"""
Conte quantas vezes cada categoria aparece na lista de pedidos.

Exemplo:

    resolver(["Moda", "Casa", "Moda", "Moda"])
    ->  {"Moda": 3, "Casa": 1}

Este é o padrão de contagem mais usado em toda a análise de dados —
e ele reaparece, em outra forma, em quase todo módulo daqui para frente.
"""

META = {
    "id": "A08-009",
    "titulo": "Contagem de ocorrências",
    "nivel": 3,
    "tempo_min": 8,
    "tags": ["dict", "get", "contagem", "classico"],
    "dicas": [
        "Comece com um dicionário vazio, antes do laço.",
        "Para cada item, some 1 à contagem daquela chave.",
        "contagem[categoria] = contagem.get(categoria, 0) + 1 — o .get(c, 0)\\né o que evita checar 'a chave já existe?' antes de somar.",
    ],
}


def resolver(categorias: list) -> dict:
    ...
