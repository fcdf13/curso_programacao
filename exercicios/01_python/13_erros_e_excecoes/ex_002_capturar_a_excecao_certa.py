"""
Converta um texto para número inteiro. Se o texto não for um
número válido, devolva `None`.

Exemplos:

    resolver("42")   ->  42
    resolver("abc")  ->  None

`int("abc")` levanta `ValueError` — um tipo diferente do
exercício anterior. Capture o tipo certo: `except ValueError`.
"""

META = {
    "id": "A13-002",
    "titulo": "Capturar a exceção certa",
    "nivel": 1,
    "tempo_min": 5,
    "tags": ["excecoes", "try-except", "valueerror"],
    "requer": ["A13-001"],
    "dicas": [
        "int(texto) levanta ValueError quando o texto não é um número.",
        "O try guarda só a conversão; capture ValueError, não ZeroDivisionError.",
        'try:\n        return int(texto)\n    except ValueError:\n        return None',
    ],
}


def resolver(texto: str) -> int | None:
    ...
