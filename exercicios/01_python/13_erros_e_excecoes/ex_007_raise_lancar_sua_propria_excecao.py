"""
Valide uma idade: se for negativa, **lance** um `ValueError`
com a mensagem `"idade não pode ser negativa"`. Se for válida,
devolva a própria idade.

Exemplos:

    resolver(25)  ->  25
    resolver(-1)  ->  levanta ValueError("idade não pode ser negativa")

`raise` lança uma exceção na hora — a função para ali, e quem
chamou decide se captura ou deixa propagar.
"""

META = {
    "id": "A13-007",
    "titulo": "raise: lançar sua própria exceção",
    "nivel": 3,
    "tempo_min": 8,
    "tags": ["excecoes", "raise"],
    "requer": ["A13-002"],
    "dicas": [
        'raise ValueError("mensagem") lança a exceção; o código depois dele nunca roda.',
        "Um if checa a condição inválida antes do raise; o caminho válido só tem o return.",
        'if idade < 0:\n        raise ValueError("idade não pode ser negativa")\n    return idade',
    ],
}


def resolver(idade: int) -> int:
    ...
