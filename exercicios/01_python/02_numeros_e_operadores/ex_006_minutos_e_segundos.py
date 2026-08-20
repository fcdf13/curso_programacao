"""
Uma sessão do site durou N segundos. Devolva quantos minutos inteiros e
quantos segundos sobraram, como uma tupla `(minutos, segundos)`.

Exemplos:

    resolver(125)  ->  (2, 5)      # 2 minutos e 5 segundos
    resolver(60)   ->  (1, 0)
    resolver(45)   ->  (0, 45)
    resolver(3661) ->  (61, 1)

Dá para fazer com `//` e `%` separados — ou com `divmod`, que devolve
os dois de uma vez. Os dois caminhos passam no teste.
"""

META = {
    "id": "A02-006",
    "titulo": "Minutos e segundos",
    "nivel": 3,
    "tempo_min": 7,
    "tags": ["divmod", "resto"],
    "dicas": [
        "Minutos inteiros: quantas vezes 60 cabe no total. Segundos: o que sobra.",
        "// dá o quociente inteiro e % dá o resto — exatamente o que você precisa.",
        "return divmod(total_de_segundos, 60)  # ou: return t // 60, t % 60",
    ],
}


def resolver(total_de_segundos: int) -> tuple[int, int]:
    ...
