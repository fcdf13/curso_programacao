"""
Na média ponderada cada nota tem um peso diferente. A conta é:

    soma de (nota × peso)  ÷  soma dos pesos

Devolva a média ponderada de três notas, arredondada para duas casas.

Exemplos:

    resolver(10, 1, 8, 1, 6, 2)   ->  7.5
    resolver(10, 2, 5, 1, 5, 1)   ->  7.5
    resolver(7, 1, 7, 1, 7, 1)    ->  7.0

Os parâmetros vêm em pares: nota, peso, nota, peso, nota, peso.
"""

META = {
    "id": "A02-009",
    "titulo": "Média ponderada",
    "nivel": 3,
    "tempo_min": 8,
    "tags": ["aritmetica", "media-ponderada"],
    "dicas": [
        "Em cima: cada nota multiplicada pelo seu peso, tudo somado.",
        "Embaixo: a soma dos três pesos. Não use 3 — os pesos podem não somar 3.",
        "Monte o numerador e o denominador em variáveis separadas antes de dividir.",
    ],
}


def resolver(n1, p1, n2, p2, n3, p3) -> float:
    # Dividir pelo total de pesos, e não por 3, é o que diferencia a ponderada da simples.
    soma_ponderada = n1 * p1 + n2 * p2 + n3 * p3
    soma_dos_pesos = p1 + p2 + p3
    return round(soma_ponderada / soma_dos_pesos, 2)
