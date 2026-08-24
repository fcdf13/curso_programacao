"""
Você recebe um produto como tupla `(nome, preço)`. Devolva o texto
`"nome custa R$ preço"`, com duas casas decimais.

Exemplo:

    resolver(("Fone", 99.9))  ->  "Fone custa R$ 99.90"

Desempacote a tupla em duas variáveis antes de montar o texto —
fica mais legível do que acessar `produto[0]` e `produto[1]`.
"""

META = {
    "id": "A10-002",
    "titulo": "Desempacotar dois valores",
    "nivel": 1,
    "tempo_min": 5,
    "tags": ["tupla", "desempacotamento"],
    "requer": ["A10-001"],
    "dicas": [
        "nome, preco = produto tira os dois valores de uma vez.",
        "Depois é só montar a f-string com as duas variáveis.",
        'nome, preco = produto; return f"{nome} custa R$ {preco:.2f}"',
    ],
}


def resolver(produto: tuple) -> str:
    # Desempacotar antes deixa o resto do código lendo nome e preco, não produto[0]/produto[1].
    nome, preco = produto
    return f"{nome} custa R$ {preco:.2f}"
