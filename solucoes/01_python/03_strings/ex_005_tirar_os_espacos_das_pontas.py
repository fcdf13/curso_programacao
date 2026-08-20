"""
Um cadastro veio com espaços sobrando. Devolva o texto sem os espaços
das pontas — e só das pontas.

Exemplos:

    resolver("  Ana Souza  ")  ->  "Ana Souza"
    resolver("Ana")            ->  "Ana"
    resolver("   ")            ->  ""

Repare no primeiro exemplo: o espaço entre "Ana" e "Souza" fica.
"""

META = {
    "id": "A03-005",
    "titulo": "Tirar os espaços das pontas",
    "nivel": 2,
    "tempo_min": 5,
    "tags": ["strip", "limpeza"],
    "dicas": [
        "Existe um método específico para aparar as pontas de um texto.",
        "Chama-se strip, de 'descascar'.",
        "return texto.strip()",
    ],
}


def resolver(texto: str) -> str:
    # strip() sem argumento remove espaços, tabs e quebras de linha das duas pontas.
    return texto.strip()
