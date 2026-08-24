# Plano do curso — o que existe e o que falta

Este arquivo é o mapa completo do currículo. O que está marcado ✅ já está no repositório,
com enunciado, testes, três dicas e gabarito. O resto é o roteiro para as próximas sessões
de produção — a ideia é que ninguém precise re-decidir escopo, ordem ou nomenclatura.

**Estado atual: 115 exercícios prontos** (109 do Bloco A + 6 vitrines), de ~560 planejados.

---

## Convenções de produção

**Identificador.** `BLOCO + MÓDULO - NÚMERO`, por exemplo `B11-007`. Blocos: `A` Python,
`B` Pandas, `C` SQL, `D` Ponte. A ordem lexicográfica dos ids **é** a ordem didática.

**Nível.** 1 a 5. Um módulo típico abre com 3-5 exercícios de nível 1-2 (aquecimento,
quase guiados), sustenta 8-14 de nível 2-3 (prática) e fecha com 2-3 de nível 3-4
(desafio, combinando ferramentas do módulo).

**Uma ideia nova por exercício.** Se o enunciado precisa ensinar duas coisas, são dois
exercícios. Combinações vêm nos módulos de revisão.

**Dicas.** Sempre três, escalando: (1) empurrão conceitual sem nomear a ferramenta,
(2) nomeia a ferramenta, (3) quase a resposta.

**Casos de borda são obrigatórios nos testes.** Lista vazia, texto vazio, item único,
valor exatamente no limite, todos nulos, chave duplicada. É o que separa um exercício
que ensina de um que só confere.

**Onde o teste tira o resultado esperado.** Em ordem de preferência:
1. valor explícito no teste (ideal para tabelas pequenas — o aluno confere a olho);
2. cálculo por um caminho **diferente** do da solução (ex.: gabarito com máscara booleana,
   teste com `.query()`);
3. propriedades invariantes (contagem, ordenação, ausência de nulos) quando o resultado
   é grande demais para escrever.

Nunca copie a solução para dentro do teste.

**Rounding.** Evite `ROUND` em SQL nos exercícios iniciais: DuckDB e Postgres divergem no
arredondamento do meio. Compare com tolerância no teste, ou peça o valor sem arredondar.

**Notas de dialeto.** Onde o DuckDB difere de Postgres/BigQuery, o enunciado avisa em uma
linha. O objetivo é que o conhecimento transfira para o mercado.

---

## Bloco A — Python, do zero ✅ 86 exercícios

| módulo | exercícios | conteúdo |
|---|---|---|
| A01 Primeiros passos | 12 ✅ | print × return, variáveis, tipos, conversão, f-string |
| A02 Números e operadores | 10 ✅ | `//` `%` `**`, precedência, `round`, `divmod`, `min`/`max` |
| A03 Strings | 14 ✅ | índice, fatiamento, `strip`/`replace`/`split`/`join`, formatação |
| A04 Condicionais | 12 ✅ | `if`/`elif`/`else`, `and`/`or`/`not`, `in`, comparação encadeada |
| A05 Listas | 14 ✅ | acesso, mutação, `sort` × `sorted`, `sum`/`min`/`max`, `index` |
| A06 Laços | 16 ✅ | `for`, `range`, acumulador, `while`, `break`/`continue`, `enumerate`, `zip` |
| A07 Revisão do bloco | 8 ✅ | oito problemas que combinam A1–A6 |
| A08 Dicionários e conjuntos | 14 ✅ | acesso, `get`, `items`, contagem, merge, inversão, operações de conjunto |
| A09 Complexidade e Big-O | 9 ✅ | reconhecer O(1)/O(n)/O(n²), lista × set, dict de última posição, prefix sum, `deque`, e 4 exercícios com teste **cronometrado** |

### Bloco A — o que ainda falta (~65 exercícios)

Estes módulos completam o Bloco A antes de o Bloco B fazer pleno sentido:

| módulo | exercícios | conteúdo |
|---|---|---|
| A10 Tuplas e desempacotamento | 8 | imutabilidade, `a, b = b, a`, retorno múltiplo, `*resto` |
| A11 Funções | 16 | parâmetros padrão, `*args`/`**kwargs`, escopo, funções como valor |
| A12 Compreensões | 12 | list/dict/set comp, filtro, aninhada, quando **não** usar |
| A13 Erros e exceções | 10 | `try`/`except`/`else`/`finally`, `raise`, exceções comuns, EAFP × LBYL |
| A14 Arquivos e formatos | 10 | `with open`, `csv`, `json`, `pathlib` |
| A15 Biblioteca padrão | 14 | `datetime`, `Counter`, `defaultdict`, `itertools`, `re`, `random` |
| A16 Organização de código | 8 | módulos, imports, type hints, docstrings, primeiro `pytest` |
| A17 Revisão final do bloco | 10 | combina A8–A16 |

**Nota sobre A09 (Complexidade e Big-O):** é o único módulo do curso com testes
que **cronometram** a solução, não só conferem o resultado (ferramenta
`curso.teste.cronometrar`/`verificar_tempo`). Os limites de tempo foram
calibrados rodando os dois lados (ingênuo e eficiente) neste repositório antes
de fixar o número — a diferença real passa de 500x na maioria dos casos, então
o limite escolhido fica bem no meio, com folga generosa para máquinas mais
lentas. Ao criar um novo exercício cronometrado, meça os dois lados de verdade
(um script solto, não o suite) antes de escolher `limite=`; nunca chute.

---

## Bloco B — Pandas (~170 exercícios)

| módulo | exercícios | conteúdo |
|---|---|---|
| B01 Series e DataFrame | 2 ✅ / 10 | criação, índice, `shape`, `dtypes`, vetorização |
| B02 Entrada e saída | 10 | `read_csv` (`sep`, `dtype`, `parse_dates`, `na_values`), `to_csv`, parquet |
| B03 Inspeção e diagnóstico | 10 | `head`, `info`, `describe`, `value_counts`, `nunique`, `memory_usage` |
| B04 Seleção | 12 | colchetes, `loc` × `iloc`, fatias, seleção por lista |
| B05 Filtros | 1 ✅ / 14 | máscaras, `&` `\|` `~`, `isin`, `between`, `query`, `str.contains` |
| B06 Colunas derivadas | 12 | `assign`, `np.where`, `np.select`, `map`, vetorizar × `apply`, `rename`, `drop` |
| B07 Dados faltantes | 10 | `isna`, `fillna`, `dropna`, `ffill`, `interpolate`, NaN × None × NaT |
| B08 Tipos e conversões | 10 | `astype`, `to_numeric(errors=)`, `to_datetime`, `category`, dtypes nulláveis |
| B09 Texto | 10 | acessor `.str`, `strip`, `replace`, `split`, `extract`, regex |
| B10 Ordenação e duplicatas | 10 | `sort_values`, `nlargest`, `rank`, `duplicated`, `drop_duplicates` |
| B11 groupby I | 14 | `agg` simples e múltiplo, named agg, múltiplas chaves, `reset_index` |
| B12 groupby II | 12 | `transform`, `filter`, `apply`, % do grupo, ranking dentro do grupo |
| B13 Reshape | 12 | `pivot`, `pivot_table`, `melt`, `stack`/`unstack`, `crosstab`, `explode` |
| B14 Combinar tabelas | 14 | `concat`, `merge` (todos os `how`), `validate`, `indicator`, **fan-out** |
| B15 Datas e séries temporais | 14 | `DatetimeIndex`, `resample`, `rolling`, `shift`, `diff`, `pct_change`, offsets |
| B16 Performance e armadilhas | 10 | vetorização, `chunksize`, `category`, cópia × view, `pipe`, encadeamento |
| B17 Visualização rápida | 6 | `.plot`, matplotlib básico |
| B18 Revisão do bloco | 8 | combina B1–B17 |

**Nota para quem produzir:** o repositório está fixado em **pandas 3.0**, onde
copy-on-write é o padrão e o `SettingWithCopyWarning` não existe mais. O módulo B16
precisa ensinar o modelo atual (atribuição encadeada simplesmente não propaga), e não o
folclore das versões 1.x. Também não use `.applymap` (virou `.map`) nem assuma dtype
`object` para texto (o padrão agora é `str`).

---

## Bloco C — SQL em DuckDB (~170 exercícios)

| módulo | exercícios | conteúdo |
|---|---|---|
| C01 SELECT | 2 ✅ / 12 | colunas, `AS`, `DISTINCT`, `ORDER BY`, `LIMIT` |
| C02 WHERE | 14 | comparadores, `AND`/`OR`/`NOT`, `IN`, `BETWEEN`, `LIKE`/`ILIKE`, `IS NULL` |
| C03 Expressões | 12 | aritmética, `CASE WHEN`, `COALESCE`, `NULLIF`, `CAST` |
| C04 Funções | 14 | texto, numéricas, data (`date_trunc`, `extract`, intervalos) |
| C05 Agregação | 1 ✅ / 10 | `COUNT(*)` × `COUNT(col)` × `COUNT(DISTINCT)`, `SUM`, `AVG`, NULL |
| C06 GROUP BY e HAVING | 14 | múltiplas chaves, filtrar antes × depois, `GROUPING SETS`, `ROLLUP` |
| C07 JOINs I | 14 | `INNER`, `LEFT`, chave composta, três ou mais tabelas |
| C08 JOINs II | 12 | `RIGHT`/`FULL`, self-join, `CROSS`, anti-join, semi-join, **fan-out** |
| C09 Subqueries | 12 | escalar, `IN`, `EXISTS`, correlacionada, subquery no `FROM` |
| C10 CTEs | 12 | `WITH`, encadeadas, legibilidade, recursiva (hierarquia, calendário) |
| C11 Window functions | 18 | `ROW_NUMBER`/`RANK`/`DENSE_RANK`, `PARTITION BY`, `LAG`/`LEAD`, frames, `QUALIFY` |
| C12 Operações de conjunto | 8 | `UNION` × `UNION ALL`, `INTERSECT`, `EXCEPT` |
| C13 DDL e escrita | 12 | `CREATE TABLE`, tipos, PK/FK, `INSERT`/`UPDATE`/`DELETE`, upsert, transações |
| C14 Padrões do dia a dia | 16 | top-N por grupo, dedup, running total, coorte, retenção, funil, sessionização, *gaps and islands*, pivot em SQL |
| C15 Desempenho | 8 | `EXPLAIN`, índices, sargabilidade, evitar `SELECT *` |
| C16 Revisão do bloco | 8 | combina C1–C15 |

**Nota para quem produzir:** os exercícios de C13 (escrita e transações) precisam de uma
conexão gravável. O banco é aberto em modo somente-leitura por `curso.teste.banco()` — para
esse módulo, criar um helper que copie `loja.duckdb` para um arquivo temporário por teste.

---

## Bloco D — Ponte Pandas ↔ SQL (~40 exercícios)

| módulo | exercícios | conteúdo |
|---|---|---|
| D01 Mapa de tradução | 32 | a mesma pergunta nas duas linguagens: `WHERE` ↔ máscara, `GROUP BY` ↔ `groupby`, `JOIN` ↔ `merge`, window ↔ `transform`/`rank`, `CASE` ↔ `np.select` |
| D02 Mini-projetos | 8 | relatório de vendas, coorte de retenção, RFM, funil, análise de ruptura de estoque |

O teste de um exercício da ponte exige as **duas** respostas e verifica que produzem o
mesmo resultado. Isso precisa de um pequeno acréscimo ao motor: um exercício com dois
arquivos (`ex_NNN_slug.py` e `ex_NNN_slug.sql`). Hoje `curso.teste._arquivo_do_exercicio`
resolve um arquivo só por slug — o ponto exato a estender.

---

## Ordem sugerida de produção

1. **A10–A17** (~65 ex.) — fecha o Bloco A; é o pré-requisito honesto para o Pandas.
2. **B02–B10** (~90 ex.) — o Pandas do dia a dia.
3. **C02–C09** (~100 ex.) — o SQL até subqueries; a partir daqui já dá para trabalhar.
4. **B11–B15** e **C10–C12** — groupby, reshape, merge, CTEs e window functions,
   que é onde mora a diferença entre saber e usar.
5. **B16–B18**, **C13–C16** — performance, DDL e revisões.
6. **Bloco D** — por último, porque depende dos dois anteriores.

Um bloco de ~90 exercícios cabe confortavelmente em uma sessão de produção.
