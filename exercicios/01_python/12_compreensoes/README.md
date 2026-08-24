# Módulo A12 — Compreensões

> Construir listas, dicionários e conjuntos em uma linha — e saber quando não fazer isso.

## List comprehension: construir uma lista em uma linha

```python
precos = [10.0, 20.0, 30.0]

dobrados = []
for preco in precos:
    dobrados.append(preco * 2)
# dobrados == [20.0, 40.0, 60.0]

dobrados = [preco * 2 for preco in precos]   # a mesma coisa, numa linha
```

A forma geral é `[expressão for item in iterável]` — para cada item do
iterável, calcule a expressão e guarde o resultado, na ordem.

### Com filtro: só alguns itens entram

```python
caros = [preco for preco in precos if preco >= 20.0]   # [20.0, 30.0]
```

O `if` no fim filtra **antes** da expressão rodar — só os itens que passam
no filtro chegam a virar resultado.

### Combinando transformação e filtro

```python
[preco * 1.1 for preco in precos if preco >= 20.0]   # [22.0, 33.0]
```

### Expressão condicional (`x if cond else y`) dentro da expressão

Isso é diferente do `if` de filtro de cima — aqui os **dois** lados sempre
entram no resultado, só muda qual valor:

```python
["caro" if preco >= 20.0 else "barato" for preco in precos]
# ["barato", "caro", "caro"]
```

### Dict comprehension e set comprehension

A mesma ideia, trocando os colchetes por chaves:

```python
{produto: preco for produto, preco in zip(produtos, precos)}   # dict
{categoria.upper() for categoria in categorias}                  # set, sem repetir
```

### Comprehension aninhada: mais de um `for`

```python
matriz = [[1, 2], [3, 4, 5]]
achatada = [item for linha in matriz for item in linha]
# [1, 2, 3, 4, 5]
```

Os `for` aparecem na mesma ordem em que apareceriam se você escrevesse os
laços aninhados à mão — o de fora primeiro, o de dentro depois.

## Quando **não** usar comprehension

Comprehension serve para **construir uma coleção**. Se você só quer saber
"existe algum item que...", `any()`/`all()` com uma **expressão geradora**
(a mesma sintaxe, mas sem os colchetes) é melhor — porque eles podem parar
assim que souberem a resposta, sem nunca montar a lista inteira:

```python
any(preco > 1000 for preco in precos)      # para no primeiro True
any([preco > 1000 for preco in precos])    # monta a lista TODA antes de checar
```

Com uma lista de milhões de itens e a resposta logo no início, a primeira
forma é ordens de magnitude mais rápida — a segunda paga o custo de
construir a lista inteira mesmo sem precisar de nenhum item além do primeiro.

E comprehension não serve para rodar efeitos colaterais: `[print(x) for x
in lista]` funciona, mas cria uma lista de `None`s só para jogar fora — um
`for` comum é o jeito certo quando você não está construindo nada.

## Exercícios deste módulo

12 exercícios, nível 1 a 5.

| id | título | nível |
|---|---|---|
| `A12-001` | List comprehension básica | ●○○○○ |
| `A12-002` | List comprehension com filtro | ●●○○○ |
| `A12-003` | Transformar e filtrar ao mesmo tempo | ●●○○○ |
| `A12-004` | Dict comprehension básica | ●●○○○ |
| `A12-005` | Dict comprehension com filtro | ●●●○○ |
| `A12-006` | Set comprehension | ●●○○○ |
| `A12-007` | Expressão condicional dentro da comprehension | ●●●○○ |
| `A12-008` | Comprehension com enumerate | ●●●○○ |
| `A12-009` | Comprehension aninhada: achatar uma lista de listas | ●●●●○ |
| `A12-010` | Comprehension aninhada com filtro: combinações | ●●●●○ |
| `A12-011` | Quando não usar list comprehension | ●●●●○ |
| `A12-012` | Desafio: catálogo por categoria | ●●●●● |

Comece com `curso proximo`.
