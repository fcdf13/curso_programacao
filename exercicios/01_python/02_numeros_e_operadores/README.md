# Módulo A2 — Números e operadores

> Contas que aparecem em todo relatório: porcentagem, arredondamento, resto.

## Os operadores

| operador | faz | exemplo |
|---|---|---|
| `+` `-` `*` | soma, subtrai, multiplica | `3 * 4` → `12` |
| `/` | divide — **sempre devolve float** | `10 / 2` → `5.0` |
| `//` | divide e joga fora a parte quebrada | `7 // 2` → `3` |
| `%` | o **resto** da divisão | `7 % 2` → `1` |
| `**` | eleva à potência | `2 ** 10` → `1024` |

### O resto (`%`) vale mais do que parece

`7 % 2` é 1 porque 7 dividido por 2 dá 3 e sobra 1. Isso resolve uma família inteira
de problemas:

```python
numero % 2 == 0      # é par?
ano % 4 == 0         # divisível por 4?
segundos % 60        # quantos segundos sobram depois dos minutos inteiros
```

### A ordem importa

Python segue a matemática: `**` primeiro, depois `*` `/` `//` `%`, e por último `+` `-`.

```python
2 + 3 * 4        # 14, não 20
(2 + 3) * 4      # 20
```

Na dúvida, ponha parênteses. Eles custam nada e evitam o bug mais chato de achar.

### Arredondar

`round(valor, casas)` arredonda: `round(49.876, 2)` → `49.88`.
Com uma casa só, `round(2.5)` dá `2` — Python arredonda o meio para o par mais próximo.
É pouco intuitivo, mas raramente atrapalha.

### Funções que já vêm prontas

```python
abs(-8)          # 8    — distância até o zero
min(3, 9, 1)     # 1
max(3, 9, 1)     # 9
divmod(125, 60)  # (2, 5) — o resultado inteiro e o resto, de uma vez
```

## Exercícios deste módulo

10 exercícios, nível 1 a 3.

| id | título | nível |
|---|---|---|
| `A02-001` | Área do retângulo | ●○○○○ |
| `A02-002` | Par ou ímpar | ●●○○○ |
| `A02-003` | As duas divisões | ●●○○○ |
| `A02-004` | Elevar ao quadrado | ●○○○○ |
| `A02-005` | Arredondar o preço | ●●○○○ |
| `A02-006` | Minutos e segundos | ●●●○○ |
| `A02-007` | Quanto por cento | ●●○○○ |
| `A02-008` | Maior, menor e diferença | ●●○○○ |
| `A02-009` | Média ponderada | ●●●○○ |
| `A02-010` | Juros compostos | ●●●○○ |

Comece com `curso proximo`.
