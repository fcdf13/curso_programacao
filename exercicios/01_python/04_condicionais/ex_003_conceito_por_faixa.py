"""
Converta a nota em conceito, segundo a tabela:

    nota >= 9        ->  "A"
    nota >= 7        ->  "B"
    nota >= 5        ->  "C"
    abaixo disso     ->  "D"

Exemplos:

    resolver(9.5)  ->  "A"
    resolver(7)    ->  "B"
    resolver(5)    ->  "C"
    resolver(2)    ->  "D"

A ordem dos `elif` importa: teste do mais alto para o mais baixo. Se você
começar por `nota >= 5`, todo mundo acima de 5 vira "C".
"""

META = {
    "id": "A04-003",
    "titulo": "Conceito por faixa",
    "nivel": 2,
    "tempo_min": 7,
    "tags": ["elif", "faixas"],
    "requer": ["A04-002"],
    "dicas": [
        "Comece pela faixa mais alta e vá descendo.",
        'Como cada elif só é testado se os anteriores falharam, não precisa\\nde condições como (nota >= 7 and nota < 9).',
        "if nota >= 9 ... elif nota >= 7 ... elif nota >= 5 ... else ...",
    ],
}


def resolver(nota) -> str:
    ...
