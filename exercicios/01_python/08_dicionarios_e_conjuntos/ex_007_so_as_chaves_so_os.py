"""
Devolva a tupla `(lista de produtos, lista de preços)`, na ordem em que
aparecem no dicionário.

Exemplo:

    resolver({"Fone": 99.9, "Capa": 25.0})
    ->  (["Fone", "Capa"], [99.9, 25.0])

Desde o Python 3.7, um dicionário lembra a ordem em que as chaves foram
inseridas — por isso a ordem do resultado é previsível.
"""

META = {
    "id": "A08-007",
    "titulo": "Só as chaves, só os valores",
    "nivel": 2,
    "tempo_min": 5,
    "tags": ["dict", "keys", "values"],
    "dicas": [
        ".keys() e .values() devolvem visões do dicionário, não listas de verdade.",
        "Envolva cada uma em list(...) para virar uma lista comum.",
        "return list(precos.keys()), list(precos.values())",
    ],
}


def resolver(precos: dict) -> tuple[list, list]:
    ...
