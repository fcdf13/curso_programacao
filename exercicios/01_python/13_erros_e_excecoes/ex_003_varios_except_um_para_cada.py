"""
Divida dois números que chegam como texto, devolvendo uma
mensagem diferente para cada tipo de problema.

Exemplos:

    resolver("10", "2")   ->  "5.0"
    resolver("10", "0")   ->  "Erro: divisão por zero"
    resolver("dez", "2")  ->  "Erro: valor inválido"

Dois problemas diferentes podem acontecer aqui — texto que não
é número (`ValueError`) e divisão por zero (`ZeroDivisionError`)
— e cada um pede sua própria mensagem. Um `try` aceita vários
`except`, um para cada tipo.
"""

META = {
    "id": "A13-003",
    "titulo": "Vários except, um para cada erro",
    "nivel": 2,
    "tempo_min": 7,
    "tags": ["excecoes", "try-except", "multiplos-except"],
    "requer": ["A13-001", "A13-002"],
    "dicas": [
        'A conversão pode falhar com ValueError e a divisão com\nZeroDivisionError — as duas dentro do mesmo try.',
        "Um except por tipo, cada um com sua mensagem.",
        'try:\n        return str(int(texto_a) / int(texto_b))\n    except ValueError:\n        return "Erro: valor inválido"\n    except ZeroDivisionError:\n        return "Erro: divisão por zero"',
    ],
}


def resolver(texto_a: str, texto_b: str) -> str:
    ...
