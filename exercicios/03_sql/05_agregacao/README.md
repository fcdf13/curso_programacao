# Módulo C5 — Agregação

> Espremer muitas linhas em um número só: contar, somar, tirar média.

## Funções de agregação

Elas recebem uma coluna inteira e devolvem **uma linha**:

```sql
SELECT
    COUNT(*)      AS quantas_linhas,
    SUM(preco)    AS soma,
    AVG(preco)    AS media,
    MIN(preco)    AS menor,
    MAX(preco)    AS maior
FROM produtos;
```

### `COUNT(*)` não é `COUNT(coluna)`

| forma | conta |
|---|---|
| `COUNT(*)` | todas as linhas |
| `COUNT(coluna)` | as linhas em que a coluna **não é NULL** |
| `COUNT(DISTINCT coluna)` | os valores diferentes, sem repetição |

A diferença entre as duas primeiras é uma das perguntas mais comuns em
entrevista — e uma das causas mais comuns de relatório errado.

### NULL some das contas

`AVG`, `SUM`, `MIN` e `MAX` **ignoram** NULL. Isso é bom quase sempre, mas
significa que a média de `[10, NULL, 20]` é 15, e não 10. Se você queria tratar
NULL como zero, precisa dizer isso: `AVG(COALESCE(valor, 0))`.

### Sem `GROUP BY`, o resultado tem uma linha só

A tabela inteira vira um resumo. Para ter um resumo **por categoria**, entra o
`GROUP BY` — que é o assunto do próximo módulo.

## Exercícios deste módulo

1 exercícios, nível 2 a 2.

| id | título | nível |
|---|---|---|
| `C05-001` | Resumo do catálogo | ●●○○○ |

Comece com `curso proximo`.
