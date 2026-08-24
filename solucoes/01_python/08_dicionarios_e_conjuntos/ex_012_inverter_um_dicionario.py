"""
Troque as chaves pelos valores e vice-versa. Pode assumir que os valores
originais são únicos (nenhum se repete), então nada se perde na troca.

Exemplo:

    resolver({"SP": "São Paulo", "RJ": "Rio de Janeiro"})
    ->  {"São Paulo": "SP", "Rio de Janeiro": "RJ"}

Percorra os pares originais e monte um dicionário novo com eles trocados.
"""

META = {
    "id": "A08-012",
    "titulo": "Inverter um dicionário",
    "nivel": 3,
    "tempo_min": 8,
    "tags": ["dict", "comprehension-like", "inversao"],
    "requer": ["A08-008"],
    "dicas": [
        "Percorra os pares com .items(), como no exercício das siglas.",
        "Para cada par (chave, valor), o dicionário novo ganha valor -> chave.",
        "invertido[valor] = chave, dentro do laço.",
    ],
}


def resolver(original: dict) -> dict:
    invertido = {}
    for chave, valor in original.items():
        invertido[valor] = chave
    return invertido
