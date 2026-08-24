"""
Ache o preço de um produto no catálogo, devolvendo `0.0` se ele
não existir — mas usando o estilo **EAFP** (tente o acesso,
capture o erro), não o **LBYL** (`if produto in precos`) do
módulo A8.

Exemplo:

    resolver({"Fone": 99.9}, "Fone")   ->  99.9
    resolver({"Fone": 99.9}, "Mouse")  ->  0.0

LBYL ("*look before you leap*") checa a condição antes de agir
— `if produto in precos:` seguido do acesso. EAFP ("*easier to
ask forgiveness than permission*") tenta direto e trata o erro
— uma leitura só do dicionário, em vez de duas.
"""

META = {
    "id": "A13-009",
    "titulo": "EAFP em vez de LBYL",
    "nivel": 4,
    "tempo_min": 9,
    "tags": ["excecoes", "eafp", "lbyl"],
    "requer": ["A13-001", "A08-003"],
    "dicas": [
        'O estilo LBYL seria if produto in precos: ... else: 0.0 —\nnão é o que este exercício pede.',
        "Tente precos[produto] direto dentro de um try, e capture KeyError.",
        'try:\n        return precos[produto]\n    except KeyError:\n        return 0.0',
    ],
}


def resolver(precos: dict, produto: str) -> float:
    ...
