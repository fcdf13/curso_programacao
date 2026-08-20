# Módulo B1 — Series e DataFrame

> As duas estruturas do Pandas: a coluna e a tabela.

## Series é uma coluna. DataFrame é uma tabela.

```python
import pandas as pd

precos = pd.Series([49.9, 12.0, 230.5])          # uma coluna
produtos = pd.DataFrame({                         # uma tabela
    "nome": ["Fone", "Capa", "Notebook"],
    "preco": [49.9, 12.0, 230.5],
})
```

Um DataFrame é um conjunto de Series que compartilham o mesmo **índice** — os
rótulos das linhas, que por padrão são 0, 1, 2, ...

### Por que isso muda tudo

No Bloco A, somar uma lista de preços exigia um laço. Aqui:

```python
produtos["preco"].sum()
```

A operação vale para a coluna inteira de uma vez. Isso se chama **vetorização**,
e é a razão de o Pandas dar conta de milhões de linhas: o laço existe, mas roda
em C, não em Python.

### O primeiro olhar em qualquer tabela

```python
df.shape        # (linhas, colunas)
df.columns      # os nomes das colunas
df.dtypes       # o tipo de cada coluna
df.head()       # as 5 primeiras linhas
df.info()       # resumo: tipos, nulos, memória
df.describe()   # estatísticas das colunas numéricas
```

Antes de qualquer análise, `shape` e `dtypes`. Metade dos bugs de Pandas é uma
coluna que você achava numérica e o Pandas leu como texto.

### O dataset do curso

A Loja Aurora tem sete tabelas limpas — `clientes`, `produtos`, `pedidos`,
`itens_pedido`, `pagamentos`, `eventos_web`, `estoque_diario` — e duas sujas de
propósito, `clientes_bruto` e `avaliacoes_bruto`, para os módulos de limpeza.
Elas são as mesmas que você vai consultar em SQL no Bloco C.

## Exercícios deste módulo

2 exercícios, nível 1 a 2.

| id | título | nível |
|---|---|---|
| `B01-001` | Montar um DataFrame | ●○○○○ |
| `B01-002` | Cartão de visita da tabela | ●●○○○ |

Comece com `curso proximo`.
