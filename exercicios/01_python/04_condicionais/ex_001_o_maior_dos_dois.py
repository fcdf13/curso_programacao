"""
Devolva o maior entre dois números. Se forem iguais, devolva qualquer um.

Exemplos:

    resolver(10, 3)   ->  10
    resolver(3, 10)   ->  10
    resolver(5, 5)    ->  5

Faça com `if` e `else` — este módulo é sobre isso. (Sim, `max` resolveria
em uma linha, e você já viu isso no A02-008.)
"""

META = {
    "id": "A04-001",
    "titulo": "O maior dos dois",
    "nivel": 1,
    "tempo_min": 4,
    "tags": ["if", "comparacao"],
    "dicas": [
        "A pergunta é: a é maior que b?",
        "Se for, devolva a; senão, devolva b.",
        "if a > b: return a — e um else: return b logo abaixo.",
    ],
}


def resolver(a, b):
    ...
