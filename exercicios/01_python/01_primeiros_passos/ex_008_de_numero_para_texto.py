"""
O caminho de volta: `str(42)` devolve o texto `"42"`.

Você recebe o número de um pedido. Devolva o texto no formato:

    Pedido nº 1042

Exemplos:

    resolver(1042)  ->  "Pedido nº 1042"
    resolver(7)     ->  "Pedido nº 7"

Nesta versão, monte o texto **grudando pedaços com `+`** — que é onde
a conversão se torna necessária. (No exercício A01-010 você vai reescrever
isso de um jeito bem melhor.)
"""

META = {
    "id": "A01-008",
    "titulo": "De número para texto",
    "nivel": 2,
    "tempo_min": 5,
    "tags": ["conversao", "str"],
    "dicas": [
        'Texto gruda com +, mas "abc" + 42 dá erro: os dois lados precisam ser texto.',
        "str(numero) transforma o número em texto.",
        'return "Pedido nº " + str(numero)',
    ],
}


def resolver(numero: int) -> str:
    ...
