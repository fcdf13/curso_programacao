"""
`type(valor)` responde de que tipo é um valor:

    type(42)        ->  <class 'int'>
    type(3.14)      ->  <class 'float'>
    type("Aurora")  ->  <class 'str'>
    type(True)      ->  <class 'bool'>

Devolva o tipo do valor recebido.

Exemplos:

    resolver(42)        ->  int
    resolver("Aurora")  ->  str
"""

META = {
    "id": "A01-006",
    "titulo": "Qual é o tipo",
    "nivel": 2,
    "tempo_min": 5,
    "tags": ["tipos", "type"],
    "dicas": [
        "A resposta é o próprio resultado de type(...), não um texto.",
        'Não escreva return "int" — isso é o texto \'int\', não o tipo int.',
        "return type(valor)",
    ],
}


def resolver(valor):
    ...
