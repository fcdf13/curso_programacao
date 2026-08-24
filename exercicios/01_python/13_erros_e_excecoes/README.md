# Módulo A13 — Erros e exceções

> Capturar o erro certo, lançar o seu próprio, e decidir entre perguntar antes ou pedir perdão depois.

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

## Exercícios deste módulo

10 exercícios, nível 1 a 5.

| id | título | nível |
|---|---|---|
| `A13-001` | try/except: um plano B para o erro | ●○○○○ |
| `A13-002` | Capturar a exceção certa | ●○○○○ |
| `A13-003` | Vários except, um para cada erro | ●●○○○ |
| `A13-004` | except ... as erro: a mensagem original | ●●○○○ |
| `A13-005` | else: só roda se nada deu errado | ●●○○○ |
| `A13-006` | finally: roda sempre, com ou sem erro | ●●●○○ |
| `A13-007` | raise: lançar sua própria exceção | ●●●○○ |
| `A13-008` | Capturar um erro e relançar um mais claro | ●●●○○ |
| `A13-009` | EAFP em vez de LBYL | ●●●●○ |
| `A13-010` | Desafio: processar um pedido com parcelas | ●●●●● |

Comece com `curso proximo`.
