# Módulo A4 — Condicionais

> Fazer o programa escolher: if, elif, else e os operadores lógicos.

## Perguntar antes de agir

```python
if valor > 100:
    frete = 0
elif valor > 50:
    frete = 9.90
else:
    frete = 19.90
```

Três regras que resolvem quase todos os erros de iniciante:

1. Os dois-pontos no fim da linha do `if` são obrigatórios.
2. O que está **indentado** embaixo do `if` só roda se a condição for verdadeira.
3. Os `elif` só são testados se os anteriores deram falso — o primeiro que
   bater vence, e o resto é ignorado.

### `=` não é `==`

`=` **atribui** um valor. `==` **compara**. Trocar os dois é erro de sintaxe
dentro de um `if`, então o Python te avisa — mas o susto é garantido.

### Comparações

| operador | significa |
|---|---|
| `==` `!=` | igual, diferente |
| `<` `<=` `>` `>=` | menor, menor ou igual, maior, maior ou igual |

Toda comparação produz `True` ou `False`. Isso significa que você pode
**devolver a comparação direto**, sem `if`:

```python
def e_par(n):
    if n % 2 == 0:      # jeito longo
        return True
    else:
        return False

def e_par(n):
    return n % 2 == 0   # mesma coisa, melhor
```

### Combinar condições

```python
idade >= 18 and tem_cadastro       # as duas precisam ser verdadeiras
uf == "SP" or uf == "RJ"           # basta uma
not cancelado                      # inverte
```

Python também aceita a comparação encadeada, que quase nenhuma outra linguagem tem:

```python
0 <= nota <= 10        # em vez de: nota >= 0 and nota <= 10
```

### `in` funciona com listas

```python
uf in ["SP", "RJ", "MG"]     # muito melhor do que três or seguidos
```

## Exercícios deste módulo

12 exercícios, nível 1 a 3.

| id | título | nível |
|---|---|---|
| `A04-001` | O maior dos dois | ●○○○○ |
| `A04-002` | Aprovado ou reprovado | ●○○○○ |
| `A04-003` | Conceito por faixa | ●●○○○ |
| `A04-004` | As duas condições | ●●○○○ |
| `A04-005` | Pedido em aberto | ●●○○○ |
| `A04-006` | Dentro da faixa | ●●○○○ |
| `A04-007` | Frete por região | ●●○○○ |
| `A04-008` | Faixa etária | ●●○○○ |
| `A04-009` | Desconto progressivo | ●●●○○ |
| `A04-010` | Ano bissexto | ●●●○○ |
| `A04-011` | Que triângulo é esse | ●●●○○ |
| `A04-012` | Prazo de entrega | ●●●○○ |

Comece com `curso proximo`.
