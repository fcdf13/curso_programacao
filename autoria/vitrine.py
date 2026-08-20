"""Exercícios-vitrine dos blocos B (Pandas) e C (SQL).

Existem para você conferir os três formatos de exercício — Python puro, Pandas e
SQL — antes de o material completo dos blocos B, C e D ser escrito. O conteúdo é
real: são os primeiros exercícios de verdade de cada um desses módulos.
"""

from autoria.modelo import Exercicio as Ex
from autoria.modelo import Modulo

IMPORTA_PANDAS = "import pandas as pd"

# --------------------------------------------------------------------------- #
# B01 — Series e DataFrame
# --------------------------------------------------------------------------- #

B01 = Modulo(
    id="B01",
    titulo="Módulo B1 — Series e DataFrame",
    resumo="As duas estruturas do Pandas: a coluna e a tabela.",
    teoria="""
## Series é uma coluna. DataFrame é uma tabela.

```python
import pandas as pd

precos = pd.Series([49.9, 12.0, 230.5])          # uma coluna
produtos = pd.DataFrame({                         # uma tabela
    "nome": ["Fone", "Capa", "Notebook"],
    "preco": [49.9, 12.0, 230.5],
})
```

Um DataFrame é um conjunto de Series que compartilham o mesmo **índice** — os
rótulos das linhas, que por padrão são 0, 1, 2, ...

### Por que isso muda tudo

No Bloco A, somar uma lista de preços exigia um laço. Aqui:

```python
produtos["preco"].sum()
```

A operação vale para a coluna inteira de uma vez. Isso se chama **vetorização**,
e é a razão de o Pandas dar conta de milhões de linhas: o laço existe, mas roda
em C, não em Python.

### O primeiro olhar em qualquer tabela

```python
df.shape        # (linhas, colunas)
df.columns      # os nomes das colunas
df.dtypes       # o tipo de cada coluna
df.head()       # as 5 primeiras linhas
df.info()       # resumo: tipos, nulos, memória
df.describe()   # estatísticas das colunas numéricas
```

Antes de qualquer análise, `shape` e `dtypes`. Metade dos bugs de Pandas é uma
coluna que você achava numérica e o Pandas leu como texto.

### O dataset do curso

A Loja Aurora tem sete tabelas limpas — `clientes`, `produtos`, `pedidos`,
`itens_pedido`, `pagamentos`, `eventos_web`, `estoque_diario` — e duas sujas de
propósito, `clientes_bruto` e `avaliacoes_bruto`, para os módulos de limpeza.
Elas são as mesmas que você vai consultar em SQL no Bloco C.
""",
    exercicios=[
        Ex(
            id="B01-001", titulo="Montar um DataFrame", nivel=1, tempo_min=6,
            tags=["dataframe", "criacao"], linguagem="python",
            preambulo=IMPORTA_PANDAS, preambulo_do_teste=IMPORTA_PANDAS,
            enunciado="""
            Monte um DataFrame de duas colunas a partir de duas listas.

            A coluna com os nomes deve se chamar `nome`; a com os preços, `preco`.
            A ordem das colunas importa: `nome` primeiro.

            Exemplo:

                resolver(["Fone", "Capa"], [49.9, 12.0])

                ->     nome  preco
                    0  Fone   49.9
                    1  Capa   12.0

            A forma mais direta é passar um dicionário para `pd.DataFrame`:
            cada chave vira o nome de uma coluna, e cada valor, o conteúdo dela.
            """,
            assinatura="def resolver(nomes: list, precos: list) -> pd.DataFrame:",
            dicas=[
                "pd.DataFrame(...) aceita um dicionário de {nome_da_coluna: lista}.",
                "As chaves do dicionário são exatamente os nomes pedidos: \"nome\" e \"preco\".",
                'return pd.DataFrame({"nome": nomes, "preco": precos})',
            ],
            solucao='    return pd.DataFrame({"nome": nomes, "preco": precos})',
            nota_da_solucao="A ordem das chaves do dicionário vira a ordem das colunas.",
            testes="""
def teste_duas_linhas():
    esperado = pd.DataFrame({"nome": ["Fone", "Capa"], "preco": [49.9, 12.0]})
    verificar(ex.resolver(["Fone", "Capa"], [49.9, 12.0]), esperado)


def teste_uma_linha():
    esperado = pd.DataFrame({"nome": ["Livro"], "preco": [30.0]})
    verificar(ex.resolver(["Livro"], [30.0]), esperado)


def teste_listas_vazias():
    resultado = ex.resolver([], [])
    verificar(list(resultado.columns), ["nome", "preco"], nome="nome das colunas")
    verificar(len(resultado), 0, nome="número de linhas")
""",
        ),
        Ex(
            id="B01-002", titulo="Cartão de visita da tabela", nivel=2, tempo_min=7,
            tags=["shape", "columns", "inspecao"], linguagem="python",
            requer=["B01-001"],
            preambulo=IMPORTA_PANDAS, preambulo_do_teste=IMPORTA_PANDAS,
            enunciado="""
            A primeira coisa que se faz com uma tabela desconhecida é medi-la.

            Devolva a tupla `(número de linhas, número de colunas, lista com os
            nomes das colunas)`.

            Exemplo, para a tabela de produtos da Loja Aurora:

                resolver(produtos)
                ->  (400, 8, ['produto_id', 'nome', 'categoria', 'subcategoria',
                              'preco', 'custo', 'peso_kg', 'ativo'])

            `df.shape` já devolve `(linhas, colunas)` numa tupla. `df.columns`
            devolve os nomes — mas num objeto Index, que você precisa converter
            para lista.
            """,
            assinatura="def resolver(df: pd.DataFrame) -> tuple:",
            dicas=[
                "shape é um atributo, não um método: df.shape, sem parênteses.",
                "df.shape[0] são as linhas e df.shape[1] as colunas.",
                "list(df.columns) converte o Index para uma lista de verdade.",
            ],
            solucao="""
            linhas, colunas = df.shape
            return linhas, colunas, list(df.columns)
            """,
            nota_da_solucao="Desempacotar df.shape em duas variáveis deixa a intenção mais clara do que usar [0] e [1].",
            testes="""
def teste_tabela_pequena():
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4], "c": [5, 6]})
    verificar(ex.resolver(df), (2, 3, ["a", "b", "c"]))


def teste_tabela_real_de_produtos():
    produtos = t.tabela("produtos")
    verificar(
        ex.resolver(produtos),
        (400, 8, ["produto_id", "nome", "categoria", "subcategoria",
                  "preco", "custo", "peso_kg", "ativo"]),
    )


def teste_devolve_lista_e_nao_index():
    df = pd.DataFrame({"x": [1]})
    verificar(type(ex.resolver(df)[2]), list, nome="tipo do terceiro item",
              dica="df.columns é um Index; envolva em list(...).")
""",
        ),
    ],
)


# --------------------------------------------------------------------------- #
# B05 — Filtros
# --------------------------------------------------------------------------- #

B05 = Modulo(
    id="B05",
    titulo="Módulo B5 — Filtros",
    resumo="Selecionar linhas por condição: a operação mais frequente de todas.",
    teoria="""
## A máscara booleana

Uma comparação aplicada a uma coluna devolve uma Series de `True`/`False` —
a **máscara**. Usar a máscara dentro dos colchetes mantém só as linhas `True`.

```python
produtos["preco"] > 100          # Series de booleanos, uma por linha
produtos[produtos["preco"] > 100]  # as linhas em que isso é verdade
```

### Combinar condições: `&`, `|`, `~`

Aqui está a diferença que mais derruba quem vem do Python puro:

| Python puro | Pandas |
|---|---|
| `and` | `&` |
| `or` | `\\|` |
| `not` | `~` |

E **cada condição precisa de parênteses**, porque `&` tem precedência maior que
`>`:

```python
produtos[(produtos["preco"] > 100) & (produtos["ativo"])]     # certo
produtos[produtos["preco"] > 100 & produtos["ativo"]]         # erro
```

Se esquecer os parênteses, o Pandas levanta um erro difícil de ler. Se usar `and`
em vez de `&`, ele levanta o famoso *"The truth value of a Series is ambiguous"*.

### Ferramentas que evitam ors encadeados

```python
produtos[produtos["categoria"].isin(["Moda", "Casa"])]
produtos[produtos["preco"].between(50, 100)]
produtos[produtos["nome"].str.contains("Fone")]
produtos[~produtos["ativo"]]
```

### `query`: a mesma coisa, lendo melhor

```python
produtos.query("preco > 100 and ativo")
```

Dentro do `query` valem `and`/`or`/`not` normais e não são precisos colchetes.
Para filtros longos, costuma ser mais legível.
""",
    exercicios=[
        Ex(
            id="B05-001", titulo="Produtos ativos e caros", nivel=2, tempo_min=8,
            tags=["filtro", "mascara-booleana", "and"], linguagem="python",
            preambulo=IMPORTA_PANDAS, preambulo_do_teste=IMPORTA_PANDAS,
            enunciado="""
            Devolva apenas os produtos que estão **ativos** e cujo preço é
            **maior ou igual** ao mínimo informado.

            Mantenha todas as colunas e a ordem original das linhas.

            Exemplo:

                produtos = pd.DataFrame({
                    "nome":  ["Fone", "Capa", "Notebook"],
                    "preco": [200.0,  30.0,   3000.0],
                    "ativo": [True,   True,   False],
                })
                resolver(produtos, 100)

                ->        nome  preco  ativo
                    0     Fone  200.0   True

            O Notebook fica de fora por estar inativo; a Capa, por ser barata.

            Lembre: em Pandas o "e" é `&`, e cada condição vai entre parênteses.
            """,
            assinatura="def resolver(produtos: pd.DataFrame, preco_minimo: float) -> pd.DataFrame:",
            dicas=[
                "Cada condição vira uma máscara booleana separada.",
                "Combine as duas com & — e ponha parênteses em volta de cada uma.",
                'return produtos[(produtos["ativo"]) & (produtos["preco"] >= preco_minimo)]',
            ],
            solucao="""
            return produtos[(produtos["ativo"]) & (produtos["preco"] >= preco_minimo)]
            """,
            nota_da_solucao="A coluna ativo já é booleana: comparar com == True seria redundante.",
            testes="""
def _amostra():
    return pd.DataFrame({
        "nome": ["Fone", "Capa", "Notebook"],
        "preco": [200.0, 30.0, 3000.0],
        "ativo": [True, True, False],
    })


def teste_filtra_por_preco_e_por_ativo():
    esperado = _amostra().iloc[[0]]
    verificar(ex.resolver(_amostra(), 100), esperado)


def teste_limite_inclui_o_valor_exato():
    esperado = _amostra().iloc[[0]]
    verificar(ex.resolver(_amostra(), 200), esperado,
              dica="O enunciado diz MAIOR OU IGUAL: o preço exato entra.")


def teste_nenhum_produto_passa():
    verificar(len(ex.resolver(_amostra(), 99999)), 0, nome="número de linhas")


def teste_mantem_todas_as_colunas():
    verificar(list(ex.resolver(_amostra(), 0).columns), ["nome", "preco", "ativo"],
              nome="nome das colunas")


def teste_na_tabela_real():
    produtos = t.tabela("produtos")
    esperado = produtos.query("ativo and preco >= 1000")
    verificar(ex.resolver(produtos, 1000), esperado)
""",
        ),
    ],
)


# --------------------------------------------------------------------------- #
# C01 — SELECT
# --------------------------------------------------------------------------- #

C01 = Modulo(
    id="C01",
    titulo="Módulo C1 — SELECT",
    resumo="Escolher colunas, filtrar linhas, ordenar e limitar. O arroz com feijão.",
    teoria="""
## A consulta mínima

```sql
SELECT nome, uf
FROM clientes
WHERE uf = 'SP'
ORDER BY nome
LIMIT 10;
```

Você escreve nessa ordem, mas o banco **executa** em outra: primeiro `FROM`,
depois `WHERE`, depois `SELECT`, depois `ORDER BY` e por último `LIMIT`. Saber
disso explica por que um apelido criado no `SELECT` não pode ser usado no `WHERE`.

### Detalhes que economizam tempo

- Texto vai entre **aspas simples**: `'SP'`. Aspas duplas em SQL identificam
  colunas, não texto.
- `=` compara (em SQL não existe `==`).
- `SELECT *` traz todas as colunas. Serve para explorar; em consulta que vai
  para produção, liste o que você precisa.
- `DISTINCT` remove linhas repetidas do resultado: `SELECT DISTINCT uf FROM clientes`.
- `ORDER BY coluna DESC` inverte a ordem.
- Apelidos com `AS`: `SELECT preco AS preco_atual`.
- Todo comando termina com ponto e vírgula.

### O motor deste curso

Os exercícios rodam em **DuckDB**, que fala um SQL analítico praticamente igual
ao do PostgreSQL. Onde houver diferença relevante de dialeto, o enunciado avisa.

As tabelas disponíveis são `clientes`, `produtos`, `pedidos`, `itens_pedido`,
`pagamentos`, `eventos_web` e `estoque_diario` — as mesmas do Bloco B.
Para ver as colunas de qualquer uma: `DESCRIBE clientes;`
""",
    exercicios=[
        Ex(
            id="C01-001", titulo="Clientes de São Paulo", nivel=1, tempo_min=6,
            tags=["select", "where", "order-by", "limit"], linguagem="sql",
            esqueleto="-- Escreva sua consulta aqui, terminando com ponto e vírgula.",
            preambulo_do_teste=IMPORTA_PANDAS,
            enunciado="""
            Liste os clientes do estado de São Paulo.

            Devolva as colunas `cliente_id`, `nome` e `cidade`, apenas das linhas
            em que a `uf` é `SP`, ordenadas por `cliente_id` crescente, e traga
            só os **10 primeiros**.

            As colunas precisam sair nessa ordem e com esses nomes.
            """,
            dicas=[
                "São quatro cláusulas, nesta ordem: SELECT, FROM, WHERE, ORDER BY, LIMIT.",
                "Texto em SQL vai entre aspas simples: uf = 'SP'.",
                "SELECT cliente_id, nome, cidade FROM clientes WHERE ... ORDER BY ... LIMIT 10;",
            ],
            solucao="""
            SELECT cliente_id, nome, cidade
            FROM clientes
            WHERE uf = 'SP'
            ORDER BY cliente_id
            LIMIT 10;
            """,
            nota_da_solucao="O LIMIT age por último — depois do ORDER BY —, então são os 10 menores cliente_id.",
            testes="""
def teste_resultado_bate_com_a_tabela():
    clientes = t.tabela("clientes")
    esperado = (
        clientes[clientes["uf"] == "SP"]
        .sort_values("cliente_id")
        .head(10)[["cliente_id", "nome", "cidade"]]
        .reset_index(drop=True)
    )
    verificar(t.consultar(ex), esperado)


def teste_traz_exatamente_dez_linhas():
    verificar(len(t.consultar(ex)), 10, nome="número de linhas",
              dica="Faltou o LIMIT 10, ou ele veio antes do ORDER BY.")


def teste_apenas_colunas_pedidas():
    verificar(list(t.consultar(ex).columns), ["cliente_id", "nome", "cidade"],
              nome="nome das colunas",
              dica="SELECT * traria as 8 colunas — liste só as três pedidas.")
""",
        ),
        Ex(
            id="C01-002", titulo="Os cinco produtos mais caros", nivel=2, tempo_min=7,
            tags=["select", "alias", "order-by", "desc"], linguagem="sql",
            requer=["C01-001"],
            esqueleto="-- Escreva sua consulta aqui, terminando com ponto e vírgula.",
            preambulo_do_teste=IMPORTA_PANDAS,
            enunciado="""
            Monte a vitrine dos produtos mais caros que ainda estão à venda.

            Traga os **5 produtos ativos de maior preço**, com duas colunas:

                produto        o nome do produto
                preco_atual    o preço

            Ou seja: as colunas `nome` e `preco` precisam sair **renomeadas** com
            `AS`. Ordene do mais caro para o mais barato.

            A coluna `ativo` já é booleana — `WHERE ativo` basta, sem `= true`.
            """,
            dicas=[
                "AS dá um apelido à coluna: SELECT nome AS produto.",
                "Para ordenar do maior para o menor, use ORDER BY preco DESC.",
                "WHERE ativo filtra os ativos; LIMIT 5 corta no fim.",
            ],
            solucao="""
            SELECT nome AS produto, preco AS preco_atual
            FROM produtos
            WHERE ativo
            ORDER BY preco DESC
            LIMIT 5;
            """,
            nota_da_solucao="O ORDER BY pode usar a coluna original (preco) mesmo com o apelido no SELECT.",
            testes="""
def teste_resultado_bate_com_a_tabela():
    produtos = t.tabela("produtos")
    esperado = (
        produtos[produtos["ativo"]]
        .sort_values("preco", ascending=False)
        .head(5)[["nome", "preco"]]
        .rename(columns={"nome": "produto", "preco": "preco_atual"})
        .reset_index(drop=True)
    )
    verificar(t.consultar(ex), esperado)


def teste_colunas_renomeadas():
    verificar(list(t.consultar(ex).columns), ["produto", "preco_atual"],
              nome="nome das colunas",
              dica="Use AS para renomear: SELECT nome AS produto, preco AS preco_atual.")


def teste_ordem_decrescente():
    precos = t.consultar(ex)["preco_atual"].tolist()
    verificar(precos, sorted(precos, reverse=True), nome="ordem dos preços",
              dica="Faltou o DESC no ORDER BY.")
""",
        ),
    ],
)


# --------------------------------------------------------------------------- #
# C05 — Agregação
# --------------------------------------------------------------------------- #

C05 = Modulo(
    id="C05",
    titulo="Módulo C5 — Agregação",
    resumo="Espremer muitas linhas em um número só: contar, somar, tirar média.",
    teoria="""
## Funções de agregação

Elas recebem uma coluna inteira e devolvem **uma linha**:

```sql
SELECT
    COUNT(*)      AS quantas_linhas,
    SUM(preco)    AS soma,
    AVG(preco)    AS media,
    MIN(preco)    AS menor,
    MAX(preco)    AS maior
FROM produtos;
```

### `COUNT(*)` não é `COUNT(coluna)`

| forma | conta |
|---|---|
| `COUNT(*)` | todas as linhas |
| `COUNT(coluna)` | as linhas em que a coluna **não é NULL** |
| `COUNT(DISTINCT coluna)` | os valores diferentes, sem repetição |

A diferença entre as duas primeiras é uma das perguntas mais comuns em
entrevista — e uma das causas mais comuns de relatório errado.

### NULL some das contas

`AVG`, `SUM`, `MIN` e `MAX` **ignoram** NULL. Isso é bom quase sempre, mas
significa que a média de `[10, NULL, 20]` é 15, e não 10. Se você queria tratar
NULL como zero, precisa dizer isso: `AVG(COALESCE(valor, 0))`.

### Sem `GROUP BY`, o resultado tem uma linha só

A tabela inteira vira um resumo. Para ter um resumo **por categoria**, entra o
`GROUP BY` — que é o assunto do próximo módulo.
""",
    exercicios=[
        Ex(
            id="C05-001", titulo="Resumo do catálogo", nivel=2, tempo_min=8,
            tags=["agregacao", "count", "avg", "min-max"], linguagem="sql",
            esqueleto="-- Escreva sua consulta aqui, terminando com ponto e vírgula.",
            preambulo_do_teste=IMPORTA_PANDAS,
            enunciado="""
            Monte o resumo do catálogo inteiro, em **uma única linha**, com quatro
            colunas nesta ordem e com estes nomes:

                total_produtos    quantos produtos existem
                categorias        quantas categorias diferentes existem
                preco_medio       o preço médio (sem arredondar)
                preco_maximo      o preço mais alto

            Considere todos os produtos, ativos ou não.

            Duas coisas para prestar atenção: `categorias` pede valores **distintos**,
            e `preco_medio` não deve ser arredondado — arredondamento em SQL tem
            pegadinhas de dialeto que ficam para um módulo mais à frente.
            """,
            dicas=[
                "São quatro funções de agregação num SELECT só, separadas por vírgula.",
                "Contar valores diferentes é COUNT(DISTINCT coluna).",
                "SELECT COUNT(*) AS total_produtos, COUNT(DISTINCT categoria) AS categorias, ...",
            ],
            solucao="""
            SELECT
                COUNT(*)                    AS total_produtos,
                COUNT(DISTINCT categoria)   AS categorias,
                AVG(preco)                  AS preco_medio,
                MAX(preco)                  AS preco_maximo
            FROM produtos;
            """,
            nota_da_solucao="Sem GROUP BY, as agregações espremem a tabela inteira numa linha só.",
            testes="""
def teste_resumo_completo():
    produtos = t.tabela("produtos")
    esperado = pd.DataFrame({
        "total_produtos": [len(produtos)],
        "categorias": [produtos["categoria"].nunique()],
        "preco_medio": [produtos["preco"].mean()],
        "preco_maximo": [produtos["preco"].max()],
    })
    verificar(t.consultar(ex), esperado, tolerancia=1e-6)


def teste_uma_linha_so():
    verificar(len(t.consultar(ex)), 1, nome="número de linhas",
              dica="Agregação sem GROUP BY sempre devolve exatamente uma linha.")


def teste_categorias_sao_distintas():
    produtos = t.tabela("produtos")
    verificar(int(t.consultar(ex)["categorias"].iloc[0]),
              produtos["categoria"].nunique(), nome="total de categorias",
              dica="Sem o DISTINCT, você contaria 400 — uma por produto.")
""",
        ),
    ],
)

MODULOS = [B01, B05, C01, C05]
