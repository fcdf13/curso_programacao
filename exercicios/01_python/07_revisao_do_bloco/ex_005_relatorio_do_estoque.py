"""
Monte um relatório de estoque, uma linha por produto, no formato:

    nome: quantidade (situação)

A situação depende da quantidade:

    0            ->  "esgotado"
    1 a 9        ->  "critico"
    10 ou mais   ->  "ok"

Exemplos:

    resolver(["Fone", "Capa"], [0, 25])
    ->  ["Fone: 0 (esgotado)", "Capa: 25 (ok)"]

    resolver(["Livro"], [3])   ->  ["Livro: 3 (critico)"]
    resolver([], [])           ->  []
"""

META = {
    "id": "A07-005",
    "titulo": "Relatório do estoque",
    "nivel": 3,
    "tempo_min": 10,
    "tags": ["zip", "laco", "f-string", "condicional", "revisao"],
    "requer": ["A06-011", "A04-003"],
    "dicas": [
        "zip percorre nome e quantidade em paralelo.",
        "Decida a situação num if/elif dentro do laço, guardando numa variável.",
        'Monte a linha com f"{nome}: {quantidade} ({situacao})".',
    ],
}


def resolver(nomes: list, quantidades: list) -> list:
    ...
