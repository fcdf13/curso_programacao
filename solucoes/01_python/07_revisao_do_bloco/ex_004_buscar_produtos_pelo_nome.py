"""
Devolva a lista de produtos cujo nome contém o termo procurado,
**ignorando maiúsculas e minúsculas**.

Os nomes devolvidos mantêm a grafia original.

Exemplos:

    resolver(["Fone Aurora", "Capa Slim", "Fone Pro"], "fone")
    ->  ["Fone Aurora", "Fone Pro"]

    resolver(["Capa Slim"], "FONE")   ->  []
    resolver([], "fone")              ->  []
    resolver(["Capa Slim"], "")       ->  ["Capa Slim"]

No último caso: todo texto contém o texto vazio.
"""

META = {
    "id": "A07-004",
    "titulo": "Buscar produtos pelo nome",
    "nivel": 3,
    "tempo_min": 9,
    "tags": ["laco", "strings", "lista", "revisao"],
    "requer": ["A06-005", "A03-004"],
    "dicas": [
        "Padronize os dois lados da comparação para minúsculas.",
        'Padronizar o nome só para comparar não muda o que você acrescenta\\nna lista de resultados.',
        "if termo.lower() in nome.lower(): encontrados.append(nome)",
    ],
}


def resolver(nomes: list, termo: str) -> list:
    # Comparar em minúsculas mas guardar o original é o padrão de toda busca amigável.
    encontrados = []
    procurado = termo.lower()
    for nome in nomes:
        if procurado in nome.lower():
            encontrados.append(nome)
    return encontrados
