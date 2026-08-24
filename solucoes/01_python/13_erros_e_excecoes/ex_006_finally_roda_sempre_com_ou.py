"""
Divida dois números, devolvendo `None` se o segundo for zero —
e conte **toda** tentativa, deu certo ou não, num contador
global.

Exemplo (chamadas em sequência):

    resolver(10, 2)  ->  5.0
    resolver(10, 0)  ->  None

Depois das duas chamadas, `tentativas` vale 2 — contando as
duas, não só a que deu certo. Um bloco `finally` roda
**sempre**, com ou sem exceção — mesmo quando a função termina
com `return` dentro do `except`.
"""

META = {
    "id": "A13-006",
    "titulo": "finally: roda sempre, com ou sem erro",
    "nivel": 3,
    "tempo_min": 8,
    "tags": ["excecoes", "try-except-finally", "escopo"],
    "requer": ["A13-001", "A11-010"],
    "dicas": [
        'finally vem depois do except (ou do else, se tiver) e roda\nnão importa o que aconteceu no try.',
        "A conta em tentativas precisa de global tentativas, como no módulo A11.",
        'global tentativas\n    try:\n        return a / b\n    except ZeroDivisionError:\n        return None\n    finally:\n        tentativas += 1',
    ],
}


tentativas = 0


def resolver(a: float, b: float) -> float | None:
    # finally roda mesmo com um return dentro do try ou do except — é o único jeito de garantir código que sempre executa, dê certo ou não.
    global tentativas
    try:
        return a / b
    except ZeroDivisionError:
        return None
    finally:
        tentativas += 1
