"""
Devolva o produto mais caro do catálogo — só o nome, não o preço.
Se houver empate, devolva qualquer um dos empatados.

Exemplo:

    resolver({"Fone": 200.0, "Notebook": 3000.0, "Capa": 30.0})
    ->  "Notebook"

`max(dicionario)` devolveria a maior **chave** (ordem alfabética) — não é
o que você quer. Você precisa comparar pelos **valores**.
"""

META = {
    "id": "A08-010",
    "titulo": "A chave do maior valor",
    "nivel": 3,
    "tempo_min": 8,
    "tags": ["dict", "max", "key"],
    "requer": ["A08-009"],
    "dicas": [
        "max(precos) compara as chaves; você quer comparar pelos valores.",
        "max aceita um argumento key= que diz por qual critério comparar.",
        "return max(precos, key=precos.get)",
    ],
}


def resolver(precos: dict) -> str:
    # `key=precos.get` diz: para decidir o maior, olhe precos.get(chave) — não a chave em si.
    return max(precos, key=precos.get)
