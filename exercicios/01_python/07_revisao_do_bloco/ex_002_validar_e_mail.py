"""
Uma validação simples de e-mail, do tipo que todo formulário faz.

Devolva `True` quando o texto satisfizer **todas** as regras:

    - contém exatamente um "@"
    - tem pelo menos um caractere antes do "@"
    - depois do "@" existe um "."
    - não tem espaços

Exemplos:

    resolver("ana@loja.com")   ->  True
    resolver("analoja.com")    ->  False   (sem @)
    resolver("@loja.com")      ->  False   (nada antes do @)
    resolver("ana@lojacom")    ->  False   (sem ponto no domínio)
    resolver("a na@loja.com")  ->  False   (tem espaço)
    resolver("a@b@loja.com")   ->  False   (dois @)

Dica de estratégia: separe o texto no "@" e analise as duas partes.
"""

META = {
    "id": "A07-002",
    "titulo": "Validar e-mail",
    "nivel": 3,
    "tempo_min": 9,
    "tags": ["strings", "booleano", "validacao", "revisao"],
    "requer": ["A03-009", "A04-004"],
    "dicas": [
        'email.count("@") diz quantos arrobas existem — comece por aí.',
        'email.split("@") devolve uma lista; com exatamente um @, ela tem 2 partes.',
        'Guarde antes, depois = email.split("@") e teste cada parte separadamente.',
    ],
}


def resolver(email: str) -> bool:
    ...
