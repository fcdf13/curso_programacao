"""
O caminho inverso do `split`. Devolva as palavras da lista unidas por
vírgula e espaço.

Exemplos:

    resolver(["Moda", "Casa", "Livros"])  ->  "Moda, Casa, Livros"
    resolver(["Moda"])                    ->  "Moda"
    resolver([])                          ->  ""

A sintaxe de `join` costuma pegar de surpresa: quem chama o método é o
**separador**, e a lista vai como argumento.

    ", ".join(["a", "b"])    ->  'a, b'
"""

META = {
    "id": "A03-008",
    "titulo": "Juntar palavras",
    "nivel": 2,
    "tempo_min": 6,
    "tags": ["join"],
    "requer": ["A03-007"],
    "dicas": [
        "Quem chama o join é o texto que vai ficar ENTRE os itens.",
        'O separador aqui é ", " — vírgula e espaço.',
        'return ", ".join(palavras)',
    ],
}


def resolver(palavras: list[str]) -> str:
    # Com lista vazia o join devolve texto vazio, sem erro — de graça.
    return ", ".join(palavras)
