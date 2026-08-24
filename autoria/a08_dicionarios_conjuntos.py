"""Bloco A, módulo 8: dicionários e conjuntos."""

from autoria.modelo import Exercicio as Ex
from autoria.modelo import Modulo

A08 = Modulo(
    id="A08",
    titulo="Módulo A8 — Dicionários e conjuntos",
    resumo="As duas estruturas que resolvem 'isso já apareceu?' e 'quanto disso existe?'.",
    teoria="""
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
""",
    exercicios=[
        Ex(
            id="A08-001", titulo="Montar um dicionário", nivel=1, tempo_min=4,
            tags=["dict", "criacao"],
            enunciado="""
            Monte um dicionário de preços a partir de duas listas alinhadas: nomes e preços.

            Exemplo:

                resolver(["Fone", "Capa"], [99.9, 25.0])
                ->  {"Fone": 99.9, "Capa": 25.0}

            `zip` junta as duas listas par a par; `dict(...)` transforma os pares em
            dicionário.
            """,
            assinatura="def resolver(nomes: list, precos: list) -> dict:",
            dicas=[
                "zip(nomes, precos) entrega pares (nome, preco), um por vez.",
                "A função dict(...) aceita uma sequência de pares e monta o dicionário.",
                "return dict(zip(nomes, precos))",
            ],
            solucao="    return dict(zip(nomes, precos))",
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
            id="A08-002", titulo="Acessar com risco", nivel=1, tempo_min=4,
            tags=["dict", "acesso"], requer=["A08-001"],
            enunciado="""
            Devolva o preço do produto informado, buscando direto no dicionário.

            Exemplo:

                resolver({"Fone": 99.9, "Capa": 25.0}, "Fone")  ->  99.9

            Pode assumir que o produto sempre existe no dicionário — este exercício
            é só sobre o acesso direto. O que fazer quando ele pode não existir é o
            próximo.
            """,
            assinatura="def resolver(precos: dict, produto: str) -> float:",
            dicas=[
                "Acesso direto em dicionário usa colchetes, como em lista — mas com a chave.",
                "precos[produto]",
                "return precos[produto]",
            ],
            solucao="    return precos[produto]",
            testes="""
def teste_acha_o_preco():
    verificar(ex.resolver({"Fone": 99.9, "Capa": 25.0}, "Fone"), 99.9)


def teste_outro_produto():
    verificar(ex.resolver({"Fone": 99.9, "Capa": 25.0}, "Capa"), 25.0)
""",
        ),
        Ex(
            id="A08-003", titulo="Acessar sem risco", nivel=2, tempo_min=5,
            tags=["dict", "get"], requer=["A08-002"],
            enunciado="""
            Agora o produto pode **não existir** no catálogo. Devolva o preço se existir,
            ou `0.0` caso contrário — sem estourar erro.

            Exemplos:

                resolver({"Fone": 99.9}, "Fone")   ->  99.9
                resolver({"Fone": 99.9}, "Mouse")  ->  0.0

            `precos["Mouse"]` estouraria `KeyError`. `.get(chave, padrao)` não estoura —
            devolve o padrão quando a chave não existe.
            """,
            assinatura="def resolver(precos: dict, produto: str) -> float:",
            dicas=[
                "Existe uma versão de acesso que não estoura quando a chave falta.",
                "d.get(chave, padrao) devolve padrao em vez de erro.",
                "return precos.get(produto, 0.0)",
            ],
            solucao="    return precos.get(produto, 0.0)",
            nota_da_solucao="`.get` com padrão é o jeito idiomático de 'buscar, e se não tiver, tanto faz'.",
            testes="""
def teste_produto_existe():
    verificar(ex.resolver({"Fone": 99.9}, "Fone"), 99.9)


def teste_produto_nao_existe():
    verificar(ex.resolver({"Fone": 99.9}, "Mouse"), 0.0,
              dica="precos[produto] estouraria KeyError; use .get(produto, 0.0).")


def teste_catalogo_vazio():
    verificar(ex.resolver({}, "Fone"), 0.0)
""",
        ),
        Ex(
            id="A08-004", titulo="Chave, não valor", nivel=2, tempo_min=5,
            tags=["dict", "in"],
            enunciado="""
            Devolva `True` se o texto informado for uma **chave** do dicionário.

            Exemplos:

                resolver({"SP": 15.0, "RJ": 15.0}, "SP")    ->  True
                resolver({"SP": 15.0, "RJ": 15.0}, 15.0)    ->  False
                resolver({"SP": 15.0, "RJ": 15.0}, "AM")    ->  False

            O segundo caso é a pegadinha: `15.0` é um **valor** que existe no
            dicionário, mas `in` só enxerga chaves.
            """,
            assinatura="def resolver(precos: dict, alvo) -> bool:",
            dicas=[
                "in em um dicionário testa se o valor é uma das chaves.",
                "Não importa se o valor procurado aparece do lado dos valores.",
                "return alvo in precos",
            ],
            solucao="    return alvo in precos",
            testes="""
def teste_e_uma_chave():
    verificar(ex.resolver({"SP": 15.0, "RJ": 15.0}, "SP"), True)


def teste_e_um_valor_nao_uma_chave():
    verificar(ex.resolver({"SP": 15.0, "RJ": 15.0}, 15.0), False,
              dica="in testa as chaves. 15.0 é um valor, não uma chave.")


def teste_nao_existe():
    verificar(ex.resolver({"SP": 15.0, "RJ": 15.0}, "AM"), False)
""",
        ),
        Ex(
            id="A08-005", titulo="Criar ou atualizar", nivel=2, tempo_min=5,
            tags=["dict", "mutacao"],
            enunciado="""
            Registre o preço de um produto no dicionário — funciona tanto para um
            produto novo quanto para atualizar um preço existente — e devolva o
            dicionário.

            Exemplos:

                resolver({"Fone": 99.9}, "Fone", 89.9)   ->  {"Fone": 89.9}
                resolver({"Fone": 99.9}, "Capa", 25.0)   ->  {"Fone": 99.9, "Capa": 25.0}

            A mesma linha resolve os dois casos: não existe diferença de sintaxe
            entre criar e atualizar uma chave.
            """,
            assinatura="def resolver(precos: dict, produto: str, novo_preco: float) -> dict:",
            dicas=[
                "Atribuir a uma chave que já existe substitui o valor.",
                "Atribuir a uma chave que não existe cria a entrada.",
                "precos[produto] = novo_preco, e depois return precos.",
            ],
            solucao="""
            precos[produto] = novo_preco
            return precos
            """,
            testes="""
def teste_atualiza_existente():
    verificar(ex.resolver({"Fone": 99.9}, "Fone", 89.9), {"Fone": 89.9})


def teste_cria_novo():
    verificar(ex.resolver({"Fone": 99.9}, "Capa", 25.0),
              {"Fone": 99.9, "Capa": 25.0})


def teste_dicionario_vazio():
    verificar(ex.resolver({}, "Fone", 99.9), {"Fone": 99.9})
""",
        ),
        Ex(
            id="A08-006", titulo="Remover uma chave", nivel=2, tempo_min=5,
            tags=["dict", "pop"], requer=["A08-005"],
            enunciado="""
            Remova o produto do catálogo, se ele existir, e devolva o dicionário.
            Se o produto não existir, devolva o dicionário sem alterar nada — sem
            estourar erro.

            Exemplos:

                resolver({"Fone": 99.9, "Capa": 25.0}, "Capa")  ->  {"Fone": 99.9}
                resolver({"Fone": 99.9}, "Mouse")               ->  {"Fone": 99.9}

            `del precos[produto]` estouraria `KeyError` no segundo caso.
            `.pop(chave, None)` não estoura.
            """,
            assinatura="def resolver(precos: dict, produto: str) -> dict:",
            dicas=[
                "del estoura erro se a chave não existir; existe uma alternativa que não estoura.",
                "precos.pop(produto, None) remove se existir, e não faz nada (sem erro) se não existir.",
                "precos.pop(produto, None), e depois return precos.",
            ],
            solucao="""
            precos.pop(produto, None)
            return precos
            """,
            testes="""
def teste_remove_existente():
    verificar(ex.resolver({"Fone": 99.9, "Capa": 25.0}, "Capa"), {"Fone": 99.9})


def teste_remove_inexistente_nao_quebra():
    verificar(ex.resolver({"Fone": 99.9}, "Mouse"), {"Fone": 99.9},
              dica="del estouraria KeyError aqui — use .pop(produto, None).")
""",
        ),
        Ex(
            id="A08-007", titulo="Só as chaves, só os valores", nivel=2, tempo_min=5,
            tags=["dict", "keys", "values"],
            enunciado="""
            Devolva a tupla `(lista de produtos, lista de preços)`, na ordem em que
            aparecem no dicionário.

            Exemplo:

                resolver({"Fone": 99.9, "Capa": 25.0})
                ->  (["Fone", "Capa"], [99.9, 25.0])

            Desde o Python 3.7, um dicionário lembra a ordem em que as chaves foram
            inseridas — por isso a ordem do resultado é previsível.
            """,
            assinatura="def resolver(precos: dict) -> tuple[list, list]:",
            dicas=[
                ".keys() e .values() devolvem visões do dicionário, não listas de verdade.",
                "Envolva cada uma em list(...) para virar uma lista comum.",
                "return list(precos.keys()), list(precos.values())",
            ],
            solucao="    return list(precos.keys()), list(precos.values())",
            testes="""
def teste_dois_produtos():
    verificar(ex.resolver({"Fone": 99.9, "Capa": 25.0}),
              (["Fone", "Capa"], [99.9, 25.0]))


def teste_dicionario_vazio():
    verificar(ex.resolver({}), ([], []))
""",
        ),
        Ex(
            id="A08-008", titulo="Pares chave-valor", nivel=2, tempo_min=6,
            tags=["dict", "items", "f-string"], requer=["A08-007"],
            enunciado="""
            Monte uma lista de textos no formato `"produto: preço"`, um por item do
            dicionário, com duas casas decimais.

            Exemplo:

                resolver({"Fone": 99.9, "Capa": 25.0})
                ->  ["Fone: 99.90", "Capa: 25.00"]

            `.items()` entrega os pares `(chave, valor)` prontos para desempacotar
            num `for`, igual ao `zip` do módulo de laços.
            """,
            assinatura="def resolver(precos: dict) -> list:",
            dicas=[
                "for produto, preco in precos.items(): desempacota o par a cada volta.",
                'Formate com f"{produto}: {preco:.2f}".',
                "Acrescente cada texto numa lista que começa vazia.",
            ],
            solucao="""
            linhas = []
            for produto, preco in precos.items():
                linhas.append(f"{produto}: {preco:.2f}")
            return linhas
            """,
            testes="""
def teste_dois_produtos():
    verificar(ex.resolver({"Fone": 99.9, "Capa": 25.0}),
              ["Fone: 99.90", "Capa: 25.00"])


def teste_dicionario_vazio():
    verificar(ex.resolver({}), [])
""",
        ),
        Ex(
            id="A08-009", titulo="Contagem de ocorrências", nivel=3, tempo_min=8,
            tags=["dict", "get", "contagem", "classico"],
            enunciado="""
            Conte quantas vezes cada categoria aparece na lista de pedidos.

            Exemplo:

                resolver(["Moda", "Casa", "Moda", "Moda"])
                ->  {"Moda": 3, "Casa": 1}

            Este é o padrão de contagem mais usado em toda a análise de dados —
            e ele reaparece, em outra forma, em quase todo módulo daqui para frente.
            """,
            assinatura="def resolver(categorias: list) -> dict:",
            dicas=[
                "Comece com um dicionário vazio, antes do laço.",
                "Para cada item, some 1 à contagem daquela chave.",
                "contagem[categoria] = contagem.get(categoria, 0) + 1 — o .get(c, 0)\\né o que evita checar 'a chave já existe?' antes de somar.",
            ],
            solucao="""
            contagem = {}
            for categoria in categorias:
                contagem[categoria] = contagem.get(categoria, 0) + 1
            return contagem
            """,
            nota_da_solucao="`.get(chave, 0) + 1` resume duas linhas (checar e depois somar) numa só.",
            testes="""
def teste_categorias_repetidas():
    verificar(ex.resolver(["Moda", "Casa", "Moda", "Moda"]), {"Moda": 3, "Casa": 1})


def teste_todas_diferentes():
    verificar(ex.resolver(["A", "B", "C"]), {"A": 1, "B": 1, "C": 1})


def teste_lista_vazia():
    verificar(ex.resolver([]), {})


def teste_um_item_repetido_varias_vezes():
    verificar(ex.resolver(["X", "X", "X"]), {"X": 3})
""",
        ),
        Ex(
            id="A08-010", titulo="A chave do maior valor", nivel=3, tempo_min=8,
            tags=["dict", "max", "key"], requer=["A08-009"],
            enunciado="""
            Devolva o produto mais caro do catálogo — só o nome, não o preço.
            Se houver empate, devolva qualquer um dos empatados.

            Exemplo:

                resolver({"Fone": 200.0, "Notebook": 3000.0, "Capa": 30.0})
                ->  "Notebook"

            `max(dicionario)` devolveria a maior **chave** (ordem alfabética) — não é
            o que você quer. Você precisa comparar pelos **valores**.
            """,
            assinatura="def resolver(precos: dict) -> str:",
            dicas=[
                "max(precos) compara as chaves; você quer comparar pelos valores.",
                "max aceita um argumento key= que diz por qual critério comparar.",
                "return max(precos, key=precos.get)",
            ],
            solucao="    return max(precos, key=precos.get)",
            nota_da_solucao="`key=precos.get` diz: para decidir o maior, olhe precos.get(chave) — não a chave em si.",
            testes="""
def teste_um_produto_claramente_mais_caro():
    verificar(ex.resolver({"Fone": 200.0, "Notebook": 3000.0, "Capa": 30.0}), "Notebook")


def teste_produto_unico():
    verificar(ex.resolver({"Fone": 200.0}), "Fone")


def teste_nao_e_ordem_alfabetica():
    verificar(ex.resolver({"Zebra": 1.0, "Abelha": 99.0}), "Abelha",
              dica="max(precos) sozinho compararia as chaves em ordem alfabética.")
""",
        ),
        Ex(
            id="A08-011", titulo="Juntar dois catálogos", nivel=3, tempo_min=8,
            tags=["dict", "merge"],
            enunciado="""
            Junte dois catálogos de preço num só. Quando o mesmo produto aparece
            nos dois, **o segundo catálogo vence**.

            Exemplo:

                resolver({"Fone": 99.9, "Capa": 25.0}, {"Capa": 20.0, "Mouse": 45.0})
                ->  {"Fone": 99.9, "Capa": 20.0, "Mouse": 45.0}

            Repare no preço da Capa: veio do segundo dicionário, não do primeiro.
            """,
            assinatura="def resolver(catalogo_a: dict, catalogo_b: dict) -> dict:",
            dicas=[
                "Existe um operador que junta dois dicionários: |.",
                "Em a | b, quando a chave se repete, o valor de b vence.",
                "return catalogo_a | catalogo_b",
            ],
            solucao="    return catalogo_a | catalogo_b",
            nota_da_solucao="O operador | (Python 3.9+) resolve em uma expressão o que antes precisava de um loop.",
            testes="""
def teste_chave_repetida_o_segundo_vence():
    verificar(
        ex.resolver({"Fone": 99.9, "Capa": 25.0}, {"Capa": 20.0, "Mouse": 45.0}),
        {"Fone": 99.9, "Capa": 20.0, "Mouse": 45.0},
    )


def teste_sem_sobreposicao():
    verificar(ex.resolver({"A": 1}, {"B": 2}), {"A": 1, "B": 2})


def teste_segundo_vazio():
    verificar(ex.resolver({"A": 1}, {}), {"A": 1})
""",
        ),
        Ex(
            id="A08-012", titulo="Inverter um dicionário", nivel=3, tempo_min=8,
            tags=["dict", "comprehension-like", "inversao"], requer=["A08-008"],
            enunciado="""
            Troque as chaves pelos valores e vice-versa. Pode assumir que os valores
            originais são únicos (nenhum se repete), então nada se perde na troca.

            Exemplo:

                resolver({"SP": "São Paulo", "RJ": "Rio de Janeiro"})
                ->  {"São Paulo": "SP", "Rio de Janeiro": "RJ"}

            Percorra os pares originais e monte um dicionário novo com eles trocados.
            """,
            assinatura="def resolver(original: dict) -> dict:",
            dicas=[
                "Percorra os pares com .items(), como no exercício das siglas.",
                "Para cada par (chave, valor), o dicionário novo ganha valor -> chave.",
                "invertido[valor] = chave, dentro do laço.",
            ],
            solucao="""
            invertido = {}
            for chave, valor in original.items():
                invertido[valor] = chave
            return invertido
            """,
            testes="""
def teste_duas_siglas():
    verificar(ex.resolver({"SP": "São Paulo", "RJ": "Rio de Janeiro"}),
              {"São Paulo": "SP", "Rio de Janeiro": "RJ"})


def teste_dicionario_vazio():
    verificar(ex.resolver({}), {})


def teste_um_par_so():
    verificar(ex.resolver({"A": 1}), {1: "A"})
""",
        ),
        Ex(
            id="A08-013", titulo="Sem repetir", nivel=1, tempo_min=4,
            tags=["set", "criacao", "dedup"],
            enunciado="""
            Devolva os valores distintos da lista, como um **conjunto**.

            Exemplo:

                resolver(["SP", "RJ", "SP", "MG", "RJ"])  ->  {"SP", "RJ", "MG"}

            `set(lista)` remove as repetições de uma vez — não importa a ordem.
            """,
            assinatura="def resolver(itens: list) -> set:",
            dicas=[
                "Existe uma função que transforma qualquer sequência em conjunto.",
                "set(...) remove as repetições automaticamente.",
                "return set(itens)",
            ],
            solucao="    return set(itens)",
            testes="""
def teste_com_repetidos():
    verificar(ex.resolver(["SP", "RJ", "SP", "MG", "RJ"]), {"SP", "RJ", "MG"})


def teste_ja_sem_repeticao():
    verificar(ex.resolver(["A", "B"]), {"A", "B"})


def teste_lista_vazia():
    verificar(ex.resolver([]), set())
""",
        ),
        Ex(
            id="A08-014", titulo="Clientes de duas campanhas", nivel=4, tempo_min=10,
            tags=["set", "operacoes-de-conjunto", "regra-de-negocio"],
            requer=["A08-013"],
            enunciado="""
            A loja rodou duas campanhas de e-mail. Você recebe a lista de clientes
            que abriram a campanha A e a lista de quem abriu a campanha B.

            Devolva uma tupla com três conjuntos, nesta ordem:

                (abriram as duas, só a A, só a B)

            Exemplo:

                resolver(["ana", "bruno", "caio"], ["bruno", "caio", "duda"])
                ->  ({"bruno", "caio"}, {"ana"}, {"duda"})

            Três operações de conjunto resolvem os três, uma de cada.
            """,
            assinatura="def resolver(abriram_a: list, abriram_b: list) -> tuple[set, set, set]:",
            dicas=[
                "Transforme as duas listas em conjuntos primeiro — as operações\\nde conjunto não funcionam direto em listas.",
                "'as duas' é interseção (&); 'só a A' é diferença (A - B); 'só a B' é\\na diferença no sentido contrário (B - A).",
                "a, b = set(abriram_a), set(abriram_b); return a & b, a - b, b - a",
            ],
            solucao="""
            a = set(abriram_a)
            b = set(abriram_b)
            return a & b, a - b, b - a
            """,
            nota_da_solucao="Cada operação de conjunto responde exatamente uma das três perguntas — não precisa de laço.",
            testes="""
def teste_caso_geral():
    verificar(
        ex.resolver(["ana", "bruno", "caio"], ["bruno", "caio", "duda"]),
        ({"bruno", "caio"}, {"ana"}, {"duda"}),
    )


def teste_sem_sobreposicao():
    verificar(ex.resolver(["ana"], ["bruno"]), (set(), {"ana"}, {"bruno"}))


def teste_listas_identicas():
    verificar(ex.resolver(["ana", "bruno"], ["ana", "bruno"]),
              ({"ana", "bruno"}, set(), set()))


def teste_uma_lista_vazia():
    verificar(ex.resolver([], ["ana"]), (set(), set(), {"ana"}))
""",
        ),
    ],
)

MODULOS = [A08]
