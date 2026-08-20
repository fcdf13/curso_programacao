# Módulo A1 — Primeiros passos

> Mostrar, devolver, guardar. As três coisas que todo programa faz.

## O que você vai aprender

Um programa faz três coisas o tempo todo: **calcula** um valor, **guarda** esse valor
em algum lugar e **entrega** o resultado para alguém. Este módulo é sobre as três.

### print não é return

É a confusão número um de quem começa, e vale resolver logo:

```python
def mostrar():
    print("Olá")        # escreve na tela e devolve None

def devolver():
    return "Olá"        # não escreve nada; entrega o texto para quem chamou
```

`print` fala com o **ser humano** que está olhando o terminal.
`return` fala com o **resto do programa**.

```python
x = mostrar()     # aparece "Olá" na tela, e x fica valendo None
y = devolver()    # nada aparece na tela, e y fica valendo "Olá"
```

Neste curso quase todo exercício pede `return`, porque é assim que o corretor
consegue conferir o seu resultado. Quando o enunciado pedir `print`, ele diz isso
com todas as letras.

### Variáveis são etiquetas

```python
preco = 49.90
```

Não existe "caixinha" — `preco` é uma etiqueta colada no valor `49.90`. Colar a
etiqueta em outro valor depois é normal: `preco = 39.90`.

### Os quatro tipos do começo

| tipo | o que é | exemplo |
|---|---|---|
| `int` | número inteiro | `42`, `-7` |
| `float` | número com vírgula (que em Python é ponto) | `3.14`, `49.9` |
| `str` | texto, sempre entre aspas | `"Aurora"`, `'oi'` |
| `bool` | verdadeiro ou falso | `True`, `False` |

`type(valor)` diz qual é o tipo. `int("42")` e `str(42)` convertem de um para outro —
e **`"3" + "4"` dá `"34"`, não `7`**, porque para texto o `+` é grudar.

### f-string: o jeito moderno de montar texto

```python
nome = "Ana"
idade = 30
f"{nome} tem {idade} anos"     # 'Ana tem 30 anos'
```

O `f` antes da aspa é obrigatório. Dentro das chaves vai qualquer expressão Python.

## Exercícios deste módulo

12 exercícios, nível 1 a 2.

| id | título | nível |
|---|---|---|
| `A01-001` | Olá, Aurora | ●○○○○ |
| `A01-002` | Três linhas na tela | ●○○○○ |
| `A01-003` | Devolver em vez de mostrar | ●○○○○ |
| `A01-004` | Guardar em uma variável | ●○○○○ |
| `A01-005` | Somar dois números | ●○○○○ |
| `A01-006` | Qual é o tipo | ●●○○○ |
| `A01-007` | De texto para número | ●●○○○ |
| `A01-008` | De número para texto | ●●○○○ |
| `A01-009` | Nome completo | ●○○○○ |
| `A01-010` | A mesma frase com f-string | ●●○○○ |
| `A01-011` | Média de três notas | ●●○○○ |
| `A01-012` | Trocar dois valores de lugar | ●●○○○ |

Comece com `curso proximo`.
