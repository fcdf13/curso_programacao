"""
Adicione um item a um histórico, devolvendo o histórico
atualizado. Quando nenhum histórico é passado, comece um novo —
vazio.

Exemplos:

    resolver("Fone")                  ->  ["Fone"]
    resolver("Capa", ["Fone"])         ->  ["Fone", "Capa"]

**Não** escreva `historico=[]` na assinatura — um valor padrão
mutável (uma lista, um dict) é criado **uma vez só**, na hora
que a função é definida, e essa mesma lista seria reaproveitada
em toda chamada onde ninguém passa `historico`. Use `None` como
sentinela e crie a lista de dentro, quando ela não vier.
"""

META = {
    "id": "A11-008",
    "titulo": "A armadilha do argumento padrão mutável",
    "nivel": 3,
    "tempo_min": 9,
    "tags": ["funcoes", "parametro-padrao", "armadilha", "mutabilidade"],
    "requer": ["A11-001"],
    "dicas": [
        'historico=[] pareceria funcionar, mas a mesma lista seria reaproveitada\nem toda chamada sem historico — chame a função duas vezes seguidas para ver o bug.',
        "Use historico: list | None = None, e crie a lista de dentro quando vier None.",
        'if historico is None:\n        historico = []\n    historico.append(item)\n    return historico',
    ],
}


def resolver(item: str, historico: list | None = None) -> list:
    # historico=[] direto na assinatura compartilharia a MESMA lista entre chamadas diferentes que não passam historico — o bug clássico do argumento padrão mutável. None é o sentinela seguro.
    if historico is None:
        historico = []
    historico.append(item)
    return historico
