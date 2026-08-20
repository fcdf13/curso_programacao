"""
Um pedido ganha frete grátis quando o valor passa de R$ 200 **e** o
cliente é assinante.

Devolva `True` ou `False`.

Exemplos:

    resolver(250, True)   ->  True
    resolver(250, False)  ->  False
    resolver(150, True)   ->  False
    resolver(200, True)   ->  False

Repare no último caso: "passa de 200" não inclui o 200.
Nenhum `if` é necessário — a expressão já vale `True` ou `False`.
"""

META = {
    "id": "A04-004",
    "titulo": "As duas condições",
    "nivel": 2,
    "tempo_min": 6,
    "tags": ["and", "or", "booleano"],
    "dicas": [
        '"E" em Python se escreve and.',
        '"Passa de 200" é > 200, sem o igual.',
        "return valor > 200 and e_assinante",
    ],
}


def resolver(valor, e_assinante: bool) -> bool:
    ...
