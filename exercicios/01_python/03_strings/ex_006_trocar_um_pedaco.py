"""
Códigos de produto vieram com hífen, mas o sistema espera barra.

Devolva o texto com todos os hífens trocados por `/`.

Exemplos:

    resolver("SP-01-A")  ->  "SP/01/A"
    resolver("SP01")     ->  "SP01"
    resolver("-")        ->  "/"

`replace` troca **todas** as ocorrências, não só a primeira.
"""

META = {
    "id": "A03-006",
    "titulo": "Trocar um pedaço",
    "nivel": 2,
    "tempo_min": 5,
    "tags": ["replace"],
    "dicas": [
        "O método recebe dois argumentos: o que procurar e o que colocar no lugar.",
        'texto.replace("velho", "novo")',
        'return codigo.replace("-", "/")',
    ],
}


def resolver(codigo: str) -> str:
    ...
