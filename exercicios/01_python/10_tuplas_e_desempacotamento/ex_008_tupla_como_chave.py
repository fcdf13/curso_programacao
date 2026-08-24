"""
Some as vendas por par **(estado, categoria)** — uma combinação que
uma chave só (a UF, ou só a categoria) não conseguiria representar.

Você recebe três listas alinhadas: estados, categorias e valores.
Devolva um dicionário onde a chave é a tupla `(uf, categoria)` e o
valor é a soma das vendas daquela combinação.

Exemplo:

    resolver(["SP", "SP", "RJ"], ["Moda", "Casa", "Moda"], [100.0, 50.0, 80.0])
    ->  {("SP", "Moda"): 100.0, ("SP", "Casa"): 50.0, ("RJ", "Moda"): 80.0}

Uma lista `[uf, categoria]` não poderia ser chave de dicionário —
listas não são hasháveis. Uma tupla `(uf, categoria)` pode, porque
não muda depois de criada.
"""

META = {
    "id": "A10-008",
    "titulo": "Tupla como chave",
    "nivel": 4,
    "tempo_min": 10,
    "tags": ["tupla", "dict", "hashable", "regra-de-negocio"],
    "requer": ["A08-009", "A10-002"],
    "dicas": [
        'A chave do dicionário é uma tupla (uf, categoria) montada a\\ncada volta do laço.',
        "Sem essa tupla, o dicionário não teria como distinguir\\n('SP', 'Moda') de ('SP', 'Casa').",
        "chave = (uf, categoria); total[chave] = total.get(chave, 0) + valor",
    ],
}


def resolver(ufs: list, categorias: list, valores: list) -> dict:
    ...
