"""
Um cliente tem um saldo e gasta um valor fixo por mês. Devolva quantos
meses inteiros o saldo aguenta.

Exemplos:

    resolver(100, 30)  ->  3     (30, 60, 90 — no quarto mês faltaria)
    resolver(100, 100) ->  1
    resolver(50, 80)   ->  0
    resolver(0, 10)    ->  0

Use `while`: você não sabe de antemão quantas voltas serão.
"""

META = {
    "id": "A06-006",
    "titulo": "Enquanto houver saldo",
    "nivel": 2,
    "tempo_min": 8,
    "tags": ["while", "contador"],
    "dicas": [
        "Enquanto o saldo der para pagar mais um mês, desconte e conte o mês.",
        "A condição é saldo >= gasto_mensal.",
        'Dentro do while: saldo -= gasto_mensal e meses += 1. Se você não\\ndiminuir o saldo, o laço nunca termina.',
    ],
}


def resolver(saldo, gasto_mensal) -> int:
    ...
