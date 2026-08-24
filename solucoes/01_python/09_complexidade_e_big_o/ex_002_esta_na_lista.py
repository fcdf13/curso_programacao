"""
Verifique se um código de cupom está na lista de cupons válidos.

Exemplo:

    resolver(["BEMVINDO10", "FRETEGRATIS"], "BEMVINDO10")  ->  True
    resolver(["BEMVINDO10", "FRETEGRATIS"], "XYZ")         ->  False

Nada de novo na sintaxe — o ponto deste exercício é o próximo: `in`
numa lista precisa, no pior caso, olhar item por item até o fim.
Para uma lista de tamanho `n`, isso é O(n).
"""

META = {
    "id": "A09-002",
    "titulo": "Está na lista",
    "nivel": 2,
    "tempo_min": 5,
    "tags": ["big-o", "lista", "membership"],
    "dicas": [
        "O operador in já resolve isto, igual você viu no módulo A5.",
        "Não precisa de laço escrito por você — in faz a busca sozinho.",
        "return codigo in cupons_validos",
    ],
}


def resolver(cupons_validos: list, codigo: str) -> bool:
    # Correto, e O(n): no pior caso, in percorre a lista inteira até decidir.
    return codigo in cupons_validos
