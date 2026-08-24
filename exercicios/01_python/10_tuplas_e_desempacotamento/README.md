# Módulo A10 — Tuplas e desempacotamento

> A estrutura que não muda — e o jeito elegante de tirar valores dela.

## Tupla: como uma lista, mas travada

```python
ponto = (3, 4)
ponto[0]        # 3   — indexação funciona igual à lista
len(ponto)      # 2
```

Você já usa tuplas desde o A1 — todo `return a, b` devolve uma. A diferença que
importa agora: **tupla não muda depois de criada**.

```python
ponto[0] = 10        # TypeError: 'tuple' object does not support item assignment
```

Se você precisa de outra versão, cria uma tupla nova — não edita a antiga:

```python
ponto = (10, ponto[1])     # troca só o primeiro valor, criando uma tupla nova
```

### Desempacotar: tirar os valores de uma vez

```python
ponto = (3, 4)
x, y = ponto        # x=3, y=4 — uma variável para cada posição

nome, idade = "Ana", 30    # os parênteses da tupla são opcionais aqui
```

O número de variáveis à esquerda precisa bater com o de valores à direita —
senão é `ValueError: too many values to unpack` (ou de menos).

### O `_` para o que você não quer

```python
_, uf, _ = ("Ana", "SP", "2024-01-01")   # só a UF interessa desta vez
```

`_` é uma variável como outra qualquer — o nome é só uma convenção para dizer
"não vou usar isto".

### `*` pega "o resto"

```python
numeros = [10, 20, 30, 40]

primeiro, *resto = numeros      # primeiro=10, resto=[20, 30, 40]
*inicio, ultimo = numeros       # inicio=[10, 20, 30], ultimo=40
primeiro, *meio, ultimo = numeros   # primeiro=10, meio=[20, 30], ultimo=40
```

O `*` sempre vira uma **lista** (mesmo que a entrada original fosse tupla), e só
pode aparecer uma vez em cada desempacotamento — o Python não saberia como
dividir "o resto" em dois lugares diferentes.

### Por que a imutabilidade importa: tupla é hashável

Dicionário e conjunto exigem que a chave seja **hashável** — e uma lista não é
(porque ela muda; se mudasse depois de virar chave, a tabela hash quebraria).
Uma tupla é hashável, então serve de chave onde uma lista não serviria:

```python
vendas_por_uf_e_categoria = {}
vendas_por_uf_e_categoria[("SP", "Moda")] = 1500.0   # a chave é uma tupla
```

## Exercícios deste módulo

8 exercícios, nível 1 a 4.

| id | título | nível |
|---|---|---|
| `A10-001` | Criar e indexar uma tupla | ●○○○○ |
| `A10-002` | Desempacotar dois valores | ●○○○○ |
| `A10-003` | Tupla não muda — cria outra | ●●○○○ |
| `A10-004` | Trocar dois itens de uma lista | ●●○○○ |
| `A10-005` | Só o que interessa | ●●○○○ |
| `A10-006` | O primeiro e o resto | ●●●○○ |
| `A10-007` | O resto e o último | ●●●○○ |
| `A10-008` | Tupla como chave | ●●●●○ |

Comece com `curso proximo`.
