"""
Divida dois números. Se o segundo for zero, devolva `None` em
vez de deixar o programa quebrar.

Exemplos:

    resolver(10, 2)  ->  5.0
    resolver(10, 0)  ->  None

`10 / 0` levanta `ZeroDivisionError`. Um bloco `try`/`except`
deixa você decidir o que fazer quando isso acontece, em vez de
travar o programa.
"""

META = {
    "id": "A13-001",
    "titulo": "try/except: um plano B para o erro",
    "nivel": 1,
    "tempo_min": 5,
    "tags": ["excecoes", "try-except", "zerodivisionerror"],
    "dicas": [
        'try: ... except ZeroDivisionError: ... — o except só roda se\num erro daquele tipo acontecer dentro do try.',
        "O que fica dentro do try é só a divisão; o except devolve None.",
        'try:\n        return a / b\n    except ZeroDivisionError:\n        return None',
    ],
}


def resolver(a: float, b: float) -> float | None:
    ...
