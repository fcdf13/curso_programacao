"""
Um CPF chega como 11 dígitos grudados. Devolva no formato
`000.000.000-00`.

Se o texto não tiver exatamente 11 caracteres, devolva `"invalido"`.

Exemplos:

    resolver("12345678901")   ->  "123.456.789-01"
    resolver("00000000000")   ->  "000.000.000-00"
    resolver("123")           ->  "invalido"
    resolver("")              ->  "invalido"

Fatiamento (A3) mais validação de tamanho (A4).
"""

META = {
    "id": "A07-003",
    "titulo": "Formatar CPF",
    "nivel": 3,
    "tempo_min": 8,
    "tags": ["strings", "fatiamento", "validacao", "revisao"],
    "requer": ["A03-003", "A03-011"],
    "dicas": [
        "Valide o tamanho antes de fatiar.",
        "São quatro pedaços: 0:3, 3:6, 6:9 e 9:11.",
        'Monte o resultado com f-string: f"{cpf[0:3]}.{cpf[3:6]}..."',
    ],
}


def resolver(cpf: str) -> str:
    ...
