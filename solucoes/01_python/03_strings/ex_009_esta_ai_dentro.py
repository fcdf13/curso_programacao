"""
Devolva `True` se o texto procurado aparecer dentro da frase.

Exemplos:

    resolver("Fone Aurora Pro", "Aurora")  ->  True
    resolver("Fone Aurora Pro", "aurora")  ->  False
    resolver("Fone", "")                   ->  True

A busca diferencia maiúsculas de minúsculas — por isso o segundo exemplo
dá `False`.
"""

META = {
    "id": "A03-009",
    "titulo": "Está aí dentro?",
    "nivel": 1,
    "tempo_min": 4,
    "tags": ["in", "booleano"],
    "dicas": [
        "Python tem uma palavra-chave para 'está contido em'.",
        'É o operador in: "ro" in "aurora".',
        "return procurado in frase",
    ],
}


def resolver(frase: str, procurado: str) -> bool:
    return procurado in frase
