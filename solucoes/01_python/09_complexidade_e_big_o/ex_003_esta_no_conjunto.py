"""
O mesmo exercício anterior — mas agora `cupons_validos` chega como um
**conjunto**, não uma lista.

Exemplo:

    resolver({"BEMVINDO10", "FRETEGRATIS"}, "BEMVINDO10")  ->  True

O código muda pouco (ou nada). O que muda é o custo: um `set` em
Python é implementado como tabela hash, e `in` num set é O(1) em
média — não importa se o conjunto tem 10 ou 10 milhões de itens.
"""

META = {
    "id": "A09-003",
    "titulo": "Está no conjunto",
    "nivel": 2,
    "tempo_min": 5,
    "tags": ["big-o", "set", "membership"],
    "requer": ["A09-002", "A08-013"],
    "dicas": [
        "O operador in funciona em conjuntos exatamente como em listas.",
        "A sintaxe não muda — o que muda é a estrutura recebida.",
        "return codigo in cupons_validos",
    ],
}


def resolver(cupons_validos: set, codigo: str) -> bool:
    # Mesmo código do exercício anterior, mas agora O(1): é a estrutura que decide o custo, não a sintaxe.
    return codigo in cupons_validos
