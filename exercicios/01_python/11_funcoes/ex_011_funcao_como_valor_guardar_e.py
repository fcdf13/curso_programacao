"""
Aplique uma função a um valor — a função chega como argumento,
não escrita dentro do `resolver`.

Exemplo:

    def dobro(x):
        return x * 2

    resolver(dobro, 5)  ->  10

Uma função é um valor como outro qualquer: pode ser guardada
numa variável, passada como argumento, chamada com `()` mais
tarde.
"""

META = {
    "id": "A11-011",
    "titulo": "Função como valor: guardar e passar adiante",
    "nivel": 3,
    "tempo_min": 8,
    "tags": ["funcoes", "primeira-classe", "ordem-superior"],
    "dicas": [
        "funcao chega como valor comum — sem (), só é possível guardá-la ou passá-la adiante.",
        "Para chamá-la de verdade, use funcao(valor), com parênteses.",
        "return funcao(valor)",
    ],
}


def resolver(funcao, valor):
    ...
