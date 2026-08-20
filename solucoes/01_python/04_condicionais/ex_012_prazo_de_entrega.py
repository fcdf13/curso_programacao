"""
O prazo de entrega em dias combina duas informações:

                        frete expresso    frete comum
    SP, RJ, MG, ES            1                4
    PR, SC, RS                2                6
    demais estados            4               12

Devolva o prazo em dias.

Exemplos:

    resolver("SP", True)   ->  1
    resolver("SP", False)  ->  4
    resolver("BA", True)   ->  4
    resolver("RS", False)  ->  6
"""

META = {
    "id": "A04-012",
    "titulo": "Prazo de entrega",
    "nivel": 3,
    "tempo_min": 9,
    "tags": ["elif", "and", "regra-de-negocio"],
    "requer": ["A04-007"],
    "dicas": [
        "Duas dimensões: a região e o tipo de frete. Resolva uma de cada vez.",
        'Descubra a região primeiro e guarde numa variável; depois decida o\\nprazo com base na região e no expresso.',
        "Você pode fazer um if por região com um if interno para o expresso.",
    ],
}


def resolver(uf: str, expresso: bool) -> int:
    # `a if condicao else b` é o if em forma de expressão — cabe direto no return.
    if uf in ["SP", "RJ", "MG", "ES"]:
        return 1 if expresso else 4
    elif uf in ["PR", "SC", "RS"]:
        return 2 if expresso else 6
    else:
        return 4 if expresso else 12
