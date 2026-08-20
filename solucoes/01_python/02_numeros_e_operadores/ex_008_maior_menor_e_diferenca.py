"""
Você recebe três valores de venda. Devolva a tupla
`(maior, menor, diferença entre eles)`.

A diferença nunca é negativa.

Exemplos:

    resolver(10, 3, 7)     ->  (10, 3, 7)
    resolver(-5, -1, -9)   ->  (-1, -9, 8)
    resolver(4, 4, 4)      ->  (4, 4, 0)

`max(...)` e `min(...)` aceitam vários argumentos de uma vez.
"""

META = {
    "id": "A02-008",
    "titulo": "Maior, menor e diferença",
    "nivel": 2,
    "tempo_min": 6,
    "tags": ["min-max", "abs", "tupla"],
    "dicas": [
        "max e min aceitam quantos argumentos você quiser: max(a, b, c).",
        "A diferença é o maior menos o menor — que nunca dá negativo.",
        "Calcule maior e menor em variáveis e depois devolva os três valores.",
    ],
}


def resolver(a, b, c):
    # Guardar em variáveis evita chamar max e min duas vezes cada.
    maior = max(a, b, c)
    menor = min(a, b, c)
    return maior, menor, maior - menor
