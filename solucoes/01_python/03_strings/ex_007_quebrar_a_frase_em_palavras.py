"""
Devolva a lista de palavras de uma frase.

Exemplos:

    resolver("Fone Aurora Pro")  ->  ["Fone", "Aurora", "Pro"]
    resolver("Casa")             ->  ["Casa"]

`split()` sem argumento quebra em qualquer espaço em branco e ignora
espaços repetidos — é quase sempre o que você quer.
"""

META = {
    "id": "A03-007",
    "titulo": "Quebrar a frase em palavras",
    "nivel": 2,
    "tempo_min": 5,
    "tags": ["split", "lista"],
    "dicas": [
        "O método que quebra texto em pedaços se chama split.",
        "Chamado sem argumento, ele separa por espaços.",
        "return frase.split()",
    ],
}


def resolver(frase: str) -> list[str]:
    return frase.split()
