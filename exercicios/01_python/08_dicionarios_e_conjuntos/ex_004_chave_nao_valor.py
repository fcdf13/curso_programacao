"""
Devolva `True` se o texto informado for uma **chave** do dicionário.

Exemplos:

    resolver({"SP": 15.0, "RJ": 15.0}, "SP")    ->  True
    resolver({"SP": 15.0, "RJ": 15.0}, 15.0)    ->  False
    resolver({"SP": 15.0, "RJ": 15.0}, "AM")    ->  False

O segundo caso é a pegadinha: `15.0` é um **valor** que existe no
dicionário, mas `in` só enxerga chaves.
"""

META = {
    "id": "A08-004",
    "titulo": "Chave, não valor",
    "nivel": 2,
    "tempo_min": 5,
    "tags": ["dict", "in"],
    "dicas": [
        "in em um dicionário testa se o valor é uma das chaves.",
        "Não importa se o valor procurado aparece do lado dos valores.",
        "return alvo in precos",
    ],
}


def resolver(precos: dict, alvo) -> bool:
    ...
