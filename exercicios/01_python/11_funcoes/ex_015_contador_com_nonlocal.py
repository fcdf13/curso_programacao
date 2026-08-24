"""
Crie e devolva um contador: uma função sem argumentos que, a
cada chamada, soma 1 a um total interno e devolve o total
atualizado.

Exemplo:

    contador = resolver()
    contador()   ->  1
    contador()   ->  2
    contador()   ->  3

A função de dentro precisa **mudar** uma variável da função de
fora (não só ler, como no exercício anterior) — para isso,
declare `nonlocal total` antes de usá-la. Sem `nonlocal`,
`total += 1` criaria uma variável local nova e estouraria
`UnboundLocalError`.
"""

META = {
    "id": "A11-015",
    "titulo": "Contador com nonlocal",
    "nivel": 4,
    "tempo_min": 10,
    "tags": ["funcoes", "closure", "nonlocal", "escopo"],
    "requer": ["A11-014"],
    "dicas": [
        "Comece com total = 0 dentro de resolver, antes de definir a função interna.",
        'A função interna precisa de nonlocal total para poder somar 1 a ela —\nsó ler não precisaria, mas mudar precisa.',
        'def contador():\n        nonlocal total\n        total += 1\n        return total\n    return contador',
    ],
}


def resolver():
    ...
