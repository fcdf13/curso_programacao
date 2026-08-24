"""Bloco A, módulo 10: tuplas e desempacotamento."""

from autoria.modelo import Exercicio as Ex
from autoria.modelo import Modulo

A10 = Modulo(
    id="A10",
    titulo="Módulo A10 — Tuplas e desempacotamento",
    resumo="A estrutura que não muda — e o jeito elegante de tirar valores dela.",
    teoria="""
## Tupla: como uma lista, mas travada

```python
ponto = (3, 4)
ponto[0]        # 3   — indexação funciona igual à lista
len(ponto)      # 2
```

Você já usa tuplas desde o A1 — todo `return a, b` devolve uma. A diferença que
importa agora: **tupla não muda depois de criada**.

```python
ponto[0] = 10        # TypeError: 'tuple' object does not support item assignment
```

Se você precisa de outra versão, cria uma tupla nova — não edita a antiga:

```python
ponto = (10, ponto[1])     # troca só o primeiro valor, criando uma tupla nova
```

### Desempacotar: tirar os valores de uma vez

```python
ponto = (3, 4)
x, y = ponto        # x=3, y=4 — uma variável para cada posição

nome, idade = "Ana", 30    # os parênteses da tupla são opcionais aqui
```

O número de variáveis à esquerda precisa bater com o de valores à direita —
senão é `ValueError: too many values to unpack` (ou de menos).

### O `_` para o que você não quer

```python
_, uf, _ = ("Ana", "SP", "2024-01-01")   # só a UF interessa desta vez
```

`_` é uma variável como outra qualquer — o nome é só uma convenção para dizer
"não vou usar isto".

### `*` pega "o resto"

```python
numeros = [10, 20, 30, 40]

primeiro, *resto = numeros      # primeiro=10, resto=[20, 30, 40]
*inicio, ultimo = numeros       # inicio=[10, 20, 30], ultimo=40
primeiro, *meio, ultimo = numeros   # primeiro=10, meio=[20, 30], ultimo=40
```

O `*` sempre vira uma **lista** (mesmo que a entrada original fosse tupla), e só
pode aparecer uma vez em cada desempacotamento — o Python não saberia como
dividir "o resto" em dois lugares diferentes.

### Por que a imutabilidade importa: tupla é hashável

Dicionário e conjunto exigem que a chave seja **hashável** — e uma lista não é
(porque ela muda; se mudasse depois de virar chave, a tabela hash quebraria).
Uma tupla é hashável, então serve de chave onde uma lista não serviria:

```python
vendas_por_uf_e_categoria = {}
vendas_por_uf_e_categoria[("SP", "Moda")] = 1500.0   # a chave é uma tupla
```
""",
    exercicios=[
        Ex(
            id="A10-001", titulo="Criar e indexar uma tupla", nivel=1, tempo_min=4,
            tags=["tupla", "criacao"],
            enunciado="""
            Monte uma tupla com o nome do produto e o preço, nessa ordem.

            Exemplo:

                resolver("Fone", 99.9)  ->  ("Fone", 99.9)

            Tupla se escreve entre parênteses, com vírgula separando os itens —
            igual à lista, mas com `()` no lugar de `[]`.
            """,
            assinatura="def resolver(nome: str, preco: float) -> tuple:",
            dicas=[
                "Parênteses com itens separados por vírgula criam uma tupla.",
                "A ordem dos itens na tupla é a ordem em que você escreve.",
                'return (nome, preco)',
            ],
            solucao="    return (nome, preco)",
            testes="""
def teste_produto_e_preco():
    verificar(ex.resolver("Fone", 99.9), ("Fone", 99.9))


def teste_outro_produto():
    verificar(ex.resolver("Capa", 25.0), ("Capa", 25.0))
""",
        ),
        Ex(
            id="A10-002", titulo="Desempacotar dois valores", nivel=1, tempo_min=5,
            tags=["tupla", "desempacotamento"], requer=["A10-001"],
            enunciado="""
            Você recebe um produto como tupla `(nome, preço)`. Devolva o texto
            `"nome custa R$ preço"`, com duas casas decimais.

            Exemplo:

                resolver(("Fone", 99.9))  ->  "Fone custa R$ 99.90"

            Desempacote a tupla em duas variáveis antes de montar o texto —
            fica mais legível do que acessar `produto[0]` e `produto[1]`.
            """,
            assinatura="def resolver(produto: tuple) -> str:",
            dicas=[
                "nome, preco = produto tira os dois valores de uma vez.",
                "Depois é só montar a f-string com as duas variáveis.",
                'nome, preco = produto; return f"{nome} custa R$ {preco:.2f}"',
            ],
            solucao="""
            nome, preco = produto
            return f"{nome} custa R$ {preco:.2f}"
            """,
            nota_da_solucao="Desempacotar antes deixa o resto do código lendo nome e preco, não produto[0]/produto[1].",
            testes="""
def teste_produto_simples():
    verificar(ex.resolver(("Fone", 99.9)), "Fone custa R$ 99.90")


def teste_preco_redondo():
    verificar(ex.resolver(("Livro", 30.0)), "Livro custa R$ 30.00")
""",
        ),
        Ex(
            id="A10-003", titulo="Tupla não muda — cria outra", nivel=2, tempo_min=6,
            tags=["tupla", "imutabilidade"], requer=["A10-002"],
            enunciado="""
            Você recebe um produto como `(nome, preço)` e um preço novo. Devolva
            uma tupla **nova** com o mesmo nome e o preço atualizado.

            Exemplo:

                resolver(("Fone", 99.9), 79.9)  ->  ("Fone", 79.9)

            `produto[1] = novo_preco` estouraria `TypeError` — tupla não aceita
            atribuição por índice depois de criada. O jeito é montar uma tupla
            nova, reaproveitando o que não mudou.
            """,
            assinatura="def resolver(produto: tuple, novo_preco: float) -> tuple:",
            dicas=[
                "Tente produto[1] = novo_preco só para ver o erro — depois apague.",
                "Desempacote o produto para pegar o nome, e monte uma tupla nova.",
                "nome, _ = produto; return (nome, novo_preco)",
            ],
            solucao="""
            nome, _ = produto
            return (nome, novo_preco)
            """,
            nota_da_solucao="O _ marca que o preço antigo foi descartado de propósito — a tupla velha não é alterada, só ignorada.",
            testes="""
def teste_atualiza_preco():
    verificar(ex.resolver(("Fone", 99.9), 79.9), ("Fone", 79.9))


def teste_preco_para_zero():
    verificar(ex.resolver(("Amostra", 10.0), 0.0), ("Amostra", 0.0))
""",
        ),
        Ex(
            id="A10-004", titulo="Trocar dois itens de uma lista", nivel=2, tempo_min=6,
            tags=["tupla", "desempacotamento", "lista"], requer=["A01-012"],
            enunciado="""
            Troque de lugar os itens das posições `i` e `j` de uma lista, e
            devolva a lista.

            Exemplo:

                resolver([10, 20, 30, 40], 0, 3)  ->  [40, 20, 30, 10]

            Você já trocou duas variáveis de lugar no módulo A1
            (`a, b = b, a`). A mesma ideia funciona com posições de lista —
            sem precisar de uma variável temporária para guardar o valor.
            """,
            assinatura="def resolver(itens: list, i: int, j: int) -> list:",
            dicas=[
                "A troca sem variável temporária que você viu no A1 funciona\\ntambém com itens[i] e itens[j].",
                "Os dois lados da atribuição são montados antes de qualquer\\nvalor ser sobrescrito.",
                "itens[i], itens[j] = itens[j], itens[i]",
            ],
            solucao="""
            itens[i], itens[j] = itens[j], itens[i]
            return itens
            """,
            nota_da_solucao="Python monta a tupla (itens[j], itens[i]) inteira antes de atribuir — por isso não precisa de variável auxiliar.",
            testes="""
def teste_pontas_opostas():
    verificar(ex.resolver([10, 20, 30, 40], 0, 3), [40, 20, 30, 10])


def teste_posicoes_vizinhas():
    verificar(ex.resolver([1, 2, 3], 0, 1), [2, 1, 3])


def teste_mesma_posicao_nao_muda_nada():
    verificar(ex.resolver([1, 2, 3], 1, 1), [1, 2, 3])
""",
        ),
        Ex(
            id="A10-005", titulo="Só o que interessa", nivel=2, tempo_min=6,
            tags=["tupla", "desempacotamento", "descarte"],
            enunciado="""
            Um registro de cadastro chega como `(nome, uf, data_cadastro)`.
            Devolva só a UF.

            Exemplo:

                resolver(("Ana", "SP", "2024-01-15"))  ->  "SP"

            Dá para escrever `return registro[1]` — mas o exercício é sobre
            desempacotar os três valores de uma vez, descartando os dois que
            não interessam com `_`.
            """,
            assinatura="def resolver(registro: tuple) -> str:",
            dicas=[
                "Desempacote os três valores de uma vez, um nome por posição.",
                "Use _ no lugar de nome e de data — você não vai usar nenhum dos dois.",
                "_, uf, _ = registro; return uf",
            ],
            solucao="""
            _, uf, _ = registro
            return uf
            """,
            nota_da_solucao="Usar _ duas vezes é permitido — cada um é só uma variável descartável, sem relação entre si.",
            testes="""
def teste_registro_completo():
    verificar(ex.resolver(("Ana", "SP", "2024-01-15")), "SP")


def teste_outro_estado():
    verificar(ex.resolver(("Bruno", "RJ", "2023-06-01")), "RJ")
""",
        ),
        Ex(
            id="A10-006", titulo="O primeiro e o resto", nivel=3, tempo_min=7,
            tags=["tupla", "desempacotamento", "star-expression"],
            requer=["A10-005"],
            enunciado="""
            Devolva uma tupla `(primeiro item, lista com os demais)`.

            Exemplos:

                resolver([10, 20, 30])  ->  (10, [20, 30])
                resolver([5])           ->  (5, [])

            `*resto` no desempacotamento junta "tudo que sobrou" numa lista —
            mesmo que a entrada seja só um item.
            """,
            assinatura="def resolver(itens: list) -> tuple:",
            dicas=[
                "O desempacotamento aceita um * na frente de uma das variáveis.",
                "primeiro, *resto = itens separa o primeiro do restante.",
                "primeiro, *resto = itens; return primeiro, resto",
            ],
            solucao="""
            primeiro, *resto = itens
            return primeiro, resto
            """,
            nota_da_solucao="*resto sempre vira lista, mesmo quando só sobra um item — ou nenhum.",
            testes="""
def teste_tres_itens():
    verificar(ex.resolver([10, 20, 30]), (10, [20, 30]))


def teste_um_item_so():
    verificar(ex.resolver([5]), (5, []))


def teste_dois_itens():
    verificar(ex.resolver(["a", "b"]), ("a", ["b"]))
""",
        ),
        Ex(
            id="A10-007", titulo="O resto e o último", nivel=3, tempo_min=7,
            tags=["tupla", "desempacotamento", "star-expression"],
            requer=["A10-006"],
            enunciado="""
            Devolva uma tupla `(lista com todos menos o último, último item)` —
            o espelho do exercício anterior.

            Exemplos:

                resolver([10, 20, 30])  ->  ([10, 20], 30)
                resolver([5])           ->  ([], 5)

            O `*` também funciona no começo do desempacotamento — o que sobra
            fica sempre do lado sem asterisco.
            """,
            assinatura="def resolver(itens: list) -> tuple:",
            dicas=[
                "Desta vez o * vai na primeira variável, não na última.",
                "*inicio, ultimo = itens deixa ultimo com o último item, e\\ninicio com todo o resto.",
                "*inicio, ultimo = itens; return inicio, ultimo",
            ],
            solucao="""
            *inicio, ultimo = itens
            return inicio, ultimo
            """,
            testes="""
def teste_tres_itens():
    verificar(ex.resolver([10, 20, 30]), ([10, 20], 30))


def teste_um_item_so():
    verificar(ex.resolver([5]), ([], 5))


def teste_dois_itens():
    verificar(ex.resolver(["a", "b"]), (["a"], "b"))
""",
        ),
        Ex(
            id="A10-008", titulo="Tupla como chave", nivel=4, tempo_min=10,
            tags=["tupla", "dict", "hashable", "regra-de-negocio"],
            requer=["A08-009", "A10-002"],
            enunciado="""
            Some as vendas por par **(estado, categoria)** — uma combinação que
            uma chave só (a UF, ou só a categoria) não conseguiria representar.

            Você recebe três listas alinhadas: estados, categorias e valores.
            Devolva um dicionário onde a chave é a tupla `(uf, categoria)` e o
            valor é a soma das vendas daquela combinação.

            Exemplo:

                resolver(["SP", "SP", "RJ"], ["Moda", "Casa", "Moda"], [100.0, 50.0, 80.0])
                ->  {("SP", "Moda"): 100.0, ("SP", "Casa"): 50.0, ("RJ", "Moda"): 80.0}

            Uma lista `[uf, categoria]` não poderia ser chave de dicionário —
            listas não são hasháveis. Uma tupla `(uf, categoria)` pode, porque
            não muda depois de criada.
            """,
            assinatura="def resolver(ufs: list, categorias: list, valores: list) -> dict:",
            dicas=[
                "A chave do dicionário é uma tupla (uf, categoria) montada a\\ncada volta do laço.",
                "Sem essa tupla, o dicionário não teria como distinguir\\n('SP', 'Moda') de ('SP', 'Casa').",
                "chave = (uf, categoria); total[chave] = total.get(chave, 0) + valor",
            ],
            solucao="""
            total = {}
            for uf, categoria, valor in zip(ufs, categorias, valores):
                chave = (uf, categoria)
                total[chave] = total.get(chave, 0) + valor
            return total
            """,
            nota_da_solucao="Mesmo padrão de contagem do A8, mas com uma tupla no lugar de uma chave só — só é possível porque tupla é hashável.",
            testes="""
def teste_tres_combinacoes():
    verificar(
        ex.resolver(["SP", "SP", "RJ"], ["Moda", "Casa", "Moda"], [100.0, 50.0, 80.0]),
        {("SP", "Moda"): 100.0, ("SP", "Casa"): 50.0, ("RJ", "Moda"): 80.0},
    )


def teste_mesma_combinacao_repetida():
    verificar(
        ex.resolver(["SP", "SP"], ["Moda", "Moda"], [100.0, 50.0]),
        {("SP", "Moda"): 150.0},
    )


def teste_listas_vazias():
    verificar(ex.resolver([], [], []), {})
""",
        ),
    ],
)

MODULOS = [A10]
