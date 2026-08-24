"""
Um sistema de pedidos vê IDs chegando em sequência e quer flagar
repetições **próximas demais para ser coincidência** — a mesma ID
aparecendo de novo a `k` posições ou menos de distância.

Devolva `True` se existir alguma ID repetida com distância **menor ou
igual** a `k` entre as duas ocorrências.

Exemplos:

    resolver(["a", "b", "c", "a"], 3)  ->  True   (distância 3)
    resolver(["a", "b", "c", "a"], 2)  ->  False  (distância 3 > 2)
    resolver(["a", "b", "a"], 2)       ->  True   (distância 2)

Guarde num dicionário a **última posição** em que cada valor
apareceu. Ao encontrar o valor de novo, a distância é a posição atual
menos a posição guardada — sem precisar comparar com todas as
ocorrências anteriores, só com a mais recente.
"""

META = {
    "id": "A09-004",
    "titulo": "Duplicata perto demais",
    "nivel": 3,
    "tempo_min": 9,
    "tags": ["big-o", "dict", "last-seen-index", "classico"],
    "requer": ["A08-009"],
    "dicas": [
        'Percorra com o índice (enumerate) e guarde a última posição de\\ncada valor num dicionário.',
        "Ao rever um valor, a distância é indice_atual - ultima_posicao[valor].",
        'Se a distância for <= k, já pode devolver True; senão, atualize\\na última posição e continue.',
    ],
}


def resolver(ids: list, k: int) -> bool:
    # Uma passada só, O(n): o dicionário guarda só a ocorrência mais recente de cada valor.
    ultima_posicao = {}
    for indice, valor in enumerate(ids):
        if valor in ultima_posicao and indice - ultima_posicao[valor] <= k:
            return True
        ultima_posicao[valor] = indice
    return False
