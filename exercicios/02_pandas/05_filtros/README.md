# Módulo B5 — Filtros

> Selecionar linhas por condição: a operação mais frequente de todas.

## A máscara booleana

Uma comparação aplicada a uma coluna devolve uma Series de `True`/`False` —
a **máscara**. Usar a máscara dentro dos colchetes mantém só as linhas `True`.

```python
produtos["preco"] > 100          # Series de booleanos, uma por linha
produtos[produtos["preco"] > 100]  # as linhas em que isso é verdade
```

### Combinar condições: `&`, `|`, `~`

Aqui está a diferença que mais derruba quem vem do Python puro:

| Python puro | Pandas |
|---|---|
| `and` | `&` |
| `or` | `\|` |
| `not` | `~` |

E **cada condição precisa de parênteses**, porque `&` tem precedência maior que
`>`:

```python
produtos[(produtos["preco"] > 100) & (produtos["ativo"])]     # certo
produtos[produtos["preco"] > 100 & produtos["ativo"]]         # erro
```

Se esquecer os parênteses, o Pandas levanta um erro difícil de ler. Se usar `and`
em vez de `&`, ele levanta o famoso *"The truth value of a Series is ambiguous"*.

### Ferramentas que evitam ors encadeados

```python
produtos[produtos["categoria"].isin(["Moda", "Casa"])]
produtos[produtos["preco"].between(50, 100)]
produtos[produtos["nome"].str.contains("Fone")]
produtos[~produtos["ativo"]]
```

### `query`: a mesma coisa, lendo melhor

```python
produtos.query("preco > 100 and ativo")
```

Dentro do `query` valem `and`/`or`/`not` normais e não são precisos colchetes.
Para filtros longos, costuma ser mais legível.

## Exercícios deste módulo

1 exercícios, nível 2 a 2.

| id | título | nível |
|---|---|---|
| `B05-001` | Produtos ativos e caros | ●●○○○ |

Comece com `curso proximo`.
