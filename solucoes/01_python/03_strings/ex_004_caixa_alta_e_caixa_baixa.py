"""
Devolva uma tupla com o texto em maiúsculas e em minúsculas.

Exemplos:

    resolver("Aurora")  ->  ("AURORA", "aurora")
    resolver("sp")      ->  ("SP", "sp")

Padronizar caixa é a primeira coisa que se faz ao limpar dados —
`SP`, `sp` e `Sp` são o mesmo estado, mas o computador não sabe disso.
"""

META = {
    "id": "A03-004",
    "titulo": "Caixa alta e caixa baixa",
    "nivel": 1,
    "tempo_min": 4,
    "tags": ["upper", "lower", "tupla"],
    "dicas": [
        "São dois métodos com nomes bem diretos, em inglês.",
        "Métodos são chamados com ponto: texto.upper().",
        "return texto.upper(), texto.lower()",
    ],
}


def resolver(texto: str) -> tuple[str, str]:
    return texto.upper(), texto.lower()
