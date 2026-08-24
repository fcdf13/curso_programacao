"""
Talvez o problema mais clássico de entrevista de programação, na
versão da Loja Aurora: um cliente tem um vale-presente de valor exato
e quer gastar tudo em **duas** ofertas.

Devolva os **índices** (i, j), com i < j, de duas ofertas cujos
preços somam exatamente o valor do vale. Se não houver par assim,
devolva `None`. Pode assumir que, quando existe solução, ela é única.

Exemplos:

    resolver([2, 7, 11, 15], 9)   ->  (0, 1)   # 2 + 7 = 9
    resolver([2, 7, 11, 15], 26)  ->  (2, 3)   # 11 + 15 = 26
    resolver([2, 7, 11, 15], 99)  ->  None

A solução com dois laços (`for i ... for j ...`) funciona, mas é
O(n²) — para cada oferta, ela revê todas as outras. Um dicionário
resolve em uma passada só: para cada preço, pergunte "o que falta
para completar o vale já apareceu antes?".
"""

META = {
    "id": "A09-008",
    "titulo": "Duas ofertas que somam ao vale-presente",
    "nivel": 4,
    "tempo_min": 11,
    "tags": ["big-o", "dict", "two-sum", "classico", "cronometrado"],
    "requer": ["A08-003"],
    "dicas": [
        'Não compare cada preço com todos os outros — percorra a lista\\numa vez só, guardando o que já viu.',
        "Para o preço atual, o que falta é vale - preco. Já apareceu antes?",
        'vistos é um dict {preco: indice}; a cada item, cheque\\nvale - preco_atual em vistos antes de adicionar o atual.',
    ],
}


def resolver(precos: list, vale: int) -> tuple[int, int] | None:
    ...
