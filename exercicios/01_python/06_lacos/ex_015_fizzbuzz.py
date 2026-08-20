"""
O exercício mais famoso de entrevista de programação.

Para cada número de 1 a n, devolva na lista:

    "FizzBuzz"   se for divisível por 3 E por 5
    "Fizz"       se for divisível só por 3
    "Buzz"       se for divisível só por 5
    o próprio número (como int)  nos demais casos

Exemplo:

    resolver(15)
    ->  [1, 2, "Fizz", 4, "Buzz", "Fizz", 7, 8, "Fizz", "Buzz",
         11, "Fizz", 13, 14, "FizzBuzz"]

A pegadinha é a ordem: se você testar "divisível por 3" primeiro,
o 15 vira "Fizz" e nunca chega a "FizzBuzz". O caso mais específico
vem sempre antes.
"""

META = {
    "id": "A06-015",
    "titulo": "FizzBuzz",
    "nivel": 3,
    "tempo_min": 10,
    "tags": ["for", "resto", "elif", "classico"],
    "requer": ["A04-003", "A06-002"],
    "dicas": [
        "Percorra de 1 até n e decida o que acrescentar em cada volta.",
        "Teste a condição mais restritiva primeiro: divisível por 3 E por 5.",
        "numero % 3 == 0 and numero % 5 == 0 — esse if vem antes dos outros dois.",
    ],
}


def resolver(n: int) -> list:
    ...
