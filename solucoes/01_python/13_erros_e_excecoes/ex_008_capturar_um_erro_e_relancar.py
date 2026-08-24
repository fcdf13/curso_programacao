"""
Converta um texto para inteiro. Se não for possível, lance um
`ValueError` com uma mensagem mais clara do que a original —
incluindo o texto que falhou.

Exemplos:

    resolver("42")   ->  42
    resolver("abc")  ->  levanta ValueError("'abc' não é um número válido")

Capture o `ValueError` que `int()` já levanta, e **lance outro
no lugar** — com a mensagem que faz sentido para quem usa a sua
função, não a mensagem interna do `int()`.
"""

META = {
    "id": "A13-008",
    "titulo": "Capturar um erro e relançar um mais claro",
    "nivel": 3,
    "tempo_min": 9,
    "tags": ["excecoes", "raise", "reraise"],
    "requer": ["A13-002", "A13-007"],
    "dicas": [
        'Dentro do except, um novo raise substitui a exceção original\npor outra — mesmo tipo, mensagem diferente.',
        "from None no fim do raise evita empilhar as duas exceções na mensagem.",
        'try:\n        return int(texto)\n    except ValueError:\n        raise ValueError(f"\'{texto}\' não é um número válido") from None',
    ],
}


def resolver(texto: str) -> int:
    try:
        return int(texto)
    except ValueError:
        raise ValueError(f"'{texto}' não é um número válido") from None
