"""Bloco A, módulo 13: erros e exceções."""

from autoria.modelo import Exercicio as Ex
from autoria.modelo import Modulo

A13 = Modulo(
    id="A13",
    titulo="Módulo A13 — Erros e exceções",
    resumo="Capturar o erro certo, lançar o seu próprio, e decidir entre perguntar antes ou pedir perdão depois.",
    teoria="""
## `try`/`except`: tentar, e ter um plano B

```python
def dividir(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None

dividir(10, 2)   # 5.0
dividir(10, 0)   # None — a exceção foi capturada, o programa não quebrou
```

Sem o `try`, `10 / 0` estouraria `ZeroDivisionError` e pararia o programa
(ou o teste). Com o `try`, você decide o que fazer quando aquele erro
específico acontece.

### Cada exceção tem um tipo — capture o tipo certo

```python
try:
    int("abc")
except ValueError:
    print("não é um número")
```

| exceção | quando acontece |
|---|---|
| `ZeroDivisionError` | dividir por zero |
| `ValueError` | valor do tipo certo, mas com conteúdo inválido (`int("abc")`) |
| `KeyError` | chave que não existe num dicionário |
| `IndexError` | posição que não existe numa lista |
| `TypeError` | operação entre tipos incompatíveis (`None * 2`) |

Capturar `Exception` (o tipo genérico que engloba quase tudo) esconde bugs
de verdade — capture só o tipo que você sabe tratar.

### Vários `except`, um para cada tipo

```python
try:
    return int(a) / int(b)
except ValueError:
    return "valor inválido"
except ZeroDivisionError:
    return "divisão por zero"
```

Python testa os `except` na ordem escrita e usa o primeiro que bate com o
tipo da exceção levantada.

### `except ... as erro`: pegando a mensagem

```python
try:
    float("abc")
except ValueError as erro:
    print(str(erro))   # "could not convert string to float: 'abc'"
```

### `else`: só roda se nada deu errado

```python
try:
    numero = int(texto)
except ValueError:
    print("não é número")
else:
    print(f"número: {numero}")   # só chega aqui se int() não estourou
```

### `finally`: roda sempre, com ou sem erro

```python
try:
    resultado = arriscado()
except ValueError:
    resultado = None
finally:
    tentativas += 1   # conta a tentativa, dê certo ou não
```

`finally` roda mesmo quando o `try` ou o `except` termina com `return` —
é o único jeito de garantir código que sempre executa.

## `raise`: lançar sua própria exceção

```python
def validar_idade(idade):
    if idade < 0:
        raise ValueError("idade não pode ser negativa")
    return idade
```

`raise` interrompe a função na hora — o código depois dele nunca roda.
Quem chama pode capturar com `except ValueError`, ou deixar propagar.

### Capturar um erro de baixo nível e relançar um mais claro

```python
try:
    return int(texto)
except ValueError:
    raise ValueError(f"'{texto}' não é um número válido") from None
```

A mensagem original (`invalid literal for int() with base 10: 'abc'`) fala
do `int()`; a nova fala do seu problema. `from None` evita empilhar as duas
exceções na mensagem de erro.

## EAFP × LBYL

Duas filosofias para o mesmo problema — acessar algo que pode não existir:

```python
# LBYL — Look Before You Leap: confere antes de agir
if produto in precos:
    preco = precos[produto]
else:
    preco = 0.0

# EAFP — Easier to Ask Forgiveness than Permission: tenta, trata se falhar
try:
    preco = precos[produto]
except KeyError:
    preco = 0.0
```

Python prefere EAFP: o caminho de sucesso fica mais limpo (uma leitura só,
não duas), e evita um problema sutil — entre o `if` e o acesso, algo
poderia mudar. LBYL ainda é válido quando checar a condição é mais barato
ou mais claro do que capturar o erro.
""",
    exercicios=[
        Ex(
            id="A13-001", titulo="try/except: um plano B para o erro", nivel=1, tempo_min=5,
            tags=["excecoes", "try-except", "zerodivisionerror"],
            enunciado="""
            Divida dois números. Se o segundo for zero, devolva `None` em
            vez de deixar o programa quebrar.

            Exemplos:

                resolver(10, 2)  ->  5.0
                resolver(10, 0)  ->  None

            `10 / 0` levanta `ZeroDivisionError`. Um bloco `try`/`except`
            deixa você decidir o que fazer quando isso acontece, em vez de
            travar o programa.
            """,
            assinatura="def resolver(a: float, b: float) -> float | None:",
            dicas=[
                "try: ... except ZeroDivisionError: ... — o except só roda se\num erro daquele tipo acontecer dentro do try.",
                "O que fica dentro do try é só a divisão; o except devolve None.",
                "try:\n        return a / b\n    except ZeroDivisionError:\n        return None",
            ],
            solucao="""
            try:
                return a / b
            except ZeroDivisionError:
                return None
            """,
            testes="""
def teste_divisao_normal():
    verificar(ex.resolver(10, 2), 5.0)


def teste_divisao_por_zero():
    verificar(ex.resolver(10, 0), None)


def teste_zero_dividido_por_numero():
    verificar(ex.resolver(0, 5), 0.0)
""",
        ),
        Ex(
            id="A13-002", titulo="Capturar a exceção certa", nivel=1, tempo_min=5,
            tags=["excecoes", "try-except", "valueerror"], requer=["A13-001"],
            enunciado="""
            Converta um texto para número inteiro. Se o texto não for um
            número válido, devolva `None`.

            Exemplos:

                resolver("42")   ->  42
                resolver("abc")  ->  None

            `int("abc")` levanta `ValueError` — um tipo diferente do
            exercício anterior. Capture o tipo certo: `except ValueError`.
            """,
            assinatura="def resolver(texto: str) -> int | None:",
            dicas=[
                "int(texto) levanta ValueError quando o texto não é um número.",
                "O try guarda só a conversão; capture ValueError, não ZeroDivisionError.",
                "try:\n        return int(texto)\n    except ValueError:\n        return None",
            ],
            solucao="""
            try:
                return int(texto)
            except ValueError:
                return None
            """,
            testes="""
def teste_texto_valido():
    verificar(ex.resolver("42"), 42)


def teste_texto_invalido():
    verificar(ex.resolver("abc"), None)


def teste_texto_vazio():
    verificar(ex.resolver(""), None)


def teste_numero_negativo_em_texto():
    verificar(ex.resolver("-7"), -7)
""",
        ),
        Ex(
            id="A13-003", titulo="Vários except, um para cada erro", nivel=2, tempo_min=7,
            tags=["excecoes", "try-except", "multiplos-except"],
            requer=["A13-001", "A13-002"],
            enunciado="""
            Divida dois números que chegam como texto, devolvendo uma
            mensagem diferente para cada tipo de problema.

            Exemplos:

                resolver("10", "2")   ->  "5.0"
                resolver("10", "0")   ->  "Erro: divisão por zero"
                resolver("dez", "2")  ->  "Erro: valor inválido"

            Dois problemas diferentes podem acontecer aqui — texto que não
            é número (`ValueError`) e divisão por zero (`ZeroDivisionError`)
            — e cada um pede sua própria mensagem. Um `try` aceita vários
            `except`, um para cada tipo.
            """,
            assinatura="def resolver(texto_a: str, texto_b: str) -> str:",
            dicas=[
                "A conversão pode falhar com ValueError e a divisão com\nZeroDivisionError — as duas dentro do mesmo try.",
                "Um except por tipo, cada um com sua mensagem.",
                'try:\n        return str(int(texto_a) / int(texto_b))\n    except ValueError:\n        return "Erro: valor inválido"\n    except ZeroDivisionError:\n        return "Erro: divisão por zero"',
            ],
            solucao='''
            try:
                return str(int(texto_a) / int(texto_b))
            except ValueError:
                return "Erro: valor inválido"
            except ZeroDivisionError:
                return "Erro: divisão por zero"
            ''',
            testes="""
def teste_divisao_valida():
    verificar(ex.resolver("10", "2"), "5.0")


def teste_divisao_por_zero():
    verificar(ex.resolver("10", "0"), "Erro: divisão por zero")


def teste_primeiro_valor_invalido():
    verificar(ex.resolver("dez", "2"), "Erro: valor inválido")


def teste_segundo_valor_invalido():
    verificar(ex.resolver("10", "dois"), "Erro: valor inválido")
""",
        ),
        Ex(
            id="A13-004", titulo="except ... as erro: a mensagem original", nivel=2, tempo_min=6,
            tags=["excecoes", "try-except", "mensagem-de-erro"], requer=["A13-002"],
            enunciado="""
            Converta um texto para número decimal. Se falhar, devolva a
            mensagem de erro que o Python já gerou, com o prefixo
            `"Não deu: "`.

            Exemplo:

                resolver("abc")  ->  "Não deu: could not convert string to float: 'abc'"

            `except ValueError as erro` guarda a exceção numa variável —
            `str(erro)` é a mensagem, a mesma que apareceria numa falha sem
            tratamento.
            """,
            assinatura="def resolver(texto: str) -> str:",
            dicas=[
                "except ValueError as erro guarda a exceção capturada na variável erro.",
                "str(erro) devolve a mensagem original, pronta para usar numa f-string.",
                'try:\n        return str(float(texto))\n    except ValueError as erro:\n        return f"Não deu: {erro}"',
            ],
            solucao='''
            try:
                return str(float(texto))
            except ValueError as erro:
                return f"Não deu: {erro}"
            ''',
            testes="""
def teste_texto_valido():
    verificar(ex.resolver("3.5"), "3.5")


def teste_texto_invalido():
    verificar(ex.resolver("abc"), "Não deu: could not convert string to float: 'abc'")


def teste_texto_vazio():
    verificar(ex.resolver(""), "Não deu: could not convert string to float: ''")
""",
        ),
        Ex(
            id="A13-005", titulo="else: só roda se nada deu errado", nivel=2, tempo_min=7,
            tags=["excecoes", "try-except-else"], requer=["A13-002"],
            enunciado="""
            Converta um texto para número. Devolva `f"número: {valor}"` se
            der certo, ou `"não é número"` se não der.

            Exemplos:

                resolver("42")   ->  "número: 42"
                resolver("abc")  ->  "não é número"

            Um `else` depois do `except` roda só quando o `try` **não**
            levantou nenhuma exceção — é o lugar certo para o "caminho de
            sucesso", separado do que trata o erro.
            """,
            assinatura="def resolver(texto: str) -> str:",
            dicas=[
                "try converte; except captura o ValueError; else roda só\nquando a conversão deu certo.",
                "O valor convertido só existe se o try não estourou — por isso\nele é usado dentro do else, não depois do try inteiro.",
                'try:\n        valor = int(texto)\n    except ValueError:\n        return "não é número"\n    else:\n        return f"número: {valor}"',
            ],
            solucao='''
            try:
                valor = int(texto)
            except ValueError:
                return "não é número"
            else:
                return f"número: {valor}"
            ''',
            testes="""
def teste_numero_valido():
    verificar(ex.resolver("42"), "número: 42")


def teste_nao_e_numero():
    verificar(ex.resolver("abc"), "não é número")


def teste_numero_negativo():
    verificar(ex.resolver("-5"), "número: -5")
""",
        ),
        Ex(
            id="A13-006", titulo="finally: roda sempre, com ou sem erro", nivel=3, tempo_min=8,
            tags=["excecoes", "try-except-finally", "escopo"],
            requer=["A13-001", "A11-010"],
            preambulo="tentativas = 0",
            enunciado="""
            Divida dois números, devolvendo `None` se o segundo for zero —
            e conte **toda** tentativa, deu certo ou não, num contador
            global.

            Exemplo (chamadas em sequência):

                resolver(10, 2)  ->  5.0
                resolver(10, 0)  ->  None

            Depois das duas chamadas, `tentativas` vale 2 — contando as
            duas, não só a que deu certo. Um bloco `finally` roda
            **sempre**, com ou sem exceção — mesmo quando a função termina
            com `return` dentro do `except`.
            """,
            assinatura="def resolver(a: float, b: float) -> float | None:",
            dicas=[
                "finally vem depois do except (ou do else, se tiver) e roda\nnão importa o que aconteceu no try.",
                "A conta em tentativas precisa de global tentativas, como no módulo A11.",
                "global tentativas\n    try:\n        return a / b\n    except ZeroDivisionError:\n        return None\n    finally:\n        tentativas += 1",
            ],
            solucao="""
            global tentativas
            try:
                return a / b
            except ZeroDivisionError:
                return None
            finally:
                tentativas += 1
            """,
            nota_da_solucao="finally roda mesmo com um return dentro do try ou do except — é o único jeito de garantir código que sempre executa, dê certo ou não.",
            testes="""
def teste_conta_as_duas_tentativas():
    verificar(ex.resolver(10, 2), 5.0)
    verificar(ex.resolver(10, 0), None)
    verificar(ex.tentativas, 2, nome="tentativas")


def teste_conta_mesmo_so_com_sucesso():
    anterior = ex.tentativas
    ex.resolver(4, 2)
    verificar(ex.tentativas, anterior + 1, nome="tentativas")
""",
        ),
        Ex(
            id="A13-007", titulo="raise: lançar sua própria exceção", nivel=3, tempo_min=8,
            tags=["excecoes", "raise"], requer=["A13-002"],
            preambulo_do_teste="import pytest",
            enunciado="""
            Valide uma idade: se for negativa, **lance** um `ValueError`
            com a mensagem `"idade não pode ser negativa"`. Se for válida,
            devolva a própria idade.

            Exemplos:

                resolver(25)  ->  25
                resolver(-1)  ->  levanta ValueError("idade não pode ser negativa")

            `raise` lança uma exceção na hora — a função para ali, e quem
            chamou decide se captura ou deixa propagar.
            """,
            assinatura="def resolver(idade: int) -> int:",
            dicas=[
                'raise ValueError("mensagem") lança a exceção; o código depois dele nunca roda.',
                "Um if checa a condição inválida antes do raise; o caminho válido só tem o return.",
                'if idade < 0:\n        raise ValueError("idade não pode ser negativa")\n    return idade',
            ],
            solucao='''
            if idade < 0:
                raise ValueError("idade não pode ser negativa")
            return idade
            ''',
            testes="""
def teste_idade_valida():
    verificar(ex.resolver(25), 25)


def teste_idade_zero_e_valida():
    verificar(ex.resolver(0), 0)


def teste_idade_negativa_levanta_erro():
    with pytest.raises(ValueError):
        ex.resolver(-1)
""",
        ),
        Ex(
            id="A13-008", titulo="Capturar um erro e relançar um mais claro", nivel=3, tempo_min=9,
            tags=["excecoes", "raise", "reraise"], requer=["A13-002", "A13-007"],
            preambulo_do_teste="import pytest",
            enunciado="""
            Converta um texto para inteiro. Se não for possível, lance um
            `ValueError` com uma mensagem mais clara do que a original —
            incluindo o texto que falhou.

            Exemplos:

                resolver("42")   ->  42
                resolver("abc")  ->  levanta ValueError("'abc' não é um número válido")

            Capture o `ValueError` que `int()` já levanta, e **lance outro
            no lugar** — com a mensagem que faz sentido para quem usa a sua
            função, não a mensagem interna do `int()`.
            """,
            assinatura="def resolver(texto: str) -> int:",
            dicas=[
                "Dentro do except, um novo raise substitui a exceção original\npor outra — mesmo tipo, mensagem diferente.",
                "from None no fim do raise evita empilhar as duas exceções na mensagem.",
                "try:\n        return int(texto)\n    except ValueError:\n        raise ValueError(f\"'{texto}' não é um número válido\") from None",
            ],
            solucao='''
            try:
                return int(texto)
            except ValueError:
                raise ValueError(f"'{texto}' não é um número válido") from None
            ''',
            testes="""
def teste_texto_valido():
    verificar(ex.resolver("42"), 42)


def teste_texto_invalido_levanta_erro_com_mensagem_clara():
    with pytest.raises(ValueError, match="não é um número válido"):
        ex.resolver("abc")
""",
        ),
        Ex(
            id="A13-009", titulo="EAFP em vez de LBYL", nivel=4, tempo_min=9,
            tags=["excecoes", "eafp", "lbyl"], requer=["A13-001", "A08-003"],
            enunciado="""
            Ache o preço de um produto no catálogo, devolvendo `0.0` se ele
            não existir — mas usando o estilo **EAFP** (tente o acesso,
            capture o erro), não o **LBYL** (`if produto in precos`) do
            módulo A8.

            Exemplo:

                resolver({"Fone": 99.9}, "Fone")   ->  99.9
                resolver({"Fone": 99.9}, "Mouse")  ->  0.0

            LBYL ("*look before you leap*") checa a condição antes de agir
            — `if produto in precos:` seguido do acesso. EAFP ("*easier to
            ask forgiveness than permission*") tenta direto e trata o erro
            — uma leitura só do dicionário, em vez de duas.
            """,
            assinatura="def resolver(precos: dict, produto: str) -> float:",
            dicas=[
                "O estilo LBYL seria if produto in precos: ... else: 0.0 —\nnão é o que este exercício pede.",
                "Tente precos[produto] direto dentro de um try, e capture KeyError.",
                "try:\n        return precos[produto]\n    except KeyError:\n        return 0.0",
            ],
            solucao="""
            try:
                return precos[produto]
            except KeyError:
                return 0.0
            """,
            nota_da_solucao="LBYL faz dois acessos ao dicionário (o in e depois o []); EAFP faz um só — e ainda evita um problema sutil se o dicionário mudasse entre o if e o acesso.",
            testes="""
def teste_produto_existe():
    verificar(ex.resolver({"Fone": 99.9}, "Fone"), 99.9)


def teste_produto_nao_existe():
    verificar(ex.resolver({"Fone": 99.9}, "Mouse"), 0.0)


def teste_catalogo_vazio():
    verificar(ex.resolver({}, "Fone"), 0.0)
""",
        ),
        Ex(
            id="A13-010", titulo="Desafio: processar um pedido com parcelas", nivel=5, tempo_min=13,
            tags=["excecoes", "desafio", "try-except-else-finally", "raise"],
            requer=["A13-003", "A13-006", "A13-007"],
            preambulo="tentativas_de_processamento = 0",
            preambulo_do_teste="import pytest",
            enunciado="""
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
            """,
            assinatura="def resolver(preco, quantidade: int, parcelas: int) -> str:",
            dicas=[
                "O raise de quantidade fica fora do try, no começo da função\n— ele não é um erro para capturar, é uma validação que barra a conta\nantes de começar.",
                "Dentro do try, um except ZeroDivisionError e um except\nTypeError, cada um com sua mensagem; o finally conta a tentativa nos dois\ncasos (e também no caminho de sucesso).",
                'global tentativas_de_processamento\n    if quantidade <= 0:\n        raise ValueError("quantidade deve ser positiva")\n    try:\n        valor = (preco * quantidade) / parcelas\n    except ZeroDivisionError:\n        return "Erro: número de parcelas inválido"\n    except TypeError:\n        return "Erro: preço inválido"\n    else:\n        return f"{parcelas}x de R$ {valor:.2f}"\n    finally:\n        tentativas_de_processamento += 1',
            ],
            solucao='''
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
            ''',
            nota_da_solucao="A validação de quantidade fica fora do try de propósito — misturar 'regra de negócio que barra a operação' com 'erro técnico que a operação pode encontrar' deixa o código mais difícil de ler.",
            testes="""
def teste_calculo_correto():
    verificar(ex.resolver(300.0, 2, 3), "3x de R$ 200.00")


def teste_parcelas_zero():
    verificar(ex.resolver(300.0, 2, 0), "Erro: número de parcelas inválido")


def teste_preco_invalido():
    verificar(ex.resolver(None, 2, 3), "Erro: preço inválido")


def teste_quantidade_invalida_levanta_erro():
    with pytest.raises(ValueError):
        ex.resolver(300.0, 0, 3)


def teste_conta_todas_as_tentativas_exceto_a_barrada_pelo_raise():
    anterior = ex.tentativas_de_processamento
    ex.resolver(300.0, 2, 3)
    ex.resolver(300.0, 2, 0)
    ex.resolver(None, 2, 3)
    verificar(ex.tentativas_de_processamento, anterior + 3, nome="tentativas_de_processamento")
""",
        ),
    ],
)

MODULOS = [A13]
