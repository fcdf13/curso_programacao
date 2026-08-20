"""
Acrescente o novo item ao fim da lista e devolva a lista.

Exemplos:

    resolver([1, 2], 3)   ->  [1, 2, 3]
    resolver([], "a")     ->  ["a"]

Atenção: `append` **altera a lista e devolve `None`**. Se você escrever
`return itens.append(novo)`, sua função devolve `None` e o teste reprova.
São duas linhas: uma que acrescenta, outra que devolve.
"""

META = {
    "id": "A05-004",
    "titulo": "Acrescentar no fim",
    "nivel": 2,
    "tempo_min": 6,
    "tags": ["append", "mutacao"],
    "dicas": [
        "append acrescenta um item no fim da lista.",
        "Ele NÃO devolve a lista — devolve None. Não dá para usar no return.",
        "itens.append(novo) numa linha; return itens na linha seguinte.",
    ],
}


def resolver(itens: list, novo) -> list:
    ...
