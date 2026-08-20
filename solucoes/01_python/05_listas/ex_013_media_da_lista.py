"""
Devolva a média dos números da lista, arredondada para duas casas.
Se a lista estiver vazia, devolva `0.0`.

Exemplos:

    resolver([10, 8, 6])  ->  8.0
    resolver([1, 2])      ->  1.5
    resolver([])          ->  0.0

A lista vazia é o caso que quebra o código de quem esquece dela:
dividir por `len([])` é dividir por zero.
"""

META = {
    "id": "A05-013",
    "titulo": "Média da lista",
    "nivel": 2,
    "tempo_min": 6,
    "tags": ["sum", "len", "media"],
    "requer": ["A05-008"],
    "dicas": [
        "Média é a soma dividida pela quantidade.",
        "Trate a lista vazia ANTES de dividir.",
        "if not numeros: return 0.0 — e só depois faça a conta.",
    ],
}


def resolver(numeros: list) -> float:
    # `if not numeros` é o jeito idiomático de perguntar 'a lista está vazia?'.
    if not numeros:
        return 0.0
    return round(sum(numeros) / len(numeros), 2)
