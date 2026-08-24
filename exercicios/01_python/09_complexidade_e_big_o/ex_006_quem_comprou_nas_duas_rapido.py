"""
A mesma pergunta do exercício de campanhas do módulo A8 — quem abriu
as duas — só que agora o catálogo de clientes é grande de verdade:
centenas de milhares de nomes, não meia dúzia.

Devolva o conjunto de clientes que aparecem nas duas listas.

Exemplo:

    resolver(["ana", "bruno"], ["bruno", "caio"])  ->  {"bruno"}

Comparar cada nome da lista A com **todos** os nomes da lista B
(`x in lista_b` dentro de um `for x in lista_a`) é O(n × m) — com as
duas listas grandes, isso demora visivelmente. Transformar as duas em
conjuntos primeiro custa O(n + m) e a interseção é imediata.
"""

META = {
    "id": "A09-006",
    "titulo": "Quem comprou nas duas, rápido",
    "nivel": 4,
    "tempo_min": 10,
    "tags": ["big-o", "set", "desempenho", "cronometrado"],
    "requer": ["A08-014", "A09-003"],
    "dicas": [
        "Nada de comparar item a item entre as duas listas originais.",
        "Transforme as duas listas em conjuntos antes de qualquer comparação.",
        "return set(clientes_a) & set(clientes_b)",
    ],
}


def resolver(clientes_a: list, clientes_b: list) -> set:
    ...
