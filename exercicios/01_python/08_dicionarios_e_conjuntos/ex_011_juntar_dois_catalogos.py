"""
Junte dois catálogos de preço num só. Quando o mesmo produto aparece
nos dois, **o segundo catálogo vence**.

Exemplo:

    resolver({"Fone": 99.9, "Capa": 25.0}, {"Capa": 20.0, "Mouse": 45.0})
    ->  {"Fone": 99.9, "Capa": 20.0, "Mouse": 45.0}

Repare no preço da Capa: veio do segundo dicionário, não do primeiro.
"""

META = {
    "id": "A08-011",
    "titulo": "Juntar dois catálogos",
    "nivel": 3,
    "tempo_min": 8,
    "tags": ["dict", "merge"],
    "dicas": [
        "Existe um operador que junta dois dicionários: |.",
        "Em a | b, quando a chave se repete, o valor de b vence.",
        "return catalogo_a | catalogo_b",
    ],
}


def resolver(catalogo_a: dict, catalogo_b: dict) -> dict:
    ...
