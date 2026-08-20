"""
A nota de corte é 7. Devolva `"aprovado"` se a nota for 7 ou mais,
e `"reprovado"` caso contrário.

Exemplos:

    resolver(7)    ->  "aprovado"
    resolver(6.9)  ->  "reprovado"
    resolver(10)   ->  "aprovado"

Cuidado com o 7 exato: o enunciado diz "7 ou mais".
"""

META = {
    "id": "A04-002",
    "titulo": "Aprovado ou reprovado",
    "nivel": 1,
    "tempo_min": 4,
    "tags": ["if", "else"],
    "dicas": [
        '"7 ou mais" inclui o próprio 7 — o operador é >=, não >.',
        "São dois caminhos: um no if, outro no else.",
        'if nota >= 7: return "aprovado"',
    ],
}


def resolver(nota) -> str:
    if nota >= 7:
        return "aprovado"
    else:
        return "reprovado"
