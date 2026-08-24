"""
Aplique a taxa padrão do módulo sobre um preço.

Exemplo:

    resolver(100.0)  ->  105.0

`TAXA_PADRAO` está definida no topo deste arquivo. Uma função
**lê** uma variável global sem precisar de nenhuma palavra
especial — só usar.
"""

META = {
    "id": "A11-009",
    "titulo": "Escopo: ler uma variável global",
    "nivel": 2,
    "tempo_min": 6,
    "tags": ["funcoes", "escopo", "global"],
    "dicas": [
        "Uma função lê variáveis globais sem nada de especial — só usar o nome.",
        "TAXA_PADRAO já existe no arquivo, acima da função resolver.",
        "return preco * (1 + TAXA_PADRAO)",
    ],
}


TAXA_PADRAO = 0.05


def resolver(preco: float) -> float:
    ...
