"""Bloco A, módulos 4 a 6: condicionais, listas e laços."""

from autoria.modelo import Exercicio as Ex
from autoria.modelo import Modulo

# --------------------------------------------------------------------------- #
# A04 — Condicionais
# --------------------------------------------------------------------------- #

A04 = Modulo(
    id="A04",
    titulo="Módulo A4 — Condicionais",
    resumo="Fazer o programa escolher: if, elif, else e os operadores lógicos.",
    teoria="""
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
""",
    exercicios=[
        Ex(
            id="A04-001", titulo="O maior dos dois", nivel=1, tempo_min=4,
            tags=["if", "comparacao"],
            enunciado="""
            Devolva o maior entre dois números. Se forem iguais, devolva qualquer um.

            Exemplos:

                resolver(10, 3)   ->  10
                resolver(3, 10)   ->  10
                resolver(5, 5)    ->  5

            Faça com `if` e `else` — este módulo é sobre isso. (Sim, `max` resolveria
            em uma linha, e você já viu isso no A02-008.)
            """,
            assinatura="def resolver(a, b):",
            dicas=[
                "A pergunta é: a é maior que b?",
                "Se for, devolva a; senão, devolva b.",
                "if a > b: return a — e um else: return b logo abaixo.",
            ],
            solucao="""
            if a > b:
                return a
            else:
                return b
            """,
            nota_da_solucao="Como o return já encerra a função, o else é opcional aqui — mas deixa a intenção explícita.",
            testes="""
def teste_primeiro_maior():
    verificar(ex.resolver(10, 3), 10)


def teste_segundo_maior():
    verificar(ex.resolver(3, 10), 10)


def teste_iguais():
    verificar(ex.resolver(5, 5), 5)


def teste_negativos():
    verificar(ex.resolver(-2, -9), -2)
""",
        ),
        Ex(
            id="A04-002", titulo="Aprovado ou reprovado", nivel=1, tempo_min=4,
            tags=["if", "else"],
            enunciado="""
            A nota de corte é 7. Devolva `"aprovado"` se a nota for 7 ou mais,
            e `"reprovado"` caso contrário.

            Exemplos:

                resolver(7)    ->  "aprovado"
                resolver(6.9)  ->  "reprovado"
                resolver(10)   ->  "aprovado"

            Cuidado com o 7 exato: o enunciado diz "7 ou mais".
            """,
            assinatura="def resolver(nota) -> str:",
            dicas=[
                "\"7 ou mais\" inclui o próprio 7 — o operador é >=, não >.",
                "São dois caminhos: um no if, outro no else.",
                'if nota >= 7: return "aprovado"',
            ],
            solucao="""
            if nota >= 7:
                return "aprovado"
            else:
                return "reprovado"
            """,
            testes="""
def teste_acima_da_media():
    verificar(ex.resolver(10), "aprovado")


def teste_na_nota_de_corte():
    verificar(ex.resolver(7), "aprovado",
              dica="7 exato aprova: a comparação é >=, não >.")


def teste_logo_abaixo_do_corte():
    verificar(ex.resolver(6.9), "reprovado")


def teste_zero():
    verificar(ex.resolver(0), "reprovado")
""",
        ),
        Ex(
            id="A04-003", titulo="Conceito por faixa", nivel=2, tempo_min=7,
            tags=["elif", "faixas"], requer=["A04-002"],
            enunciado="""
            Converta a nota em conceito, segundo a tabela:

                nota >= 9        ->  "A"
                nota >= 7        ->  "B"
                nota >= 5        ->  "C"
                abaixo disso     ->  "D"

            Exemplos:

                resolver(9.5)  ->  "A"
                resolver(7)    ->  "B"
                resolver(5)    ->  "C"
                resolver(2)    ->  "D"

            A ordem dos `elif` importa: teste do mais alto para o mais baixo. Se você
            começar por `nota >= 5`, todo mundo acima de 5 vira "C".
            """,
            assinatura="def resolver(nota) -> str:",
            dicas=[
                "Comece pela faixa mais alta e vá descendo.",
                "Como cada elif só é testado se os anteriores falharam, não precisa\\nde condições como (nota >= 7 and nota < 9).",
                "if nota >= 9 ... elif nota >= 7 ... elif nota >= 5 ... else ...",
            ],
            solucao="""
            if nota >= 9:
                return "A"
            elif nota >= 7:
                return "B"
            elif nota >= 5:
                return "C"
            else:
                return "D"
            """,
            nota_da_solucao="Descer do maior para o menor dispensa os limites superiores de cada faixa.",
            testes="""
def teste_conceito_a():
    verificar(ex.resolver(9.5), "A")


def teste_limite_de_a():
    verificar(ex.resolver(9), "A")


def teste_conceito_b():
    verificar(ex.resolver(7), "B")


def teste_conceito_c():
    verificar(ex.resolver(5), "C")


def teste_conceito_d():
    verificar(ex.resolver(2), "D")


def teste_nota_maxima():
    verificar(ex.resolver(10), "A")
""",
        ),
        Ex(
            id="A04-004", titulo="As duas condições", nivel=2, tempo_min=6,
            tags=["and", "or", "booleano"],
            enunciado="""
            Um pedido ganha frete grátis quando o valor passa de R$ 200 **e** o
            cliente é assinante.

            Devolva `True` ou `False`.

            Exemplos:

                resolver(250, True)   ->  True
                resolver(250, False)  ->  False
                resolver(150, True)   ->  False
                resolver(200, True)   ->  False

            Repare no último caso: "passa de 200" não inclui o 200.
            Nenhum `if` é necessário — a expressão já vale `True` ou `False`.
            """,
            assinatura="def resolver(valor, e_assinante: bool) -> bool:",
            dicas=[
                "\"E\" em Python se escreve and.",
                "\"Passa de 200\" é > 200, sem o igual.",
                "return valor > 200 and e_assinante",
            ],
            solucao="    return valor > 200 and e_assinante",
            nota_da_solucao="Comparar e_assinante == True é redundante: ele já é booleano.",
            testes="""
def teste_atende_aos_dois():
    verificar(ex.resolver(250, True), True)


def teste_nao_e_assinante():
    verificar(ex.resolver(250, False), False)


def teste_valor_baixo():
    verificar(ex.resolver(150, True), False)


def teste_valor_exatamente_no_limite():
    verificar(ex.resolver(200, True), False,
              dica="\\"Passa de 200\\" exclui o próprio 200.")
""",
        ),
        Ex(
            id="A04-005", titulo="Pedido em aberto", nivel=2, tempo_min=6,
            tags=["not", "in", "lista"],
            enunciado="""
            Um pedido está **em aberto** quando o status não é nem `"entregue"`
            nem `"cancelado"`.

            Devolva `True` para pedidos em aberto.

            Exemplos:

                resolver("processando")  ->  True
                resolver("enviado")      ->  True
                resolver("entregue")     ->  False
                resolver("cancelado")    ->  False

            Dá para escrever com dois `and`, mas `not ... in [...]` fica bem melhor.
            """,
            assinatura="def resolver(status: str) -> bool:",
            dicas=[
                "O operador in também funciona com listas: x in [\"a\", \"b\"].",
                "Você quer o contrário disso — existe o operador not.",
                'return status not in ["entregue", "cancelado"]',
            ],
            solucao='    return status not in ["entregue", "cancelado"]',
            nota_da_solucao="`not in` é um operador só; lê-se exatamente como a regra de negócio.",
            testes="""
def teste_processando():
    verificar(ex.resolver("processando"), True)


def teste_enviado():
    verificar(ex.resolver("enviado"), True)


def teste_entregue():
    verificar(ex.resolver("entregue"), False)


def teste_cancelado():
    verificar(ex.resolver("cancelado"), False)


def teste_status_desconhecido():
    verificar(ex.resolver("devolvido"), True)
""",
        ),
        Ex(
            id="A04-006", titulo="Dentro da faixa", nivel=2, tempo_min=5,
            tags=["comparacao-encadeada"],
            enunciado="""
            Devolva `True` se a nota estiver entre 0 e 10, incluindo as pontas.

            Exemplos:

                resolver(7)    ->  True
                resolver(0)    ->  True
                resolver(10)   ->  True
                resolver(-1)   ->  False
                resolver(10.5) ->  False

            Python permite escrever `0 <= nota <= 10` — exatamente como na matemática.
            """,
            assinatura="def resolver(nota) -> bool:",
            dicas=[
                "Duas comparações ao mesmo tempo: o limite de baixo e o de cima.",
                "Em Python elas podem ficar na mesma expressão, encadeadas.",
                "return 0 <= nota <= 10",
            ],
            solucao="    return 0 <= nota <= 10",
            testes="""
def teste_no_meio():
    verificar(ex.resolver(7), True)


def teste_limite_inferior():
    verificar(ex.resolver(0), True)


def teste_limite_superior():
    verificar(ex.resolver(10), True)


def teste_abaixo():
    verificar(ex.resolver(-1), False)


def teste_acima():
    verificar(ex.resolver(10.5), False)
""",
        ),
        Ex(
            id="A04-007", titulo="Frete por região", nivel=2, tempo_min=7,
            tags=["elif", "in", "strings"], requer=["A04-005"],
            enunciado="""
            O frete da Loja Aurora depende do estado:

                SP, RJ, MG, ES           ->  15.0   (Sudeste)
                PR, SC, RS               ->  22.0   (Sul)
                qualquer outro estado    ->  35.0

            Exemplos:

                resolver("SP")  ->  15.0
                resolver("RS")  ->  22.0
                resolver("AM")  ->  35.0
            """,
            assinatura="def resolver(uf: str) -> float:",
            dicas=[
                "Testar uf == \"SP\" or uf == \"RJ\" or ... funciona, mas é longo.",
                "in com uma lista deixa cada condição em uma linha só.",
                'if uf in ["SP", "RJ", "MG", "ES"]: return 15.0 — e siga com elif.',
            ],
            solucao="""
            if uf in ["SP", "RJ", "MG", "ES"]:
                return 15.0
            elif uf in ["PR", "SC", "RS"]:
                return 22.0
            else:
                return 35.0
            """,
            testes="""
def teste_sudeste():
    verificar(ex.resolver("SP"), 15.0)


def teste_outro_do_sudeste():
    verificar(ex.resolver("ES"), 15.0)


def teste_sul():
    verificar(ex.resolver("RS"), 22.0)


def teste_demais_estados():
    verificar(ex.resolver("AM"), 35.0)


def teste_estado_do_nordeste():
    verificar(ex.resolver("BA"), 35.0)
""",
        ),
        Ex(
            id="A04-008", titulo="Faixa etária", nivel=2, tempo_min=7,
            tags=["elif", "faixas"],
            enunciado="""
            Classifique o cliente pela idade:

                menos de 18       ->  "menor"
                de 18 a 59        ->  "adulto"
                60 ou mais        ->  "idoso"

            Exemplos:

                resolver(15)  ->  "menor"
                resolver(18)  ->  "adulto"
                resolver(59)  ->  "adulto"
                resolver(60)  ->  "idoso"

            Preste atenção nos limites — 18 e 60 são os pontos onde a maioria erra.
            """,
            assinatura="def resolver(idade: int) -> str:",
            dicas=[
                "São três faixas, então if / elif / else.",
                "Comece pelo mais novo ou pelo mais velho — só não misture as ordens.",
                "if idade < 18 ... elif idade < 60 ... else ...",
            ],
            solucao="""
            if idade < 18:
                return "menor"
            elif idade < 60:
                return "adulto"
            else:
                return "idoso"
            """,
            testes="""
def teste_crianca():
    verificar(ex.resolver(15), "menor")


def teste_limite_da_maioridade():
    verificar(ex.resolver(18), "adulto")


def teste_ultimo_ano_de_adulto():
    verificar(ex.resolver(59), "adulto")


def teste_limite_da_terceira_idade():
    verificar(ex.resolver(60), "idoso")


def teste_recem_nascido():
    verificar(ex.resolver(0), "menor")
""",
        ),
        Ex(
            id="A04-009", titulo="Desconto progressivo", nivel=3, tempo_min=9,
            tags=["elif", "aritmetica", "regra-de-negocio"], requer=["A04-003"],
            enunciado="""
            A loja dá desconto conforme o valor da compra:

                a partir de R$ 500   ->  15%
                a partir de R$ 200   ->  10%
                a partir de R$ 100   ->  5%
                abaixo de R$ 100     ->  sem desconto

            Devolva o **valor final** já com o desconto aplicado, arredondado
            para duas casas.

            Exemplos:

                resolver(600)  ->  510.0
                resolver(200)  ->  180.0
                resolver(150)  ->  142.5
                resolver(50)   ->  50.0
            """,
            assinatura="def resolver(valor: float) -> float:",
            dicas=[
                "Primeiro descubra a taxa de desconto; só depois aplique no valor.",
                "Aplicar 15% de desconto é multiplicar por (1 - 0.15).",
                "Guarde a taxa numa variável dentro dos if/elif e faça um único\\nreturn round(valor * (1 - taxa), 2) no fim.",
            ],
            solucao="""
            if valor >= 500:
                taxa = 0.15
            elif valor >= 200:
                taxa = 0.10
            elif valor >= 100:
                taxa = 0.05
            else:
                taxa = 0.0
            return round(valor * (1 - taxa), 2)
            """,
            nota_da_solucao="Separar 'decidir a taxa' de 'aplicar a taxa' evita repetir a mesma conta em quatro lugares.",
            testes="""
def teste_faixa_de_quinze():
    verificar(ex.resolver(600), 510.0)


def teste_limite_de_duzentos():
    verificar(ex.resolver(200), 180.0)


def teste_faixa_de_cinco():
    verificar(ex.resolver(150), 142.5)


def teste_sem_desconto():
    verificar(ex.resolver(50), 50.0)


def teste_limite_de_quinhentos():
    verificar(ex.resolver(500), 425.0)


def teste_logo_abaixo_de_cem():
    verificar(ex.resolver(99.99), 99.99)
""",
        ),
        Ex(
            id="A04-010", titulo="Ano bissexto", nivel=3, tempo_min=9,
            tags=["resto", "and", "or", "logica"],
            enunciado="""
            Um ano é bissexto quando:

                é divisível por 4
                E NÃO é divisível por 100
                OU é divisível por 400

            Escrito com precisão: divisível por 4 e não por 100; **ou** divisível por 400.

            Exemplos:

                resolver(2024)  ->  True    (divisível por 4, não por 100)
                resolver(2023)  ->  False
                resolver(1900)  ->  False   (divisível por 100, mas não por 400)
                resolver(2000)  ->  True    (divisível por 400)

            O 1900 e o 2000 são o teste de verdade — muita gente erra os dois.
            """,
            assinatura="def resolver(ano: int) -> bool:",
            dicas=[
                "\"Divisível por N\" é ano % N == 0.",
                "São duas partes ligadas por or; a primeira tem um and dentro dela.",
                "Parênteses em volta da parte do and deixam a precedência explícita:\\n(A and B) or C",
            ],
            solucao="""
            divisivel_por_4 = ano % 4 == 0
            divisivel_por_100 = ano % 100 == 0
            divisivel_por_400 = ano % 400 == 0
            return (divisivel_por_4 and not divisivel_por_100) or divisivel_por_400
            """,
            nota_da_solucao="Nomear cada condição transforma uma expressão críptica em algo que se lê como a regra.",
            testes="""
def teste_ano_comum_bissexto():
    verificar(ex.resolver(2024), True)


def teste_ano_normal():
    verificar(ex.resolver(2023), False)


def teste_seculo_nao_bissexto():
    verificar(ex.resolver(1900), False,
              dica="1900 é divisível por 100 e não por 400 — logo, não é bissexto.")


def teste_seculo_bissexto():
    verificar(ex.resolver(2000), True,
              dica="2000 é divisível por 400, então a regra do 100 não vale.")


def teste_outro_ano_par():
    verificar(ex.resolver(2022), False)


def teste_ano_zero():
    verificar(ex.resolver(0), True)
""",
        ),
        Ex(
            id="A04-011", titulo="Que triângulo é esse", nivel=3, tempo_min=10,
            tags=["elif", "logica", "validacao"],
            enunciado="""
            Recebendo os três lados, devolva:

                "invalido"    se os lados não formam triângulo
                "equilatero"  se os três lados são iguais
                "isosceles"   se exatamente dois lados são iguais
                "escaleno"    se os três lados são diferentes

            Um triângulo existe quando **cada lado é menor que a soma dos outros dois**.

            Exemplos:

                resolver(3, 3, 3)   ->  "equilatero"
                resolver(5, 5, 3)   ->  "isosceles"
                resolver(3, 4, 5)   ->  "escaleno"
                resolver(1, 2, 10)  ->  "invalido"
                resolver(1, 2, 3)   ->  "invalido"

            O último caso é o traiçoeiro: 1 + 2 dá exatamente 3, e a soma precisa ser
            **maior**, não igual.
            """,
            assinatura="def resolver(a, b, c) -> str:",
            dicas=[
                "Valide primeiro: se não for triângulo, nem faz sentido classificar.",
                "São três desigualdades ligadas por and — uma para cada lado.",
                "Depois de validar, compare a==b, b==c e a==c para decidir o tipo.",
            ],
            solucao="""
            existe = a + b > c and a + c > b and b + c > a
            if not existe:
                return "invalido"
            if a == b == c:
                return "equilatero"
            if a == b or b == c or a == c:
                return "isosceles"
            return "escaleno"
            """,
            nota_da_solucao="Devolver cedo no caso inválido evita aninhar todo o resto dentro de um else.",
            testes="""
def teste_equilatero():
    verificar(ex.resolver(3, 3, 3), "equilatero")


def teste_isosceles():
    verificar(ex.resolver(5, 5, 3), "isosceles")


def teste_isosceles_em_outra_posicao():
    verificar(ex.resolver(3, 5, 5), "isosceles")


def teste_escaleno():
    verificar(ex.resolver(3, 4, 5), "escaleno")


def teste_invalido_por_folga():
    verificar(ex.resolver(1, 2, 10), "invalido")


def teste_invalido_no_limite():
    verificar(ex.resolver(1, 2, 3), "invalido",
              dica="A soma precisa ser MAIOR que o terceiro lado; 1+2 é igual a 3.")
""",
        ),
        Ex(
            id="A04-012", titulo="Prazo de entrega", nivel=3, tempo_min=9,
            tags=["elif", "and", "regra-de-negocio"], requer=["A04-007"],
            enunciado="""
            O prazo de entrega em dias combina duas informações:

                                    frete expresso    frete comum
                SP, RJ, MG, ES            1                4
                PR, SC, RS                2                6
                demais estados            4               12

            Devolva o prazo em dias.

            Exemplos:

                resolver("SP", True)   ->  1
                resolver("SP", False)  ->  4
                resolver("BA", True)   ->  4
                resolver("RS", False)  ->  6
            """,
            assinatura="def resolver(uf: str, expresso: bool) -> int:",
            dicas=[
                "Duas dimensões: a região e o tipo de frete. Resolva uma de cada vez.",
                "Descubra a região primeiro e guarde numa variável; depois decida o\\nprazo com base na região e no expresso.",
                "Você pode fazer um if por região com um if interno para o expresso.",
            ],
            solucao="""
            if uf in ["SP", "RJ", "MG", "ES"]:
                return 1 if expresso else 4
            elif uf in ["PR", "SC", "RS"]:
                return 2 if expresso else 6
            else:
                return 4 if expresso else 12
            """,
            nota_da_solucao="`a if condicao else b` é o if em forma de expressão — cabe direto no return.",
            testes="""
def teste_sudeste_expresso():
    verificar(ex.resolver("SP", True), 1)


def teste_sudeste_comum():
    verificar(ex.resolver("SP", False), 4)


def teste_sul_comum():
    verificar(ex.resolver("RS", False), 6)


def teste_sul_expresso():
    verificar(ex.resolver("PR", True), 2)


def teste_outros_expresso():
    verificar(ex.resolver("BA", True), 4)


def teste_outros_comum():
    verificar(ex.resolver("AM", False), 12)
""",
        ),
    ],
)


# --------------------------------------------------------------------------- #
# A05 — Listas
# --------------------------------------------------------------------------- #

A05 = Modulo(
    id="A05",
    titulo="Módulo A5 — Listas",
    resumo="A estrutura mais usada de Python: vários valores em ordem, num nome só.",
    teoria="""
## Uma lista guarda vários valores em ordem

```python
precos = [49.90, 12.00, 230.50]
precos[0]      # 49.9   — o primeiro
precos[-1]     # 230.5  — o último
len(precos)    # 3
```

Índices e fatiamento funcionam igual aos de string, porque os dois são sequências.

```python
precos[0:2]    # [49.9, 12.0]
precos[::-1]   # [230.5, 12.0, 49.9]
```

### Listas mudam — strings não

Essa é a diferença estrutural entre as duas.

```python
precos.append(99.90)      # acrescenta no fim
precos.insert(0, 5.00)    # insere na posição 0, empurrando o resto
precos.remove(12.00)      # tira a primeira ocorrência DESSE VALOR
precos.pop()              # tira o último e DEVOLVE ele
precos[1] = 15.00         # troca o item da posição 1
```

### O par que confunde todo mundo: `sort` e `sorted`

```python
numeros = [3, 1, 2]

numeros.sort()            # reordena a própria lista; devolve None
ordenados = sorted(numeros)   # devolve uma lista NOVA; a original fica intacta
```

O erro clássico é escrever `numeros = numeros.sort()` — e ficar com `None`.
A regra vale para vários métodos de lista: **os que alteram devolvem `None`**.

### Funções que resumem uma lista

```python
sum(precos)      # soma tudo
min(precos)      # menor
max(precos)      # maior
len(precos)      # quantos
precos.count(49.9)   # quantas vezes esse valor aparece
precos.index(49.9)   # em que posição está a primeira ocorrência
49.9 in precos       # existe?
```

### Juntar e repetir

```python
[1, 2] + [3]     # [1, 2, 3]
[0] * 3          # [0, 0, 0]
```
""",
    exercicios=[
        Ex(
            id="A05-001", titulo="Montar uma lista", nivel=1, tempo_min=4,
            tags=["lista", "criacao"],
            enunciado="""
            Devolva uma lista com os três valores recebidos, na mesma ordem.

            Exemplos:

                resolver(1, 2, 3)          ->  [1, 2, 3]
                resolver("a", "b", "c")    ->  ["a", "b", "c"]

            Lista se escreve entre colchetes, com os itens separados por vírgula.
            """,
            assinatura="def resolver(a, b, c) -> list:",
            dicas=[
                "Colchetes criam a lista: [x, y, z].",
                "Você pode montar a lista direto na linha do return.",
                "return [a, b, c]",
            ],
            solucao="    return [a, b, c]",
            testes="""
def teste_numeros():
    verificar(ex.resolver(1, 2, 3), [1, 2, 3])


def teste_textos():
    verificar(ex.resolver("a", "b", "c"), ["a", "b", "c"])


def teste_tipos_misturados():
    verificar(ex.resolver(1, "a", True), [1, "a", True])
""",
        ),
        Ex(
            id="A05-002", titulo="Primeiro, último e quantos", nivel=1, tempo_min=5,
            tags=["indexacao", "len"],
            enunciado="""
            Devolva uma tupla `(primeiro item, último item, quantidade de itens)`.

            Exemplos:

                resolver([10, 20, 30])  ->  (10, 30, 3)
                resolver(["a"])         ->  ("a", "a", 1)

            Pode contar com a lista nunca estar vazia.
            """,
            assinatura="def resolver(itens: list) -> tuple:",
            dicas=[
                "Índice 0 é o primeiro; -1 é o último.",
                "len(itens) diz quantos são.",
                "return itens[0], itens[-1], len(itens)",
            ],
            solucao="    return itens[0], itens[-1], len(itens)",
            testes="""
def teste_tres_itens():
    verificar(ex.resolver([10, 20, 30]), (10, 30, 3))


def teste_um_item():
    verificar(ex.resolver(["a"]), ("a", "a", 1))


def teste_lista_longa():
    verificar(ex.resolver([1, 2, 3, 4, 5, 6]), (1, 6, 6))
""",
        ),
        Ex(
            id="A05-003", titulo="Fatiar a lista", nivel=2, tempo_min=5,
            tags=["fatiamento"], requer=["A03-003"],
            enunciado="""
            Devolva os **dois primeiros** itens da lista.

            Exemplos:

                resolver([10, 20, 30, 40])  ->  [10, 20]
                resolver([7])               ->  [7]
                resolver([])                ->  []

            Fatiar lista é igual a fatiar texto — e o resultado é sempre uma lista nova.
            """,
            assinatura="def resolver(itens: list) -> list:",
            dicas=[
                "Colchetes com dois-pontos: itens[inicio:fim].",
                "Para dois itens a partir do começo, o fim é 2.",
                "return itens[:2]",
            ],
            solucao="    return itens[:2]",
            testes="""
def teste_lista_maior():
    verificar(ex.resolver([10, 20, 30, 40]), [10, 20])


def teste_lista_menor_que_o_pedido():
    verificar(ex.resolver([7]), [7])


def teste_lista_vazia():
    verificar(ex.resolver([]), [])
""",
        ),
        Ex(
            id="A05-004", titulo="Acrescentar no fim", nivel=2, tempo_min=6,
            tags=["append", "mutacao"],
            enunciado="""
            Acrescente o novo item ao fim da lista e devolva a lista.

            Exemplos:

                resolver([1, 2], 3)   ->  [1, 2, 3]
                resolver([], "a")     ->  ["a"]

            Atenção: `append` **altera a lista e devolve `None`**. Se você escrever
            `return itens.append(novo)`, sua função devolve `None` e o teste reprova.
            São duas linhas: uma que acrescenta, outra que devolve.
            """,
            assinatura="def resolver(itens: list, novo) -> list:",
            dicas=[
                "append acrescenta um item no fim da lista.",
                "Ele NÃO devolve a lista — devolve None. Não dá para usar no return.",
                "itens.append(novo) numa linha; return itens na linha seguinte.",
            ],
            solucao="""
            itens.append(novo)
            return itens
            """,
            nota_da_solucao="Métodos que alteram a lista devolvem None; essa é a pegadinha mais comum de listas.",
            testes="""
def teste_acrescenta_no_fim():
    verificar(ex.resolver([1, 2], 3), [1, 2, 3])


def teste_lista_vazia():
    verificar(ex.resolver([], "a"), ["a"])


def teste_nao_devolve_none():
    verificar(ex.resolver([1], 2), [1, 2],
              dica="Se veio None, você escreveu return itens.append(...).")
""",
        ),
        Ex(
            id="A05-005", titulo="Tirar um item", nivel=2, tempo_min=6,
            tags=["remove", "mutacao"], requer=["A05-004"],
            enunciado="""
            Remova da lista a primeira ocorrência do valor indicado e devolva a lista.

            Exemplos:

                resolver([1, 2, 3], 2)      ->  [1, 3]
                resolver([1, 2, 2], 2)      ->  [1, 2]
                resolver(["a", "b"], "a")   ->  ["b"]

            Repare no segundo exemplo: `remove` tira só a **primeira** ocorrência.
            Pode contar com o valor sempre existir na lista.
            """,
            assinatura="def resolver(itens: list, valor) -> list:",
            dicas=[
                "remove recebe o VALOR a tirar, não a posição.",
                "Assim como append, ele devolve None — precisa de duas linhas.",
                "itens.remove(valor) e depois return itens",
            ],
            solucao="""
            itens.remove(valor)
            return itens
            """,
            nota_da_solucao="remove trabalha por valor; para tirar por posição existe pop(indice) ou del.",
            testes="""
def teste_remove_do_meio():
    verificar(ex.resolver([1, 2, 3], 2), [1, 3])


def teste_remove_so_a_primeira():
    verificar(ex.resolver([1, 2, 2], 2), [1, 2])


def teste_remove_texto():
    verificar(ex.resolver(["a", "b"], "a"), ["b"])
""",
        ),
        Ex(
            id="A05-006", titulo="sorted não é sort", nivel=3, tempo_min=8,
            tags=["sorted", "sort", "imutabilidade"],
            enunciado="""
            O exercício mais importante do módulo, porque a diferença aqui gera bug
            silencioso a vida inteira:

                sorted(lista)   devolve uma lista NOVA ordenada; a original fica igual
                lista.sort()    reordena a PRÓPRIA lista e devolve None

            Devolva a tupla `(lista ordenada, lista original)` — usando `sorted`,
            de modo que a original chegue **intacta** no segundo item.

            Exemplo:

                resolver([3, 1, 2])  ->  ([1, 2, 3], [3, 1, 2])

            Se você usar `.sort()`, os dois itens da tupla vão sair ordenados e o
            teste vai pegar.
            """,
            assinatura="def resolver(numeros: list) -> tuple[list, list]:",
            dicas=[
                "Só um dos dois preserva a lista original.",
                "sorted(...) é função, não método: sorted(numeros), sem ponto.",
                "return sorted(numeros), numeros",
            ],
            solucao="    return sorted(numeros), numeros",
            nota_da_solucao="Regra prática: se precisar da lista original depois, use sorted.",
            testes="""
def teste_ordena_e_preserva():
    verificar(ex.resolver([3, 1, 2]), ([1, 2, 3], [3, 1, 2]),
              dica="Se a original também saiu ordenada, você usou .sort().")


def teste_ja_ordenada():
    verificar(ex.resolver([1, 2]), ([1, 2], [1, 2]))


def teste_com_repetidos():
    verificar(ex.resolver([2, 1, 2]), ([1, 2, 2], [2, 1, 2]))


def teste_a_original_nao_muda_de_fora():
    entrada = [5, 3, 9]
    ex.resolver(entrada)
    verificar(entrada, [5, 3, 9], nome="lista recebida",
              dica="Sua função não deve modificar a lista que recebeu.")
""",
        ),
        Ex(
            id="A05-007", titulo="De trás para frente", nivel=2, tempo_min=5,
            tags=["fatiamento", "inversao"], requer=["A03-012"],
            enunciado="""
            Devolva uma lista nova com os itens na ordem inversa, **sem alterar**
            a lista recebida.

            Exemplos:

                resolver([1, 2, 3])  ->  [3, 2, 1]
                resolver([])         ->  []

            `lista.reverse()` inverteria a original — não é o que queremos aqui.
            """,
            assinatura="def resolver(itens: list) -> list:",
            dicas=[
                "O fatiamento com passo -1 funciona igual ao das strings.",
                "itens[::-1] devolve uma cópia invertida.",
                "return itens[::-1]",
            ],
            solucao="    return itens[::-1]",
            testes="""
def teste_inverte():
    verificar(ex.resolver([1, 2, 3]), [3, 2, 1])


def teste_lista_vazia():
    verificar(ex.resolver([]), [])


def teste_nao_altera_a_original():
    entrada = [1, 2, 3]
    ex.resolver(entrada)
    verificar(entrada, [1, 2, 3], nome="lista recebida",
              dica="reverse() altera a original; o fatiamento [::-1] faz uma cópia.")
""",
        ),
        Ex(
            id="A05-008", titulo="Resumo dos números", nivel=2, tempo_min=6,
            tags=["sum", "min-max"],
            enunciado="""
            Devolva a tupla `(soma, menor, maior)` de uma lista de números.

            Exemplos:

                resolver([1, 2, 3])       ->  (6, 1, 3)
                resolver([10])            ->  (10, 10, 10)
                resolver([-5, 0, 5])      ->  (0, -5, 5)

            As três funções já existem prontas — não precisa de laço.
            """,
            assinatura="def resolver(numeros: list) -> tuple:",
            dicas=[
                "Três funções embutidas com nomes bem diretos.",
                "sum, min e max — todas recebem a lista inteira.",
                "return sum(numeros), min(numeros), max(numeros)",
            ],
            solucao="    return sum(numeros), min(numeros), max(numeros)",
            testes="""
def teste_tres_numeros():
    verificar(ex.resolver([1, 2, 3]), (6, 1, 3))


def teste_um_numero():
    verificar(ex.resolver([10]), (10, 10, 10))


def teste_com_negativos():
    verificar(ex.resolver([-5, 0, 5]), (0, -5, 5))
""",
        ),
        Ex(
            id="A05-009", titulo="Em que posição está", nivel=2, tempo_min=6,
            tags=["index", "in"],
            enunciado="""
            Devolva a posição do valor na lista. Se o valor não estiver lá,
            devolva `-1`.

            Exemplos:

                resolver(["a", "b", "c"], "b")  ->  1
                resolver(["a", "b"], "z")       ->  -1
                resolver([1, 2, 1], 1)          ->  0

            `lista.index(valor)` daria erro quando o valor não existe — então
            confira antes com `in`.
            """,
            assinatura="def resolver(itens: list, valor) -> int:",
            dicas=[
                "index() devolve a posição da primeira ocorrência, mas estoura se não achar.",
                "Confira com `if valor in itens` antes de chamar index.",
                "if valor in itens: return itens.index(valor) — e um return -1 no fim.",
            ],
            solucao="""
            if valor in itens:
                return itens.index(valor)
            return -1
            """,
            nota_da_solucao="Perguntar antes de agir evita a exceção — no módulo A13 você vê a alternativa com try/except.",
            testes="""
def teste_encontra_no_meio():
    verificar(ex.resolver(["a", "b", "c"], "b"), 1)


def teste_nao_encontra():
    verificar(ex.resolver(["a", "b"], "z"), -1)


def teste_primeira_ocorrencia():
    verificar(ex.resolver([1, 2, 1], 1), 0)


def teste_lista_vazia():
    verificar(ex.resolver([], "a"), -1)
""",
        ),
        Ex(
            id="A05-010", titulo="Juntar e repetir", nivel=2, tempo_min=6,
            tags=["concatenacao", "repeticao"],
            enunciado="""
            Listas respondem a `+` e a `*` como as strings:

                [1, 2] + [3]   ->  [1, 2, 3]
                [0] * 3        ->  [0, 0, 0]

            Devolva a tupla `(as duas listas juntas, a primeira repetida 2 vezes)`.

            Exemplos:

                resolver([1], [2, 3])   ->  ([1, 2, 3], [1, 1])
                resolver([], ["a"])     ->  (["a"], [])
            """,
            assinatura="def resolver(a: list, b: list) -> tuple[list, list]:",
            dicas=[
                "+ concatena duas listas numa terceira.",
                "* repete os itens de uma lista.",
                "return a + b, a * 2",
            ],
            solucao="    return a + b, a * 2",
            testes="""
def teste_junta_e_repete():
    verificar(ex.resolver([1], [2, 3]), ([1, 2, 3], [1, 1]))


def teste_primeira_vazia():
    verificar(ex.resolver([], ["a"]), (["a"], []))


def teste_duas_com_itens():
    verificar(ex.resolver(["x", "y"], ["z"]),
              (["x", "y", "z"], ["x", "y", "x", "y"]))
""",
        ),
        Ex(
            id="A05-011", titulo="Quantas vezes aparece", nivel=2, tempo_min=5,
            tags=["count"], requer=["A03-013"],
            enunciado="""
            Devolva quantas vezes o valor aparece na lista.

            Exemplos:

                resolver(["SP", "RJ", "SP"], "SP")  ->  2
                resolver([1, 2, 3], 9)              ->  0
                resolver([], "a")                   ->  0
            """,
            assinatura="def resolver(itens: list, valor) -> int:",
            dicas=[
                "Listas têm o mesmo método de contagem que as strings.",
                "itens.count(valor)",
                "return itens.count(valor)",
            ],
            solucao="    return itens.count(valor)",
            testes="""
def teste_duas_ocorrencias():
    verificar(ex.resolver(["SP", "RJ", "SP"], "SP"), 2)


def teste_nenhuma():
    verificar(ex.resolver([1, 2, 3], 9), 0)


def teste_lista_vazia():
    verificar(ex.resolver([], "a"), 0)
""",
        ),
        Ex(
            id="A05-012", titulo="Trocar um item", nivel=2, tempo_min=6,
            tags=["indexacao", "mutacao"],
            enunciado="""
            Substitua o item que está na posição indicada e devolva a lista.

            Exemplos:

                resolver([1, 2, 3], 1, 99)      ->  [1, 99, 3]
                resolver(["a", "b"], 0, "z")    ->  ["z", "b"]
                resolver([1, 2, 3], -1, 0)      ->  [1, 2, 0]

            Pode contar com a posição sempre ser válida.
            """,
            assinatura="def resolver(itens: list, posicao: int, novo) -> list:",
            dicas=[
                "Diferente das strings, uma lista aceita atribuição por índice.",
                "itens[posicao] = novo altera a lista no lugar.",
                "Depois de alterar, devolva a lista numa segunda linha.",
            ],
            solucao="""
            itens[posicao] = novo
            return itens
            """,
            nota_da_solucao="Strings não aceitam isso: texto[0] = 'x' dá TypeError, porque string é imutável.",
            testes="""
def teste_troca_no_meio():
    verificar(ex.resolver([1, 2, 3], 1, 99), [1, 99, 3])


def teste_troca_no_comeco():
    verificar(ex.resolver(["a", "b"], 0, "z"), ["z", "b"])


def teste_troca_no_fim_com_indice_negativo():
    verificar(ex.resolver([1, 2, 3], -1, 0), [1, 2, 0])
""",
        ),
        Ex(
            id="A05-013", titulo="Média da lista", nivel=2, tempo_min=6,
            tags=["sum", "len", "media"], requer=["A05-008"],
            enunciado="""
            Devolva a média dos números da lista, arredondada para duas casas.
            Se a lista estiver vazia, devolva `0.0`.

            Exemplos:

                resolver([10, 8, 6])  ->  8.0
                resolver([1, 2])      ->  1.5
                resolver([])          ->  0.0

            A lista vazia é o caso que quebra o código de quem esquece dela:
            dividir por `len([])` é dividir por zero.
            """,
            assinatura="def resolver(numeros: list) -> float:",
            dicas=[
                "Média é a soma dividida pela quantidade.",
                "Trate a lista vazia ANTES de dividir.",
                "if not numeros: return 0.0 — e só depois faça a conta.",
            ],
            solucao="""
            if not numeros:
                return 0.0
            return round(sum(numeros) / len(numeros), 2)
            """,
            nota_da_solucao="`if not numeros` é o jeito idiomático de perguntar 'a lista está vazia?'.",
            testes="""
def teste_media_inteira():
    verificar(ex.resolver([10, 8, 6]), 8.0)


def teste_media_quebrada():
    verificar(ex.resolver([1, 2]), 1.5)


def teste_lista_vazia():
    verificar(ex.resolver([]), 0.0,
              dica="Sem tratar a lista vazia, len() vale 0 e a divisão estoura.")


def teste_arredonda():
    verificar(ex.resolver([1, 1, 2]), 1.33)
""",
        ),
        Ex(
            id="A05-014", titulo="Os três maiores", nivel=3, tempo_min=9,
            tags=["sorted", "fatiamento", "reverse", "composicao"],
            requer=["A05-006", "A05-003"],
            enunciado="""
            Devolva os três maiores valores da lista, do maior para o menor.
            Se a lista tiver menos de três itens, devolva todos os que houver
            (ainda em ordem decrescente).

            Exemplos:

                resolver([5, 1, 9, 3, 7])  ->  [9, 7, 5]
                resolver([2, 8])           ->  [8, 2]
                resolver([])               ->  []

            Combine ordenação com fatiamento. `sorted` aceita `reverse=True`
            para ordenar do maior para o menor.
            """,
            assinatura="def resolver(numeros: list) -> list:",
            dicas=[
                "Ordene primeiro; depois é só pegar os três primeiros.",
                "sorted(numeros, reverse=True) ordena do maior para o menor.",
                "Fatiar com [:3] já lida sozinho com listas menores que três.",
            ],
            solucao="    return sorted(numeros, reverse=True)[:3]",
            nota_da_solucao="O fatiamento nunca estoura: com 2 itens ele devolve 2, sem precisar de if.",
            testes="""
def teste_lista_grande():
    verificar(ex.resolver([5, 1, 9, 3, 7]), [9, 7, 5])


def teste_menos_de_tres():
    verificar(ex.resolver([2, 8]), [8, 2])


def teste_lista_vazia():
    verificar(ex.resolver([]), [])


def teste_com_repetidos():
    verificar(ex.resolver([4, 4, 4, 1]), [4, 4, 4])


def teste_exatamente_tres():
    verificar(ex.resolver([1, 3, 2]), [3, 2, 1])
""",
        ),
    ],
)


# --------------------------------------------------------------------------- #
# A06 — Laços
# --------------------------------------------------------------------------- #

A06 = Modulo(
    id="A06",
    titulo="Módulo A6 — Laços",
    resumo="Repetir sem copiar e colar. É aqui que o programa começa a valer a pena.",
    teoria="""
## `for`: uma volta para cada item

```python
for preco in [10, 20, 30]:
    print(preco)
```

Leia como "para cada preço nessa lista, faça isto". A variável `preco` recebe
um item por vez, automaticamente.

### `range`: uma sequência de números

```python
range(5)         # 0, 1, 2, 3, 4        — começa no 0, o 5 não entra
range(1, 6)      # 1, 2, 3, 4, 5
range(0, 10, 2)  # 0, 2, 4, 6, 8        — de dois em dois
```

O fim nunca entra — mesma lógica do fatiamento.

### O acumulador

O padrão mais importante do módulo. Sempre a mesma forma:

```python
total = 0                  # 1. começa vazio, FORA do laço
for preco in precos:
    total = total + preco  # 2. atualiza a cada volta  (ou: total += preco)
return total               # 3. usa depois que o laço acabou
```

Se você criar `total = 0` dentro do laço, ele zera a cada volta — o bug número um
de iniciante. Se colocar o `return` dentro do laço, a função para na primeira volta —
o bug número dois.

O mesmo esqueleto serve para **contar** (`quantos += 1`) e para **construir uma
lista** (`resultado.append(...)`).

### `while`: repetir enquanto algo for verdade

```python
saldo = 100
while saldo > 0:
    saldo = saldo - 30
```

Use `while` quando você **não sabe de antemão** quantas voltas serão. E garanta
que a condição um dia fique falsa — senão o programa trava.

### `break` e `continue`

```python
for x in itens:
    if x is None:
        continue     # pula esta volta, segue para a próxima
    if x == alvo:
        break        # abandona o laço inteiro
```

### Percorrer com o índice junto

```python
for posicao, nome in enumerate(["a", "b"]):
    ...              # posicao vale 0 e depois 1

for nome, preco in zip(nomes, precos):
    ...              # anda nas duas listas ao mesmo tempo
```

`zip` para na mais curta das duas.
""",
    exercicios=[
        Ex(
            id="A06-001", titulo="Percorrer uma lista", nivel=1, tempo_min=5,
            tags=["for", "print"],
            enunciado="""
            Imprima cada item da lista, um por linha, na ordem em que aparecem.

            Exemplo — para `["Moda", "Casa"]`, a tela deve mostrar:

                Moda
                Casa

            Este é um dos poucos exercícios que pedem `print`.
            """,
            assinatura="def resolver(itens: list) -> None:",
            dicas=[
                "A forma do laço é: for algo in lista:",
                "O corpo do laço fica indentado embaixo, com 4 espaços.",
                "for item in itens: e dentro, print(item)",
            ],
            solucao="""
            for item in itens:
                print(item)
            """,
            testes="""
def teste_duas_categorias():
    verificar(t.saida_de(ex.resolver, ["Moda", "Casa"]), "Moda\\nCasa",
              nome="texto impresso")


def teste_um_item():
    verificar(t.saida_de(ex.resolver, ["Livros"]), "Livros", nome="texto impresso")


def teste_lista_vazia_nao_imprime_nada():
    verificar(t.saida_de(ex.resolver, []), "", nome="texto impresso")
""",
        ),
        Ex(
            id="A06-002", titulo="Uma sequência de números", nivel=2, tempo_min=6,
            tags=["range", "lista"],
            enunciado="""
            Devolva uma lista com os números de 1 até n, incluindo o n.

            Exemplos:

                resolver(5)  ->  [1, 2, 3, 4, 5]
                resolver(1)  ->  [1]
                resolver(0)  ->  []

            Lembre que `range(1, 5)` para no 4 — o fim nunca entra. Para incluir
            o n, o fim precisa ser `n + 1`.
            """,
            assinatura="def resolver(n: int) -> list:",
            dicas=[
                "range(inicio, fim) vai do início até o fim MENOS UM.",
                "Para chegar até n, o fim precisa ser n + 1.",
                "list(range(1, n + 1)) transforma o range em lista.",
            ],
            solucao="    return list(range(1, n + 1))",
            nota_da_solucao="range é preguiçoso: ele não é uma lista até você pedir com list().",
            testes="""
def teste_ate_cinco():
    verificar(ex.resolver(5), [1, 2, 3, 4, 5])


def teste_ate_um():
    verificar(ex.resolver(1), [1])


def teste_zero_devolve_vazio():
    verificar(ex.resolver(0), [])


def teste_inclui_o_ultimo():
    verificar(ex.resolver(3), [1, 2, 3],
              dica="Se faltou o 3, o fim do range precisa ser n + 1.")
""",
        ),
        Ex(
            id="A06-003", titulo="Somar com acumulador", nivel=2, tempo_min=7,
            tags=["for", "acumulador"],
            enunciado="""
            Devolva a soma dos números da lista — **usando um laço**, sem `sum`.

            Exemplos:

                resolver([1, 2, 3])  ->  6
                resolver([])         ->  0
                resolver([-1, 1])    ->  0

            Sim, `sum` resolveria. O objetivo aqui é o padrão do acumulador, que você
            vai reusar a vida inteira para coisas que não têm função pronta.
            """,
            assinatura="def resolver(numeros: list):",
            dicas=[
                "Crie a variável do total ANTES do laço, valendo 0.",
                "A cada volta, some o item ao total: total += numero.",
                "O return vem depois do laço, sem indentação extra.",
            ],
            solucao="""
            total = 0
            for numero in numeros:
                total += numero
            return total
            """,
            nota_da_solucao="Iniciar fora, atualizar dentro, usar depois: esse é o esqueleto do acumulador.",
            testes="""
def teste_soma_simples():
    verificar(ex.resolver([1, 2, 3]), 6)


def teste_lista_vazia():
    verificar(ex.resolver([]), 0,
              dica="Com o total iniciado em 0 antes do laço, este caso sai de graça.")


def teste_com_negativos():
    verificar(ex.resolver([-1, 1]), 0)


def teste_lista_longa():
    verificar(ex.resolver(list(range(1, 101))), 5050,
              dica="Se veio só 1, o return está dentro do laço.")
""",
        ),
        Ex(
            id="A06-004", titulo="Contar quantos passam", nivel=2, tempo_min=7,
            tags=["for", "contador", "if"], requer=["A06-003"],
            enunciado="""
            Devolva quantos números da lista são maiores que o limite.

            Exemplos:

                resolver([10, 5, 20], 8)   ->  2
                resolver([1, 2], 100)      ->  0
                resolver([], 0)            ->  0

            Mesmo esqueleto do acumulador, mas somando 1 em vez do valor —
            e só quando a condição bate.
            """,
            assinatura="def resolver(numeros: list, limite) -> int:",
            dicas=[
                "Um contador que começa em 0, fora do laço.",
                "Dentro do laço, um if decide se o contador cresce.",
                "quantos += 1 acrescenta um ao contador.",
            ],
            solucao="""
            quantos = 0
            for numero in numeros:
                if numero > limite:
                    quantos += 1
            return quantos
            """,
            testes="""
def teste_dois_passam():
    verificar(ex.resolver([10, 5, 20], 8), 2)


def teste_nenhum_passa():
    verificar(ex.resolver([1, 2], 100), 0)


def teste_lista_vazia():
    verificar(ex.resolver([], 0), 0)


def teste_igual_ao_limite_nao_conta():
    verificar(ex.resolver([8, 9], 8), 1,
              dica="O enunciado diz MAIORES que o limite — o 8 não entra.")
""",
        ),
        Ex(
            id="A06-005", titulo="Construir uma lista nova", nivel=2, tempo_min=8,
            tags=["for", "append", "transformacao"], requer=["A05-004"],
            enunciado="""
            Devolva uma lista com todos os preços reajustados em 10%,
            arredondados para duas casas.

            Exemplos:

                resolver([100, 50])   ->  [110.0, 55.0]
                resolver([9.99])      ->  [10.99]
                resolver([])          ->  []

            Mesma estrutura do acumulador, mas o que acumula é uma lista:
            comece com `[]` e vá acrescentando.
            """,
            assinatura="def resolver(precos: list) -> list:",
            dicas=[
                "Comece com uma lista vazia antes do laço.",
                "A cada volta, calcule o novo preço e acrescente com .append().",
                "Reajustar em 10% é multiplicar por 1.1.",
            ],
            solucao="""
            reajustados = []
            for preco in precos:
                reajustados.append(round(preco * 1.1, 2))
            return reajustados
            """,
            nota_da_solucao="Este é exatamente o padrão que a list comprehension do módulo A12 vai encurtar.",
            testes="""
def teste_dois_precos():
    verificar(ex.resolver([100, 50]), [110.0, 55.0])


def teste_um_preco():
    verificar(ex.resolver([9.99]), [10.99])


def teste_lista_vazia():
    verificar(ex.resolver([]), [])


def teste_nao_altera_a_original():
    entrada = [100.0]
    ex.resolver(entrada)
    verificar(entrada, [100.0], nome="lista recebida")
""",
        ),
        Ex(
            id="A06-006", titulo="Enquanto houver saldo", nivel=2, tempo_min=8,
            tags=["while", "contador"],
            enunciado="""
            Um cliente tem um saldo e gasta um valor fixo por mês. Devolva quantos
            meses inteiros o saldo aguenta.

            Exemplos:

                resolver(100, 30)  ->  3     (30, 60, 90 — no quarto mês faltaria)
                resolver(100, 100) ->  1
                resolver(50, 80)   ->  0
                resolver(0, 10)    ->  0

            Use `while`: você não sabe de antemão quantas voltas serão.
            """,
            assinatura="def resolver(saldo, gasto_mensal) -> int:",
            dicas=[
                "Enquanto o saldo der para pagar mais um mês, desconte e conte o mês.",
                "A condição é saldo >= gasto_mensal.",
                "Dentro do while: saldo -= gasto_mensal e meses += 1. Se você não\\ndiminuir o saldo, o laço nunca termina.",
            ],
            solucao="""
            meses = 0
            while saldo >= gasto_mensal:
                saldo -= gasto_mensal
                meses += 1
            return meses
            """,
            nota_da_solucao="Todo while precisa de algo que caminhe rumo à condição falsa — aqui, o saldo diminuindo.",
            testes="""
def teste_tres_meses():
    verificar(ex.resolver(100, 30), 3)


def teste_um_mes_exato():
    verificar(ex.resolver(100, 100), 1)


def teste_nao_da_nem_um_mes():
    verificar(ex.resolver(50, 80), 0)


def teste_sem_saldo():
    verificar(ex.resolver(0, 10), 0)
""",
        ),
        Ex(
            id="A06-007", titulo="Parar na primeira", nivel=2, tempo_min=7,
            tags=["for", "break", "busca"],
            enunciado="""
            Devolva a posição do primeiro número negativo da lista.
            Se não houver nenhum, devolva `-1`.

            Exemplos:

                resolver([5, 3, -2, -8])  ->  2
                resolver([1, 2, 3])       ->  -1
                resolver([-1])            ->  0

            Assim que achar, pare — não faz sentido continuar procurando.
            Com `return` dentro do laço, você já sai da função de uma vez.
            """,
            assinatura="def resolver(numeros: list) -> int:",
            dicas=[
                "Você precisa da posição, não do valor — então percorra os índices,\\nou use enumerate.",
                "for posicao in range(len(numeros)) te dá as posições.",
                "Ao encontrar, return posicao na hora. O return -1 fica depois do laço.",
            ],
            solucao="""
            for posicao in range(len(numeros)):
                if numeros[posicao] < 0:
                    return posicao
            return -1
            """,
            nota_da_solucao="Aqui o return faz o papel do break e ainda entrega a resposta.",
            testes="""
def teste_encontra_no_meio():
    verificar(ex.resolver([5, 3, -2, -8]), 2,
              dica="A resposta é a posição do PRIMEIRO negativo.")


def teste_nao_ha_negativos():
    verificar(ex.resolver([1, 2, 3]), -1)


def teste_primeiro_ja_e_negativo():
    verificar(ex.resolver([-1]), 0)


def teste_lista_vazia():
    verificar(ex.resolver([]), -1)
""",
        ),
        Ex(
            id="A06-008", titulo="Pular os inválidos", nivel=2, tempo_min=8,
            tags=["for", "continue", "limpeza"],
            enunciado="""
            Some os valores da lista, **ignorando** os que são `None`.

            Exemplos:

                resolver([10, None, 5])  ->  15
                resolver([None, None])   ->  0
                resolver([1, 2])         ->  3

            Dados reais vêm cheios de buracos — pular o que não dá para usar é
            rotina. Você pode usar `continue` ou simplesmente um `if` positivo.
            """,
            assinatura="def resolver(valores: list):",
            dicas=[
                "Compare com None usando `is None` (e não ==).",
                "continue abandona a volta atual e vai para a próxima.",
                "if valor is None: continue — e a soma vem depois, dentro do laço.",
            ],
            solucao="""
            total = 0
            for valor in valores:
                if valor is None:
                    continue
                total += valor
            return total
            """,
            nota_da_solucao="`is None` compara identidade; para None é o jeito correto e mais rápido.",
            testes="""
def teste_ignora_um_nulo():
    verificar(ex.resolver([10, None, 5]), 15)


def teste_todos_nulos():
    verificar(ex.resolver([None, None]), 0)


def teste_sem_nulos():
    verificar(ex.resolver([1, 2]), 3)


def teste_zero_nao_e_nulo():
    verificar(ex.resolver([0, None, 0]), 0,
              dica="Zero é um valor válido — só o None deve ser pulado.")
""",
        ),
        Ex(
            id="A06-009", titulo="Achar o maior na mão", nivel=3, tempo_min=8,
            tags=["for", "acumulador", "comparacao"], requer=["A06-003"],
            enunciado="""
            Devolva o maior número da lista — **sem usar `max`**.
            Se a lista estiver vazia, devolva `None`.

            Exemplos:

                resolver([3, 9, 2])     ->  9
                resolver([-5, -1, -9])  ->  -1
                resolver([])            ->  None

            O truque: comece assumindo que o primeiro item é o maior, e vá
            corrigindo. Começar com `maior = 0` quebra em listas de negativos —
            e é por isso que este exercício é nível 3.
            """,
            assinatura="def resolver(numeros: list):",
            dicas=[
                "Trate a lista vazia primeiro e devolva None.",
                "Não comece o maior em 0: comece no primeiro item da lista.",
                "maior = numeros[0], e no laço: if numero > maior: maior = numero",
            ],
            solucao="""
            if not numeros:
                return None
            maior = numeros[0]
            for numero in numeros:
                if numero > maior:
                    maior = numero
            return maior
            """,
            nota_da_solucao="Iniciar o acumulador com um elemento real, e não com zero, é o que salva o caso dos negativos.",
            testes="""
def teste_positivos():
    verificar(ex.resolver([3, 9, 2]), 9)


def teste_so_negativos():
    verificar(ex.resolver([-5, -1, -9]), -1,
              dica="Se veio 0, você iniciou o maior em 0 em vez do primeiro item.")


def teste_lista_vazia():
    verificar(ex.resolver([]), None)


def teste_um_item():
    verificar(ex.resolver([7]), 7)


def teste_maior_no_fim():
    verificar(ex.resolver([1, 2, 100]), 100)
""",
        ),
        Ex(
            id="A06-010", titulo="A posição junto com o item", nivel=2, tempo_min=7,
            tags=["enumerate", "f-string"], requer=["A01-010"],
            enunciado="""
            Devolva uma lista de textos numerando os itens a partir de 1:

                resolver(["Moda", "Casa"])  ->  ["1. Moda", "2. Casa"]
                resolver(["Livros"])        ->  ["1. Livros"]
                resolver([])                ->  []

            `enumerate(lista)` entrega posição e item ao mesmo tempo. Ele começa
            no 0, mas aceita um segundo argumento: `enumerate(lista, 1)` começa no 1.
            """,
            assinatura="def resolver(itens: list) -> list:",
            dicas=[
                "for posicao, item in enumerate(itens): desempacota os dois de uma vez.",
                "enumerate(itens, 1) faz a contagem começar em 1.",
                'Monte cada texto com f"{posicao}. {item}" e vá acrescentando na lista.',
            ],
            solucao="""
            numerados = []
            for posicao, item in enumerate(itens, 1):
                numerados.append(f"{posicao}. {item}")
            return numerados
            """,
            nota_da_solucao="O segundo argumento do enumerate evita o clássico posicao + 1 espalhado pelo código.",
            testes="""
def teste_dois_itens():
    verificar(ex.resolver(["Moda", "Casa"]), ["1. Moda", "2. Casa"])


def teste_um_item():
    verificar(ex.resolver(["Livros"]), ["1. Livros"],
              dica="A numeração começa em 1, não em 0.")


def teste_lista_vazia():
    verificar(ex.resolver([]), [])
""",
        ),
        Ex(
            id="A06-011", titulo="Duas listas ao mesmo tempo", nivel=2, tempo_min=8,
            tags=["zip", "for"],
            enunciado="""
            Você recebe os nomes dos produtos e seus preços, em duas listas alinhadas.
            Devolva uma lista de textos no formato `"nome: preço"`, com duas casas.

            Exemplos:

                resolver(["Fone", "Capa"], [99.9, 25])  ->  ["Fone: 99.90", "Capa: 25.00"]
                resolver([], [])                        ->  []

            `zip` anda nas duas listas em paralelo e para na mais curta.
            """,
            assinatura="def resolver(nomes: list, precos: list) -> list:",
            dicas=[
                "for nome, preco in zip(nomes, precos): pega um par por volta.",
                'A formatação de duas casas é {preco:.2f} dentro da f-string.',
                'Acrescente f"{nome}: {preco:.2f}" numa lista de resultados.',
            ],
            solucao="""
            linhas = []
            for nome, preco in zip(nomes, precos):
                linhas.append(f"{nome}: {preco:.2f}")
            return linhas
            """,
            testes="""
def teste_dois_produtos():
    verificar(ex.resolver(["Fone", "Capa"], [99.9, 25]),
              ["Fone: 99.90", "Capa: 25.00"])


def teste_listas_vazias():
    verificar(ex.resolver([], []), [])


def teste_para_na_mais_curta():
    verificar(ex.resolver(["Fone", "Capa"], [10]), ["Fone: 10.00"],
              dica="zip para quando a lista mais curta acaba.")
""",
        ),
        Ex(
            id="A06-012", titulo="Percorrer um texto", nivel=2, tempo_min=7,
            tags=["for", "string", "contador"],
            enunciado="""
            Conte quantas vogais existem no texto, sem diferenciar maiúsculas
            de minúsculas.

            Exemplos:

                resolver("Aurora")  ->  4
                resolver("XYZ")     ->  0
                resolver("")        ->  0

            Um `for` sobre uma string entrega um caractere por vez.
            Considere apenas a, e, i, o, u (sem acentos).
            """,
            assinatura="def resolver(texto: str) -> int:",
            dicas=[
                "Passe o texto todo para minúsculas antes de percorrer — resolve a\\nquestão da caixa de uma vez.",
                'Você pode testar com: if letra in "aeiou"',
                "Um contador iniciado em 0 antes do laço, incrementado dentro do if.",
            ],
            solucao="""
            quantas = 0
            for letra in texto.lower():
                if letra in "aeiou":
                    quantas += 1
            return quantas
            """,
            nota_da_solucao="Normalizar a caixa uma vez, antes do laço, é mais barato do que comparar duas vezes por letra.",
            testes="""
def teste_com_maiuscula():
    verificar(ex.resolver("Aurora"), 4)


def teste_sem_vogais():
    verificar(ex.resolver("XYZ"), 0)


def teste_texto_vazio():
    verificar(ex.resolver(""), 0)


def teste_tudo_maiusculo():
    verificar(ex.resolver("AEIOU"), 5,
              dica="Converta para minúsculas antes de comparar.")
""",
        ),
        Ex(
            id="A06-013", titulo="Tabuada", nivel=3, tempo_min=9,
            tags=["for", "laco-aninhado", "range"],
            enunciado="""
            Devolva uma lista com todos os produtos da tabuada, de `1 x 1` até
            `n x n`, lidos linha por linha.

            Exemplos:

                resolver(2)  ->  [1, 2, 2, 4]
                resolver(3)  ->  [1, 2, 3, 2, 4, 6, 3, 6, 9]
                resolver(1)  ->  [1]

            Para n=2 a leitura é: 1x1, 1x2, 2x1, 2x2.

            Isso pede um laço **dentro** do outro. O de fora anda nas linhas,
            o de dentro anda nas colunas — e o de dentro roda inteiro a cada
            volta do de fora.
            """,
            assinatura="def resolver(n: int) -> list:",
            dicas=[
                "Dois for encaixados, cada um com seu range(1, n + 1).",
                "A lista de resultados é criada antes dos dois laços.",
                "O append fica no laço de dentro, com a multiplicação das duas variáveis.",
            ],
            solucao="""
            resultados = []
            for linha in range(1, n + 1):
                for coluna in range(1, n + 1):
                    resultados.append(linha * coluna)
            return resultados
            """,
            nota_da_solucao="O laço interno completa todas as voltas antes de o externo avançar uma — daí n × n resultados.",
            testes="""
def teste_tabuada_de_dois():
    verificar(ex.resolver(2), [1, 2, 2, 4])


def teste_tabuada_de_tres():
    verificar(ex.resolver(3), [1, 2, 3, 2, 4, 6, 3, 6, 9])


def teste_tabuada_de_um():
    verificar(ex.resolver(1), [1])


def teste_quantidade_de_resultados():
    verificar(len(ex.resolver(4)), 16, nome="tamanho do resultado",
              dica="São n × n produtos no total.")
""",
        ),
        Ex(
            id="A06-014", titulo="Contagem regressiva", nivel=2, tempo_min=7,
            tags=["while", "lista"], requer=["A06-006"],
            enunciado="""
            Devolva a contagem regressiva de n até 1, como lista.

            Exemplos:

                resolver(3)  ->  [3, 2, 1]
                resolver(1)  ->  [1]
                resolver(0)  ->  []

            Use `while`. (Com `range` daria em uma linha — mas a ideia aqui é
            controlar o contador na mão.)
            """,
            assinatura="def resolver(n: int) -> list:",
            dicas=[
                "Comece com uma lista vazia e um contador valendo n.",
                "O laço continua enquanto o contador for >= 1.",
                "Dentro: acrescente o contador na lista e depois diminua 1 dele.",
            ],
            solucao="""
            numeros = []
            atual = n
            while atual >= 1:
                numeros.append(atual)
                atual -= 1
            return numeros
            """,
            testes="""
def teste_de_tres_a_um():
    verificar(ex.resolver(3), [3, 2, 1])


def teste_so_um():
    verificar(ex.resolver(1), [1])


def teste_zero_nao_conta():
    verificar(ex.resolver(0), [])


def teste_numero_maior():
    verificar(ex.resolver(5), [5, 4, 3, 2, 1])
""",
        ),
        Ex(
            id="A06-015", titulo="FizzBuzz", nivel=3, tempo_min=10,
            tags=["for", "resto", "elif", "classico"], requer=["A04-003", "A06-002"],
            enunciado="""
            O exercício mais famoso de entrevista de programação.

            Para cada número de 1 a n, devolva na lista:

                "FizzBuzz"   se for divisível por 3 E por 5
                "Fizz"       se for divisível só por 3
                "Buzz"       se for divisível só por 5
                o próprio número (como int)  nos demais casos

            Exemplo:

                resolver(15)
                ->  [1, 2, "Fizz", 4, "Buzz", "Fizz", 7, 8, "Fizz", "Buzz",
                     11, "Fizz", 13, 14, "FizzBuzz"]

            A pegadinha é a ordem: se você testar "divisível por 3" primeiro,
            o 15 vira "Fizz" e nunca chega a "FizzBuzz". O caso mais específico
            vem sempre antes.
            """,
            assinatura="def resolver(n: int) -> list:",
            dicas=[
                "Percorra de 1 até n e decida o que acrescentar em cada volta.",
                "Teste a condição mais restritiva primeiro: divisível por 3 E por 5.",
                "numero % 3 == 0 and numero % 5 == 0 — esse if vem antes dos outros dois.",
            ],
            solucao="""
            resultado = []
            for numero in range(1, n + 1):
                if numero % 3 == 0 and numero % 5 == 0:
                    resultado.append("FizzBuzz")
                elif numero % 3 == 0:
                    resultado.append("Fizz")
                elif numero % 5 == 0:
                    resultado.append("Buzz")
                else:
                    resultado.append(numero)
            return resultado
            """,
            nota_da_solucao="Ordenar os elif do mais específico para o mais geral é o que o exercício realmente testa.",
            testes="""
def teste_ate_cinco():
    verificar(ex.resolver(5), [1, 2, "Fizz", 4, "Buzz"])


def teste_pega_o_quinze():
    verificar(ex.resolver(15)[-1], "FizzBuzz", nome="último item",
              dica="Se veio 'Fizz', o teste de divisível por 3 está vindo antes.")


def teste_lista_completa():
    verificar(
        ex.resolver(15),
        [1, 2, "Fizz", 4, "Buzz", "Fizz", 7, 8, "Fizz", "Buzz",
         11, "Fizz", 13, 14, "FizzBuzz"],
    )


def teste_numeros_seguem_inteiros():
    verificar(ex.resolver(2), [1, 2],
              dica="Os números que não são Fizz nem Buzz entram como int, não como texto.")


def teste_zero():
    verificar(ex.resolver(0), [])
""",
        ),
        Ex(
            id="A06-016", titulo="Total do carrinho", nivel=3, tempo_min=10,
            tags=["zip", "acumulador", "arredondamento", "composicao"],
            requer=["A06-011", "A06-003"],
            enunciado="""
            Fechando o módulo com algo que a loja realmente faria.

            Você recebe três listas alinhadas: preços unitários, quantidades e
            descontos (em fração, `0.1` = 10%). Devolva o total do carrinho,
            arredondado para duas casas.

            O total de cada item é: `preço × quantidade × (1 - desconto)`.

            Exemplos:

                resolver([100, 50], [1, 2], [0, 0.1])  ->  190.0
                resolver([10], [3], [0])               ->  30.0
                resolver([], [], [])                   ->  0.0

            Confira o primeiro: 100×1×1 = 100, mais 50×2×0.9 = 90, dá 190.
            """,
            assinatura="def resolver(precos: list, quantidades: list, descontos: list) -> float:",
            dicas=[
                "zip aceita mais de duas listas: zip(a, b, c) entrega trios.",
                "Acumule o total item a item, e arredonde só no fim.",
                "Arredondar dentro do laço acumula erro de centavos — deixe o round\\npara a linha do return.",
            ],
            solucao="""
            total = 0
            for preco, quantidade, desconto in zip(precos, quantidades, descontos):
                total += preco * quantidade * (1 - desconto)
            return round(total, 2)
            """,
            nota_da_solucao="Arredondar uma vez, no fim, em vez de a cada item — a diferença aparece em carrinhos grandes.",
            testes="""
def teste_dois_itens_com_desconto():
    verificar(ex.resolver([100, 50], [1, 2], [0, 0.1]), 190.0)


def teste_item_unico():
    verificar(ex.resolver([10], [3], [0]), 30.0)


def teste_carrinho_vazio():
    verificar(ex.resolver([], [], []), 0.0)


def teste_desconto_total():
    verificar(ex.resolver([100], [1], [1]), 0.0)


def teste_valores_quebrados():
    verificar(ex.resolver([19.99, 5.55], [3, 2], [0.15, 0]), 62.07)
""",
        ),
    ],
)

MODULOS = [A04, A05, A06]
