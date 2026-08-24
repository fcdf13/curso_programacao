"""
Crie uma fábrica de validadores de desconto: dado um teto
máximo (padrão `0.5`, ou seja 50%), devolva uma função que
recebe uma quantidade qualquer de descontos e devolve quais
deles **não** passam do teto.

Exemplo:

    validar = resolver()                    # teto padrão: 0.5
    validar(0.1, 0.6, 0.3)  ->  [0.1, 0.3]

    validar_rigido = resolver(teto=0.2)
    validar_rigido(0.1, 0.6, 0.3)  ->  [0.1]

Combina tudo do módulo: `teto` é um parâmetro com valor padrão;
a função devolvida recebe os descontos por `*args`; e ela
lembra do `teto` da fábrica por clausura, mesmo chamada bem
depois.
"""

META = {
    "id": "A11-016",
    "titulo": "Desafio: fábrica de validador de desconto",
    "nivel": 5,
    "tempo_min": 12,
    "tags": ["funcoes", "closure", "parametro-padrao", "desafio"],
    "requer": ["A11-008", "A11-014", "A11-007"],
    "dicas": [
        "resolver devolve uma função nova — ela é quem recebe os descontos, via *args.",
        'A função de dentro só lê teto (não muda), então nonlocal não é\nnecessário aqui — só ler já enxerga a variável de fora.',
        'def validar(*descontos):\n        aceitos = []\n        for d in descontos:\n            if d <= teto:\n                aceitos.append(d)\n        return aceitos\n    return validar',
    ],
}


def resolver(teto: float = 0.5):
    ...
