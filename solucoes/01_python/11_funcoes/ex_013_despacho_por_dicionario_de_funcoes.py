"""
Aplique uma operação sobre dois números, escolhida por nome —
sem escrever uma corrente de `if`/`elif` para cada uma.

Exemplo:

    resolver("soma", 4, 3)      ->  7
    resolver("subtracao", 4, 3) ->  1

Como funções são valores, um dicionário pode guardar
`{"soma": funcao_soma, "subtracao": funcao_subtracao, ...}` e
escolher qual chamar buscando pela chave — o mesmo
`dicionario[chave]` do módulo A8, só que o valor é uma função.
"""

META = {
    "id": "A11-013",
    "titulo": "Despacho por dicionário de funções",
    "nivel": 4,
    "tempo_min": 9,
    "tags": ["funcoes", "primeira-classe", "dict", "regra-de-negocio"],
    "requer": ["A11-011", "A08-002"],
    "dicas": [
        'Defina uma função pequena para cada operação (soma, subtracao,\nmultiplicacao, divisao) antes de resolver, e guarde as quatro num dicionário.',
        'operacoes = {"soma": soma, "subtracao": subtracao, ...} — sem (), é a\nfunção em si que vai no dicionário.',
        "return operacoes[operacao](a, b)",
    ],
}


def resolver(operacao: str, a: float, b: float) -> float:
    # Guardar funções num dicionário substitui uma corrente de if/elif por operação — para adicionar uma operação nova, basta uma linha no dicionário, não mais um elif.
    def soma(x, y):
        return x + y

    def subtracao(x, y):
        return x - y

    def multiplicacao(x, y):
        return x * y

    def divisao(x, y):
        return x / y

    operacoes = {
        "soma": soma,
        "subtracao": subtracao,
        "multiplicacao": multiplicacao,
        "divisao": divisao,
    }
    return operacoes[operacao](a, b)
