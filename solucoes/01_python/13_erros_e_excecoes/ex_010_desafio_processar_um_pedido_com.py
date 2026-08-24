"""
Calcule o valor de cada parcela de um pedido, combinando tudo o
que o módulo ensinou:

- Se `quantidade` for menor ou igual a zero, **lance**
  `ValueError("quantidade deve ser positiva")`.
- Tente calcular `(preco * quantidade) / parcelas`.
- Se `parcelas` for zero, devolva `"Erro: número de parcelas inválido"`.
- Se `preco` não for um número (por exemplo, `None`), devolva
  `"Erro: preço inválido"`.
- Se o cálculo der certo, devolva `f"{parcelas}x de R$ {valor:.2f}"`.
- Em **qualquer** caso (deu certo, deu erro, ou nem chegou a
  tentar por causa do `raise`), conte a tentativa em
  `tentativas_de_processamento`.

Exemplos:

    resolver(300.0, 2, 3)   ->  "3x de R$ 200.00"
    resolver(300.0, 2, 0)   ->  "Erro: número de parcelas inválido"
    resolver(None, 2, 3)    ->  "Erro: preço inválido"
    resolver(300.0, 0, 3)   ->  levanta ValueError("quantidade deve ser positiva")

`None * 2` levanta `TypeError` — é assim que um preço inválido
aparece aqui. Repare que o `raise` de quantidade inválida
acontece **antes** do `try`: ele não é um erro que o `try`
deveria capturar, é uma regra de negócio que impede a conta de
sequer começar.
"""

META = {
    "id": "A13-010",
    "titulo": "Desafio: processar um pedido com parcelas",
    "nivel": 5,
    "tempo_min": 13,
    "tags": ["excecoes", "desafio", "try-except-else-finally", "raise"],
    "requer": ["A13-003", "A13-006", "A13-007"],
    "dicas": [
        'O raise de quantidade fica fora do try, no começo da função\n— ele não é um erro para capturar, é uma validação que barra a conta\nantes de começar.',
        'Dentro do try, um except ZeroDivisionError e um except\nTypeError, cada um com sua mensagem; o finally conta a tentativa nos dois\ncasos (e também no caminho de sucesso).',
        'global tentativas_de_processamento\n    if quantidade <= 0:\n        raise ValueError("quantidade deve ser positiva")\n    try:\n        valor = (preco * quantidade) / parcelas\n    except ZeroDivisionError:\n        return "Erro: número de parcelas inválido"\n    except TypeError:\n        return "Erro: preço inválido"\n    else:\n        return f"{parcelas}x de R$ {valor:.2f}"\n    finally:\n        tentativas_de_processamento += 1',
    ],
}


tentativas_de_processamento = 0


def resolver(preco, quantidade: int, parcelas: int) -> str:
    # A validação de quantidade fica fora do try de propósito — misturar 'regra de negócio que barra a operação' com 'erro técnico que a operação pode encontrar' deixa o código mais difícil de ler.
    global tentativas_de_processamento
    if quantidade <= 0:
        raise ValueError("quantidade deve ser positiva")
    try:
        valor = (preco * quantidade) / parcelas
    except ZeroDivisionError:
        return "Erro: número de parcelas inválido"
    except TypeError:
        return "Erro: preço inválido"
    else:
        return f"{parcelas}x de R$ {valor:.2f}"
    finally:
        tentativas_de_processamento += 1
