"""
Cada `print` escreve uma linha e pula para a próxima.

Faça `resolver()` imprimir estas três linhas, nesta ordem:

    Loja Aurora
    Catálogo 2026
    Bem-vindo!
"""

META = {
    "id": "A01-002",
    "titulo": "Três linhas na tela",
    "nivel": 1,
    "tempo_min": 3,
    "tags": ["print"],
    "requer": ["A01-001"],
    "dicas": [
        "Três linhas na tela = três chamadas de print, uma embaixo da outra.",
        "Todas com a mesma indentação (4 espaços), dentro da função.",
        'print("Loja Aurora") e depois as outras duas, no mesmo recuo.',
    ],
}


def resolver() -> None:
    ...
