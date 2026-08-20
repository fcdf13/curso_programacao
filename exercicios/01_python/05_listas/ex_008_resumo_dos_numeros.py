"""
Devolva a tupla `(soma, menor, maior)` de uma lista de números.

Exemplos:

    resolver([1, 2, 3])       ->  (6, 1, 3)
    resolver([10])            ->  (10, 10, 10)
    resolver([-5, 0, 5])      ->  (0, -5, 5)

As três funções já existem prontas — não precisa de laço.
"""

META = {
    "id": "A05-008",
    "titulo": "Resumo dos números",
    "nivel": 2,
    "tempo_min": 6,
    "tags": ["sum", "min-max"],
    "dicas": [
        "Três funções embutidas com nomes bem diretos.",
        "sum, min e max — todas recebem a lista inteira.",
        "return sum(numeros), min(numeros), max(numeros)",
    ],
}


def resolver(numeros: list) -> tuple:
    ...
