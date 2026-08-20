"""
Classifique o cliente pela idade:

    menos de 18       ->  "menor"
    de 18 a 59        ->  "adulto"
    60 ou mais        ->  "idoso"

Exemplos:

    resolver(15)  ->  "menor"
    resolver(18)  ->  "adulto"
    resolver(59)  ->  "adulto"
    resolver(60)  ->  "idoso"

Preste atenção nos limites — 18 e 60 são os pontos onde a maioria erra.
"""

META = {
    "id": "A04-008",
    "titulo": "Faixa etária",
    "nivel": 2,
    "tempo_min": 7,
    "tags": ["elif", "faixas"],
    "dicas": [
        "São três faixas, então if / elif / else.",
        "Comece pelo mais novo ou pelo mais velho — só não misture as ordens.",
        "if idade < 18 ... elif idade < 60 ... else ...",
    ],
}


def resolver(idade: int) -> str:
    ...
