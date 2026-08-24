# Módulo A8 — Dicionários e conjuntos

> As duas estruturas que resolvem 'isso já apareceu?' e 'quanto disso existe?'.

## Dicionário: pares de chave e valor

```python
precos = {"Fone": 99.9, "Capa": 25.0}
precos["Fone"]          # 99.9  — acesso direto, KeyError se a chave não existir
precos.get("Mouse")     # None  — não estoura, só devolve None
precos.get("Mouse", 0)  # 0     — um padrão seu, em vez de None
```

`in` num dicionário testa as **chaves**, nunca os valores:

```python
"Fone" in precos    # True  — é uma chave
99.9 in precos      # False — é um valor, não uma chave
```

### Mudar o dicionário

```python
precos["Mouse"] = 45.0   # cria se não existir, atualiza se já existir
del precos["Capa"]       # remove — estoura KeyError se a chave não existir
precos.pop("Capa", None) # remove sem estourar; devolve o valor removido (ou o padrão)
```

### Percorrer

```python
list(precos.keys())     # só as chaves
list(precos.values())   # só os valores
list(precos.items())    # pares (chave, valor), como tuplas

for nome, preco in precos.items():
    ...                  # desempacota o par a cada volta, igual ao zip
```

### O padrão mais usado de todos: contagem

```python
contagem = {}
for palavra in texto.split():
    contagem[palavra] = contagem.get(palavra, 0) + 1
```

`.get(chave, 0)` é o que permite somar 1 sem antes checar se a chave existe.

## Conjunto (set): valores únicos, sem ordem

```python
vistos = {1, 2, 2, 3}    # {1, 2, 3} — repetição desaparece na criação
vistos = set([1, 2, 2])  # o mesmo, a partir de uma lista

vistos.add(4)            # acrescenta
vistos.discard(1)         # remove, sem estourar se não existir
3 in vistos               # True — busca em set é muito mais rápida que em lista
```

### As quatro operações de conjunto

```python
a = {1, 2, 3}
b = {2, 3, 4}

a | b   # união: {1, 2, 3, 4}
a & b   # interseção: {2, 3}
a - b   # diferença: {1}           — o que está em a e não em b
a ^ b   # diferença simétrica: {1, 4} — o que está em só um dos dois
```

Cada operação também tem uma versão-função: `a.union(b)`, `a.intersection(b)`,
`a.difference(b)`.

Dicionário e conjunto compartilham a mesma vantagem por baixo do capô: os dois usam
**tabela hash**, o que torna `in`, inserir e remover extremamente rápidos — o
módulo A9 mostra exatamente o quanto isso importa na prática.

## Exercícios deste módulo

14 exercícios, nível 1 a 4.

| id | título | nível |
|---|---|---|
| `A08-001` | Montar um dicionário | ●○○○○ |
| `A08-002` | Acessar com risco | ●○○○○ |
| `A08-003` | Acessar sem risco | ●●○○○ |
| `A08-004` | Chave, não valor | ●●○○○ |
| `A08-005` | Criar ou atualizar | ●●○○○ |
| `A08-006` | Remover uma chave | ●●○○○ |
| `A08-007` | Só as chaves, só os valores | ●●○○○ |
| `A08-008` | Pares chave-valor | ●●○○○ |
| `A08-009` | Contagem de ocorrências | ●●●○○ |
| `A08-010` | A chave do maior valor | ●●●○○ |
| `A08-011` | Juntar dois catálogos | ●●●○○ |
| `A08-012` | Inverter um dicionário | ●●●○○ |
| `A08-013` | Sem repetir | ●○○○○ |
| `A08-014` | Clientes de duas campanhas | ●●●●○ |

Comece com `curso proximo`.
