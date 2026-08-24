# Módulo A9 — Complexidade e Big-O

> Por que a mesma resposta certa pode levar 2 milissegundos ou 2 minutos.

## A pergunta que Big-O responde

Não é "quanto tempo demora" — é **como o tempo cresce quando a entrada cresce**.
Dobrar o tamanho da entrada dobra o tempo? Quadruplica? Não muda quase nada?
Essa taxa de crescimento é o Big-O, e ela é o que decide se o seu código aguenta
1 mil linhas, 1 milhão, ou nenhuma das duas.

| notação | como cresce | exemplo |
|---|---|---|
| O(1) | não cresce | acessar `lista[0]`, ler `dicionario[chave]` |
| O(n) | na mesma proporção da entrada | um `for` que passa pela lista uma vez |
| O(n²) | ao quadrado | um `for` dentro de outro `for`, ambos sobre a entrada |

A conta mental é simples: **conte quantas vezes o corpo do laço mais interno
roda**, em função de `n`. Um laço só, um `for` de tamanho `n`: roda `n` vezes,
O(n). Um laço dentro de outro, os dois de tamanho `n`: o de dentro roda `n`
vezes a cada volta do de fora, que também tem `n` voltas — `n × n`, O(n²).

### A armadilha que aparece o tempo todo

```python
if item in uma_lista:      # percorre a lista inteira até achar (ou não achar)
    ...                     # isso sozinho é O(n)

for item in outra_lista:    # um for de tamanho n...
    if item in uma_lista:   # ...com um "in" de tamanho n dentro
        ...
# O laço inteiro é O(n) × O(n) = O(n²)
```

A correção não muda uma linha de lógica — só a estrutura de dado:

```python
conjunto = set(uma_lista)   # construir o set custa O(n), uma vez só
for item in outra_lista:
    if item in conjunto:    # "in" num set é O(1) em média
        ...
# Agora é O(n) + O(n) = O(n) no total
```

Você já viu essa troca nos módulos A5 e A8 sem o nome "Big-O" — aqui é onde o
nome e o motivo se encontram.

### Outras trocas que valem a pena conhecer

- **Contagem/agrupamento**: um dicionário resolve em O(n) o que comparar todo
  mundo com todo mundo resolveria em O(n²) — é o padrão do A8.
- **Última posição vista**: guardar num dicionário `{valor: posição}` a última
  vez que cada valor apareceu resolve em O(n) perguntas do tipo "isso já
  apareceu há menos de k posições?" — sem comparar cada item com todos os
  anteriores.
- **Somas de intervalo repetidas**: se você vai somar pedaços de uma lista
  várias vezes, some tudo **uma vez** num array de somas acumuladas
  (`prefixo[i] = soma de tudo até i`) e depois cada pergunta vira uma subtração.
- **Fila que só cresce por um lado e sai pelo outro**: `lista.pop(0)` parece
  inocente, mas desloca todo mundo uma posição — é O(n) por chamada.
  `collections.deque` faz a mesma coisa em O(1), porque foi construída para isso.

### Como os testes deste módulo cobram isso

Alguns exercícios trazem duas verificações: uma pequena, conferindo se a
resposta está certa; outra grande, conferindo se a resposta **chega a tempo**.
Se a sua solução for O(n²) onde caberia O(n), o segundo teste falha explicando
quantos segundos ela levou — mesmo com a resposta certa.

## Exercícios deste módulo

9 exercícios, nível 1 a 4.

| id | título | nível |
|---|---|---|
| `A09-001` | Quantas vezes o laço roda | ●○○○○ |
| `A09-002` | Está na lista | ●●○○○ |
| `A09-003` | Está no conjunto | ●●○○○ |
| `A09-004` | Duplicata perto demais | ●●●○○ |
| `A09-005` | Some o intervalo sem repetir a conta | ●●●○○ |
| `A09-006` | Quem comprou nas duas, rápido | ●●●●○ |
| `A09-007` | Sem repetir, na ordem, rápido | ●●●○○ |
| `A09-008` | Duas ofertas que somam ao vale-presente | ●●●●○ |
| `A09-009` | Fila sem gargalo | ●●●●○ |

Comece com `curso proximo`.
