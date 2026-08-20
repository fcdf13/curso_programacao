# Módulo C1 — SELECT

> Escolher colunas, filtrar linhas, ordenar e limitar. O arroz com feijão.

## A consulta mínima

```sql
SELECT nome, uf
FROM clientes
WHERE uf = 'SP'
ORDER BY nome
LIMIT 10;
```

Você escreve nessa ordem, mas o banco **executa** em outra: primeiro `FROM`,
depois `WHERE`, depois `SELECT`, depois `ORDER BY` e por último `LIMIT`. Saber
disso explica por que um apelido criado no `SELECT` não pode ser usado no `WHERE`.

### Detalhes que economizam tempo

- Texto vai entre **aspas simples**: `'SP'`. Aspas duplas em SQL identificam
  colunas, não texto.
- `=` compara (em SQL não existe `==`).
- `SELECT *` traz todas as colunas. Serve para explorar; em consulta que vai
  para produção, liste o que você precisa.
- `DISTINCT` remove linhas repetidas do resultado: `SELECT DISTINCT uf FROM clientes`.
- `ORDER BY coluna DESC` inverte a ordem.
- Apelidos com `AS`: `SELECT preco AS preco_atual`.
- Todo comando termina com ponto e vírgula.

### O motor deste curso

Os exercícios rodam em **DuckDB**, que fala um SQL analítico praticamente igual
ao do PostgreSQL. Onde houver diferença relevante de dialeto, o enunciado avisa.

As tabelas disponíveis são `clientes`, `produtos`, `pedidos`, `itens_pedido`,
`pagamentos`, `eventos_web` e `estoque_diario` — as mesmas do Bloco B.
Para ver as colunas de qualquer uma: `DESCRIBE clientes;`

## Exercícios deste módulo

2 exercícios, nível 1 a 2.

| id | título | nível |
|---|---|---|
| `C01-001` | Clientes de São Paulo | ●○○○○ |
| `C01-002` | Os cinco produtos mais caros | ●●○○○ |

Comece com `curso proximo`.
