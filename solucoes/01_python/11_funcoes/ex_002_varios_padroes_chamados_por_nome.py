"""
Descreva um item do carrinho: produto, quantidade (padrão `1`) e
desconto (padrão `0`, sem desconto).

Exemplos:

    resolver("Fone")                  ->  "1x Fone"
    resolver("Fone", 3)                ->  "3x Fone"
    resolver("Fone", desconto=0.1)     ->  "1x Fone (10% de desconto)"
    resolver("Fone", 2, 0.2)           ->  "2x Fone (20% de desconto)"

Repare no terceiro exemplo: para pular `quantidade` e só mudar
`desconto`, quem chama passa `desconto=0.1` por nome — não dá
para pular um argumento no meio só na base da posição.
"""

META = {
    "id": "A11-002",
    "titulo": "Vários padrões, chamados por nome",
    "nivel": 1,
    "tempo_min": 5,
    "tags": ["funcoes", "parametro-padrao", "argumento-nomeado"],
    "requer": ["A11-001"],
    "dicas": [
        'Sem desconto, o texto é só "{quantidade}x {produto}".',
        'Com desconto (diferente de 0), acrescente " ({X}% de desconto)", com X = desconto*100.',
        'if desconto:\n        return f"{quantidade}x {produto} ({int(desconto*100)}% de desconto)"\n    return f"{quantidade}x {produto}"',
    ],
}


def resolver(produto: str, quantidade: int = 1, desconto: float = 0.0) -> str:
    if desconto:
        return f"{quantidade}x {produto} ({int(desconto*100)}% de desconto)"
    return f"{quantidade}x {produto}"
