"""
Converta um texto para número. Devolva `f"número: {valor}"` se
der certo, ou `"não é número"` se não der.

Exemplos:

    resolver("42")   ->  "número: 42"
    resolver("abc")  ->  "não é número"

Um `else` depois do `except` roda só quando o `try` **não**
levantou nenhuma exceção — é o lugar certo para o "caminho de
sucesso", separado do que trata o erro.
"""

META = {
    "id": "A13-005",
    "titulo": "else: só roda se nada deu errado",
    "nivel": 2,
    "tempo_min": 7,
    "tags": ["excecoes", "try-except-else"],
    "requer": ["A13-002"],
    "dicas": [
        'try converte; except captura o ValueError; else roda só\nquando a conversão deu certo.',
        'O valor convertido só existe se o try não estourou — por isso\nele é usado dentro do else, não depois do try inteiro.',
        'try:\n        valor = int(texto)\n    except ValueError:\n        return "não é número"\n    else:\n        return f"número: {valor}"',
    ],
}


def resolver(texto: str) -> str:
    ...
