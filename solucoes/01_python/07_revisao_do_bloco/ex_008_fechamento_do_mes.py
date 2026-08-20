"""
O exercício final do bloco. Você recebe três listas alinhadas:
categorias, valores vendidos e quantidades de pedidos.

Devolva um texto de uma linha por categoria, mais uma linha de total,
**tudo junto numa lista de textos**, no formato:

    CATEGORIA: R$ 1234.50 em 10 pedidos (ticket R$ 123.45)
    ...
    TOTAL: R$ 9999.99 em 99 pedidos

Regras:

    - a categoria sai em MAIÚSCULAS
    - o ticket médio é valor ÷ pedidos, com 2 casas
    - categorias com zero pedidos são **ignoradas** (não entram no relatório
      nem no total)
    - se nenhuma categoria sobrar, devolva `["TOTAL: R$ 0.00 em 0 pedidos"]`

Exemplo:

    resolver(["moda", "casa"], [1000.0, 500.0], [10, 5])
    ->  ["MODA: R$ 1000.00 em 10 pedidos (ticket R$ 100.00)",
         "CASA: R$ 500.00 em 5 pedidos (ticket R$ 100.00)",
         "TOTAL: R$ 1500.00 em 15 pedidos"]
"""

META = {
    "id": "A07-008",
    "titulo": "Fechamento do mês",
    "nivel": 4,
    "tempo_min": 14,
    "tags": ["zip", "laco", "condicional", "f-string", "composicao", "revisao"],
    "requer": ["A06-016", "A07-006"],
    "dicas": [
        'Três acumuladores: as linhas do relatório, o total em dinheiro e o\\ntotal de pedidos.',
        'O continue resolve as categorias com zero pedidos — e de quebra evita\\na divisão por zero do ticket.',
        "A linha do TOTAL é montada depois do laço e acrescentada por último.",
    ],
}


def resolver(categorias: list, valores: list, pedidos: list) -> list:
    # Pular a categoria vazia com continue mata dois coelhos: o filtro do relatório e a divisão por zero.
    linhas = []
    total_valor = 0.0
    total_pedidos = 0

    for categoria, valor, quantidade in zip(categorias, valores, pedidos):
        if quantidade == 0:
            continue
        ticket = valor / quantidade
        linhas.append(
            f"{categoria.upper()}: R$ {valor:.2f} em {quantidade} pedidos "
            f"(ticket R$ {ticket:.2f})"
        )
        total_valor += valor
        total_pedidos += quantidade

    linhas.append(f"TOTAL: R$ {total_valor:.2f} em {total_pedidos} pedidos")
    return linhas
