"""
Monte um dicionário `categoria -> lista de produtos caros`
daquela categoria (preço maior ou igual a um mínimo).

Exemplo:

    resolver(
        ["Fone", "Sofá", "Caneca", "Mesa"],
        ["Eletrônicos", "Casa", "Casa", "Casa"],
        [150.0, 800.0, 15.0, 300.0],
        50.0,
    )
    ->  {"Eletrônicos": ["Fone"], "Casa": ["Sofá", "Mesa"]}

(`"Caneca"` fica de fora — custa menos que o mínimo — mas
`"Casa"` continua no dicionário, porque `"Sofá"` e `"Mesa"`
passam.)

Combina os três tipos do módulo: um set comprehension para as
categorias sem repetir, e um dict comprehension cujo valor é,
para cada categoria, um list comprehension filtrando os
produtos daquela categoria.
"""

META = {
    "id": "A12-012",
    "titulo": "Desafio: catálogo por categoria",
    "nivel": 5,
    "tempo_min": 13,
    "tags": ["compreensao", "desafio", "dict-comprehension", "set-comprehension"],
    "requer": ["A12-005", "A12-006"],
    "dicas": [
        'Primeiro monte o conjunto de categorias sem repetir — o set\ncomprehension do exercício A12-006.',
        'O dicionário final é {cat: [...] for cat in categorias_unicas}\n— e o valor de cada chave é, por sua vez, uma list comprehension.',
        'categorias_unicas = {c for c in categorias}\n    return {\n        cat: [p for p, c, v in zip(produtos, categorias, precos) if c == cat and v >= minimo]\n        for cat in categorias_unicas\n    }',
    ],
}


def resolver(produtos: list, categorias: list, precos: list, minimo: float) -> dict:
    # Uma comprehension dentro de outra: o valor de cada chave do dict comprehension é, ele mesmo, um list comprehension completo, filtrando pela categoria da vez.
    categorias_unicas = {c for c in categorias}
    return {
        cat: [p for p, c, v in zip(produtos, categorias, precos) if c == cat and v >= minimo]
        for cat in categorias_unicas
    }
