"""
Reúna características de um produto, passadas como argumentos
nomeados, num dicionário.

Exemplos:

    resolver(cor="azul", tamanho="M")  ->  {"cor": "azul", "tamanho": "M"}
    resolver()                          ->  {}

`**caracteristicas` na assinatura junta qualquer quantidade de
argumentos nomeados num dicionário.
"""

META = {
    "id": "A11-005",
    "titulo": "**kwargs: os argumentos nomeados soltos",
    "nivel": 2,
    "tempo_min": 6,
    "tags": ["funcoes", "kwargs", "variadico"],
    "dicas": [
        "**caracteristicas junta os argumentos nomeados soltos num dicionário.",
        "Dentro da função, caracteristicas já é um dict comum — não precisa montar nada.",
        "return caracteristicas",
    ],
}


def resolver(**caracteristicas) -> dict:
    ...
