# Módulo A6 — Laços

> Repetir sem copiar e colar. É aqui que o programa começa a valer a pena.

## `for`: uma volta para cada item

```python
for preco in [10, 20, 30]:
    print(preco)
```

Leia como "para cada preço nessa lista, faça isto". A variável `preco` recebe
um item por vez, automaticamente.

### `range`: uma sequência de números

```python
range(5)         # 0, 1, 2, 3, 4        — começa no 0, o 5 não entra
range(1, 6)      # 1, 2, 3, 4, 5
range(0, 10, 2)  # 0, 2, 4, 6, 8        — de dois em dois
```

O fim nunca entra — mesma lógica do fatiamento.

### O acumulador

O padrão mais importante do módulo. Sempre a mesma forma:

```python
total = 0                  # 1. começa vazio, FORA do laço
for preco in precos:
    total = total + preco  # 2. atualiza a cada volta  (ou: total += preco)
return total               # 3. usa depois que o laço acabou
```

Se você criar `total = 0` dentro do laço, ele zera a cada volta — o bug número um
de iniciante. Se colocar o `return` dentro do laço, a função para na primeira volta —
o bug número dois.

O mesmo esqueleto serve para **contar** (`quantos += 1`) e para **construir uma
lista** (`resultado.append(...)`).

### `while`: repetir enquanto algo for verdade

```python
saldo = 100
while saldo > 0:
    saldo = saldo - 30
```

Use `while` quando você **não sabe de antemão** quantas voltas serão. E garanta
que a condição um dia fique falsa — senão o programa trava.

### `break` e `continue`

```python
for x in itens:
    if x is None:
        continue     # pula esta volta, segue para a próxima
    if x == alvo:
        break        # abandona o laço inteiro
```

### Percorrer com o índice junto

```python
for posicao, nome in enumerate(["a", "b"]):
    ...              # posicao vale 0 e depois 1

for nome, preco in zip(nomes, precos):
    ...              # anda nas duas listas ao mesmo tempo
```

`zip` para na mais curta das duas.

## Exercícios deste módulo

16 exercícios, nível 1 a 3.

| id | título | nível |
|---|---|---|
| `A06-001` | Percorrer uma lista | ●○○○○ |
| `A06-002` | Uma sequência de números | ●●○○○ |
| `A06-003` | Somar com acumulador | ●●○○○ |
| `A06-004` | Contar quantos passam | ●●○○○ |
| `A06-005` | Construir uma lista nova | ●●○○○ |
| `A06-006` | Enquanto houver saldo | ●●○○○ |
| `A06-007` | Parar na primeira | ●●○○○ |
| `A06-008` | Pular os inválidos | ●●○○○ |
| `A06-009` | Achar o maior na mão | ●●●○○ |
| `A06-010` | A posição junto com o item | ●●○○○ |
| `A06-011` | Duas listas ao mesmo tempo | ●●○○○ |
| `A06-012` | Percorrer um texto | ●●○○○ |
| `A06-013` | Tabuada | ●●●○○ |
| `A06-014` | Contagem regressiva | ●●○○○ |
| `A06-015` | FizzBuzz | ●●●○○ |
| `A06-016` | Total do carrinho | ●●●○○ |

Comece com `curso proximo`.
