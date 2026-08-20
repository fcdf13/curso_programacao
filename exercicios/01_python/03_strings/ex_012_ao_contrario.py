"""
O fatiamento aceita um terceiro número, o **passo**:

    texto[inicio:fim:passo]

Com passo `-1`, ele percorre o texto de trás para frente.

Devolva o texto invertido:

    resolver("Aurora")  ->  "aroruA"
    resolver("ana")     ->  "ana"
    resolver("")        ->  ""
"""

META = {
    "id": "A03-012",
    "titulo": "Ao contrário",
    "nivel": 2,
    "tempo_min": 5,
    "tags": ["fatiamento", "passo"],
    "requer": ["A03-003"],
    "dicas": [
        "Deixe início e fim em branco para pegar o texto inteiro.",
        "Sobram dois-pontos duplos antes do passo: texto[::passo].",
        "return texto[::-1]",
    ],
}


def resolver(texto: str) -> str:
    ...
