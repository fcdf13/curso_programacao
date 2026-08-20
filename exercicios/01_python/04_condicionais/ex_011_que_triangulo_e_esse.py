"""
Recebendo os três lados, devolva:

    "invalido"    se os lados não formam triângulo
    "equilatero"  se os três lados são iguais
    "isosceles"   se exatamente dois lados são iguais
    "escaleno"    se os três lados são diferentes

Um triângulo existe quando **cada lado é menor que a soma dos outros dois**.

Exemplos:

    resolver(3, 3, 3)   ->  "equilatero"
    resolver(5, 5, 3)   ->  "isosceles"
    resolver(3, 4, 5)   ->  "escaleno"
    resolver(1, 2, 10)  ->  "invalido"
    resolver(1, 2, 3)   ->  "invalido"

O último caso é o traiçoeiro: 1 + 2 dá exatamente 3, e a soma precisa ser
**maior**, não igual.
"""

META = {
    "id": "A04-011",
    "titulo": "Que triângulo é esse",
    "nivel": 3,
    "tempo_min": 10,
    "tags": ["elif", "logica", "validacao"],
    "dicas": [
        "Valide primeiro: se não for triângulo, nem faz sentido classificar.",
        "São três desigualdades ligadas por and — uma para cada lado.",
        "Depois de validar, compare a==b, b==c e a==c para decidir o tipo.",
    ],
}


def resolver(a, b, c) -> str:
    ...
