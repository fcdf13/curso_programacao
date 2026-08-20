"""
Devolva os dois valores recebidos, na ordem invertida.

Exemplos:

    resolver(1, 2)          ->  (2, 1)
    resolver("a", "b")      ->  ("b", "a")

O resultado é uma **tupla**: dois valores viajando juntos, escritos entre
parênteses. Em Python, `return b, a` já cria a tupla — os parênteses são
opcionais.
"""

META = {
    "id": "A01-012",
    "titulo": "Trocar dois valores de lugar",
    "nivel": 2,
    "tempo_min": 5,
    "tags": ["tupla", "desempacotamento"],
    "dicas": [
        "Você não precisa de uma variável temporária: dá para devolver os dois de uma vez.",
        "Uma vírgula entre dois valores já forma uma tupla.",
        "return b, a",
    ],
}


def resolver(a, b):
    # A mesma sintaxe troca variáveis no lugar: a, b = b, a.
    return b, a
