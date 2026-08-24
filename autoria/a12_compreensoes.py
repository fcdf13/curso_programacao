"""Bloco A, módulo 12: compreensões."""

from autoria.modelo import Exercicio as Ex
from autoria.modelo import Modulo

PREAMBULO_TESTE_CRONOMETRADO = "import time  # noqa: F401  (t.cronometrar já cuida da medição)"

A12 = Modulo(
    id="A12",
    titulo="Módulo A12 — Compreensões",
    resumo="Construir listas, dicionários e conjuntos em uma linha — e saber quando não fazer isso.",
    teoria="""
## List comprehension: construir uma lista em uma linha

```python
precos = [10.0, 20.0, 30.0]

dobrados = []
for preco in precos:
    dobrados.append(preco * 2)
# dobrados == [20.0, 40.0, 60.0]

dobrados = [preco * 2 for preco in precos]   # a mesma coisa, numa linha
```

A forma geral é `[expressão for item in iterável]` — para cada item do
iterável, calcule a expressão e guarde o resultado, na ordem.

### Com filtro: só alguns itens entram

```python
caros = [preco for preco in precos if preco >= 20.0]   # [20.0, 30.0]
```

O `if` no fim filtra **antes** da expressão rodar — só os itens que passam
no filtro chegam a virar resultado.

### Combinando transformação e filtro

```python
[preco * 1.1 for preco in precos if preco >= 20.0]   # [22.0, 33.0]
```

### Expressão condicional (`x if cond else y`) dentro da expressão

Isso é diferente do `if` de filtro de cima — aqui os **dois** lados sempre
entram no resultado, só muda qual valor:

```python
["caro" if preco >= 20.0 else "barato" for preco in precos]
# ["barato", "caro", "caro"]
```

### Dict comprehension e set comprehension

A mesma ideia, trocando os colchetes por chaves:

```python
{produto: preco for produto, preco in zip(produtos, precos)}   # dict
{categoria.upper() for categoria in categorias}                  # set, sem repetir
```

### Comprehension aninhada: mais de um `for`

```python
matriz = [[1, 2], [3, 4, 5]]
achatada = [item for linha in matriz for item in linha]
# [1, 2, 3, 4, 5]
```

Os `for` aparecem na mesma ordem em que apareceriam se você escrevesse os
laços aninhados à mão — o de fora primeiro, o de dentro depois.

## Quando **não** usar comprehension

Comprehension serve para **construir uma coleção**. Se você só quer saber
"existe algum item que...", `any()`/`all()` com uma **expressão geradora**
(a mesma sintaxe, mas sem os colchetes) é melhor — porque eles podem parar
assim que souberem a resposta, sem nunca montar a lista inteira:

```python
any(preco > 1000 for preco in precos)      # para no primeiro True
any([preco > 1000 for preco in precos])    # monta a lista TODA antes de checar
```

Com uma lista de milhões de itens e a resposta logo no início, a primeira
forma é ordens de magnitude mais rápida — a segunda paga o custo de
construir a lista inteira mesmo sem precisar de nenhum item além do primeiro.

E comprehension não serve para rodar efeitos colaterais: `[print(x) for x
in lista]` funciona, mas cria uma lista de `None`s só para jogar fora — um
`for` comum é o jeito certo quando você não está construindo nada.
""",
    exercicios=[
        Ex(
            id="A12-001", titulo="List comprehension básica", nivel=1, tempo_min=5,
            tags=["compreensao", "list-comprehension"], requer=["A06-005"],
            enunciado="""
            Dobre cada preço da lista.

            Exemplo:

                resolver([10.0, 20.0, 30.0])  ->  [20.0, 40.0, 60.0]

            É o mesmo resultado do laço com `.append()` que você já escreveu
            no módulo A6 — só que numa linha: `[expressão for item in lista]`.
            """,
            assinatura="def resolver(precos: list) -> list:",
            dicas=[
                "A forma geral é [expressao for item in lista].",
                "Aqui a expressão é preco * 2, e item é preco.",
                "return [preco * 2 for preco in precos]",
            ],
            solucao="    return [preco * 2 for preco in precos]",
            nota_da_solucao="O mesmo padrão de A06-005 (lista vazia + append num laço), só que expresso numa linha só.",
            testes="""
def teste_tres_precos():
    verificar(ex.resolver([10.0, 20.0, 30.0]), [20.0, 40.0, 60.0])


def teste_lista_vazia():
    verificar(ex.resolver([]), [])


def teste_um_preco():
    verificar(ex.resolver([5.0]), [10.0])
""",
        ),
        Ex(
            id="A12-002", titulo="List comprehension com filtro", nivel=2, tempo_min=6,
            tags=["compreensao", "filtro"], requer=["A12-001"],
            enunciado="""
            Devolva só os preços que são maiores ou iguais a um mínimo.

            Exemplo:

                resolver([10.0, 200.0, 50.0], 100.0)  ->  [200.0]

            Um `if` no fim da comprehension filtra: só os itens que passam
            nele viram parte do resultado. `[item for item in lista if condicao]`.
            """,
            assinatura="def resolver(precos: list, minimo: float) -> list:",
            dicas=[
                "O if vai depois do for, dentro dos mesmos colchetes.",
                "[preco for preco in precos if preco >= minimo]",
                "return [preco for preco in precos if preco >= minimo]",
            ],
            solucao="    return [preco for preco in precos if preco >= minimo]",
            testes="""
def teste_alguns_passam():
    verificar(ex.resolver([10.0, 200.0, 50.0], 100.0), [200.0])


def teste_nenhum_passa():
    verificar(ex.resolver([10.0, 20.0], 100.0), [])


def teste_todos_passam():
    verificar(ex.resolver([200.0, 300.0], 100.0), [200.0, 300.0])


def teste_lista_vazia():
    verificar(ex.resolver([], 100.0), [])
""",
        ),
        Ex(
            id="A12-003", titulo="Transformar e filtrar ao mesmo tempo", nivel=2, tempo_min=7,
            tags=["compreensao", "filtro", "zip"], requer=["A12-002", "A06-011"],
            enunciado="""
            Devolva, em maiúsculas, os nomes dos produtos cujo preço é maior
            ou igual a um mínimo.

            Exemplo:

                resolver(["Fone", "Livro"], [150.0, 20.0], 100.0)  ->  ["FONE"]

            `zip` anda nas duas listas em paralelo, como no módulo A6 —
            dentro da comprehension funciona igual: `for nome, preco in
            zip(nomes, precos)`.
            """,
            assinatura="def resolver(produtos: list, precos: list, minimo: float) -> list:",
            dicas=[
                "for nome, preco in zip(produtos, precos) desempacota os dois de\num par por vez, dentro da comprehension.",
                "A expressão é nome.upper(); o filtro é if preco >= minimo.",
                "return [nome.upper() for nome, preco in zip(produtos, precos) if preco >= minimo]",
            ],
            solucao='    return [nome.upper() for nome, preco in zip(produtos, precos) if preco >= minimo]',
            testes="""
def teste_um_produto_passa():
    verificar(ex.resolver(["Fone", "Livro"], [150.0, 20.0], 100.0), ["FONE"])


def teste_nenhum_produto_passa():
    verificar(ex.resolver(["Fone", "Livro"], [10.0, 20.0], 100.0), [])


def teste_todos_passam():
    verificar(ex.resolver(["Fone", "Capa"], [150.0, 200.0], 100.0), ["FONE", "CAPA"])
""",
        ),
        Ex(
            id="A12-004", titulo="Dict comprehension básica", nivel=2, tempo_min=6,
            tags=["compreensao", "dict-comprehension", "zip"], requer=["A12-001", "A06-011"],
            enunciado="""
            Monte um dicionário `produto -> preço`, a partir de duas listas
            alinhadas.

            Exemplo:

                resolver(["Fone", "Capa"], [99.9, 25.0])
                ->  {"Fone": 99.9, "Capa": 25.0}

            Dict comprehension é a mesma ideia da list comprehension, com
            `{chave: valor for ... in ...}` no lugar de colchetes.
            """,
            assinatura="def resolver(produtos: list, precos: list) -> dict:",
            dicas=[
                "A forma geral é {chave: valor for item in iteravel}.",
                "zip(produtos, precos) entrega os pares (nome, preco) de uma vez.",
                "return {nome: preco for nome, preco in zip(produtos, precos)}",
            ],
            solucao="    return {nome: preco for nome, preco in zip(produtos, precos)}",
            testes="""
def teste_dois_produtos():
    verificar(ex.resolver(["Fone", "Capa"], [99.9, 25.0]), {"Fone": 99.9, "Capa": 25.0})


def teste_listas_vazias():
    verificar(ex.resolver([], []), {})


def teste_um_produto():
    verificar(ex.resolver(["Livro"], [30.0]), {"Livro": 30.0})
""",
        ),
        Ex(
            id="A12-005", titulo="Dict comprehension com filtro", nivel=3, tempo_min=7,
            tags=["compreensao", "dict-comprehension", "filtro"], requer=["A12-004", "A12-002"],
            enunciado="""
            Monte um dicionário `produto -> preço`, mas só com os produtos
            cujo preço é maior ou igual a um mínimo.

            Exemplo:

                resolver(["Fone", "Capa"], [150.0, 20.0], 100.0)
                ->  {"Fone": 150.0}

            Igual ao exercício anterior, com um `if` no fim — o mesmo
            filtro que você já usou na list comprehension.
            """,
            assinatura="def resolver(produtos: list, precos: list, minimo: float) -> dict:",
            dicas=[
                "O if de filtro funciona em dict comprehension do mesmo jeito\nque em list comprehension.",
                "{nome: preco for nome, preco in zip(produtos, precos) if preco >= minimo}",
                "return {nome: preco for nome, preco in zip(produtos, precos) if preco >= minimo}",
            ],
            solucao="    return {nome: preco for nome, preco in zip(produtos, precos) if preco >= minimo}",
            testes="""
def teste_um_produto_passa():
    verificar(ex.resolver(["Fone", "Capa"], [150.0, 20.0], 100.0), {"Fone": 150.0})


def teste_nenhum_produto_passa():
    verificar(ex.resolver(["Fone", "Capa"], [10.0, 20.0], 100.0), {})


def teste_todos_passam():
    verificar(
        ex.resolver(["Fone", "Capa"], [150.0, 200.0], 100.0),
        {"Fone": 150.0, "Capa": 200.0},
    )
""",
        ),
        Ex(
            id="A12-006", titulo="Set comprehension", nivel=2, tempo_min=6,
            tags=["compreensao", "set-comprehension"], requer=["A12-001", "A08-013"],
            enunciado="""
            Devolva as categorias, em maiúsculas, sem repetir.

            Exemplo:

                resolver(["moda", "casa", "moda"])  ->  {"MODA", "CASA"}

            Set comprehension é a mesma ideia da list comprehension, com
            `{}` no lugar de `[]` — e, como todo conjunto, remove as
            repetições sozinho.
            """,
            assinatura="def resolver(categorias: list) -> set:",
            dicas=[
                "A forma geral é {expressao for item in iteravel} — chaves, sem dois-pontos.",
                "A expressão é categoria.upper().",
                "return {categoria.upper() for categoria in categorias}",
            ],
            solucao="    return {categoria.upper() for categoria in categorias}",
            nota_da_solucao="Sem dois-pontos, {} vira set comprehension; com chave: valor, vira dict comprehension.",
            testes="""
def teste_com_repeticao():
    verificar(ex.resolver(["moda", "casa", "moda"]), {"MODA", "CASA"})


def teste_sem_repeticao():
    verificar(ex.resolver(["moda", "casa"]), {"MODA", "CASA"})


def teste_lista_vazia():
    verificar(ex.resolver([]), set())
""",
        ),
        Ex(
            id="A12-007", titulo="Expressão condicional dentro da comprehension", nivel=3, tempo_min=7,
            tags=["compreensao", "ternario"], requer=["A12-001"],
            enunciado="""
            Rotule cada preço como `"caro"` (maior ou igual ao limite) ou
            `"barato"` (menor que o limite).

            Exemplo:

                resolver([10.0, 500.0, 5.0], 100.0)  ->  ["barato", "caro", "barato"]

            Isto é diferente do `if` de filtro dos exercícios anteriores:
            aqui **todo** item continua no resultado — só muda qual dos
            dois valores entra. A forma é
            `valor_a if condicao else valor_b`, no lugar da expressão.
            """,
            assinatura="def resolver(precos: list, limite: float) -> list:",
            dicas=[
                'Isto não é filtro — a lista de saída tem o mesmo tamanho da\nde entrada, um rótulo para cada preço.',
                'A expressão inteira é "caro" if preco >= limite else "barato".',
                'return ["caro" if preco >= limite else "barato" for preco in precos]',
            ],
            solucao='    return ["caro" if preco >= limite else "barato" for preco in precos]',
            nota_da_solucao="O if aqui faz parte da EXPRESSÃO (antes do for) — o if de filtro fica depois do for. São dois usos diferentes do mesmo palavra-chave.",
            testes="""
def teste_mistura():
    verificar(ex.resolver([10.0, 500.0, 5.0], 100.0), ["barato", "caro", "barato"])


def teste_exatamente_no_limite():
    verificar(ex.resolver([100.0], 100.0), ["caro"])


def teste_lista_vazia():
    verificar(ex.resolver([], 100.0), [])
""",
        ),
        Ex(
            id="A12-008", titulo="Comprehension com enumerate", nivel=3, tempo_min=7,
            tags=["compreensao", "enumerate", "filtro"], requer=["A12-002", "A06-010"],
            enunciado="""
            Devolva as posições (a partir de 0) dos preços maiores que um
            limite.

            Exemplo:

                resolver([10.0, 500.0, 5.0, 800.0], 100.0)  ->  [1, 3]

            `enumerate` entrega posição e item ao mesmo tempo, como no
            módulo A6 — dentro da comprehension funciona igual:
            `for posicao, preco in enumerate(precos)`.
            """,
            assinatura="def resolver(precos: list, limite: float) -> list:",
            dicas=[
                "for posicao, preco in enumerate(precos) desempacota os dois,\ndentro da comprehension.",
                "A expressão é só a posicao; o filtro é if preco > limite.",
                "return [posicao for posicao, preco in enumerate(precos) if preco > limite]",
            ],
            solucao="    return [posicao for posicao, preco in enumerate(precos) if preco > limite]",
            testes="""
def teste_duas_posicoes():
    verificar(ex.resolver([10.0, 500.0, 5.0, 800.0], 100.0), [1, 3])


def teste_nenhuma_posicao():
    verificar(ex.resolver([10.0, 20.0], 100.0), [])


def teste_lista_vazia():
    verificar(ex.resolver([], 100.0), [])
""",
        ),
        Ex(
            id="A12-009", titulo="Comprehension aninhada: achatar uma lista de listas", nivel=4, tempo_min=9,
            tags=["compreensao", "aninhada"], requer=["A12-001"],
            enunciado="""
            Você recebe uma lista de pedidos, cada um com uma lista de
            itens. Devolva uma única lista com todos os itens, na ordem.

            Exemplo:

                resolver([["Fone", "Capa"], ["Livro"], []])
                ->  ["Fone", "Capa", "Livro"]

            Uma comprehension aceita mais de um `for`, na mesma ordem em
            que você escreveria os laços aninhados à mão — o de fora
            primeiro: `[item for pedido in pedidos for item in pedido]`.
            """,
            assinatura="def resolver(pedidos: list) -> list:",
            dicas=[
                "Escreva primeiro com dois laços aninhados de verdade (for pedido\nin pedidos: for item in pedido: ...append(item)) — depois junte numa linha.",
                "Os dois for ficam um atrás do outro, na mesma ordem dos laços\naninhados: for pedido in pedidos for item in pedido.",
                "return [item for pedido in pedidos for item in pedido]",
            ],
            solucao="    return [item for pedido in pedidos for item in pedido]",
            nota_da_solucao="A ordem dos for é a mesma da versão com laços aninhados: o primeiro for é o laço de fora.",
            testes="""
def teste_tres_pedidos():
    verificar(
        ex.resolver([["Fone", "Capa"], ["Livro"], []]),
        ["Fone", "Capa", "Livro"],
    )


def teste_lista_vazia():
    verificar(ex.resolver([]), [])


def teste_um_pedido_so():
    verificar(ex.resolver([["Mouse"]]), ["Mouse"])


def teste_todos_pedidos_vazios():
    verificar(ex.resolver([[], []]), [])
""",
        ),
        Ex(
            id="A12-010", titulo="Comprehension aninhada com filtro: combinações", nivel=4, tempo_min=10,
            tags=["compreensao", "aninhada", "filtro"], requer=["A12-009", "A12-002"],
            enunciado="""
            Gere todas as combinações de (UF, categoria) para uma campanha
            de anúncios — exceto a combinação de `"SP"` com `"Luxo"`, que já
            tem loja física e não precisa de anúncio.

            Exemplo:

                resolver(["SP", "RJ"], ["Moda", "Luxo"])
                ->  [("SP", "Moda"), ("RJ", "Moda"), ("RJ", "Luxo")]

            Dois `for` geram todas as combinações (o produto cartesiano); um
            `if` no fim filtra a que não interessa — os dois no mesmo par
            de colchetes.
            """,
            assinatura="def resolver(ufs: list, categorias: list) -> list:",
            dicas=[
                "Dois for, um para uf e outro para categoria, geram um par\n(uf, categoria) para cada combinação possível.",
                "O filtro exclui só um caso: uf == \"SP\" and categoria == \"Luxo\".",
                'return [(uf, cat) for uf in ufs for cat in categorias if not (uf == "SP" and cat == "Luxo")]',
            ],
            solucao='    return [(uf, cat) for uf in ufs for cat in categorias if not (uf == "SP" and cat == "Luxo")]',
            testes="""
def teste_exclui_sp_luxo():
    verificar(
        ex.resolver(["SP", "RJ"], ["Moda", "Luxo"]),
        [("SP", "Moda"), ("RJ", "Moda"), ("RJ", "Luxo")],
    )


def teste_sem_luxo_nao_exclui_nada():
    verificar(
        ex.resolver(["SP", "RJ"], ["Moda", "Casa"]),
        [("SP", "Moda"), ("SP", "Casa"), ("RJ", "Moda"), ("RJ", "Casa")],
    )


def teste_lista_de_ufs_vazia():
    verificar(ex.resolver([], ["Moda"]), [])
""",
        ),
        Ex(
            id="A12-011", titulo="Quando não usar list comprehension", nivel=4, tempo_min=10,
            tags=["compreensao", "generator", "desempenho", "cronometrado"],
            requer=["A12-002", "A09-003"],
            preambulo_do_teste=PREAMBULO_TESTE_CRONOMETRADO,
            enunciado="""
            Verifique se algum preço passa de um limite.

            Exemplo:

                resolver([10.0, 5000.0, 20.0], 1000.0)  ->  True
                resolver([10.0, 20.0], 1000.0)           ->  False

            `any([preco > limite for preco in precos])` dá a resposta certa,
            mas **monta a lista inteira antes** de `any()` sequer começar a
            olhar — mesmo que o primeiro item já bastasse. Uma expressão
            geradora (a mesma sintaxe, sem os colchetes) deixa `any()` parar
            assim que encontrar um `True`, sem nunca montar lista nenhuma:
            `any(preco > limite for preco in precos)`.
            """,
            assinatura="def resolver(precos: list, limite: float) -> bool:",
            dicas=[
                "any(...) já para no primeiro True — o problema é só o que vai\ndentro dos parênteses.",
                "Tirar os colchetes de dentro do any() transforma a list\ncomprehension numa expressão geradora, sem montar lista nenhuma.",
                "return any(preco > limite for preco in precos)",
            ],
            solucao="    return any(preco > limite for preco in precos)",
            nota_da_solucao="any([...]) e any(...) sem colchetes dão a mesma resposta — a diferença é só que o segundo pode parar cedo, sem montar a lista inteira primeiro.",
            testes="""
def teste_encontra_acima_do_limite():
    verificar(ex.resolver([10.0, 5000.0, 20.0], 1000.0), True)


def teste_nenhum_acima_do_limite():
    verificar(ex.resolver([10.0, 20.0], 1000.0), False)


def teste_lista_vazia():
    verificar(ex.resolver([], 1000.0), False)


def teste_generator_para_cedo_numa_lista_enorme():
    # 5 milhões de preços, com o único valor alto logo no início: any() com
    # uma expressão geradora encontra a resposta quase na hora; any() com
    # uma list comprehension precisa montar a lista dos 5 milhões primeiro.
    precos = [10.0] * 5_000_000
    precos[0] = 999_999.0

    with t.cronometrar() as tempo:
        obtido = ex.resolver(precos, 500_000.0)

    verificar(obtido, True)
    t.verificar_tempo(
        tempo["segundos"], limite=0.5,
        dica="troque any([... for ...]) por any(... for ...), sem colchetes.",
    )
""",
        ),
        Ex(
            id="A12-012", titulo="Desafio: catálogo por categoria", nivel=5, tempo_min=13,
            tags=["compreensao", "desafio", "dict-comprehension", "set-comprehension"],
            requer=["A12-005", "A12-006"],
            enunciado="""
            Monte um dicionário `categoria -> lista de produtos caros`
            daquela categoria (preço maior ou igual a um mínimo).

            Exemplo:

                resolver(
                    ["Fone", "Sofá", "Caneca", "Mesa"],
                    ["Eletrônicos", "Casa", "Casa", "Casa"],
                    [150.0, 800.0, 15.0, 300.0],
                    50.0,
                )
                ->  {"Eletrônicos": ["Fone"], "Casa": ["Sofá", "Mesa"]}

            (`"Caneca"` fica de fora — custa menos que o mínimo — mas
            `"Casa"` continua no dicionário, porque `"Sofá"` e `"Mesa"`
            passam.)

            Combina os três tipos do módulo: um set comprehension para as
            categorias sem repetir, e um dict comprehension cujo valor é,
            para cada categoria, um list comprehension filtrando os
            produtos daquela categoria.
            """,
            assinatura="def resolver(produtos: list, categorias: list, precos: list, minimo: float) -> dict:",
            dicas=[
                "Primeiro monte o conjunto de categorias sem repetir — o set\ncomprehension do exercício A12-006.",
                "O dicionário final é {cat: [...] for cat in categorias_unicas}\n— e o valor de cada chave é, por sua vez, uma list comprehension.",
                "categorias_unicas = {c for c in categorias}\n    return {\n        cat: [p for p, c, v in zip(produtos, categorias, precos) if c == cat and v >= minimo]\n        for cat in categorias_unicas\n    }",
            ],
            solucao="""
            categorias_unicas = {c for c in categorias}
            return {
                cat: [p for p, c, v in zip(produtos, categorias, precos) if c == cat and v >= minimo]
                for cat in categorias_unicas
            }
            """,
            nota_da_solucao="Uma comprehension dentro de outra: o valor de cada chave do dict comprehension é, ele mesmo, um list comprehension completo, filtrando pela categoria da vez.",
            testes="""
def teste_duas_categorias():
    verificar(
        ex.resolver(
            ["Fone", "Sofá", "Caneca", "Mesa"],
            ["Eletrônicos", "Casa", "Casa", "Casa"],
            [150.0, 800.0, 15.0, 300.0],
            50.0,
        ),
        {"Eletrônicos": ["Fone"], "Casa": ["Sofá", "Mesa"]},
    )


def teste_categoria_fica_com_lista_vazia_se_nada_passa():
    verificar(
        ex.resolver(["Caneca"], ["Casa"], [15.0], 50.0),
        {"Casa": []},
    )


def teste_entrada_vazia():
    verificar(ex.resolver([], [], [], 50.0), {})
""",
        ),
    ],
)

MODULOS = [A12]
