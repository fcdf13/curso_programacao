"""
Um ano é bissexto quando:

    é divisível por 4
    E NÃO é divisível por 100
    OU é divisível por 400

Escrito com precisão: divisível por 4 e não por 100; **ou** divisível por 400.

Exemplos:

    resolver(2024)  ->  True    (divisível por 4, não por 100)
    resolver(2023)  ->  False
    resolver(1900)  ->  False   (divisível por 100, mas não por 400)
    resolver(2000)  ->  True    (divisível por 400)

O 1900 e o 2000 são o teste de verdade — muita gente erra os dois.
"""

META = {
    "id": "A04-010",
    "titulo": "Ano bissexto",
    "nivel": 3,
    "tempo_min": 9,
    "tags": ["resto", "and", "or", "logica"],
    "dicas": [
        '"Divisível por N" é ano % N == 0.',
        "São duas partes ligadas por or; a primeira tem um and dentro dela.",
        'Parênteses em volta da parte do and deixam a precedência explícita:\\n(A and B) or C',
    ],
}


def resolver(ano: int) -> bool:
    ...
