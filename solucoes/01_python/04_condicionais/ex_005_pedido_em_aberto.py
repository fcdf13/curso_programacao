"""
Um pedido está **em aberto** quando o status não é nem `"entregue"`
nem `"cancelado"`.

Devolva `True` para pedidos em aberto.

Exemplos:

    resolver("processando")  ->  True
    resolver("enviado")      ->  True
    resolver("entregue")     ->  False
    resolver("cancelado")    ->  False

Dá para escrever com dois `and`, mas `not ... in [...]` fica bem melhor.
"""

META = {
    "id": "A04-005",
    "titulo": "Pedido em aberto",
    "nivel": 2,
    "tempo_min": 6,
    "tags": ["not", "in", "lista"],
    "dicas": [
        'O operador in também funciona com listas: x in ["a", "b"].',
        "Você quer o contrário disso — existe o operador not.",
        'return status not in ["entregue", "cancelado"]',
    ],
}


def resolver(status: str) -> bool:
    # `not in` é um operador só; lê-se exatamente como a regra de negócio.
    return status not in ["entregue", "cancelado"]
