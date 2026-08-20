# Módulo A3 — Strings

> Texto é metade do trabalho com dados: nomes, e-mails, categorias, CEPs.

## Texto é uma sequência

Cada caractere tem uma posição, e a contagem **começa no zero**:

```
 A   u   r   o   r   a
 0   1   2   3   4   5
-6  -5  -4  -3  -2  -1
```

```python
nome = "Aurora"
nome[0]     # 'A'  — o primeiro
nome[-1]    # 'a'  — o último, sem precisar saber o tamanho
len(nome)   # 6
```

### Fatiar: `texto[inicio:fim]`

O `inicio` entra, o `fim` **não** entra. Parece estranho no começo e depois vira
natural — `texto[0:3]` pega exatamente 3 caracteres.

```python
"Aurora"[0:3]    # 'Aur'
"Aurora"[3:]     # 'ora'    — do 3 até o fim
"Aurora"[:3]     # 'Aur'    — do começo até o 3
"Aurora"[::-1]   # 'aroruA' — o passo -1 percorre de trás para frente
```

### Métodos que você vai usar todo dia

```python
"  ana  ".strip()          # 'ana'      — tira espaços das pontas
"ana".upper()              # 'ANA'
"ANA".lower()              # 'ana'
"ana souza".title()        # 'Ana Souza'
"sp-01".replace("-", "/")  # 'sp/01'
"a,b,c".split(",")         # ['a', 'b', 'c']
"-".join(["a", "b"])       # 'a-b'
"aurora".count("r")        # 2
"aurora".startswith("au")  # True
"ro" in "aurora"           # True
```

### Strings não mudam

`nome.upper()` **devolve** um texto novo; `nome` continua igual. Se você quer
guardar a mudança, precisa atribuir:

```python
nome = nome.upper()    # sem isso, nada muda
```

### Formatar dentro da f-string

```python
preco = 1234.5
f"R$ {preco:.2f}"     # 'R$ 1234.50'  — duas casas decimais
f"{0.256:.1%}"        # '25.6%'
```

## Exercícios deste módulo

14 exercícios, nível 1 a 3.

| id | título | nível |
|---|---|---|
| `A03-001` | Tamanho do texto | ●○○○○ |
| `A03-002` | Primeira e última letra | ●●○○○ |
| `A03-003` | Um pedaço do texto | ●●○○○ |
| `A03-004` | Caixa alta e caixa baixa | ●○○○○ |
| `A03-005` | Tirar os espaços das pontas | ●●○○○ |
| `A03-006` | Trocar um pedaço | ●●○○○ |
| `A03-007` | Quebrar a frase em palavras | ●●○○○ |
| `A03-008` | Juntar palavras | ●●○○○ |
| `A03-009` | Está aí dentro? | ●○○○○ |
| `A03-010` | Começa com, termina com | ●●○○○ |
| `A03-011` | Formatar dinheiro | ●●○○○ |
| `A03-012` | Ao contrário | ●●○○○ |
| `A03-013` | Contar quantas vezes | ●●○○○ |
| `A03-014` | Iniciais do nome | ●●●○○ |

Comece com `curso proximo`.
