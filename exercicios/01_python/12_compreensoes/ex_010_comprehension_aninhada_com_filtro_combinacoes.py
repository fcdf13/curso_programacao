"""
Gere todas as combinações de (UF, categoria) para uma campanha
de anúncios — exceto a combinação de `"SP"` com `"Luxo"`, que já
tem loja física e não precisa de anúncio.

Exemplo:

    resolver(["SP", "RJ"], ["Moda", "Luxo"])
    ->  [("SP", "Moda"), ("RJ", "Moda"), ("RJ", "Luxo")]

Dois `for` geram todas as combinações (o produto cartesiano); um
`if` no fim filtra a que não interessa — os dois no mesmo par
de colchetes.
"""

META = {
    "id": "A12-010",
    "titulo": "Comprehension aninhada com filtro: combinações",
    "nivel": 4,
    "tempo_min": 10,
    "tags": ["compreensao", "aninhada", "filtro"],
    "requer": ["A12-009", "A12-002"],
    "dicas": [
        'Dois for, um para uf e outro para categoria, geram um par\n(uf, categoria) para cada combinação possível.',
        'O filtro exclui só um caso: uf == "SP" and categoria == "Luxo".',
        'return [(uf, cat) for uf in ufs for cat in categorias if not (uf == "SP" and cat == "Luxo")]',
    ],
}


def resolver(ufs: list, categorias: list) -> list:
    ...
