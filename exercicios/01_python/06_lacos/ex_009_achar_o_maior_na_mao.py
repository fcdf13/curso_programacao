"""
Devolva o maior número da lista — **sem usar `max`**.
Se a lista estiver vazia, devolva `None`.

Exemplos:

    resolver([3, 9, 2])     ->  9
    resolver([-5, -1, -9])  ->  -1
    resolver([])            ->  None

O truque: comece assumindo que o primeiro item é o maior, e vá
corrigindo. Começar com `maior = 0` quebra em listas de negativos —
e é por isso que este exercício é nível 3.
"""

META = {
    "id": "A06-009",
    "titulo": "Achar o maior na mão",
    "nivel": 3,
    "tempo_min": 8,
    "tags": ["for", "acumulador", "comparacao"],
    "requer": ["A06-003"],
    "dicas": [
        "Trate a lista vazia primeiro e devolva None.",
        "Não comece o maior em 0: comece no primeiro item da lista.",
        "maior = numeros[0], e no laço: if numero > maior: maior = numero",
    ],
}


def resolver(numeros: list):
    ...
