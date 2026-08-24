"""
Remova os itens repetidos de uma lista, **preservando a ordem da
primeira aparição de cada um** — e fazendo isso rápido mesmo para
listas grandes.

Exemplo:

    resolver([3, 1, 3, 2, 1])  ->  [3, 1, 2]

`set(lista)` sozinho remove as repetições, mas **não preserva a
ordem original** — e o exercício pede a ordem da primeira aparição.
A armadilha comum é escrever `if item not in resultado` para checar
se um item já foi colocado na lista de saída: isso funciona, mas
`resultado` cresce a cada volta, e cada `in` custa O(tamanho de
resultado) — o laço inteiro vira O(n²). Use um `set` à parte só para
lembrar o que já foi visto; verificar nele é O(1).
"""

META = {
    "id": "A09-007",
    "titulo": "Sem repetir, na ordem, rápido",
    "nivel": 3,
    "tempo_min": 9,
    "tags": ["big-o", "set", "dedup", "desempenho", "cronometrado"],
    "requer": ["A05-006", "A09-003"],
    "dicas": [
        'Dois acumuladores: a lista de resultado (na ordem) e um set\\nà parte, só para saber o que já apareceu.',
        "Checar 'já vi este item?' deve ser feito no set, nunca na lista\\nde resultado — senão o custo do 'in' cresce junto com o resultado.",
        "if item not in vistos: vistos.add(item); resultado.append(item)",
    ],
}


def resolver(itens: list) -> list:
    ...
