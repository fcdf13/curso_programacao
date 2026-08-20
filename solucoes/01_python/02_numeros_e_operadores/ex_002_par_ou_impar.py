"""
Devolva `True` se o número for par e `False` se for ímpar.

Exemplos:

    resolver(4)   ->  True
    resolver(7)   ->  False
    resolver(0)   ->  True
    resolver(-3)  ->  False

Um número é par quando o resto da divisão por 2 é zero.
E não precisa de `if`: a comparação `== 0` já produz `True` ou `False`.
"""

META = {
    "id": "A02-002",
    "titulo": "Par ou ímpar",
    "nivel": 2,
    "tempo_min": 5,
    "tags": ["resto", "booleano"],
    "dicas": [
        "O operador % devolve o resto: 7 % 2 é 1, e 4 % 2 é 0.",
        "Comparar com == já gera um booleano; você pode devolver a comparação inteira.",
        "return numero % 2 == 0",
    ],
}


def resolver(numero: int) -> bool:
    # Devolver a comparação direto evita o if/else desnecessário — comum e mais legível.
    return numero % 2 == 0
