"""
Guarde o nome da loja em uma variável chamada `loja` e devolva essa variável.

O resultado deve ser o texto `Aurora`.

Parece o exercício anterior, e é de propósito: a diferença é que agora o
valor passa por uma variável antes de sair. Programas reais fazem isso o
tempo todo — calculam, guardam, devolvem.
"""

META = {
    "id": "A01-004",
    "titulo": "Guardar em uma variável",
    "nivel": 1,
    "tempo_min": 4,
    "tags": ["variavel", "return"],
    "dicas": [
        "Criar uma variável é só escrever nome = valor.",
        "São duas linhas: uma que guarda, outra que devolve.",
        'loja = "Aurora" e depois return loja',
    ],
}


def resolver() -> str:
    loja = "Aurora"
    return loja
