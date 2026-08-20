"""Bloco A, módulos 1 a 3: primeiros passos, números e strings."""

from autoria.modelo import Exercicio as Ex
from autoria.modelo import Modulo

# --------------------------------------------------------------------------- #
# A01 — Primeiros passos
# --------------------------------------------------------------------------- #

A01 = Modulo(
    id="A01",
    titulo="Módulo A1 — Primeiros passos",
    resumo="Mostrar, devolver, guardar. As três coisas que todo programa faz.",
    teoria="""
## O que você vai aprender

Um programa faz três coisas o tempo todo: **calcula** um valor, **guarda** esse valor
em algum lugar e **entrega** o resultado para alguém. Este módulo é sobre as três.

### print não é return

É a confusão número um de quem começa, e vale resolver logo:

```python
def mostrar():
    print("Olá")        # escreve na tela e devolve None

def devolver():
    return "Olá"        # não escreve nada; entrega o texto para quem chamou
```

`print` fala com o **ser humano** que está olhando o terminal.
`return` fala com o **resto do programa**.

```python
x = mostrar()     # aparece "Olá" na tela, e x fica valendo None
y = devolver()    # nada aparece na tela, e y fica valendo "Olá"
```

Neste curso quase todo exercício pede `return`, porque é assim que o corretor
consegue conferir o seu resultado. Quando o enunciado pedir `print`, ele diz isso
com todas as letras.

### Variáveis são etiquetas

```python
preco = 49.90
```

Não existe "caixinha" — `preco` é uma etiqueta colada no valor `49.90`. Colar a
etiqueta em outro valor depois é normal: `preco = 39.90`.

### Os quatro tipos do começo

| tipo | o que é | exemplo |
|---|---|---|
| `int` | número inteiro | `42`, `-7` |
| `float` | número com vírgula (que em Python é ponto) | `3.14`, `49.9` |
| `str` | texto, sempre entre aspas | `"Aurora"`, `'oi'` |
| `bool` | verdadeiro ou falso | `True`, `False` |

`type(valor)` diz qual é o tipo. `int("42")` e `str(42)` convertem de um para outro —
e **`"3" + "4"` dá `"34"`, não `7`**, porque para texto o `+` é grudar.

### f-string: o jeito moderno de montar texto

```python
nome = "Ana"
idade = 30
f"{nome} tem {idade} anos"     # 'Ana tem 30 anos'
```

O `f` antes da aspa é obrigatório. Dentro das chaves vai qualquer expressão Python.
""",
    exercicios=[
        Ex(
            id="A01-001", titulo="Olá, Aurora", nivel=1, tempo_min=3,
            tags=["print", "primeiro-programa"],
            enunciado="""
            O programa mais antigo do mundo, na versão da nossa loja.

            Faça `resolver()` **imprimir** na tela exatamente:

                Olá, Aurora!

            Repare que aqui o enunciado pede `print`, não `return` — é o único
            módulo em que isso acontece com frequência.
            """,
            assinatura="def resolver() -> None:",
            dicas=[
                "print é uma função: o texto vai entre parênteses.",
                "Texto em Python fica entre aspas: print(\"algum texto\").",
                'A linha inteira é: print("Olá, Aurora!")',
            ],
            solucao='    print("Olá, Aurora!")',
            nota_da_solucao="print escreve na tela e devolve None — não é o mesmo que return.",
            testes="""
def teste_imprime_a_saudacao():
    verificar(t.saida_de(ex.resolver), "Olá, Aurora!", nome="texto impresso")
""",
        ),
        Ex(
            id="A01-002", titulo="Três linhas na tela", nivel=1, tempo_min=3,
            tags=["print"], requer=["A01-001"],
            enunciado="""
            Cada `print` escreve uma linha e pula para a próxima.

            Faça `resolver()` imprimir estas três linhas, nesta ordem:

                Loja Aurora
                Catálogo 2026
                Bem-vindo!
            """,
            assinatura="def resolver() -> None:",
            dicas=[
                "Três linhas na tela = três chamadas de print, uma embaixo da outra.",
                "Todas com a mesma indentação (4 espaços), dentro da função.",
                'print("Loja Aurora") e depois as outras duas, no mesmo recuo.',
            ],
            solucao="""
            print("Loja Aurora")
            print("Catálogo 2026")
            print("Bem-vindo!")
            """,
            testes="""
def teste_imprime_as_tres_linhas():
    verificar(
        t.saida_de(ex.resolver),
        "Loja Aurora\\nCatálogo 2026\\nBem-vindo!",
        nome="texto impresso",
    )
""",
        ),
        Ex(
            id="A01-003", titulo="Devolver em vez de mostrar", nivel=1, tempo_min=4,
            tags=["return", "string"], requer=["A01-001"],
            enunciado="""
            Agora o contrário: nada deve aparecer na tela.

            Faça `resolver()` **devolver** o texto `Olá, Aurora!` — sem imprimir.

            Exemplo de como sua função será usada:

                mensagem = resolver()
                # mensagem passa a valer "Olá, Aurora!"

            Se você usar `print` aqui, a função devolve `None` e o teste reprova.
            Essa diferença é o assunto do módulo inteiro.
            """,
            assinatura="def resolver() -> str:",
            dicas=[
                "return entrega o valor para quem chamou a função; print só desenha na tela.",
                "A palavra return vem antes do valor, sem parênteses obrigatórios.",
                'return "Olá, Aurora!"',
            ],
            solucao='    return "Olá, Aurora!"',
            nota_da_solucao="Sem print: quem chamou a função recebe o texto e decide o que fazer com ele.",
            testes="""
def teste_devolve_a_saudacao():
    verificar(ex.resolver(), "Olá, Aurora!")


def teste_nao_imprime_nada():
    verificar(t.saida_de(ex.resolver), "", nome="texto impresso",
              dica="Este exercício é sobre return. Tire o print.")
""",
        ),
        Ex(
            id="A01-004", titulo="Guardar em uma variável", nivel=1, tempo_min=4,
            tags=["variavel", "return"],
            enunciado="""
            Guarde o nome da loja em uma variável chamada `loja` e devolva essa variável.

            O resultado deve ser o texto `Aurora`.

            Parece o exercício anterior, e é de propósito: a diferença é que agora o
            valor passa por uma variável antes de sair. Programas reais fazem isso o
            tempo todo — calculam, guardam, devolvem.
            """,
            assinatura="def resolver() -> str:",
            dicas=[
                "Criar uma variável é só escrever nome = valor.",
                "São duas linhas: uma que guarda, outra que devolve.",
                'loja = "Aurora" e depois return loja',
            ],
            solucao="""
            loja = "Aurora"
            return loja
            """,
            testes="""
def teste_devolve_o_nome_da_loja():
    verificar(ex.resolver(), "Aurora")
""",
        ),
        Ex(
            id="A01-005", titulo="Somar dois números", nivel=1, tempo_min=4,
            tags=["parametro", "aritmetica"],
            enunciado="""
            Sua função vai receber dois valores de fora — os **parâmetros** `a` e `b`.

            Devolva a soma dos dois.

            Exemplos:

                resolver(2, 3)      ->  5
                resolver(10, -4)    ->  6
                resolver(1.5, 0.5)  ->  2.0

            Repare que a função precisa funcionar para qualquer par de números,
            não só para os do exemplo. É por isso que ela recebe parâmetros.
            """,
            assinatura="def resolver(a, b):",
            dicas=[
                "a e b já existem dentro da função — você não precisa criá-los.",
                "O sinal de somar em Python é +, como na calculadora.",
                "return a + b",
            ],
            solucao="    return a + b",
            testes="""
def teste_soma_inteiros():
    verificar(ex.resolver(2, 3), 5)


def teste_soma_com_negativo():
    verificar(ex.resolver(10, -4), 6)


def teste_soma_com_virgula():
    verificar(ex.resolver(1.5, 0.5), 2.0)


def teste_soma_zeros():
    verificar(ex.resolver(0, 0), 0)
""",
        ),
        Ex(
            id="A01-006", titulo="Qual é o tipo", nivel=2, tempo_min=5,
            tags=["tipos", "type"],
            enunciado="""
            `type(valor)` responde de que tipo é um valor:

                type(42)        ->  <class 'int'>
                type(3.14)      ->  <class 'float'>
                type("Aurora")  ->  <class 'str'>
                type(True)      ->  <class 'bool'>

            Devolva o tipo do valor recebido.

            Exemplos:

                resolver(42)        ->  int
                resolver("Aurora")  ->  str
            """,
            assinatura="def resolver(valor):",
            dicas=[
                "A resposta é o próprio resultado de type(...), não um texto.",
                "Não escreva return \"int\" — isso é o texto 'int', não o tipo int.",
                "return type(valor)",
            ],
            solucao="    return type(valor)",
            nota_da_solucao="type devolve a classe do valor; em Python até os tipos são valores.",
            testes="""
def teste_inteiro():
    verificar(ex.resolver(42), int)


def teste_decimal():
    verificar(ex.resolver(3.14), float)


def teste_texto():
    verificar(ex.resolver("Aurora"), str)


def teste_booleano():
    verificar(ex.resolver(True), bool)
""",
        ),
        Ex(
            id="A01-007", titulo="De texto para número", nivel=2, tempo_min=5,
            tags=["conversao", "int"],
            enunciado="""
            Um formulário sempre entrega números como **texto**: `"7"`, e não `7`.
            E texto não soma — gruda:

                "7" + "3"    ->  "73"
                int("7") + int("3")  ->  10

            Você recebe duas quantidades em texto. Devolva a soma delas como número.

            Exemplos:

                resolver("7", "3")     ->  10
                resolver("100", "25")  ->  125
            """,
            assinatura="def resolver(a: str, b: str) -> int:",
            dicas=[
                "int(\"7\") transforma o texto \"7\" no número 7.",
                "Converta cada um dos dois antes de somar.",
                "return int(a) + int(b)",
            ],
            solucao="    return int(a) + int(b)",
            nota_da_solucao="Converter na entrada é a regra: dado de fora chega como texto até prova em contrário.",
            testes="""
def teste_soma_simples():
    verificar(ex.resolver("7", "3"), 10)


def teste_numeros_maiores():
    verificar(ex.resolver("100", "25"), 125)


def teste_devolve_numero_e_nao_texto():
    verificar(ex.resolver("2", "2"), 4,
              dica="Se o resultado for '22', você somou os textos sem converter.")
""",
        ),
        Ex(
            id="A01-008", titulo="De número para texto", nivel=2, tempo_min=5,
            tags=["conversao", "str"],
            enunciado="""
            O caminho de volta: `str(42)` devolve o texto `"42"`.

            Você recebe o número de um pedido. Devolva o texto no formato:

                Pedido nº 1042

            Exemplos:

                resolver(1042)  ->  "Pedido nº 1042"
                resolver(7)     ->  "Pedido nº 7"

            Nesta versão, monte o texto **grudando pedaços com `+`** — que é onde
            a conversão se torna necessária. (No exercício A01-010 você vai reescrever
            isso de um jeito bem melhor.)
            """,
            assinatura="def resolver(numero: int) -> str:",
            dicas=[
                'Texto gruda com +, mas "abc" + 42 dá erro: os dois lados precisam ser texto.',
                "str(numero) transforma o número em texto.",
                'return "Pedido nº " + str(numero)',
            ],
            solucao='    return "Pedido nº " + str(numero)',
            testes="""
def teste_numero_grande():
    verificar(ex.resolver(1042), "Pedido nº 1042")


def teste_numero_pequeno():
    verificar(ex.resolver(7), "Pedido nº 7")
""",
        ),
        Ex(
            id="A01-009", titulo="Nome completo", nivel=1, tempo_min=4,
            tags=["string", "concatenacao"],
            enunciado="""
            Junte nome e sobrenome com um espaço no meio.

            Exemplos:

                resolver("Ana", "Souza")       ->  "Ana Souza"
                resolver("Carlos", "Oliveira") ->  "Carlos Oliveira"

            Cuidado com o espaço: `nome + sobrenome` daria `"AnaSouza"`.
            """,
            assinatura="def resolver(nome: str, sobrenome: str) -> str:",
            dicas=[
                "O espaço é um caractere como outro qualquer: \" \".",
                "São três pedaços grudados: nome, espaço, sobrenome.",
                'return nome + " " + sobrenome',
            ],
            solucao='    return nome + " " + sobrenome',
            testes="""
def teste_nome_e_sobrenome():
    verificar(ex.resolver("Ana", "Souza"), "Ana Souza")


def teste_outro_nome():
    verificar(ex.resolver("Carlos", "Oliveira"), "Carlos Oliveira")
""",
        ),
        Ex(
            id="A01-010", titulo="A mesma frase com f-string", nivel=2, tempo_min=6,
            tags=["f-string", "string"], requer=["A01-008"],
            enunciado="""
            Grudar texto com `+` funciona, mas fica ilegível rápido — e obriga a
            converter tudo na mão. A f-string resolve os dois problemas:

                nome = "Ana"
                total = 3
                f"{nome} fez {total} pedidos"    ->  'Ana fez 3 pedidos'

            Dentro das chaves vai qualquer valor, de qualquer tipo, sem `str(...)`.

            Devolva, usando f-string:

                resolver("Ana", 3)     ->  "Ana fez 3 pedidos"
                resolver("Bruno", 12)  ->  "Bruno fez 12 pedidos"
            """,
            assinatura="def resolver(nome: str, pedidos: int) -> str:",
            dicas=[
                "O f vem colado na aspa de abertura: f\"...\".",
                "Os nomes das variáveis vão dentro de chaves, sem aspas por dentro.",
                'return f"{nome} fez {pedidos} pedidos"',
            ],
            solucao='    return f"{nome} fez {pedidos} pedidos"',
            nota_da_solucao="A f-string converte cada valor sozinha — o str() do exercício anterior some.",
            testes="""
def teste_frase_montada():
    verificar(ex.resolver("Ana", 3), "Ana fez 3 pedidos")


def teste_outro_cliente():
    verificar(ex.resolver("Bruno", 12), "Bruno fez 12 pedidos")
""",
        ),
        Ex(
            id="A01-011", titulo="Média de três notas", nivel=2, tempo_min=6,
            tags=["aritmetica", "precedencia"],
            enunciado="""
            Devolva a média aritmética de três avaliações.

            Exemplos:

                resolver(10, 8, 6)  ->  8.0
                resolver(5, 5, 5)   ->  5.0
                resolver(4, 5, 5)   ->  4.666666666666667

            Atenção à ordem das operações: `a + b + c / 3` **não** é a média —
            a divisão acontece antes da soma. Você vai precisar de parênteses.
            """,
            assinatura="def resolver(a, b, c):",
            dicas=[
                "Multiplicação e divisão acontecem antes de soma e subtração.",
                "Parênteses forçam a soma a acontecer primeiro.",
                "return (a + b + c) / 3",
            ],
            solucao="    return (a + b + c) / 3",
            nota_da_solucao="A barra / sempre devolve float, mesmo quando a divisão é exata: 15/3 dá 5.0.",
            testes="""
def teste_media_simples():
    verificar(ex.resolver(10, 8, 6), 8.0)


def teste_media_de_iguais():
    verificar(ex.resolver(5, 5, 5), 5.0)


def teste_media_com_dizima():
    verificar(ex.resolver(4, 5, 5), 14 / 3,
              dica="Sem parênteses, o Python divide c por 3 antes de somar.")
""",
        ),
        Ex(
            id="A01-012", titulo="Trocar dois valores de lugar", nivel=2, tempo_min=5,
            tags=["tupla", "desempacotamento"],
            enunciado="""
            Devolva os dois valores recebidos, na ordem invertida.

            Exemplos:

                resolver(1, 2)          ->  (2, 1)
                resolver("a", "b")      ->  ("b", "a")

            O resultado é uma **tupla**: dois valores viajando juntos, escritos entre
            parênteses. Em Python, `return b, a` já cria a tupla — os parênteses são
            opcionais.
            """,
            assinatura="def resolver(a, b):",
            dicas=[
                "Você não precisa de uma variável temporária: dá para devolver os dois de uma vez.",
                "Uma vírgula entre dois valores já forma uma tupla.",
                "return b, a",
            ],
            solucao="    return b, a",
            nota_da_solucao="A mesma sintaxe troca variáveis no lugar: a, b = b, a.",
            testes="""
def teste_troca_numeros():
    verificar(ex.resolver(1, 2), (2, 1))


def teste_troca_textos():
    verificar(ex.resolver("a", "b"), ("b", "a"))


def teste_troca_tipos_diferentes():
    verificar(ex.resolver(10, "dez"), ("dez", 10))
""",
        ),
    ],
)


# --------------------------------------------------------------------------- #
# A02 — Números e operadores
# --------------------------------------------------------------------------- #

A02 = Modulo(
    id="A02",
    titulo="Módulo A2 — Números e operadores",
    resumo="Contas que aparecem em todo relatório: porcentagem, arredondamento, resto.",
    teoria="""
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
""",
    exercicios=[
        Ex(
            id="A02-001", titulo="Área do retângulo", nivel=1, tempo_min=3,
            tags=["aritmetica"],
            enunciado="""
            Devolva a área de um retângulo a partir da largura e da altura.

            Exemplos:

                resolver(3, 4)      ->  12
                resolver(2.5, 4)    ->  10.0
            """,
            assinatura="def resolver(largura, altura):",
            dicas=[
                "Área de retângulo é largura vezes altura.",
                "O sinal de multiplicar em Python é *.",
                "return largura * altura",
            ],
            solucao="    return largura * altura",
            testes="""
def teste_area_inteira():
    verificar(ex.resolver(3, 4), 12)


def teste_area_com_decimal():
    verificar(ex.resolver(2.5, 4), 10.0)
""",
        ),
        Ex(
            id="A02-002", titulo="Par ou ímpar", nivel=2, tempo_min=5,
            tags=["resto", "booleano"],
            enunciado="""
            Devolva `True` se o número for par e `False` se for ímpar.

            Exemplos:

                resolver(4)   ->  True
                resolver(7)   ->  False
                resolver(0)   ->  True
                resolver(-3)  ->  False

            Um número é par quando o resto da divisão por 2 é zero.
            E não precisa de `if`: a comparação `== 0` já produz `True` ou `False`.
            """,
            assinatura="def resolver(numero: int) -> bool:",
            dicas=[
                "O operador % devolve o resto: 7 % 2 é 1, e 4 % 2 é 0.",
                "Comparar com == já gera um booleano; você pode devolver a comparação inteira.",
                "return numero % 2 == 0",
            ],
            solucao="    return numero % 2 == 0",
            nota_da_solucao="Devolver a comparação direto evita o if/else desnecessário — comum e mais legível.",
            testes="""
def teste_par():
    verificar(ex.resolver(4), True)


def teste_impar():
    verificar(ex.resolver(7), False)


def teste_zero_e_par():
    verificar(ex.resolver(0), True)


def teste_negativo_impar():
    verificar(ex.resolver(-3), False)
""",
        ),
        Ex(
            id="A02-003", titulo="As duas divisões", nivel=2, tempo_min=6,
            tags=["divisao", "tupla"],
            enunciado="""
            Python tem duas divisões, e a diferença aparece o tempo todo:

                7 / 2   ->  3.5   (divisão comum, sempre float)
                7 // 2  ->  3     (divisão inteira, joga fora a parte quebrada)

            Devolva uma tupla com as duas, nesta ordem: `(divisão comum, divisão inteira)`.

            Exemplos:

                resolver(7, 2)   ->  (3.5, 3)
                resolver(10, 5)  ->  (2.0, 2)
            """,
            assinatura="def resolver(a, b):",
            dicas=[
                "São dois cálculos com os mesmos operandos, só muda o operador.",
                "Uma vírgula entre os dois resultados já monta a tupla.",
                "return a / b, a // b",
            ],
            solucao="    return a / b, a // b",
            testes="""
def teste_divisao_com_resto():
    verificar(ex.resolver(7, 2), (3.5, 3))


def teste_divisao_exata():
    verificar(ex.resolver(10, 5), (2.0, 2))


def teste_dividendo_menor():
    verificar(ex.resolver(3, 4), (0.75, 0))
""",
        ),
        Ex(
            id="A02-004", titulo="Elevar ao quadrado", nivel=1, tempo_min=3,
            tags=["potencia"],
            enunciado="""
            Devolva o número elevado ao quadrado.

            Exemplos:

                resolver(5)   ->  25
                resolver(1.5) ->  2.25
                resolver(-3)  ->  9

            O operador de potência é `**` — dois asteriscos.
            """,
            assinatura="def resolver(numero):",
            dicas=[
                "Elevar ao quadrado é elevar à potência 2.",
                "O operador é ** (não confunda com *, que é multiplicação).",
                "return numero ** 2",
            ],
            solucao="    return numero ** 2",
            testes="""
def teste_quadrado_inteiro():
    verificar(ex.resolver(5), 25)


def teste_quadrado_decimal():
    verificar(ex.resolver(1.5), 2.25)


def teste_quadrado_de_negativo():
    verificar(ex.resolver(-3), 9)
""",
        ),
        Ex(
            id="A02-005", titulo="Arredondar o preço", nivel=2, tempo_min=5,
            tags=["round", "dinheiro"],
            enunciado="""
            Dinheiro tem duas casas decimais. Devolva o valor arredondado para centavos.

            Exemplos:

                resolver(49.876)   ->  49.88
                resolver(10.0)     ->  10.0
                resolver(3.14159)  ->  3.14
            """,
            assinatura="def resolver(valor: float) -> float:",
            dicas=[
                "round(valor) arredonda para inteiro; ele aceita um segundo argumento.",
                "O segundo argumento é quantas casas decimais manter.",
                "return round(valor, 2)",
            ],
            solucao="    return round(valor, 2)",
            testes="""
def teste_arredonda_para_cima():
    verificar(ex.resolver(49.876), 49.88)


def teste_ja_esta_redondo():
    verificar(ex.resolver(10.0), 10.0)


def teste_arredonda_para_baixo():
    verificar(ex.resolver(3.14159), 3.14)
""",
        ),
        Ex(
            id="A02-006", titulo="Minutos e segundos", nivel=3, tempo_min=7,
            tags=["divmod", "resto"],
            enunciado="""
            Uma sessão do site durou N segundos. Devolva quantos minutos inteiros e
            quantos segundos sobraram, como uma tupla `(minutos, segundos)`.

            Exemplos:

                resolver(125)  ->  (2, 5)      # 2 minutos e 5 segundos
                resolver(60)   ->  (1, 0)
                resolver(45)   ->  (0, 45)
                resolver(3661) ->  (61, 1)

            Dá para fazer com `//` e `%` separados — ou com `divmod`, que devolve
            os dois de uma vez. Os dois caminhos passam no teste.
            """,
            assinatura="def resolver(total_de_segundos: int) -> tuple[int, int]:",
            dicas=[
                "Minutos inteiros: quantas vezes 60 cabe no total. Segundos: o que sobra.",
                "// dá o quociente inteiro e % dá o resto — exatamente o que você precisa.",
                "return divmod(total_de_segundos, 60)  # ou: return t // 60, t % 60",
            ],
            solucao="    return divmod(total_de_segundos, 60)",
            nota_da_solucao="divmod faz a divisão inteira e o resto numa passada só.",
            testes="""
def teste_minutos_e_sobra():
    verificar(ex.resolver(125), (2, 5))


def teste_minuto_exato():
    verificar(ex.resolver(60), (1, 0))


def teste_menos_de_um_minuto():
    verificar(ex.resolver(45), (0, 45))


def teste_mais_de_uma_hora():
    verificar(ex.resolver(3661), (61, 1))
""",
        ),
        Ex(
            id="A02-007", titulo="Quanto por cento", nivel=2, tempo_min=6,
            tags=["porcentagem", "round"],
            enunciado="""
            Devolva quantos por cento `parte` representa de `total`, arredondado
            para uma casa decimal.

            Exemplos:

                resolver(25, 200)   ->  12.5
                resolver(1, 3)      ->  33.3
                resolver(200, 200)  ->  100.0

            Porcentagem é a fração multiplicada por 100.
            """,
            assinatura="def resolver(parte, total) -> float:",
            dicas=[
                "Primeiro a fração (parte dividida por total), depois vezes 100.",
                "round(x, 1) deixa uma casa decimal.",
                "return round(parte / total * 100, 1)",
            ],
            solucao="    return round(parte / total * 100, 1)",
            testes="""
def teste_fracao_simples():
    verificar(ex.resolver(25, 200), 12.5)


def teste_dizima_arredondada():
    verificar(ex.resolver(1, 3), 33.3)


def teste_cem_por_cento():
    verificar(ex.resolver(200, 200), 100.0)
""",
        ),
        Ex(
            id="A02-008", titulo="Maior, menor e diferença", nivel=2, tempo_min=6,
            tags=["min-max", "abs", "tupla"],
            enunciado="""
            Você recebe três valores de venda. Devolva a tupla
            `(maior, menor, diferença entre eles)`.

            A diferença nunca é negativa.

            Exemplos:

                resolver(10, 3, 7)     ->  (10, 3, 7)
                resolver(-5, -1, -9)   ->  (-1, -9, 8)
                resolver(4, 4, 4)      ->  (4, 4, 0)

            `max(...)` e `min(...)` aceitam vários argumentos de uma vez.
            """,
            assinatura="def resolver(a, b, c):",
            dicas=[
                "max e min aceitam quantos argumentos você quiser: max(a, b, c).",
                "A diferença é o maior menos o menor — que nunca dá negativo.",
                "Calcule maior e menor em variáveis e depois devolva os três valores.",
            ],
            solucao="""
            maior = max(a, b, c)
            menor = min(a, b, c)
            return maior, menor, maior - menor
            """,
            nota_da_solucao="Guardar em variáveis evita chamar max e min duas vezes cada.",
            testes="""
def teste_positivos():
    verificar(ex.resolver(10, 3, 7), (10, 3, 7))


def teste_negativos():
    verificar(ex.resolver(-5, -1, -9), (-1, -9, 8))


def teste_todos_iguais():
    verificar(ex.resolver(4, 4, 4), (4, 4, 0))
""",
        ),
        Ex(
            id="A02-009", titulo="Média ponderada", nivel=3, tempo_min=8,
            tags=["aritmetica", "media-ponderada"],
            enunciado="""
            Na média ponderada cada nota tem um peso diferente. A conta é:

                soma de (nota × peso)  ÷  soma dos pesos

            Devolva a média ponderada de três notas, arredondada para duas casas.

            Exemplos:

                resolver(10, 1, 8, 1, 6, 2)   ->  7.5
                resolver(10, 2, 5, 1, 5, 1)   ->  7.5
                resolver(7, 1, 7, 1, 7, 1)    ->  7.0

            Os parâmetros vêm em pares: nota, peso, nota, peso, nota, peso.
            """,
            assinatura="def resolver(n1, p1, n2, p2, n3, p3) -> float:",
            dicas=[
                "Em cima: cada nota multiplicada pelo seu peso, tudo somado.",
                "Embaixo: a soma dos três pesos. Não use 3 — os pesos podem não somar 3.",
                "Monte o numerador e o denominador em variáveis separadas antes de dividir.",
            ],
            solucao="""
            soma_ponderada = n1 * p1 + n2 * p2 + n3 * p3
            soma_dos_pesos = p1 + p2 + p3
            return round(soma_ponderada / soma_dos_pesos, 2)
            """,
            nota_da_solucao="Dividir pelo total de pesos, e não por 3, é o que diferencia a ponderada da simples.",
            testes="""
def teste_peso_dobrado_na_ultima():
    verificar(ex.resolver(10, 1, 8, 1, 6, 2), 7.5)


def teste_peso_dobrado_na_primeira():
    verificar(ex.resolver(10, 2, 5, 1, 5, 1), 7.5)


def teste_pesos_iguais_vira_media_simples():
    verificar(ex.resolver(7, 1, 7, 1, 7, 1), 7.0)


def teste_pesos_que_nao_somam_tres():
    verificar(ex.resolver(10, 5, 0, 5, 10, 10), 7.5,
              dica="Divida pela soma dos pesos, não por 3.")
""",
        ),
        Ex(
            id="A02-010", titulo="Juros compostos", nivel=3, tempo_min=8,
            tags=["potencia", "financeiro"],
            enunciado="""
            Um valor rende juros compostos quando os juros de cada período passam a
            render junto no período seguinte. A fórmula é:

                montante = capital × (1 + taxa) ** periodos

            A taxa vem em porcentagem (por exemplo, `10` para 10% ao mês).

            Devolva o montante final arredondado para duas casas.

            Exemplos:

                resolver(1000, 10, 2)   ->  1210.0
                resolver(1000, 10, 0)   ->  1000.0
                resolver(500, 1, 12)    ->  563.41
            """,
            assinatura="def resolver(capital, taxa_percentual, periodos) -> float:",
            dicas=[
                "A taxa chega em porcentagem: 10 precisa virar 0.10 antes de entrar na fórmula.",
                "Dividir a taxa por 100 é o primeiro passo; o ** vem depois.",
                "Guarde a taxa convertida numa variável para a fórmula ficar legível.",
            ],
            solucao="""
            taxa = taxa_percentual / 100
            montante = capital * (1 + taxa) ** periodos
            return round(montante, 2)
            """,
            nota_da_solucao="Com 0 períodos o expoente zera e o montante é o próprio capital — bom teste de sanidade.",
            testes="""
def teste_dois_periodos():
    verificar(ex.resolver(1000, 10, 2), 1210.0)


def teste_sem_periodo_nao_rende():
    verificar(ex.resolver(1000, 10, 0), 1000.0)


def teste_um_por_cento_ao_ano():
    verificar(ex.resolver(500, 1, 12), 563.41)


def teste_taxa_zero():
    verificar(ex.resolver(250, 0, 5), 250.0)
""",
        ),
    ],
)


# --------------------------------------------------------------------------- #
# A03 — Strings
# --------------------------------------------------------------------------- #

A03 = Modulo(
    id="A03",
    titulo="Módulo A3 — Strings",
    resumo="Texto é metade do trabalho com dados: nomes, e-mails, categorias, CEPs.",
    teoria="""
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
""",
    exercicios=[
        Ex(
            id="A03-001", titulo="Tamanho do texto", nivel=1, tempo_min=3,
            tags=["len"],
            enunciado="""
            Devolva quantos caracteres tem o texto recebido.

            Exemplos:

                resolver("Aurora")  ->  6
                resolver("")        ->  0
                resolver("a b")     ->  3

            Espaços contam como caractere.
            """,
            assinatura="def resolver(texto: str) -> int:",
            dicas=[
                "Existe uma função pronta para medir o tamanho de qualquer sequência.",
                "É len(...), de length.",
                "return len(texto)",
            ],
            solucao="    return len(texto)",
            testes="""
def teste_palavra():
    verificar(ex.resolver("Aurora"), 6)


def teste_texto_vazio():
    verificar(ex.resolver(""), 0)


def teste_conta_espacos():
    verificar(ex.resolver("a b"), 3)
""",
        ),
        Ex(
            id="A03-002", titulo="Primeira e última letra", nivel=2, tempo_min=5,
            tags=["indexacao"],
            enunciado="""
            Devolva uma tupla com a primeira e a última letra do texto.

            Exemplos:

                resolver("Aurora")  ->  ("A", "a")
                resolver("SP")      ->  ("S", "P")
                resolver("x")       ->  ("x", "x")

            A posição do último caractere é `-1` — assim você não precisa
            calcular `len(texto) - 1`.
            """,
            assinatura="def resolver(texto: str) -> tuple[str, str]:",
            dicas=[
                "A contagem começa no 0, então o primeiro caractere é texto[0].",
                "Índices negativos contam de trás para frente: -1 é o último.",
                "return texto[0], texto[-1]",
            ],
            solucao="    return texto[0], texto[-1]",
            testes="""
def teste_palavra():
    verificar(ex.resolver("Aurora"), ("A", "a"))


def teste_duas_letras():
    verificar(ex.resolver("SP"), ("S", "P"))


def teste_uma_letra_so():
    verificar(ex.resolver("x"), ("x", "x"))
""",
        ),
        Ex(
            id="A03-003", titulo="Um pedaço do texto", nivel=2, tempo_min=6,
            tags=["fatiamento"],
            enunciado="""
            Devolva os três primeiros caracteres do texto.

            Exemplos:

                resolver("Eletrônicos")  ->  "Ele"
                resolver("Casa")         ->  "Cas"
                resolver("SP")           ->  "SP"

            Repare no último caso: se o texto for menor que 3, o fatiamento
            simplesmente devolve o que existe, sem erro.
            """,
            assinatura="def resolver(texto: str) -> str:",
            dicas=[
                "Fatiar usa dois pontos dentro dos colchetes: texto[inicio:fim].",
                "O fim é exclusivo — para pegar 3 caracteres a partir do 0, o fim é 3.",
                "return texto[:3]",
            ],
            solucao="    return texto[:3]",
            nota_da_solucao="Omitir o início vale 'desde o começo'; fatiar nunca estoura os limites.",
            testes="""
def teste_palavra_longa():
    verificar(ex.resolver("Eletrônicos"), "Ele")


def teste_palavra_de_quatro():
    verificar(ex.resolver("Casa"), "Cas")


def teste_texto_curto_demais():
    verificar(ex.resolver("SP"), "SP")
""",
        ),
        Ex(
            id="A03-004", titulo="Caixa alta e caixa baixa", nivel=1, tempo_min=4,
            tags=["upper", "lower", "tupla"],
            enunciado="""
            Devolva uma tupla com o texto em maiúsculas e em minúsculas.

            Exemplos:

                resolver("Aurora")  ->  ("AURORA", "aurora")
                resolver("sp")      ->  ("SP", "sp")

            Padronizar caixa é a primeira coisa que se faz ao limpar dados —
            `SP`, `sp` e `Sp` são o mesmo estado, mas o computador não sabe disso.
            """,
            assinatura="def resolver(texto: str) -> tuple[str, str]:",
            dicas=[
                "São dois métodos com nomes bem diretos, em inglês.",
                "Métodos são chamados com ponto: texto.upper().",
                "return texto.upper(), texto.lower()",
            ],
            solucao="    return texto.upper(), texto.lower()",
            testes="""
def teste_nome_proprio():
    verificar(ex.resolver("Aurora"), ("AURORA", "aurora"))


def teste_sigla_minuscula():
    verificar(ex.resolver("sp"), ("SP", "sp"))
""",
        ),
        Ex(
            id="A03-005", titulo="Tirar os espaços das pontas", nivel=2, tempo_min=5,
            tags=["strip", "limpeza"],
            enunciado="""
            Um cadastro veio com espaços sobrando. Devolva o texto sem os espaços
            das pontas — e só das pontas.

            Exemplos:

                resolver("  Ana Souza  ")  ->  "Ana Souza"
                resolver("Ana")            ->  "Ana"
                resolver("   ")            ->  ""

            Repare no primeiro exemplo: o espaço entre "Ana" e "Souza" fica.
            """,
            assinatura="def resolver(texto: str) -> str:",
            dicas=[
                "Existe um método específico para aparar as pontas de um texto.",
                "Chama-se strip, de 'descascar'.",
                "return texto.strip()",
            ],
            solucao="    return texto.strip()",
            nota_da_solucao="strip() sem argumento remove espaços, tabs e quebras de linha das duas pontas.",
            testes="""
def teste_espacos_dos_dois_lados():
    verificar(ex.resolver("  Ana Souza  "), "Ana Souza")


def teste_sem_espacos():
    verificar(ex.resolver("Ana"), "Ana")


def teste_so_espacos():
    verificar(ex.resolver("   "), "")


def teste_preserva_espaco_do_meio():
    verificar(ex.resolver(" a  b "), "a  b",
              dica="strip só mexe nas pontas — o miolo fica intacto.")
""",
        ),
        Ex(
            id="A03-006", titulo="Trocar um pedaço", nivel=2, tempo_min=5,
            tags=["replace"],
            enunciado="""
            Códigos de produto vieram com hífen, mas o sistema espera barra.

            Devolva o texto com todos os hífens trocados por `/`.

            Exemplos:

                resolver("SP-01-A")  ->  "SP/01/A"
                resolver("SP01")     ->  "SP01"
                resolver("-")        ->  "/"

            `replace` troca **todas** as ocorrências, não só a primeira.
            """,
            assinatura="def resolver(codigo: str) -> str:",
            dicas=[
                "O método recebe dois argumentos: o que procurar e o que colocar no lugar.",
                'texto.replace("velho", "novo")',
                'return codigo.replace("-", "/")',
            ],
            solucao='    return codigo.replace("-", "/")',
            testes="""
def teste_dois_hifens():
    verificar(ex.resolver("SP-01-A"), "SP/01/A")


def teste_sem_hifen():
    verificar(ex.resolver("SP01"), "SP01")


def teste_so_o_hifen():
    verificar(ex.resolver("-"), "/")
""",
        ),
        Ex(
            id="A03-007", titulo="Quebrar a frase em palavras", nivel=2, tempo_min=5,
            tags=["split", "lista"],
            enunciado="""
            Devolva a lista de palavras de uma frase.

            Exemplos:

                resolver("Fone Aurora Pro")  ->  ["Fone", "Aurora", "Pro"]
                resolver("Casa")             ->  ["Casa"]

            `split()` sem argumento quebra em qualquer espaço em branco e ignora
            espaços repetidos — é quase sempre o que você quer.
            """,
            assinatura="def resolver(frase: str) -> list[str]:",
            dicas=[
                "O método que quebra texto em pedaços se chama split.",
                "Chamado sem argumento, ele separa por espaços.",
                "return frase.split()",
            ],
            solucao="    return frase.split()",
            testes="""
def teste_tres_palavras():
    verificar(ex.resolver("Fone Aurora Pro"), ["Fone", "Aurora", "Pro"])


def teste_uma_palavra():
    verificar(ex.resolver("Casa"), ["Casa"])


def teste_espacos_repetidos():
    verificar(ex.resolver("a   b"), ["a", "b"],
              dica="split() sem argumento já ignora espaços repetidos.")
""",
        ),
        Ex(
            id="A03-008", titulo="Juntar palavras", nivel=2, tempo_min=6,
            tags=["join"], requer=["A03-007"],
            enunciado="""
            O caminho inverso do `split`. Devolva as palavras da lista unidas por
            vírgula e espaço.

            Exemplos:

                resolver(["Moda", "Casa", "Livros"])  ->  "Moda, Casa, Livros"
                resolver(["Moda"])                    ->  "Moda"
                resolver([])                          ->  ""

            A sintaxe de `join` costuma pegar de surpresa: quem chama o método é o
            **separador**, e a lista vai como argumento.

                ", ".join(["a", "b"])    ->  'a, b'
            """,
            assinatura="def resolver(palavras: list[str]) -> str:",
            dicas=[
                "Quem chama o join é o texto que vai ficar ENTRE os itens.",
                'O separador aqui é ", " — vírgula e espaço.',
                'return ", ".join(palavras)',
            ],
            solucao='    return ", ".join(palavras)',
            nota_da_solucao="Com lista vazia o join devolve texto vazio, sem erro — de graça.",
            testes="""
def teste_tres_itens():
    verificar(ex.resolver(["Moda", "Casa", "Livros"]), "Moda, Casa, Livros")


def teste_um_item_so():
    verificar(ex.resolver(["Moda"]), "Moda")


def teste_lista_vazia():
    verificar(ex.resolver([]), "")
""",
        ),
        Ex(
            id="A03-009", titulo="Está aí dentro?", nivel=1, tempo_min=4,
            tags=["in", "booleano"],
            enunciado="""
            Devolva `True` se o texto procurado aparecer dentro da frase.

            Exemplos:

                resolver("Fone Aurora Pro", "Aurora")  ->  True
                resolver("Fone Aurora Pro", "aurora")  ->  False
                resolver("Fone", "")                   ->  True

            A busca diferencia maiúsculas de minúsculas — por isso o segundo exemplo
            dá `False`.
            """,
            assinatura="def resolver(frase: str, procurado: str) -> bool:",
            dicas=[
                "Python tem uma palavra-chave para 'está contido em'.",
                'É o operador in: "ro" in "aurora".',
                "return procurado in frase",
            ],
            solucao="    return procurado in frase",
            testes="""
def teste_encontra():
    verificar(ex.resolver("Fone Aurora Pro", "Aurora"), True)


def teste_caixa_diferente_nao_encontra():
    verificar(ex.resolver("Fone Aurora Pro", "aurora"), False)


def teste_texto_vazio_sempre_existe():
    verificar(ex.resolver("Fone", ""), True)
""",
        ),
        Ex(
            id="A03-010", titulo="Começa com, termina com", nivel=2, tempo_min=5,
            tags=["startswith", "endswith", "tupla"],
            enunciado="""
            Devolva uma tupla `(começa com o prefixo?, termina com o sufixo?)`.

            Exemplos:

                resolver("aurora.pro@loja.com", "aurora", ".com")  ->  (True, True)
                resolver("teste@loja.org", "aurora", ".com")       ->  (False, False)

            É assim que se valida extensão de arquivo, prefixo de código,
            domínio de e-mail — sem precisar de fatiamento.
            """,
            assinatura="def resolver(texto: str, prefixo: str, sufixo: str) -> tuple[bool, bool]:",
            dicas=[
                "São dois métodos irmãos, com nomes em inglês bem literais.",
                "startswith e endswith — cada um recebe o pedaço a conferir.",
                "return texto.startswith(prefixo), texto.endswith(sufixo)",
            ],
            solucao="    return texto.startswith(prefixo), texto.endswith(sufixo)",
            testes="""
def teste_bate_nos_dois():
    verificar(ex.resolver("aurora.pro@loja.com", "aurora", ".com"), (True, True))


def teste_nao_bate_em_nenhum():
    verificar(ex.resolver("teste@loja.org", "aurora", ".com"), (False, False))


def teste_bate_so_no_comeco():
    verificar(ex.resolver("aurora@loja.org", "aurora", ".com"), (True, False))
""",
        ),
        Ex(
            id="A03-011", titulo="Formatar dinheiro", nivel=2, tempo_min=6,
            tags=["f-string", "formatacao"], requer=["A01-010"],
            enunciado="""
            Dentro de uma f-string, dois-pontos abre o formato do valor:

                f"{1234.5:.2f}"    ->  '1234.50'

            O `.2f` significa "número com vírgula, exatamente 2 casas".

            Devolva o preço formatado como moeda:

                resolver(1234.5)  ->  "R$ 1234.50"
                resolver(9.999)   ->  "R$ 10.00"
                resolver(0)       ->  "R$ 0.00"
            """,
            assinatura="def resolver(preco: float) -> str:",
            dicas=[
                'O prefixo "R$ " é texto comum dentro da f-string.',
                "O formato vai depois de dois-pontos, dentro das chaves: {preco:.2f}.",
                'return f"R$ {preco:.2f}"',
            ],
            solucao='    return f"R$ {preco:.2f}"',
            nota_da_solucao="O .2f arredonda e garante as duas casas mesmo em valores redondos.",
            testes="""
def teste_valor_com_uma_casa():
    verificar(ex.resolver(1234.5), "R$ 1234.50")


def teste_arredonda_para_cima():
    verificar(ex.resolver(9.999), "R$ 10.00")


def teste_zero():
    verificar(ex.resolver(0), "R$ 0.00")
""",
        ),
        Ex(
            id="A03-012", titulo="Ao contrário", nivel=2, tempo_min=5,
            tags=["fatiamento", "passo"], requer=["A03-003"],
            enunciado="""
            O fatiamento aceita um terceiro número, o **passo**:

                texto[inicio:fim:passo]

            Com passo `-1`, ele percorre o texto de trás para frente.

            Devolva o texto invertido:

                resolver("Aurora")  ->  "aroruA"
                resolver("ana")     ->  "ana"
                resolver("")        ->  ""
            """,
            assinatura="def resolver(texto: str) -> str:",
            dicas=[
                "Deixe início e fim em branco para pegar o texto inteiro.",
                "Sobram dois-pontos duplos antes do passo: texto[::passo].",
                "return texto[::-1]",
            ],
            solucao="    return texto[::-1]",
            testes="""
def teste_palavra():
    verificar(ex.resolver("Aurora"), "aroruA")


def teste_palindromo():
    verificar(ex.resolver("ana"), "ana")


def teste_vazio():
    verificar(ex.resolver(""), "")
""",
        ),
        Ex(
            id="A03-013", titulo="Contar quantas vezes", nivel=2, tempo_min=5,
            tags=["count"],
            enunciado="""
            Devolva quantas vezes um trecho aparece dentro do texto.

            Exemplos:

                resolver("aurora", "r")     ->  2
                resolver("aurora", "z")     ->  0
                resolver("aaaa", "aa")      ->  2

            No último exemplo a contagem é 2, não 3: `count` não conta ocorrências
            sobrepostas — depois de achar uma, ele continua do fim dela.
            """,
            assinatura="def resolver(texto: str, trecho: str) -> int:",
            dicas=[
                "Existe um método com o nome exato da operação, em inglês.",
                "texto.count(trecho)",
                "return texto.count(trecho)",
            ],
            solucao="    return texto.count(trecho)",
            testes="""
def teste_duas_ocorrencias():
    verificar(ex.resolver("aurora", "r"), 2)


def teste_nenhuma_ocorrencia():
    verificar(ex.resolver("aurora", "z"), 0)


def teste_nao_conta_sobreposicao():
    verificar(ex.resolver("aaaa", "aa"), 2)
""",
        ),
        Ex(
            id="A03-014", titulo="Iniciais do nome", nivel=3, tempo_min=9,
            tags=["split", "indexacao", "join", "composicao"],
            requer=["A03-007", "A03-008"],
            enunciado="""
            Primeiro exercício que combina várias ferramentas de uma vez.

            Devolva as iniciais de um nome completo, em maiúsculas, separadas
            por ponto e sem ponto no final.

            Exemplos:

                resolver("ana souza lima")     ->  "A.S.L"
                resolver("Carlos Oliveira")    ->  "C.O"
                resolver("aurora")             ->  "A"

            Caminho sugerido: quebre o nome em palavras, pegue a primeira letra de
            cada uma, deixe em maiúscula e junte tudo com ponto.
            """,
            assinatura="def resolver(nome: str) -> str:",
            dicas=[
                "Três passos: separar as palavras, pegar a letra 0 de cada, juntar com ponto.",
                "Você pode montar uma lista vazia e ir acrescentando com .append() dentro de um for.",
                'Depois de ter a lista de letras, ".".join(letras) resolve o final.',
            ],
            solucao="""
            letras = []
            for palavra in nome.split():
                letras.append(palavra[0].upper())
            return ".".join(letras)
            """,
            nota_da_solucao="No módulo A10 você reescreve isto em uma linha com list comprehension.",
            testes="""
def teste_tres_nomes():
    verificar(ex.resolver("ana souza lima"), "A.S.L")


def teste_dois_nomes():
    verificar(ex.resolver("Carlos Oliveira"), "C.O")


def teste_um_nome_so():
    verificar(ex.resolver("aurora"), "A")


def teste_espacos_sobrando():
    verificar(ex.resolver("  maria  clara  "), "M.C",
              dica="split() sem argumento já lida com os espaços extras.")
""",
        ),
    ],
)

MODULOS = [A01, A02, A03]
