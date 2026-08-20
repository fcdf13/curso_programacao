"""
Devolva uma tupla `(começa com o prefixo?, termina com o sufixo?)`.

Exemplos:

    resolver("aurora.pro@loja.com", "aurora", ".com")  ->  (True, True)
    resolver("teste@loja.org", "aurora", ".com")       ->  (False, False)

É assim que se valida extensão de arquivo, prefixo de código,
domínio de e-mail — sem precisar de fatiamento.
"""

META = {
    "id": "A03-010",
    "titulo": "Começa com, termina com",
    "nivel": 2,
    "tempo_min": 5,
    "tags": ["startswith", "endswith", "tupla"],
    "dicas": [
        "São dois métodos irmãos, com nomes em inglês bem literais.",
        "startswith e endswith — cada um recebe o pedaço a conferir.",
        "return texto.startswith(prefixo), texto.endswith(sufixo)",
    ],
}


def resolver(texto: str, prefixo: str, sufixo: str) -> tuple[bool, bool]:
    ...
