"""
Monte um dicionário de preços a partir de duas listas alinhadas: nomes e preços.

Exemplo:

    resolver(["Fone", "Capa"], [99.9, 25.0])
    ->  {"Fone": 99.9, "Capa": 25.0}

`zip` junta as duas listas par a par; `dict(...)` transforma os pares em
dicionário.
"""

META = {
    "id": "A08-001",
    "titulo": "Montar um dicionário",
    "nivel": 1,
    "tempo_min": 4,
    "tags": ["dict", "criacao"],
    "dicas": [
        "zip(nomes, precos) entrega pares (nome, preco), um por vez.",
        "A função dict(...) aceita uma sequência de pares e monta o dicionário.",
        "return dict(zip(nomes, precos))",
    ],
}


def resolver(nomes: list, precos: list) -> dict:
    return dict(zip(nomes, precos))
