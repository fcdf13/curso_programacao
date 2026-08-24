"""
Registre um valor arrecadado, somando-o ao total do módulo, e
devolva o novo total.

Exemplo (chamadas em sequência):

    resolver(100.0)  ->  100.0
    resolver(50.0)   ->  150.0

Atribuir a uma variável dentro de uma função cria, por padrão,
uma variável **local** nova — mesmo que o nome já exista lá
fora. Para mudar de verdade a global `total_arrecadado`, é
preciso avisar com `global total_arrecadado` antes de usá-la.
"""

META = {
    "id": "A11-010",
    "titulo": "Escopo: modificar uma variável global",
    "nivel": 3,
    "tempo_min": 8,
    "tags": ["funcoes", "escopo", "global"],
    "requer": ["A11-009"],
    "dicas": [
        'Sem avisar nada, total_arrecadado += valor criaria uma variável local\nnova — e estouraria UnboundLocalError, porque ela ainda não tem valor antes do +=.',
        'global total_arrecadado, escrito antes de usar a variável, avisa que é\na de fora que deve mudar.',
        'global total_arrecadado\n    total_arrecadado += valor\n    return total_arrecadado',
    ],
}


total_arrecadado = 0.0


def resolver(valor: float) -> float:
    # global precisa vir antes de qualquer uso da variável na função — é um aviso ao Python de que aquele nome não é local.
    global total_arrecadado
    total_arrecadado += valor
    return total_arrecadado
