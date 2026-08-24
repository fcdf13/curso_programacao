"""
A loja rodou duas campanhas de e-mail. Você recebe a lista de clientes
que abriram a campanha A e a lista de quem abriu a campanha B.

Devolva uma tupla com três conjuntos, nesta ordem:

    (abriram as duas, só a A, só a B)

Exemplo:

    resolver(["ana", "bruno", "caio"], ["bruno", "caio", "duda"])
    ->  ({"bruno", "caio"}, {"ana"}, {"duda"})

Três operações de conjunto resolvem os três, uma de cada.
"""

META = {
    "id": "A08-014",
    "titulo": "Clientes de duas campanhas",
    "nivel": 4,
    "tempo_min": 10,
    "tags": ["set", "operacoes-de-conjunto", "regra-de-negocio"],
    "requer": ["A08-013"],
    "dicas": [
        'Transforme as duas listas em conjuntos primeiro — as operações\\nde conjunto não funcionam direto em listas.',
        "'as duas' é interseção (&); 'só a A' é diferença (A - B); 'só a B' é\\na diferença no sentido contrário (B - A).",
        "a, b = set(abriram_a), set(abriram_b); return a & b, a - b, b - a",
    ],
}


def resolver(abriram_a: list, abriram_b: list) -> tuple[set, set, set]:
    ...
