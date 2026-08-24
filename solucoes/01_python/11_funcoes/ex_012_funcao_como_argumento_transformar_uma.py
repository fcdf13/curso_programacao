"""
Aplique uma função a cada item de uma lista, devolvendo a lista
de resultados — na mesma ordem.

Exemplo:

    def dobro(x):
        return x * 2

    resolver(dobro, [1, 2, 3])  ->  [2, 4, 6]

Uma função que recebe outra função de argumento (como esta) é
chamada de **função de ordem superior**.
"""

META = {
    "id": "A11-012",
    "titulo": "Função como argumento: transformar uma lista",
    "nivel": 3,
    "tempo_min": 8,
    "tags": ["funcoes", "primeira-classe", "ordem-superior"],
    "requer": ["A11-011"],
    "dicas": [
        "Percorra itens com um laço, chamando funcao(item) para cada item.",
        "Guarde cada resultado, na ordem, numa lista nova (list.append).",
        'resultado = []\n    for item in itens:\n        resultado.append(funcao(item))\n    return resultado',
    ],
}


def resolver(funcao, itens: list) -> list:
    # Essa mesma ideia, escrita numa linha só, é o que list comprehension faz por trás — o módulo A12 chega lá.
    resultado = []
    for item in itens:
        resultado.append(funcao(item))
    return resultado
