# Módulo A5 — Listas

> A estrutura mais usada de Python: vários valores em ordem, num nome só.

## Uma lista guarda vários valores em ordem

```python
precos = [49.90, 12.00, 230.50]
precos[0]      # 49.9   — o primeiro
precos[-1]     # 230.5  — o último
len(precos)    # 3
```

Índices e fatiamento funcionam igual aos de string, porque os dois são sequências.

```python
precos[0:2]    # [49.9, 12.0]
precos[::-1]   # [230.5, 12.0, 49.9]
```

### Listas mudam — strings não

Essa é a diferença estrutural entre as duas.

```python
precos.append(99.90)      # acrescenta no fim
precos.insert(0, 5.00)    # insere na posição 0, empurrando o resto
precos.remove(12.00)      # tira a primeira ocorrência DESSE VALOR
precos.pop()              # tira o último e DEVOLVE ele
precos[1] = 15.00         # troca o item da posição 1
```

### O par que confunde todo mundo: `sort` e `sorted`

```python
numeros = [3, 1, 2]

numeros.sort()            # reordena a própria lista; devolve None
ordenados = sorted(numeros)   # devolve uma lista NOVA; a original fica intacta
```

O erro clássico é escrever `numeros = numeros.sort()` — e ficar com `None`.
A regra vale para vários métodos de lista: **os que alteram devolvem `None`**.

### Funções que resumem uma lista

```python
sum(precos)      # soma tudo
min(precos)      # menor
max(precos)      # maior
len(precos)      # quantos
precos.count(49.9)   # quantas vezes esse valor aparece
precos.index(49.9)   # em que posição está a primeira ocorrência
49.9 in precos       # existe?
```

### Juntar e repetir

```python
[1, 2] + [3]     # [1, 2, 3]
[0] * 3          # [0, 0, 0]
```

## Exercícios deste módulo

14 exercícios, nível 1 a 3.

| id | título | nível |
|---|---|---|
| `A05-001` | Montar uma lista | ●○○○○ |
| `A05-002` | Primeiro, último e quantos | ●○○○○ |
| `A05-003` | Fatiar a lista | ●●○○○ |
| `A05-004` | Acrescentar no fim | ●●○○○ |
| `A05-005` | Tirar um item | ●●○○○ |
| `A05-006` | sorted não é sort | ●●●○○ |
| `A05-007` | De trás para frente | ●●○○○ |
| `A05-008` | Resumo dos números | ●●○○○ |
| `A05-009` | Em que posição está | ●●○○○ |
| `A05-010` | Juntar e repetir | ●●○○○ |
| `A05-011` | Quantas vezes aparece | ●●○○○ |
| `A05-012` | Trocar um item | ●●○○○ |
| `A05-013` | Média da lista | ●●○○○ |
| `A05-014` | Os três maiores | ●●●○○ |

Comece com `curso proximo`.
