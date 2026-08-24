"""
Você recebe as vendas diárias de um período e uma lista de perguntas,
cada uma pedindo a soma de vendas entre dois dias (o segundo dia
**exclusivo**, igual ao fatiamento que você já usa).

Devolva a lista com a resposta de cada pergunta, na mesma ordem.

Exemplo:

    resolver([10, 20, 30, 40], [(0, 2), (1, 4), (0, 4)])
    ->  [30, 90, 100]

    # pergunta (0, 2): vendas[0] + vendas[1] = 10 + 20 = 30
    # pergunta (1, 4): vendas[1] + vendas[2] + vendas[3] = 90
    # pergunta (0, 4): a soma inteira = 100

Se houver **muitas** perguntas, somar `vendas[inicio:fim]` de novo a
cada uma custa caro: cada soma custa O(tamanho do intervalo), e isso
se repete para cada pergunta. Monte uma vez uma lista de **somas
acumuladas** (`prefixo[i]` = soma de tudo antes da posição `i`) e
responda cada pergunta com uma subtração: `prefixo[fim] - prefixo[inicio]`.
Depois do pré-processamento, cada pergunta custa O(1).
"""

META = {
    "id": "A09-005",
    "titulo": "Some o intervalo sem repetir a conta",
    "nivel": 3,
    "tempo_min": 10,
    "tags": ["big-o", "prefix-sum"],
    "dicas": [
        'Monte uma lista prefixo do mesmo tamanho de vendas + 1, começando\\nem 0, onde prefixo[i] guarda a soma de vendas[0:i].',
        'prefixo[i+1] = prefixo[i] + vendas[i] — cada posição soma o valor\\nanterior mais o item atual.',
        "Cada pergunta (inicio, fim) vira só: prefixo[fim] - prefixo[inicio].",
    ],
}


def resolver(vendas: list, perguntas: list) -> list:
    # O(n) para montar o prefixo, mais O(1) por pergunta — no total O(n + perguntas), não O(n × perguntas).
    prefixo = [0]
    for venda in vendas:
        prefixo.append(prefixo[-1] + venda)

    respostas = []
    for inicio, fim in perguntas:
        respostas.append(prefixo[fim] - prefixo[inicio])
    return respostas
