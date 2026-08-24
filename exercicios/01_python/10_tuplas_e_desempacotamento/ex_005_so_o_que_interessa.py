"""
Um registro de cadastro chega como `(nome, uf, data_cadastro)`.
Devolva só a UF.

Exemplo:

    resolver(("Ana", "SP", "2024-01-15"))  ->  "SP"

Dá para escrever `return registro[1]` — mas o exercício é sobre
desempacotar os três valores de uma vez, descartando os dois que
não interessam com `_`.
"""

META = {
    "id": "A10-005",
    "titulo": "Só o que interessa",
    "nivel": 2,
    "tempo_min": 6,
    "tags": ["tupla", "desempacotamento", "descarte"],
    "dicas": [
        "Desempacote os três valores de uma vez, um nome por posição.",
        "Use _ no lugar de nome e de data — você não vai usar nenhum dos dois.",
        "_, uf, _ = registro; return uf",
    ],
}


def resolver(registro: tuple) -> str:
    ...
