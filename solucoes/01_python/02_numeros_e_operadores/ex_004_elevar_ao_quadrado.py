"""
Devolva o número elevado ao quadrado.

Exemplos:

    resolver(5)   ->  25
    resolver(1.5) ->  2.25
    resolver(-3)  ->  9

O operador de potência é `**` — dois asteriscos.
"""

META = {
    "id": "A02-004",
    "titulo": "Elevar ao quadrado",
    "nivel": 1,
    "tempo_min": 3,
    "tags": ["potencia"],
    "dicas": [
        "Elevar ao quadrado é elevar à potência 2.",
        "O operador é ** (não confunda com *, que é multiplicação).",
        "return numero ** 2",
    ],
}


def resolver(numero):
    return numero ** 2
