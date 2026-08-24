"""
Antes de falar em Big-O, vale contar na unha.

Devolva quantas vezes o corpo do laço mais interno roda, para dois laços
aninhados, cada um de `n` voltas.

Exemplos:

    resolver(3)  ->  9    (3 × 3)
    resolver(1)  ->  1
    resolver(0)  ->  0

Não use a fórmula direto — monte os dois laços de verdade e conte.
É esse formato (`for` dentro de `for`, ambos até `n`) que qualquer
entrevista chama de O(n²): dobrar `n` quadruplica o total.
"""

META = {
    "id": "A09-001",
    "titulo": "Quantas vezes o laço roda",
    "nivel": 1,
    "tempo_min": 6,
    "tags": ["big-o", "laco-aninhado", "conceito"],
    "requer": ["A06-013"],
    "dicas": [
        "Monte um laço dentro do outro, exatamente como na tabuada do A6.",
        "Um contador que soma 1 a cada volta do laço de dentro.",
        "for _ in range(n): for _ in range(n): contador += 1",
    ],
}


def resolver(n: int) -> int:
    ...
