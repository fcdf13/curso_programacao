"""Bloco A, módulo 11: funções."""

from autoria.modelo import Exercicio as Ex
from autoria.modelo import Modulo

A11 = Modulo(
    id="A11",
    titulo="Módulo A11 — Funções",
    resumo="Parâmetros opcionais, quantidade variável de argumentos, escopo, e função como valor.",
    teoria="""
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
""",
    exercicios=[
        Ex(
            id="A11-001", titulo="Parâmetro com valor padrão", nivel=1, tempo_min=4,
            tags=["funcoes", "parametro-padrao"],
            enunciado="""
            Escreva uma saudação para um nome, com uma palavra de saudação
            que tem um valor padrão.

            Exemplos:

                resolver("Ana")               ->  "Olá, Ana!"
                resolver("Ana", "Bem-vindo")  ->  "Bem-vindo, Ana!"

            Um parâmetro pode ter um valor padrão (`saudacao="Olá"`) — quem
            chama a função pode simplesmente não passar aquele argumento.
            """,
            assinatura='def resolver(nome: str, saudacao: str = "Olá") -> str:',
            dicas=[
                'Um parâmetro pode ter um valor padrão: def f(x, y="algo").',
                "Quando quem chama não passa saudacao, o valor padrão entra no lugar.",
                'return f"{saudacao}, {nome}!"',
            ],
            solucao='    return f"{saudacao}, {nome}!"',
            testes="""
def teste_saudacao_padrao():
    verificar(ex.resolver("Ana"), "Olá, Ana!")


def teste_saudacao_customizada():
    verificar(ex.resolver("Ana", "Bem-vindo"), "Bem-vindo, Ana!")


def teste_saudacao_por_nome():
    verificar(ex.resolver("Bruno", saudacao="E aí"), "E aí, Bruno!")
""",
        ),
        Ex(
            id="A11-002", titulo="Vários padrões, chamados por nome", nivel=1, tempo_min=5,
            tags=["funcoes", "parametro-padrao", "argumento-nomeado"],
            requer=["A11-001"],
            enunciado="""
            Descreva um item do carrinho: produto, quantidade (padrão `1`) e
            desconto (padrão `0`, sem desconto).

            Exemplos:

                resolver("Fone")                  ->  "1x Fone"
                resolver("Fone", 3)                ->  "3x Fone"
                resolver("Fone", desconto=0.1)     ->  "1x Fone (10% de desconto)"
                resolver("Fone", 2, 0.2)           ->  "2x Fone (20% de desconto)"

            Repare no terceiro exemplo: para pular `quantidade` e só mudar
            `desconto`, quem chama passa `desconto=0.1` por nome — não dá
            para pular um argumento no meio só na base da posição.
            """,
            assinatura="def resolver(produto: str, quantidade: int = 1, desconto: float = 0.0) -> str:",
            dicas=[
                'Sem desconto, o texto é só "{quantidade}x {produto}".',
                'Com desconto (diferente de 0), acrescente " ({X}% de desconto)", com X = desconto*100.',
                'if desconto:\n        return f"{quantidade}x {produto} ({int(desconto*100)}% de desconto)"\n    return f"{quantidade}x {produto}"',
            ],
            solucao="""
            if desconto:
                return f"{quantidade}x {produto} ({int(desconto*100)}% de desconto)"
            return f"{quantidade}x {produto}"
            """,
            testes="""
def teste_so_produto():
    verificar(ex.resolver("Fone"), "1x Fone")


def teste_com_quantidade():
    verificar(ex.resolver("Fone", 3), "3x Fone")


def teste_pulando_quantidade_por_nome():
    verificar(ex.resolver("Fone", desconto=0.1), "1x Fone (10% de desconto)")


def teste_todos_os_argumentos():
    verificar(ex.resolver("Fone", 2, 0.2), "2x Fone (20% de desconto)")
""",
        ),
        Ex(
            id="A11-003", titulo="*args: uma quantidade qualquer de argumentos", nivel=2, tempo_min=6,
            tags=["funcoes", "args", "variadico"],
            enunciado="""
            Some uma quantidade qualquer de números.

            Exemplos:

                resolver(10, 20, 30)  ->  60
                resolver(5)            ->  5
                resolver()              ->  0

            `*valores` na assinatura junta qualquer quantidade de argumentos
            posicionais numa tupla — de zero a quantos quem chama quiser
            passar.
            """,
            assinatura="def resolver(*valores) -> float:",
            dicas=[
                "*valores junta qualquer quantidade de argumentos posicionais numa tupla.",
                "Dentro da função, valores já é uma tupla comum — soma dá para fazer com sum().",
                "return sum(valores)",
            ],
            solucao="    return sum(valores)",
            testes="""
def teste_tres_valores():
    verificar(ex.resolver(10, 20, 30), 60)


def teste_um_valor():
    verificar(ex.resolver(5), 5)


def teste_nenhum_valor():
    verificar(ex.resolver(), 0)
""",
        ),
        Ex(
            id="A11-004", titulo="*args ao lado de um parâmetro fixo", nivel=2, tempo_min=7,
            tags=["funcoes", "args", "variadico"],
            requer=["A11-003"],
            enunciado="""
            Aplique uma operação (`"soma"` ou `"produto"`) sobre uma
            quantidade qualquer de números.

            Exemplos:

                resolver("soma", 1, 2, 3)      ->  6
                resolver("produto", 2, 3, 4)   ->  24
                resolver("produto")             ->  1

            `*args` pode vir depois de um parâmetro fixo — a assinatura é
            `def resolver(operacao, *numeros)`.
            """,
            assinatura="def resolver(operacao: str, *numeros) -> float:",
            dicas=[
                "Parâmetros fixos vêm antes do *args na assinatura: def resolver(operacao, *numeros).",
                "numeros continua sendo uma tupla comum — some com sum(), multiplique com um laço.",
                'if operacao == "soma":\n        return sum(numeros)\n    total = 1\n    for n in numeros:\n        total *= n\n    return total',
            ],
            solucao="""
            if operacao == "soma":
                return sum(numeros)
            total = 1
            for n in numeros:
                total *= n
            return total
            """,
            nota_da_solucao="Multiplicação não tem um sum() pronto — o acumulador começa em 1 (o neutro da multiplicação), não em 0.",
            testes="""
def teste_soma():
    verificar(ex.resolver("soma", 1, 2, 3), 6)


def teste_produto():
    verificar(ex.resolver("produto", 2, 3, 4), 24)


def teste_produto_sem_numeros():
    verificar(ex.resolver("produto"), 1)


def teste_soma_sem_numeros():
    verificar(ex.resolver("soma"), 0)
""",
        ),
        Ex(
            id="A11-005", titulo="**kwargs: os argumentos nomeados soltos", nivel=2, tempo_min=6,
            tags=["funcoes", "kwargs", "variadico"],
            enunciado="""
            Reúna características de um produto, passadas como argumentos
            nomeados, num dicionário.

            Exemplos:

                resolver(cor="azul", tamanho="M")  ->  {"cor": "azul", "tamanho": "M"}
                resolver()                          ->  {}

            `**caracteristicas` na assinatura junta qualquer quantidade de
            argumentos nomeados num dicionário.
            """,
            assinatura="def resolver(**caracteristicas) -> dict:",
            dicas=[
                "**caracteristicas junta os argumentos nomeados soltos num dicionário.",
                "Dentro da função, caracteristicas já é um dict comum — não precisa montar nada.",
                "return caracteristicas",
            ],
            solucao="    return caracteristicas",
            testes="""
def teste_duas_caracteristicas():
    verificar(ex.resolver(cor="azul", tamanho="M"), {"cor": "azul", "tamanho": "M"})


def teste_sem_nenhuma():
    verificar(ex.resolver(), {})


def teste_uma_caracteristica():
    verificar(ex.resolver(cor="preto"), {"cor": "preto"})
""",
        ),
        Ex(
            id="A11-006", titulo="Combinar *args e **kwargs", nivel=3, tempo_min=8,
            tags=["funcoes", "args", "kwargs", "variadico"],
            requer=["A11-004", "A11-005"],
            enunciado="""
            Monte um pedido a partir de um cliente, uma quantidade qualquer
            de itens e características opcionais.

            Exemplos:

                resolver("Ana", "Fone", "Capa", desconto=0.1)
                ->  {"cliente": "Ana", "itens": ["Fone", "Capa"], "desconto": 0.1}

                resolver("Bruno")
                ->  {"cliente": "Bruno", "itens": []}

            A ordem na assinatura é sempre: parâmetros fixos, depois
            `*args`, depois `**kwargs` — `def resolver(cliente, *itens, **opcionais)`.
            """,
            assinatura="def resolver(cliente: str, *itens, **opcionais) -> dict:",
            dicas=[
                "A assinatura é def resolver(cliente, *itens, **opcionais) — fixo,\ndepois *args, depois **kwargs.",
                "list(itens) transforma a tupla em lista; opcionais já é um dict\nque dá para juntar com .update().",
                'pedido = {"cliente": cliente, "itens": list(itens)}\n    pedido.update(opcionais)\n    return pedido',
            ],
            solucao="""
            pedido = {"cliente": cliente, "itens": list(itens)}
            pedido.update(opcionais)
            return pedido
            """,
            testes="""
def teste_com_itens_e_opcional():
    verificar(
        ex.resolver("Ana", "Fone", "Capa", desconto=0.1),
        {"cliente": "Ana", "itens": ["Fone", "Capa"], "desconto": 0.1},
    )


def teste_sem_itens_nem_opcionais():
    verificar(ex.resolver("Bruno"), {"cliente": "Bruno", "itens": []})


def teste_multiplos_opcionais():
    verificar(
        ex.resolver("Carla", "Mouse", cor="preto", garantia=True),
        {"cliente": "Carla", "itens": ["Mouse"], "cor": "preto", "garantia": True},
    )
""",
        ),
        Ex(
            id="A11-007", titulo="Argumentos somente nomeados", nivel=3, tempo_min=7,
            tags=["funcoes", "argumento-nomeado", "asterisco"],
            requer=["A11-002"],
            enunciado="""
            Aplique um desconto a um preço. O desconto só pode ser passado
            por nome — nunca só pela posição.

            Exemplos:

                resolver(100.0)                    ->  100.0
                resolver(100.0, desconto=0.1)      ->  90.0

            Um `*` sozinho na assinatura marca o fim dos argumentos
            posicionais: tudo o que vem depois só pode ser passado por nome.
            `def resolver(preco, *, desconto=0.0)` impede `resolver(100.0, 0.1)`
            — teria que ser `resolver(100.0, desconto=0.1)`.
            """,
            assinatura="def resolver(preco: float, *, desconto: float = 0.0) -> float:",
            dicas=[
                "Um * sozinho na assinatura separa os posicionais dos que só podem ser nomeados.",
                "def resolver(preco, *, desconto=0.0) força desconto a vir sempre com nome.",
                "return preco * (1 - desconto)",
            ],
            solucao="    return preco * (1 - desconto)",
            testes="""
def teste_sem_desconto():
    verificar(ex.resolver(100.0), 100.0)


def teste_com_desconto():
    verificar(ex.resolver(100.0, desconto=0.1), 90.0)


def teste_desconto_total():
    verificar(ex.resolver(50.0, desconto=1.0), 0.0)
""",
        ),
        Ex(
            id="A11-008", titulo="A armadilha do argumento padrão mutável", nivel=3, tempo_min=9,
            tags=["funcoes", "parametro-padrao", "armadilha", "mutabilidade"],
            requer=["A11-001"],
            enunciado="""
            Adicione um item a um histórico, devolvendo o histórico
            atualizado. Quando nenhum histórico é passado, comece um novo —
            vazio.

            Exemplos:

                resolver("Fone")                  ->  ["Fone"]
                resolver("Capa", ["Fone"])         ->  ["Fone", "Capa"]

            **Não** escreva `historico=[]` na assinatura — um valor padrão
            mutável (uma lista, um dict) é criado **uma vez só**, na hora
            que a função é definida, e essa mesma lista seria reaproveitada
            em toda chamada onde ninguém passa `historico`. Use `None` como
            sentinela e crie a lista de dentro, quando ela não vier.
            """,
            assinatura="def resolver(item: str, historico: list | None = None) -> list:",
            dicas=[
                "historico=[] pareceria funcionar, mas a mesma lista seria reaproveitada\nem toda chamada sem historico — chame a função duas vezes seguidas para ver o bug.",
                "Use historico: list | None = None, e crie a lista de dentro quando vier None.",
                "if historico is None:\n        historico = []\n    historico.append(item)\n    return historico",
            ],
            solucao="""
            if historico is None:
                historico = []
            historico.append(item)
            return historico
            """,
            nota_da_solucao="historico=[] direto na assinatura compartilharia a MESMA lista entre chamadas diferentes que não passam historico — o bug clássico do argumento padrão mutável. None é o sentinela seguro.",
            testes="""
def teste_uma_chamada():
    verificar(ex.resolver("Fone"), ["Fone"])


def teste_historico_explicito_acumula():
    verificar(ex.resolver("Capa", ["Fone"]), ["Fone", "Capa"])


def teste_duas_chamadas_sem_historico_nao_compartilham():
    ex.resolver("Fone")
    segunda = ex.resolver("Capa")
    verificar(segunda, ["Capa"])
""",
        ),
        Ex(
            id="A11-009", titulo="Escopo: ler uma variável global", nivel=2, tempo_min=6,
            tags=["funcoes", "escopo", "global"],
            preambulo="TAXA_PADRAO = 0.05",
            enunciado="""
            Aplique a taxa padrão do módulo sobre um preço.

            Exemplo:

                resolver(100.0)  ->  105.0

            `TAXA_PADRAO` está definida no topo deste arquivo. Uma função
            **lê** uma variável global sem precisar de nenhuma palavra
            especial — só usar.
            """,
            assinatura="def resolver(preco: float) -> float:",
            dicas=[
                "Uma função lê variáveis globais sem nada de especial — só usar o nome.",
                "TAXA_PADRAO já existe no arquivo, acima da função resolver.",
                "return preco * (1 + TAXA_PADRAO)",
            ],
            solucao="    return preco * (1 + TAXA_PADRAO)",
            testes="""
def teste_aplica_a_taxa():
    verificar(ex.resolver(100.0), 105.0)


def teste_preco_zero():
    verificar(ex.resolver(0.0), 0.0)
""",
        ),
        Ex(
            id="A11-010", titulo="Escopo: modificar uma variável global", nivel=3, tempo_min=8,
            tags=["funcoes", "escopo", "global"],
            requer=["A11-009"],
            preambulo="total_arrecadado = 0.0",
            enunciado="""
            Registre um valor arrecadado, somando-o ao total do módulo, e
            devolva o novo total.

            Exemplo (chamadas em sequência):

                resolver(100.0)  ->  100.0
                resolver(50.0)   ->  150.0

            Atribuir a uma variável dentro de uma função cria, por padrão,
            uma variável **local** nova — mesmo que o nome já exista lá
            fora. Para mudar de verdade a global `total_arrecadado`, é
            preciso avisar com `global total_arrecadado` antes de usá-la.
            """,
            assinatura="def resolver(valor: float) -> float:",
            dicas=[
                "Sem avisar nada, total_arrecadado += valor criaria uma variável local\nnova — e estouraria UnboundLocalError, porque ela ainda não tem valor antes do +=.",
                "global total_arrecadado, escrito antes de usar a variável, avisa que é\na de fora que deve mudar.",
                "global total_arrecadado\n    total_arrecadado += valor\n    return total_arrecadado",
            ],
            solucao="""
            global total_arrecadado
            total_arrecadado += valor
            return total_arrecadado
            """,
            nota_da_solucao="global precisa vir antes de qualquer uso da variável na função — é um aviso ao Python de que aquele nome não é local.",
            testes="""
def teste_acumula_em_sequencia():
    verificar(ex.resolver(100.0), 100.0)
    verificar(ex.resolver(50.0), 150.0)
    verificar(ex.resolver(25.0), 175.0)


def teste_soma_exatamente_o_valor_passado():
    anterior = ex.resolver(0.0)
    verificar(ex.resolver(10.0), anterior + 10.0)
""",
        ),
        Ex(
            id="A11-011", titulo="Função como valor: guardar e passar adiante", nivel=3, tempo_min=8,
            tags=["funcoes", "primeira-classe", "ordem-superior"],
            enunciado="""
            Aplique uma função a um valor — a função chega como argumento,
            não escrita dentro do `resolver`.

            Exemplo:

                def dobro(x):
                    return x * 2

                resolver(dobro, 5)  ->  10

            Uma função é um valor como outro qualquer: pode ser guardada
            numa variável, passada como argumento, chamada com `()` mais
            tarde.
            """,
            assinatura="def resolver(funcao, valor):",
            dicas=[
                "funcao chega como valor comum — sem (), só é possível guardá-la ou passá-la adiante.",
                "Para chamá-la de verdade, use funcao(valor), com parênteses.",
                "return funcao(valor)",
            ],
            solucao="    return funcao(valor)",
            testes="""
def teste_com_funcao_definida_no_teste():
    def dobro(x):
        return x * 2

    verificar(ex.resolver(dobro, 5), 10)


def teste_com_funcao_embutida():
    verificar(ex.resolver(abs, -7), 7)


def teste_com_outra_funcao_embutida():
    verificar(ex.resolver(str, 42), "42")
""",
        ),
        Ex(
            id="A11-012", titulo="Função como argumento: transformar uma lista", nivel=3, tempo_min=8,
            tags=["funcoes", "primeira-classe", "ordem-superior"],
            requer=["A11-011"],
            enunciado="""
            Aplique uma função a cada item de uma lista, devolvendo a lista
            de resultados — na mesma ordem.

            Exemplo:

                def dobro(x):
                    return x * 2

                resolver(dobro, [1, 2, 3])  ->  [2, 4, 6]

            Uma função que recebe outra função de argumento (como esta) é
            chamada de **função de ordem superior**.
            """,
            assinatura="def resolver(funcao, itens: list) -> list:",
            dicas=[
                "Percorra itens com um laço, chamando funcao(item) para cada item.",
                "Guarde cada resultado, na ordem, numa lista nova (list.append).",
                "resultado = []\n    for item in itens:\n        resultado.append(funcao(item))\n    return resultado",
            ],
            solucao="""
            resultado = []
            for item in itens:
                resultado.append(funcao(item))
            return resultado
            """,
            nota_da_solucao="Essa mesma ideia, escrita numa linha só, é o que list comprehension faz por trás — o módulo A12 chega lá.",
            testes="""
def teste_dobrar_cada_item():
    def dobro(x):
        return x * 2

    verificar(ex.resolver(dobro, [1, 2, 3]), [2, 4, 6])


def teste_lista_vazia():
    def dobro(x):
        return x * 2

    verificar(ex.resolver(dobro, []), [])


def teste_funcao_embutida_str():
    verificar(ex.resolver(str, [1, 2, 3]), ["1", "2", "3"])
""",
        ),
        Ex(
            id="A11-013", titulo="Despacho por dicionário de funções", nivel=4, tempo_min=9,
            tags=["funcoes", "primeira-classe", "dict", "regra-de-negocio"],
            requer=["A11-011", "A08-002"],
            enunciado="""
            Aplique uma operação sobre dois números, escolhida por nome —
            sem escrever uma corrente de `if`/`elif` para cada uma.

            Exemplo:

                resolver("soma", 4, 3)      ->  7
                resolver("subtracao", 4, 3) ->  1

            Como funções são valores, um dicionário pode guardar
            `{"soma": funcao_soma, "subtracao": funcao_subtracao, ...}` e
            escolher qual chamar buscando pela chave — o mesmo
            `dicionario[chave]` do módulo A8, só que o valor é uma função.
            """,
            assinatura="def resolver(operacao: str, a: float, b: float) -> float:",
            dicas=[
                "Defina uma função pequena para cada operação (soma, subtracao,\nmultiplicacao, divisao) antes de resolver, e guarde as quatro num dicionário.",
                'operacoes = {"soma": soma, "subtracao": subtracao, ...} — sem (), é a\nfunção em si que vai no dicionário.',
                "return operacoes[operacao](a, b)",
            ],
            solucao="""
            def soma(x, y):
                return x + y

            def subtracao(x, y):
                return x - y

            def multiplicacao(x, y):
                return x * y

            def divisao(x, y):
                return x / y

            operacoes = {
                "soma": soma,
                "subtracao": subtracao,
                "multiplicacao": multiplicacao,
                "divisao": divisao,
            }
            return operacoes[operacao](a, b)
            """,
            nota_da_solucao="Guardar funções num dicionário substitui uma corrente de if/elif por operação — para adicionar uma operação nova, basta uma linha no dicionário, não mais um elif.",
            testes="""
def teste_soma():
    verificar(ex.resolver("soma", 4, 3), 7)


def teste_subtracao():
    verificar(ex.resolver("subtracao", 4, 3), 1)


def teste_multiplicacao():
    verificar(ex.resolver("multiplicacao", 4, 3), 12)


def teste_divisao():
    verificar(ex.resolver("divisao", 9, 3), 3.0)
""",
        ),
        Ex(
            id="A11-014", titulo="Função que devolve função", nivel=4, tempo_min=9,
            tags=["funcoes", "closure", "clausura"],
            requer=["A11-011"],
            enunciado="""
            Crie uma fábrica de multiplicadores: dado um fator, devolva
            **uma função** que multiplica qualquer número por esse fator.

            Exemplo:

                vezes3 = resolver(3)
                vezes3(10)   ->  30
                vezes3(2)    ->  6

            `resolver` não devolve um número — devolve uma função, definida
            por dentro, que lembra do `fator` mesmo depois que `resolver` já
            terminou. Isso é uma **clausura** (*closure*).
            """,
            assinatura="def resolver(fator: float):",
            dicas=[
                "resolver não faz a conta — ele monta e devolve uma função nova, sem chamá-la.",
                "Defina uma função por dentro de resolver, que usa fator; devolva essa\nfunção (sem parênteses — devolver a função, não o resultado dela).",
                "def multiplicar(x):\n        return x * fator\n    return multiplicar",
            ],
            solucao="""
            def multiplicar(x):
                return x * fator
            return multiplicar
            """,
            nota_da_solucao="A função de dentro lembra do fator com que foi criada, mesmo já fora do corpo de resolver — é a clausura que torna isso possível.",
            testes="""
def teste_vezes_tres():
    vezes3 = ex.resolver(3)
    verificar(vezes3(10), 30)
    verificar(vezes3(2), 6)


def teste_duas_fabricas_sao_independentes():
    vezes2 = ex.resolver(2)
    vezes5 = ex.resolver(5)
    verificar(vezes2(10), 20)
    verificar(vezes5(10), 50)
""",
        ),
        Ex(
            id="A11-015", titulo="Contador com nonlocal", nivel=4, tempo_min=10,
            tags=["funcoes", "closure", "nonlocal", "escopo"],
            requer=["A11-014"],
            enunciado="""
            Crie e devolva um contador: uma função sem argumentos que, a
            cada chamada, soma 1 a um total interno e devolve o total
            atualizado.

            Exemplo:

                contador = resolver()
                contador()   ->  1
                contador()   ->  2
                contador()   ->  3

            A função de dentro precisa **mudar** uma variável da função de
            fora (não só ler, como no exercício anterior) — para isso,
            declare `nonlocal total` antes de usá-la. Sem `nonlocal`,
            `total += 1` criaria uma variável local nova e estouraria
            `UnboundLocalError`.
            """,
            assinatura="def resolver():",
            dicas=[
                "Comece com total = 0 dentro de resolver, antes de definir a função interna.",
                "A função interna precisa de nonlocal total para poder somar 1 a ela —\nsó ler não precisaria, mas mudar precisa.",
                "def contador():\n        nonlocal total\n        total += 1\n        return total\n    return contador",
            ],
            solucao="""
            total = 0
            def contador():
                nonlocal total
                total += 1
                return total
            return contador
            """,
            testes="""
def teste_conta_a_partir_de_um():
    contador = ex.resolver()
    verificar(contador(), 1)
    verificar(contador(), 2)
    verificar(contador(), 3)


def teste_dois_contadores_sao_independentes():
    a = ex.resolver()
    b = ex.resolver()
    a()
    a()
    verificar(b(), 1)
""",
        ),
        Ex(
            id="A11-016", titulo="Desafio: fábrica de validador de desconto", nivel=5, tempo_min=12,
            tags=["funcoes", "closure", "parametro-padrao", "desafio"],
            requer=["A11-008", "A11-014", "A11-007"],
            enunciado="""
            Crie uma fábrica de validadores de desconto: dado um teto
            máximo (padrão `0.5`, ou seja 50%), devolva uma função que
            recebe uma quantidade qualquer de descontos e devolve quais
            deles **não** passam do teto.

            Exemplo:

                validar = resolver()                    # teto padrão: 0.5
                validar(0.1, 0.6, 0.3)  ->  [0.1, 0.3]

                validar_rigido = resolver(teto=0.2)
                validar_rigido(0.1, 0.6, 0.3)  ->  [0.1]

            Combina tudo do módulo: `teto` é um parâmetro com valor padrão;
            a função devolvida recebe os descontos por `*args`; e ela
            lembra do `teto` da fábrica por clausura, mesmo chamada bem
            depois.
            """,
            assinatura="def resolver(teto: float = 0.5):",
            dicas=[
                "resolver devolve uma função nova — ela é quem recebe os descontos, via *args.",
                "A função de dentro só lê teto (não muda), então nonlocal não é\nnecessário aqui — só ler já enxerga a variável de fora.",
                "def validar(*descontos):\n        aceitos = []\n        for d in descontos:\n            if d <= teto:\n                aceitos.append(d)\n        return aceitos\n    return validar",
            ],
            solucao="""
            def validar(*descontos):
                aceitos = []
                for d in descontos:
                    if d <= teto:
                        aceitos.append(d)
                return aceitos
            return validar
            """,
            nota_da_solucao="validar lê teto da fábrica por clausura — só ler não precisa de nonlocal, essa palavra só entra quando a função de dentro muda a variável de fora.",
            testes="""
def teste_teto_padrao():
    validar = ex.resolver()
    verificar(validar(0.1, 0.6, 0.3), [0.1, 0.3])


def teste_teto_customizado():
    validar_rigido = ex.resolver(teto=0.2)
    verificar(validar_rigido(0.1, 0.6, 0.3), [0.1])


def teste_nenhum_desconto_passa():
    validar = ex.resolver(teto=0.05)
    verificar(validar(0.1, 0.2), [])


def teste_sem_nenhum_desconto_informado():
    validar = ex.resolver()
    verificar(validar(), [])
""",
        ),
    ],
)

MODULOS = [A11]
