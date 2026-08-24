"""
Converta um texto para número decimal. Se falhar, devolva a
mensagem de erro que o Python já gerou, com o prefixo
`"Não deu: "`.

Exemplo:

    resolver("abc")  ->  "Não deu: could not convert string to float: 'abc'"

`except ValueError as erro` guarda a exceção numa variável —
`str(erro)` é a mensagem, a mesma que apareceria numa falha sem
tratamento.
"""

META = {
    "id": "A13-004",
    "titulo": "except ... as erro: a mensagem original",
    "nivel": 2,
    "tempo_min": 6,
    "tags": ["excecoes", "try-except", "mensagem-de-erro"],
    "requer": ["A13-002"],
    "dicas": [
        "except ValueError as erro guarda a exceção capturada na variável erro.",
        "str(erro) devolve a mensagem original, pronta para usar numa f-string.",
        'try:\n        return str(float(texto))\n    except ValueError as erro:\n        return f"Não deu: {erro}"',
    ],
}


def resolver(texto: str) -> str:
    try:
        return str(float(texto))
    except ValueError as erro:
        return f"Não deu: {erro}"
