"""
Crie uma fábrica de multiplicadores: dado um fator, devolva
**uma função** que multiplica qualquer número por esse fator.

Exemplo:

    vezes3 = resolver(3)
    vezes3(10)   ->  30
    vezes3(2)    ->  6

`resolver` não devolve um número — devolve uma função, definida
por dentro, que lembra do `fator` mesmo depois que `resolver` já
terminou. Isso é uma **clausura** (*closure*).
"""

META = {
    "id": "A11-014",
    "titulo": "Função que devolve função",
    "nivel": 4,
    "tempo_min": 9,
    "tags": ["funcoes", "closure", "clausura"],
    "requer": ["A11-011"],
    "dicas": [
        "resolver não faz a conta — ele monta e devolve uma função nova, sem chamá-la.",
        'Defina uma função por dentro de resolver, que usa fator; devolva essa\nfunção (sem parênteses — devolver a função, não o resultado dela).',
        'def multiplicar(x):\n        return x * fator\n    return multiplicar',
    ],
}


def resolver(fator: float):
    ...
