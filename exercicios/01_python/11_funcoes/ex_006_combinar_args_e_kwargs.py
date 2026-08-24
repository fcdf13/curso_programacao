"""
Monte um pedido a partir de um cliente, uma quantidade qualquer
de itens e características opcionais.

Exemplos:

    resolver("Ana", "Fone", "Capa", desconto=0.1)
    ->  {"cliente": "Ana", "itens": ["Fone", "Capa"], "desconto": 0.1}

    resolver("Bruno")
    ->  {"cliente": "Bruno", "itens": []}

A ordem na assinatura é sempre: parâmetros fixos, depois
`*args`, depois `**kwargs` — `def resolver(cliente, *itens, **opcionais)`.
"""

META = {
    "id": "A11-006",
    "titulo": "Combinar *args e **kwargs",
    "nivel": 3,
    "tempo_min": 8,
    "tags": ["funcoes", "args", "kwargs", "variadico"],
    "requer": ["A11-004", "A11-005"],
    "dicas": [
        'A assinatura é def resolver(cliente, *itens, **opcionais) — fixo,\ndepois *args, depois **kwargs.',
        'list(itens) transforma a tupla em lista; opcionais já é um dict\nque dá para juntar com .update().',
        'pedido = {"cliente": cliente, "itens": list(itens)}\n    pedido.update(opcionais)\n    return pedido',
    ],
}


def resolver(cliente: str, *itens, **opcionais) -> dict:
    ...
