"""
Grudar texto com `+` funciona, mas fica ilegível rápido — e obriga a
converter tudo na mão. A f-string resolve os dois problemas:

    nome = "Ana"
    total = 3
    f"{nome} fez {total} pedidos"    ->  'Ana fez 3 pedidos'

Dentro das chaves vai qualquer valor, de qualquer tipo, sem `str(...)`.

Devolva, usando f-string:

    resolver("Ana", 3)     ->  "Ana fez 3 pedidos"
    resolver("Bruno", 12)  ->  "Bruno fez 12 pedidos"
"""

META = {
    "id": "A01-010",
    "titulo": "A mesma frase com f-string",
    "nivel": 2,
    "tempo_min": 6,
    "tags": ["f-string", "string"],
    "requer": ["A01-008"],
    "dicas": [
        'O f vem colado na aspa de abertura: f"...".',
        "Os nomes das variáveis vão dentro de chaves, sem aspas por dentro.",
        'return f"{nome} fez {pedidos} pedidos"',
    ],
}


def resolver(nome: str, pedidos: int) -> str:
    ...
