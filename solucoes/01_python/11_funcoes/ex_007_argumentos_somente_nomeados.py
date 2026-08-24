"""
Aplique um desconto a um preço. O desconto só pode ser passado
por nome — nunca só pela posição.

Exemplos:

    resolver(100.0)                    ->  100.0
    resolver(100.0, desconto=0.1)      ->  90.0

Um `*` sozinho na assinatura marca o fim dos argumentos
posicionais: tudo o que vem depois só pode ser passado por nome.
`def resolver(preco, *, desconto=0.0)` impede `resolver(100.0, 0.1)`
— teria que ser `resolver(100.0, desconto=0.1)`.
"""

META = {
    "id": "A11-007",
    "titulo": "Argumentos somente nomeados",
    "nivel": 3,
    "tempo_min": 7,
    "tags": ["funcoes", "argumento-nomeado", "asterisco"],
    "requer": ["A11-002"],
    "dicas": [
        "Um * sozinho na assinatura separa os posicionais dos que só podem ser nomeados.",
        "def resolver(preco, *, desconto=0.0) força desconto a vir sempre com nome.",
        "return preco * (1 - desconto)",
    ],
}


def resolver(preco: float, *, desconto: float = 0.0) -> float:
    return preco * (1 - desconto)
