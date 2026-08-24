"""
O suporte da loja atende pedidos em rodadas: pega o primeiro da fila,
atende uma rodada, e — se o pedido ainda não terminou — ele volta para
o **fim** da fila. Cada pedido precisa de exatamente `rodadas`
passagens pela frente da fila para ser concluído.

Devolva a lista de pedidos **na ordem em que foram concluídos**.

Exemplo, com `rodadas=2`:

    resolver(["p1", "p2", "p3"], 2)  ->  ["p1", "p2", "p3"]
    # rodada 1: p1 (falta 1), p2 (falta 1), p3 (falta 1) — fila: p1,p2,p3 de novo
    # rodada 2: p1 conclui, p2 conclui, p3 conclui

`lista.pop(0)` tira o primeiro item, mas **desloca todos os outros
uma posição** — é O(n) a cada chamada, e aqui isso acontece milhares
de vezes. `collections.deque` foi construída exatamente para tirar e
colocar itens nas pontas em O(1): troque `pop(0)` por `popleft()`.
"""

META = {
    "id": "A09-009",
    "titulo": "Fila sem gargalo",
    "nivel": 4,
    "tempo_min": 11,
    "tags": ["big-o", "deque", "fila", "desempenho", "cronometrado"],
    "dicas": [
        "collections.deque tem os métodos popleft() e append(), os dois O(1).",
        'Simule rodada por rodada: tire o da frente, diminua o contador\\ndele, e recoloque no fim se ainda não chegou a zero.',
        'fila = deque(pedidos); restam = {p: rodadas for p in pedidos};\\ndepois um while fila: com popleft() e append().',
    ],
}


from collections import deque


def resolver(pedidos: list, rodadas: int) -> list:
    ...
