"""
Verifique se algum preço passa de um limite.

Exemplo:

    resolver([10.0, 5000.0, 20.0], 1000.0)  ->  True
    resolver([10.0, 20.0], 1000.0)           ->  False

`any([preco > limite for preco in precos])` dá a resposta certa,
mas **monta a lista inteira antes** de `any()` sequer começar a
olhar — mesmo que o primeiro item já bastasse. Uma expressão
geradora (a mesma sintaxe, sem os colchetes) deixa `any()` parar
assim que encontrar um `True`, sem nunca montar lista nenhuma:
`any(preco > limite for preco in precos)`.
"""

META = {
    "id": "A12-011",
    "titulo": "Quando não usar list comprehension",
    "nivel": 4,
    "tempo_min": 10,
    "tags": ["compreensao", "generator", "desempenho", "cronometrado"],
    "requer": ["A12-002", "A09-003"],
    "dicas": [
        'any(...) já para no primeiro True — o problema é só o que vai\ndentro dos parênteses.',
        'Tirar os colchetes de dentro do any() transforma a list\ncomprehension numa expressão geradora, sem montar lista nenhuma.',
        "return any(preco > limite for preco in precos)",
    ],
}


def resolver(precos: list, limite: float) -> bool:
    ...
