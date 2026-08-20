"""
Devolva a média aritmética de três avaliações.

Exemplos:

    resolver(10, 8, 6)  ->  8.0
    resolver(5, 5, 5)   ->  5.0
    resolver(4, 5, 5)   ->  4.666666666666667

Atenção à ordem das operações: `a + b + c / 3` **não** é a média —
a divisão acontece antes da soma. Você vai precisar de parênteses.
"""

META = {
    "id": "A01-011",
    "titulo": "Média de três notas",
    "nivel": 2,
    "tempo_min": 6,
    "tags": ["aritmetica", "precedencia"],
    "dicas": [
        "Multiplicação e divisão acontecem antes de soma e subtração.",
        "Parênteses forçam a soma a acontecer primeiro.",
        "return (a + b + c) / 3",
    ],
}


def resolver(a, b, c):
    # A barra / sempre devolve float, mesmo quando a divisão é exata: 15/3 dá 5.0.
    return (a + b + c) / 3
