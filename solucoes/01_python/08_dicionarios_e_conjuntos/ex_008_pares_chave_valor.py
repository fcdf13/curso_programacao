"""
Monte uma lista de textos no formato `"produto: preço"`, um por item do
dicionário, com duas casas decimais.

Exemplo:

    resolver({"Fone": 99.9, "Capa": 25.0})
    ->  ["Fone: 99.90", "Capa: 25.00"]

`.items()` entrega os pares `(chave, valor)` prontos para desempacotar
num `for`, igual ao `zip` do módulo de laços.
"""

META = {
    "id": "A08-008",
    "titulo": "Pares chave-valor",
    "nivel": 2,
    "tempo_min": 6,
    "tags": ["dict", "items", "f-string"],
    "requer": ["A08-007"],
    "dicas": [
        "for produto, preco in precos.items(): desempacota o par a cada volta.",
        'Formate com f"{produto}: {preco:.2f}".',
        "Acrescente cada texto numa lista que começa vazia.",
    ],
}


def resolver(precos: dict) -> list:
    linhas = []
    for produto, preco in precos.items():
        linhas.append(f"{produto}: {preco:.2f}")
    return linhas
