"""
Junte nome e sobrenome com um espaço no meio.

Exemplos:

    resolver("Ana", "Souza")       ->  "Ana Souza"
    resolver("Carlos", "Oliveira") ->  "Carlos Oliveira"

Cuidado com o espaço: `nome + sobrenome` daria `"AnaSouza"`.
"""

META = {
    "id": "A01-009",
    "titulo": "Nome completo",
    "nivel": 1,
    "tempo_min": 4,
    "tags": ["string", "concatenacao"],
    "dicas": [
        'O espaço é um caractere como outro qualquer: " ".',
        "São três pedaços grudados: nome, espaço, sobrenome.",
        'return nome + " " + sobrenome',
    ],
}


def resolver(nome: str, sobrenome: str) -> str:
    return nome + " " + sobrenome
