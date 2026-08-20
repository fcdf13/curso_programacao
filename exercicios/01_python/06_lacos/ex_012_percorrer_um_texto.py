"""
Conte quantas vogais existem no texto, sem diferenciar maiúsculas
de minúsculas.

Exemplos:

    resolver("Aurora")  ->  4
    resolver("XYZ")     ->  0
    resolver("")        ->  0

Um `for` sobre uma string entrega um caractere por vez.
Considere apenas a, e, i, o, u (sem acentos).
"""

META = {
    "id": "A06-012",
    "titulo": "Percorrer um texto",
    "nivel": 2,
    "tempo_min": 7,
    "tags": ["for", "string", "contador"],
    "dicas": [
        'Passe o texto todo para minúsculas antes de percorrer — resolve a\\nquestão da caixa de uma vez.',
        'Você pode testar com: if letra in "aeiou"',
        "Um contador iniciado em 0 antes do laço, incrementado dentro do if.",
    ],
}


def resolver(texto: str) -> int:
    ...
