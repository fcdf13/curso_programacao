"""Bloco A, módulo 9: complexidade e Big-O.

Diferente dos módulos anteriores, uma parte dos testes aqui não só confere o
resultado — também **cronometra** a solução com uma entrada grande de propósito.
Isso é intencional: "sua solução é O(n²)" é abstrato até o cronômetro mostrar
2 segundos onde deveriam caber 0,3. Os limites foram calibrados com folga (a
diferença real costuma passar de 500x), então quem já resolveu com a técnica
certa nem percebe o relógio correndo.
"""

from autoria.modelo import Exercicio as Ex
from autoria.modelo import Modulo

PREAMBULO_TESTE_CRONOMETRADO = "import time  # noqa: F401  (t.cronometrar já cuida da medição)"

A09 = Modulo(
    id="A09",
    titulo="Módulo A9 — Complexidade e Big-O",
    resumo="Por que a mesma resposta certa pode levar 2 milissegundos ou 2 minutos.",
    teoria="""
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
""",
    exercicios=[
        Ex(
            id="A09-001", titulo="Quantas vezes o laço roda", nivel=1, tempo_min=6,
            tags=["big-o", "laco-aninhado", "conceito"], requer=["A06-013"],
            enunciado="""
            Antes de falar em Big-O, vale contar na unha.

            Devolva quantas vezes o corpo do laço mais interno roda, para dois laços
            aninhados, cada um de `n` voltas.

            Exemplos:

                resolver(3)  ->  9    (3 × 3)
                resolver(1)  ->  1
                resolver(0)  ->  0

            Não use a fórmula direto — monte os dois laços de verdade e conte.
            É esse formato (`for` dentro de `for`, ambos até `n`) que qualquer
            entrevista chama de O(n²): dobrar `n` quadruplica o total.
            """,
            assinatura="def resolver(n: int) -> int:",
            dicas=[
                "Monte um laço dentro do outro, exatamente como na tabuada do A6.",
                "Um contador que soma 1 a cada volta do laço de dentro.",
                "for _ in range(n): for _ in range(n): contador += 1",
            ],
            solucao="""
            contador = 0
            for _ in range(n):
                for _ in range(n):
                    contador += 1
            return contador
            """,
            nota_da_solucao="Escrito por extenso para reforçar a forma: dois laços de tamanho n aninhados = O(n²).",
            testes="""
def teste_tres():
    verificar(ex.resolver(3), 9)


def teste_um():
    verificar(ex.resolver(1), 1)


def teste_zero():
    verificar(ex.resolver(0), 0)


def teste_cresce_ao_quadrado():
    # dobrar n de 5 para 10 deve multiplicar o resultado por 4, não por 2.
    verificar(ex.resolver(10), ex.resolver(5) * 4,
              dica="Se isso não bater, o laço de dentro não está indo até n.")
""",
        ),
        Ex(
            id="A09-002", titulo="Está na lista", nivel=2, tempo_min=5,
            tags=["big-o", "lista", "membership"],
            enunciado="""
            Verifique se um código de cupom está na lista de cupons válidos.

            Exemplo:

                resolver(["BEMVINDO10", "FRETEGRATIS"], "BEMVINDO10")  ->  True
                resolver(["BEMVINDO10", "FRETEGRATIS"], "XYZ")         ->  False

            Nada de novo na sintaxe — o ponto deste exercício é o próximo: `in`
            numa lista precisa, no pior caso, olhar item por item até o fim.
            Para uma lista de tamanho `n`, isso é O(n).
            """,
            assinatura="def resolver(cupons_validos: list, codigo: str) -> bool:",
            dicas=[
                "O operador in já resolve isto, igual você viu no módulo A5.",
                "Não precisa de laço escrito por você — in faz a busca sozinho.",
                "return codigo in cupons_validos",
            ],
            solucao="    return codigo in cupons_validos",
            nota_da_solucao="Correto, e O(n): no pior caso, in percorre a lista inteira até decidir.",
            testes="""
def teste_cupom_valido():
    verificar(ex.resolver(["BEMVINDO10", "FRETEGRATIS"], "BEMVINDO10"), True)


def teste_cupom_invalido():
    verificar(ex.resolver(["BEMVINDO10", "FRETEGRATIS"], "XYZ"), False)


def teste_lista_vazia():
    verificar(ex.resolver([], "BEMVINDO10"), False)
""",
        ),
        Ex(
            id="A09-003", titulo="Está no conjunto", nivel=2, tempo_min=5,
            tags=["big-o", "set", "membership"], requer=["A09-002", "A08-013"],
            enunciado="""
            O mesmo exercício anterior — mas agora `cupons_validos` chega como um
            **conjunto**, não uma lista.

            Exemplo:

                resolver({"BEMVINDO10", "FRETEGRATIS"}, "BEMVINDO10")  ->  True

            O código muda pouco (ou nada). O que muda é o custo: um `set` em
            Python é implementado como tabela hash, e `in` num set é O(1) em
            média — não importa se o conjunto tem 10 ou 10 milhões de itens.
            """,
            assinatura="def resolver(cupons_validos: set, codigo: str) -> bool:",
            dicas=[
                "O operador in funciona em conjuntos exatamente como em listas.",
                "A sintaxe não muda — o que muda é a estrutura recebida.",
                "return codigo in cupons_validos",
            ],
            solucao="    return codigo in cupons_validos",
            nota_da_solucao="Mesmo código do exercício anterior, mas agora O(1): é a estrutura que decide o custo, não a sintaxe.",
            testes="""
def teste_cupom_valido():
    verificar(ex.resolver({"BEMVINDO10", "FRETEGRATIS"}, "BEMVINDO10"), True)


def teste_cupom_invalido():
    verificar(ex.resolver({"BEMVINDO10", "FRETEGRATIS"}, "XYZ"), False)


def teste_conjunto_vazio():
    verificar(ex.resolver(set(), "BEMVINDO10"), False)
""",
        ),
        Ex(
            id="A09-004", titulo="Duplicata perto demais", nivel=3, tempo_min=9,
            tags=["big-o", "dict", "last-seen-index", "classico"],
            requer=["A08-009"],
            enunciado="""
            Um sistema de pedidos vê IDs chegando em sequência e quer flagar
            repetições **próximas demais para ser coincidência** — a mesma ID
            aparecendo de novo a `k` posições ou menos de distância.

            Devolva `True` se existir alguma ID repetida com distância **menor ou
            igual** a `k` entre as duas ocorrências.

            Exemplos:

                resolver(["a", "b", "c", "a"], 3)  ->  True   (distância 3)
                resolver(["a", "b", "c", "a"], 2)  ->  False  (distância 3 > 2)
                resolver(["a", "b", "a"], 2)       ->  True   (distância 2)

            Guarde num dicionário a **última posição** em que cada valor
            apareceu. Ao encontrar o valor de novo, a distância é a posição atual
            menos a posição guardada — sem precisar comparar com todas as
            ocorrências anteriores, só com a mais recente.
            """,
            assinatura="def resolver(ids: list, k: int) -> bool:",
            dicas=[
                "Percorra com o índice (enumerate) e guarde a última posição de\\ncada valor num dicionário.",
                "Ao rever um valor, a distância é indice_atual - ultima_posicao[valor].",
                "Se a distância for <= k, já pode devolver True; senão, atualize\\na última posição e continue.",
            ],
            solucao="""
            ultima_posicao = {}
            for indice, valor in enumerate(ids):
                if valor in ultima_posicao and indice - ultima_posicao[valor] <= k:
                    return True
                ultima_posicao[valor] = indice
            return False
            """,
            nota_da_solucao="Uma passada só, O(n): o dicionário guarda só a ocorrência mais recente de cada valor.",
            testes="""
def teste_distancia_igual_a_k():
    verificar(ex.resolver(["a", "b", "c", "a"], 3), True)


def teste_distancia_maior_que_k():
    verificar(ex.resolver(["a", "b", "c", "a"], 2), False)


def teste_distancia_dois():
    verificar(ex.resolver(["a", "b", "a"], 2), True)


def teste_sem_repeticao():
    verificar(ex.resolver(["a", "b", "c"], 5), False)


def teste_repeticao_distante_demais():
    verificar(ex.resolver(["a", "b", "c", "d", "a"], 2), False)


def teste_lista_vazia():
    verificar(ex.resolver([], 3), False)
""",
        ),
        Ex(
            id="A09-005", titulo="Some o intervalo sem repetir a conta", nivel=3,
            tempo_min=10, tags=["big-o", "prefix-sum"],
            enunciado="""
            Você recebe as vendas diárias de um período e uma lista de perguntas,
            cada uma pedindo a soma de vendas entre dois dias (o segundo dia
            **exclusivo**, igual ao fatiamento que você já usa).

            Devolva a lista com a resposta de cada pergunta, na mesma ordem.

            Exemplo:

                resolver([10, 20, 30, 40], [(0, 2), (1, 4), (0, 4)])
                ->  [30, 90, 100]

                # pergunta (0, 2): vendas[0] + vendas[1] = 10 + 20 = 30
                # pergunta (1, 4): vendas[1] + vendas[2] + vendas[3] = 90
                # pergunta (0, 4): a soma inteira = 100

            Se houver **muitas** perguntas, somar `vendas[inicio:fim]` de novo a
            cada uma custa caro: cada soma custa O(tamanho do intervalo), e isso
            se repete para cada pergunta. Monte uma vez uma lista de **somas
            acumuladas** (`prefixo[i]` = soma de tudo antes da posição `i`) e
            responda cada pergunta com uma subtração: `prefixo[fim] - prefixo[inicio]`.
            Depois do pré-processamento, cada pergunta custa O(1).
            """,
            assinatura="def resolver(vendas: list, perguntas: list) -> list:",
            dicas=[
                "Monte uma lista prefixo do mesmo tamanho de vendas + 1, começando\\nem 0, onde prefixo[i] guarda a soma de vendas[0:i].",
                "prefixo[i+1] = prefixo[i] + vendas[i] — cada posição soma o valor\\nanterior mais o item atual.",
                "Cada pergunta (inicio, fim) vira só: prefixo[fim] - prefixo[inicio].",
            ],
            solucao="""
            prefixo = [0]
            for venda in vendas:
                prefixo.append(prefixo[-1] + venda)

            respostas = []
            for inicio, fim in perguntas:
                respostas.append(prefixo[fim] - prefixo[inicio])
            return respostas
            """,
            nota_da_solucao="O(n) para montar o prefixo, mais O(1) por pergunta — no total O(n + perguntas), não O(n × perguntas).",
            testes="""
def teste_tres_perguntas():
    verificar(
        ex.resolver([10, 20, 30, 40], [(0, 2), (1, 4), (0, 4)]),
        [30, 90, 100],
    )


def teste_intervalo_de_um_dia():
    verificar(ex.resolver([5, 10, 15], [(1, 2)]), [10])


def teste_sem_perguntas():
    verificar(ex.resolver([1, 2, 3], []), [])


def teste_muitas_perguntas_pequenas():
    vendas = [1] * 100
    perguntas = [(i, i + 1) for i in range(100)]
    verificar(ex.resolver(vendas, perguntas), [1] * 100)
""",
        ),
        Ex(
            id="A09-006", titulo="Quem comprou nas duas, rápido", nivel=4,
            tempo_min=10, tags=["big-o", "set", "desempenho", "cronometrado"],
            requer=["A08-014", "A09-003"],
            preambulo_do_teste=PREAMBULO_TESTE_CRONOMETRADO,
            enunciado="""
            A mesma pergunta do exercício de campanhas do módulo A8 — quem abriu
            as duas — só que agora o catálogo de clientes é grande de verdade:
            centenas de milhares de nomes, não meia dúzia.

            Devolva o conjunto de clientes que aparecem nas duas listas.

            Exemplo:

                resolver(["ana", "bruno"], ["bruno", "caio"])  ->  {"bruno"}

            Comparar cada nome da lista A com **todos** os nomes da lista B
            (`x in lista_b` dentro de um `for x in lista_a`) é O(n × m) — com as
            duas listas grandes, isso demora visivelmente. Transformar as duas em
            conjuntos primeiro custa O(n + m) e a interseção é imediata.
            """,
            assinatura="def resolver(clientes_a: list, clientes_b: list) -> set:",
            dicas=[
                "Nada de comparar item a item entre as duas listas originais.",
                "Transforme as duas listas em conjuntos antes de qualquer comparação.",
                "return set(clientes_a) & set(clientes_b)",
            ],
            solucao="    return set(clientes_a) & set(clientes_b)",
            nota_da_solucao="set(...) custa O(n) e O(m); a interseção com & é O(min(n, m)) — no total, O(n + m).",
            testes="""
def teste_caso_pequeno():
    verificar(ex.resolver(["ana", "bruno"], ["bruno", "caio"]), {"bruno"})


def teste_sem_intersecao():
    verificar(ex.resolver(["ana"], ["bruno"]), set())


def teste_grande_e_rapido():
    a = [f"cliente_{i}" for i in range(10_000)]
    b = [f"cliente_{i}" for i in range(5_000, 15_000)]
    esperado = set(a) & set(b)

    with t.cronometrar() as tempo:
        obtido = ex.resolver(a, b)

    verificar(obtido, esperado, nome="conjunto de clientes em comum")
    t.verificar_tempo(
        tempo["segundos"], limite=0.3,
        dica="compare por conjuntos (&), não percorrendo uma lista dentro da outra.",
    )
""",
        ),
        Ex(
            id="A09-007", titulo="Sem repetir, na ordem, rápido", nivel=3,
            tempo_min=9, tags=["big-o", "set", "dedup", "desempenho", "cronometrado"],
            requer=["A05-006", "A09-003"],
            preambulo_do_teste=PREAMBULO_TESTE_CRONOMETRADO,
            enunciado="""
            Remova os itens repetidos de uma lista, **preservando a ordem da
            primeira aparição de cada um** — e fazendo isso rápido mesmo para
            listas grandes.

            Exemplo:

                resolver([3, 1, 3, 2, 1])  ->  [3, 1, 2]

            `set(lista)` sozinho remove as repetições, mas **não preserva a
            ordem original** — e o exercício pede a ordem da primeira aparição.
            A armadilha comum é escrever `if item not in resultado` para checar
            se um item já foi colocado na lista de saída: isso funciona, mas
            `resultado` cresce a cada volta, e cada `in` custa O(tamanho de
            resultado) — o laço inteiro vira O(n²). Use um `set` à parte só para
            lembrar o que já foi visto; verificar nele é O(1).
            """,
            assinatura="def resolver(itens: list) -> list:",
            dicas=[
                "Dois acumuladores: a lista de resultado (na ordem) e um set\\nà parte, só para saber o que já apareceu.",
                "Checar 'já vi este item?' deve ser feito no set, nunca na lista\\nde resultado — senão o custo do 'in' cresce junto com o resultado.",
                "if item not in vistos: vistos.add(item); resultado.append(item)",
            ],
            solucao="""
            vistos = set()
            resultado = []
            for item in itens:
                if item not in vistos:
                    vistos.add(item)
                    resultado.append(item)
            return resultado
            """,
            nota_da_solucao="O 'not in' aqui é no set (O(1)), não na lista de resultado — é essa troca que mantém o laço em O(n).",
            testes="""
def teste_caso_pequeno():
    verificar(ex.resolver([3, 1, 3, 2, 1]), [3, 1, 2])


def teste_sem_repeticao():
    verificar(ex.resolver([1, 2, 3]), [1, 2, 3])


def teste_lista_vazia():
    verificar(ex.resolver([]), [])


def teste_grande_e_rapido():
    dados = list(range(10_000)) * 3
    esperado = list(range(10_000))

    with t.cronometrar() as tempo:
        obtido = ex.resolver(dados)

    verificar(obtido, esperado)
    t.verificar_tempo(
        tempo["segundos"], limite=0.35,
        dica="troque 'if item not in resultado' por uma checagem num set à parte.",
    )
""",
        ),
        Ex(
            id="A09-008", titulo="Duas ofertas que somam ao vale-presente", nivel=4,
            tempo_min=11, tags=["big-o", "dict", "two-sum", "classico", "cronometrado"],
            requer=["A08-003"],
            preambulo_do_teste=PREAMBULO_TESTE_CRONOMETRADO,
            enunciado="""
            Talvez o problema mais clássico de entrevista de programação, na
            versão da Loja Aurora: um cliente tem um vale-presente de valor exato
            e quer gastar tudo em **duas** ofertas.

            Devolva os **índices** (i, j), com i < j, de duas ofertas cujos
            preços somam exatamente o valor do vale. Se não houver par assim,
            devolva `None`. Pode assumir que, quando existe solução, ela é única.

            Exemplos:

                resolver([2, 7, 11, 15], 9)   ->  (0, 1)   # 2 + 7 = 9
                resolver([2, 7, 11, 15], 26)  ->  (2, 3)   # 11 + 15 = 26
                resolver([2, 7, 11, 15], 99)  ->  None

            A solução com dois laços (`for i ... for j ...`) funciona, mas é
            O(n²) — para cada oferta, ela revê todas as outras. Um dicionário
            resolve em uma passada só: para cada preço, pergunte "o que falta
            para completar o vale já apareceu antes?".
            """,
            assinatura="def resolver(precos: list, vale: int) -> tuple[int, int] | None:",
            dicas=[
                "Não compare cada preço com todos os outros — percorra a lista\\numa vez só, guardando o que já viu.",
                "Para o preço atual, o que falta é vale - preco. Já apareceu antes?",
                "vistos é um dict {preco: indice}; a cada item, cheque\\nvale - preco_atual em vistos antes de adicionar o atual.",
            ],
            solucao="""
            vistos = {}
            for indice, preco in enumerate(precos):
                falta = vale - preco
                if falta in vistos:
                    return (vistos[falta], indice)
                vistos[preco] = indice
            return None
            """,
            nota_da_solucao="Uma passada, O(n): cada preço é comparado só contra o dicionário (O(1)), nunca contra a lista inteira.",
            testes="""
def teste_par_no_comeco():
    verificar(ex.resolver([2, 7, 11, 15], 9), (0, 1))


def teste_par_no_fim():
    verificar(ex.resolver([2, 7, 11, 15], 26), (2, 3))


def teste_sem_par():
    verificar(ex.resolver([2, 7, 11, 15], 99), None)


def teste_grande_e_rapido():
    precos = list(range(0, 120_000, 10))  # 12.000 preços, nenhum par soma ao vale
    vale = -999_999

    with t.cronometrar() as tempo:
        obtido = ex.resolver(precos, vale)

    verificar(obtido, None, nome="resultado")
    t.verificar_tempo(
        tempo["segundos"], limite=0.4,
        dica="troque os dois for aninhados por um dict de {preço: índice}.",
    )
""",
        ),
        Ex(
            id="A09-009", titulo="Fila sem gargalo", nivel=4, tempo_min=11,
            tags=["big-o", "deque", "fila", "desempenho", "cronometrado"],
            preambulo="from collections import deque",
            preambulo_do_teste=f"{PREAMBULO_TESTE_CRONOMETRADO}\nfrom collections import deque",
            enunciado="""
            O suporte da loja atende pedidos em rodadas: pega o primeiro da fila,
            atende uma rodada, e — se o pedido ainda não terminou — ele volta para
            o **fim** da fila. Cada pedido precisa de exatamente `rodadas`
            passagens pela frente da fila para ser concluído.

            Devolva a lista de pedidos **na ordem em que foram concluídos**.

            Exemplo, com `rodadas=2`:

                resolver(["p1", "p2", "p3"], 2)  ->  ["p1", "p2", "p3"]
                # rodada 1: p1 (falta 1), p2 (falta 1), p3 (falta 1) — fila: p1,p2,p3 de novo
                # rodada 2: p1 conclui, p2 conclui, p3 conclui

            `lista.pop(0)` tira o primeiro item, mas **desloca todos os outros
            uma posição** — é O(n) a cada chamada, e aqui isso acontece milhares
            de vezes. `collections.deque` foi construída exatamente para tirar e
            colocar itens nas pontas em O(1): troque `pop(0)` por `popleft()`.
            """,
            assinatura="def resolver(pedidos: list, rodadas: int) -> list:",
            dicas=[
                "collections.deque tem os métodos popleft() e append(), os dois O(1).",
                "Simule rodada por rodada: tire o da frente, diminua o contador\\ndele, e recoloque no fim se ainda não chegou a zero.",
                "fila = deque(pedidos); restam = {p: rodadas for p in pedidos};\\ndepois um while fila: com popleft() e append().",
            ],
            solucao="""
            fila = deque(pedidos)
            restam = {pedido: rodadas for pedido in pedidos}
            concluidos = []
            while fila:
                atual = fila.popleft()
                restam[atual] -= 1
                if restam[atual] == 0:
                    concluidos.append(atual)
                else:
                    fila.append(atual)
            return concluidos
            """,
            nota_da_solucao="popleft()/append() em deque são O(1) cada; a mesma simulação com list.pop(0) seria O(n) por chamada.",
            testes="""
def teste_uma_rodada_mantem_a_ordem():
    verificar(ex.resolver(["p1", "p2", "p3"], 1), ["p1", "p2", "p3"])


def teste_duas_rodadas():
    verificar(ex.resolver(["p1", "p2", "p3"], 2), ["p1", "p2", "p3"])


def teste_fila_vazia():
    verificar(ex.resolver([], 3), [])


def teste_grande_e_rapido():
    def round_robin_referencia(pedidos, rodadas):
        # Implementação de referência, independente da solução do exercício —
        # existe só para calcular o esperado, não para servir de gabarito.
        fila = deque(pedidos)
        restam = {p: rodadas for p in pedidos}
        concluidos = []
        while fila:
            atual = fila.popleft()
            restam[atual] -= 1
            if restam[atual] == 0:
                concluidos.append(atual)
            else:
                fila.append(atual)
        return concluidos

    pedidos = [f"p{i}" for i in range(80_000)]
    esperado = round_robin_referencia(pedidos, 3)

    with t.cronometrar() as tempo:
        obtido = ex.resolver(pedidos, 3)

    verificar(obtido, esperado, nome="ordem de conclusão")
    t.verificar_tempo(
        tempo["segundos"], limite=0.5,
        dica="troque a lista por collections.deque, e pop(0) por popleft().",
    )
""",
        ),
    ],
)

MODULOS = [A09]
