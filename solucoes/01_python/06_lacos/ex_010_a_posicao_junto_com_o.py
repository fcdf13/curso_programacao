"""
Devolva uma lista de textos numerando os itens a partir de 1:

    resolver(["Moda", "Casa"])  ->  ["1. Moda", "2. Casa"]
    resolver(["Livros"])        ->  ["1. Livros"]
    resolver([])                ->  []

`enumerate(lista)` entrega posição e item ao mesmo tempo. Ele começa
no 0, mas aceita um segundo argumento: `enumerate(lista, 1)` começa no 1.
"""

META = {
    "id": "A06-010",
    "titulo": "A posição junto com o item",
    "nivel": 2,
    "tempo_min": 7,
    "tags": ["enumerate", "f-string"],
    "requer": ["A01-010"],
    "dicas": [
        "for posicao, item in enumerate(itens): desempacota os dois de uma vez.",
        "enumerate(itens, 1) faz a contagem começar em 1.",
        'Monte cada texto com f"{posicao}. {item}" e vá acrescentando na lista.',
    ],
}


def resolver(itens: list) -> list:
    # O segundo argumento do enumerate evita o clássico posicao + 1 espalhado pelo código.
    numerados = []
    for posicao, item in enumerate(itens, 1):
        numerados.append(f"{posicao}. {item}")
    return numerados
