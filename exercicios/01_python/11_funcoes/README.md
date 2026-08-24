# Módulo A11 — Funções

> Parâmetros opcionais, quantidade variável de argumentos, escopo, e função como valor.

## Parâmetro com valor padrão

```python
def saudar(nome, saudacao="Olá"):
    return f"{saudacao}, {nome}!"

saudar("Ana")                # "Olá, Ana!"           — usa o padrão
saudar("Ana", "Bem-vindo")   # "Bem-vindo, Ana!"     — troca o padrão
saudar("Ana", saudacao="Oi") # "Oi, Ana!"            — por nome, mesmo efeito
```

Um parâmetro com `=valor` na assinatura vira opcional: quem chama a função
pode simplesmente não passar aquele argumento.

**A armadilha:** o valor padrão é calculado **uma vez só**, quando a função é
definida — não a cada chamada. Isso é inofensivo com números e strings, mas
vira bug com listas e dicionários:

```python
def adicionar(item, historico=[]):   # NUNCA faça isso
    historico.append(item)
    return historico

adicionar("Fone")   # ["Fone"]
adicionar("Capa")   # ["Fone", "Capa"]  — surpresa: a MESMA lista de antes!
```

O jeito seguro é usar `None` como sentinela e criar a lista de dentro:

```python
def adicionar(item, historico=None):
    if historico is None:
        historico = []
    historico.append(item)
    return historico
```

### `*args`: uma quantidade qualquer de argumentos posicionais

```python
def somar(*valores):
    return sum(valores)

somar(1, 2, 3)   # 6      — valores = (1, 2, 3)
somar()          # 0      — valores = ()
```

Dentro da função, `valores` é uma tupla comum. `*args` pode vir depois de
parâmetros fixos: `def formatar(titulo, *itens)`.

### `**kwargs`: uma quantidade qualquer de argumentos nomeados

```python
def descrever(**caracteristicas):
    return caracteristicas

descrever(cor="azul", tamanho="M")   # {"cor": "azul", "tamanho": "M"}
```

`**kwargs` junta os nomeados "soltos" (que não bateram com nenhum parâmetro
declarado) num dicionário. A ordem na assinatura é sempre: fixos, depois
`*args`, depois `**kwargs`.

### Argumentos somente nomeados

Um `*` sozinho na assinatura marca o fim dos posicionais — tudo o que vem
depois só pode ser passado por nome:

```python
def aplicar_desconto(preco, *, desconto=0.0):
    return preco * (1 - desconto)

aplicar_desconto(100.0, desconto=0.1)   # 90.0 — ok
aplicar_desconto(100.0, 0.1)            # TypeError — desconto tem que ser nomeado
```

## Escopo: onde uma variável existe

Uma variável criada **dentro** de uma função só existe lá dentro. Uma função
**lê** uma variável global sem precisar de nada especial:

```python
TAXA = 0.05

def com_taxa(preco):
    return preco * (1 + TAXA)   # lê TAXA de fora, sem problema
```

Mas **atribuir** a uma variável dentro da função cria, por padrão, uma
variável **local** nova — mesmo que o nome já exista lá fora. Para mudar de
verdade a global, é preciso avisar com `global`:

```python
total = 0

def registrar(valor):
    global total
    total += valor
    return total
```

Sem o `global`, `total += valor` estouraria `UnboundLocalError` — o Python
veria a atribuição e trataria `total` como local, uma local que ainda não tem
valor antes do `+=`.

## Função como valor

Uma função é um valor como outro qualquer: pode ser guardada numa variável,
passada como argumento, devolvida por outra função.

```python
def dobro(x):
    return x * 2

operacao = dobro        # sem (), é a função em si — não uma chamada
operacao(5)              # 10

def aplicar(funcao, valor):
    return funcao(valor)

aplicar(dobro, 5)        # 10 — dobro passou de argumento
```

## Função que devolve função (clausura)

Uma função pode ser definida dentro de outra e devolvida no lugar de um
valor comum. A função de dentro **lembra** das variáveis de fora, mesmo
depois que a de fora já terminou — isso é uma **clausura** (*closure*):

```python
def criar_multiplicador(fator):
    def multiplicar(x):
        return x * fator      # lembra de "fator", da função de fora
    return multiplicar

vezes3 = criar_multiplicador(3)
vezes3(10)   # 30
```

Se a função de dentro precisa **mudar** (não só ler) uma variável da de
fora, usa `nonlocal` — o equivalente ao `global`, mas para escopo de função:

```python
def criar_contador():
    total = 0
    def contador():
        nonlocal total
        total += 1
        return total
    return contador
```

## Exercícios deste módulo

16 exercícios, nível 1 a 5.

| id | título | nível |
|---|---|---|
| `A11-001` | Parâmetro com valor padrão | ●○○○○ |
| `A11-002` | Vários padrões, chamados por nome | ●○○○○ |
| `A11-003` | *args: uma quantidade qualquer de argumentos | ●●○○○ |
| `A11-004` | *args ao lado de um parâmetro fixo | ●●○○○ |
| `A11-005` | **kwargs: os argumentos nomeados soltos | ●●○○○ |
| `A11-006` | Combinar *args e **kwargs | ●●●○○ |
| `A11-007` | Argumentos somente nomeados | ●●●○○ |
| `A11-008` | A armadilha do argumento padrão mutável | ●●●○○ |
| `A11-009` | Escopo: ler uma variável global | ●●○○○ |
| `A11-010` | Escopo: modificar uma variável global | ●●●○○ |
| `A11-011` | Função como valor: guardar e passar adiante | ●●●○○ |
| `A11-012` | Função como argumento: transformar uma lista | ●●●○○ |
| `A11-013` | Despacho por dicionário de funções | ●●●●○ |
| `A11-014` | Função que devolve função | ●●●●○ |
| `A11-015` | Contador com nonlocal | ●●●●○ |
| `A11-016` | Desafio: fábrica de validador de desconto | ●●●●● |

Comece com `curso proximo`.
