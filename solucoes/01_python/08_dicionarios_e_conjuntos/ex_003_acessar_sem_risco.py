"""
Agora o produto pode **não existir** no catálogo. Devolva o preço se existir,
ou `0.0` caso contrário — sem estourar erro.

Exemplos:

    resolver({"Fone": 99.9}, "Fone")   ->  99.9
    resolver({"Fone": 99.9}, "Mouse")  ->  0.0

`precos["Mouse"]` estouraria `KeyError`. `.get(chave, padrao)` não estoura —
devolve o padrão quando a chave não existe.
"""

META = {
    "id": "A08-003",
    "titulo": "Acessar sem risco",
    "nivel": 2,
    "tempo_min": 5,
    "tags": ["dict", "get"],
    "requer": ["A08-002"],
    "dicas": [
        "Existe uma versão de acesso que não estoura quando a chave falta.",
        "d.get(chave, padrao) devolve padrao em vez de erro.",
        "return precos.get(produto, 0.0)",
    ],
}


def resolver(precos: dict, produto: str) -> float:
    # `.get` com padrão é o jeito idiomático de 'buscar, e se não tiver, tanto faz'.
    return precos.get(produto, 0.0)
