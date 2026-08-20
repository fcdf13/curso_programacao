"""
Devolva quantas vezes um trecho aparece dentro do texto.

Exemplos:

    resolver("aurora", "r")     ->  2
    resolver("aurora", "z")     ->  0
    resolver("aaaa", "aa")      ->  2

No último exemplo a contagem é 2, não 3: `count` não conta ocorrências
sobrepostas — depois de achar uma, ele continua do fim dela.
"""

META = {
    "id": "A03-013",
    "titulo": "Contar quantas vezes",
    "nivel": 2,
    "tempo_min": 5,
    "tags": ["count"],
    "dicas": [
        "Existe um método com o nome exato da operação, em inglês.",
        "texto.count(trecho)",
        "return texto.count(trecho)",
    ],
}


def resolver(texto: str, trecho: str) -> int:
    ...
