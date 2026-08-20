"""
Devolva `True` se a nota estiver entre 0 e 10, incluindo as pontas.

Exemplos:

    resolver(7)    ->  True
    resolver(0)    ->  True
    resolver(10)   ->  True
    resolver(-1)   ->  False
    resolver(10.5) ->  False

Python permite escrever `0 <= nota <= 10` — exatamente como na matemática.
"""

META = {
    "id": "A04-006",
    "titulo": "Dentro da faixa",
    "nivel": 2,
    "tempo_min": 5,
    "tags": ["comparacao-encadeada"],
    "dicas": [
        "Duas comparações ao mesmo tempo: o limite de baixo e o de cima.",
        "Em Python elas podem ficar na mesma expressão, encadeadas.",
        "return 0 <= nota <= 10",
    ],
}


def resolver(nota) -> bool:
    ...
