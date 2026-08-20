"""
Agora o contrário: nada deve aparecer na tela.

Faça `resolver()` **devolver** o texto `Olá, Aurora!` — sem imprimir.

Exemplo de como sua função será usada:

    mensagem = resolver()
    # mensagem passa a valer "Olá, Aurora!"

Se você usar `print` aqui, a função devolve `None` e o teste reprova.
Essa diferença é o assunto do módulo inteiro.
"""

META = {
    "id": "A01-003",
    "titulo": "Devolver em vez de mostrar",
    "nivel": 1,
    "tempo_min": 4,
    "tags": ["return", "string"],
    "requer": ["A01-001"],
    "dicas": [
        "return entrega o valor para quem chamou a função; print só desenha na tela.",
        "A palavra return vem antes do valor, sem parênteses obrigatórios.",
        'return "Olá, Aurora!"',
    ],
}


def resolver() -> str:
    # Sem print: quem chamou a função recebe o texto e decide o que fazer com ele.
    return "Olá, Aurora!"
