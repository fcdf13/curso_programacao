"""
Escreva uma saudação para um nome, com uma palavra de saudação
que tem um valor padrão.

Exemplos:

    resolver("Ana")               ->  "Olá, Ana!"
    resolver("Ana", "Bem-vindo")  ->  "Bem-vindo, Ana!"

Um parâmetro pode ter um valor padrão (`saudacao="Olá"`) — quem
chama a função pode simplesmente não passar aquele argumento.
"""

META = {
    "id": "A11-001",
    "titulo": "Parâmetro com valor padrão",
    "nivel": 1,
    "tempo_min": 4,
    "tags": ["funcoes", "parametro-padrao"],
    "dicas": [
        'Um parâmetro pode ter um valor padrão: def f(x, y="algo").',
        "Quando quem chama não passa saudacao, o valor padrão entra no lugar.",
        'return f"{saudacao}, {nome}!"',
    ],
}


def resolver(nome: str, saudacao: str = "Olá") -> str:
    ...
