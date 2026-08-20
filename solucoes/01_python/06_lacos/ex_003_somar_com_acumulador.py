"""
Devolva a soma dos números da lista — **usando um laço**, sem `sum`.

Exemplos:

    resolver([1, 2, 3])  ->  6
    resolver([])         ->  0
    resolver([-1, 1])    ->  0

Sim, `sum` resolveria. O objetivo aqui é o padrão do acumulador, que você
vai reusar a vida inteira para coisas que não têm função pronta.
"""

META = {
    "id": "A06-003",
    "titulo": "Somar com acumulador",
    "nivel": 2,
    "tempo_min": 7,
    "tags": ["for", "acumulador"],
    "dicas": [
        "Crie a variável do total ANTES do laço, valendo 0.",
        "A cada volta, some o item ao total: total += numero.",
        "O return vem depois do laço, sem indentação extra.",
    ],
}


def resolver(numeros: list):
    # Iniciar fora, atualizar dentro, usar depois: esse é o esqueleto do acumulador.
    total = 0
    for numero in numeros:
        total += numero
    return total
