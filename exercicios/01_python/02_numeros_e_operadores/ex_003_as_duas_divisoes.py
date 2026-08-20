"""
Python tem duas divisões, e a diferença aparece o tempo todo:

    7 / 2   ->  3.5   (divisão comum, sempre float)
    7 // 2  ->  3     (divisão inteira, joga fora a parte quebrada)

Devolva uma tupla com as duas, nesta ordem: `(divisão comum, divisão inteira)`.

Exemplos:

    resolver(7, 2)   ->  (3.5, 3)
    resolver(10, 5)  ->  (2.0, 2)
"""

META = {
    "id": "A02-003",
    "titulo": "As duas divisões",
    "nivel": 2,
    "tempo_min": 6,
    "tags": ["divisao", "tupla"],
    "dicas": [
        "São dois cálculos com os mesmos operandos, só muda o operador.",
        "Uma vírgula entre os dois resultados já monta a tupla.",
        "return a / b, a // b",
    ],
}


def resolver(a, b):
    ...
