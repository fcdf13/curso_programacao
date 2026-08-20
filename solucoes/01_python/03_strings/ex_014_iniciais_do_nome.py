"""
Primeiro exercício que combina várias ferramentas de uma vez.

Devolva as iniciais de um nome completo, em maiúsculas, separadas
por ponto e sem ponto no final.

Exemplos:

    resolver("ana souza lima")     ->  "A.S.L"
    resolver("Carlos Oliveira")    ->  "C.O"
    resolver("aurora")             ->  "A"

Caminho sugerido: quebre o nome em palavras, pegue a primeira letra de
cada uma, deixe em maiúscula e junte tudo com ponto.
"""

META = {
    "id": "A03-014",
    "titulo": "Iniciais do nome",
    "nivel": 3,
    "tempo_min": 9,
    "tags": ["split", "indexacao", "join", "composicao"],
    "requer": ["A03-007", "A03-008"],
    "dicas": [
        "Três passos: separar as palavras, pegar a letra 0 de cada, juntar com ponto.",
        "Você pode montar uma lista vazia e ir acrescentando com .append() dentro de um for.",
        'Depois de ter a lista de letras, ".".join(letras) resolve o final.',
    ],
}


def resolver(nome: str) -> str:
    # No módulo A10 você reescreve isto em uma linha com list comprehension.
    letras = []
    for palavra in nome.split():
        letras.append(palavra[0].upper())
    return ".".join(letras)
