# Curso Loja Aurora — Python, Pandas e SQL

Um curso local, offline e autocorrigível para aprender **Python → Pandas → SQL** do zero,
em ordem crescente de dificuldade, com **revisão espaçada** embutida: exercícios que você já
resolveu voltam a aparecer pouco antes de você esquecê-los.

Não existe servidor, conta ou mensalidade. É este repositório, o seu editor e o terminal.

```
curso hoje        →  o plano do dia
curso proximo     →  abre o próximo exercício
curso check       →  corrige em segundos, com o erro explicado
```

---

## Começar

```bash
pip install -e .     # instala o comando `curso` e as dependências
curso setup          # gera o dataset da Loja Aurora (~15s, roda uma vez só)
curso hoje           # o que fazer hoje
```

O `curso setup` cria os CSVs e o banco DuckDB a partir de `dados/gerar.py`, sempre com a
mesma semente — o dataset é idêntico em qualquer máquina, o que permite os testes
compararem resultados exatos.

Requisitos: Python 3.11+. Testado com pandas 3.0 e DuckDB 1.5.

## O ciclo

```bash
curso proximo             # mostra o enunciado e cria o arquivo para você editar
                          # → você escreve a resposta em respostas/...
curso check               # corrige
curso dica                # travou? três dicas, da mais vaga à quase-resposta
curso solucao             # desistiu? o gabarito comentado (e o exercício volta amanhã)
curso revisar             # o que venceu hoje, para resolver de novo do zero
curso progresso           # o painel
curso buscar window       # procura exercícios por tema, tag ou id
curso listar -b C         # o índice de um bloco
```

Nenhum comando é obrigatório. Se você preferir, dá para abrir `exercicios/` no editor e
usar `pytest` direto — o CLI é conveniência, não amarra.

## Como o repositório é organizado

Três árvores paralelas guardam o mesmo exercício em papéis diferentes:

| pasta | o que é | você edita? |
|---|---|---|
| `exercicios/` | enunciado + esqueleto da função + testes | não |
| `respostas/` | a sua resolução | **sim, é aqui** |
| `solucoes/` | o gabarito comentado | não |

Mais:

```
curso/        o motor: CLI, correção, progresso, revisão espaçada
dados/        o gerador do dataset (determinístico) e os arquivos gerados
autoria/      a fonte de autoria dos exercícios (veja abaixo)
testes_do_motor/  testes do próprio motor
.curso/       o seu progresso e o histórico das suas respostas (local, não versionado)
```

## Revisão espaçada

Aprender e revisar acontecem ao mesmo tempo. Toda vez que você acerta, o exercício é
reagendado por uma variação do SM-2 (o algoritmo do Anki), com a "nota" vindo de quantas
tentativas você levou:

| desempenho | próximo intervalo |
|---|---|
| acertou de primeira | cresce forte: 1 → 3 → 8 → 20 → 50 dias |
| levou 2 ou 3 tentativas | cresce devagar |
| errou, ou olhou a solução | volta para amanhã |

`curso hoje` mistura material novo com o que venceu. E `curso revisar` **arquiva a sua
resposta anterior** (em `.curso/historico/`) e devolve o esqueleto em branco: revisar aqui
é resolver de novo, não reler o que você escreveu.

## O dataset: Loja Aurora

Um e-commerce fictício, gerado com semente fixa. As mesmas tabelas estão em CSV (para o
Pandas) e em DuckDB (para o SQL) — é isso que torna possível a trilha-ponte, onde a mesma
pergunta é respondida nas duas linguagens.

| tabela | linhas | serve para |
|---|---|---|
| `clientes` | 5.000 | filtros, joins, coortes |
| `produtos` | 400 | categorias, agregação |
| `pedidos` | 50.000 | séries temporais, sazonalidade, RFM |
| `itens_pedido` | 135.413 | fan-out de join, receita |
| `pagamentos` | 50.000 | métodos, aprovação, parcelas |
| `eventos_web` | 193.941 | funil, sessionização, janelas |
| `estoque_diario` | 72.000 | rupturas, *gaps and islands* |
| `clientes_bruto` | 3.200 | **suja de propósito** |
| `avaliacoes_bruto` | 12.000 | **suja de propósito** |

As duas últimas trazem nulos, e-mails inválidos, datas em três formatos, duplicatas,
números como texto e espaços sobrando. São a matéria-prima dos módulos de limpeza —
porque limpar dados sujos não se aprende em dados limpos.

Os dados têm estrutura de verdade, não ruído aleatório: crescimento ano a ano, pico de
Black Friday, curva de popularidade concentrada em poucos produtos, coortes de aquisição
e um funil web com queda realista entre etapas.

Uma ressalva honesta: `eventos_web` é uma camada comportamental independente e **não
reconcilia** com `pedidos` — como acontece de verdade entre uma ferramenta de analytics e
o banco transacional.

## Currículo

| bloco | módulos | exercícios |
|---|---|---|
| **A — Python** | 7 de 16 | 86 ✅ |
| **B — Pandas** | 17 | 3 de ~170 |
| **C — SQL (DuckDB)** | 15 | 3 de ~170 |
| **D — Ponte Pandas ↔ SQL** | 2 | ~40 |

Os módulos A1–A7 estão completos — dá para estudar semanas com o que já está aqui.
Os blocos B, C e D têm exercícios-vitrine para você conferir o formato; o índice completo do que falta produzir está em [`PLANO_DO_CURSO.md`](PLANO_DO_CURSO.md).

Cada módulo segue a mesma curva: **aquecimento** (quase guiados) → **prática** →
**desafio** → e um módulo de **revisão** que só sai combinando o que veio antes.

## Contribuir com exercícios

Os arquivos em `exercicios/` e `solucoes/` são **gerados**. A fonte da verdade é `autoria/`,
onde cada exercício é declarado uma vez — enunciado, dicas, gabarito e testes juntos:

```python
Ex(
    id="A02-002", titulo="Par ou ímpar", nivel=2,
    tags=["resto", "booleano"],
    enunciado="...",
    dicas=["...", "...", "..."],
    solucao="    return numero % 2 == 0",
    testes="def teste_par():\n    verificar(ex.resolver(4), True)",
)
```

```bash
python -m autoria.construir --limpar    # regenera as três árvores
```

Escrever assim é o que mantém 500 exercícios consistentes: todos com três dicas, todos com
gabarito, todos com o mesmo estilo de teste.

## Qualidade

```bash
pytest --solucoes      # todo exercício passa no próprio teste com o gabarito oficial
pytest testes_do_motor # o motor: SRS, catálogo, comparação, correção
pytest                 # tudo (os exercícios reprovam até você resolvê-los — é o esperado)
```

O `pytest --solucoes` é o portão que impede um enunciado impossível ou ambíguo de entrar no
repositório. Nenhum exercício é adicionado sem esse verde.

O verso disso também é verificado: com os esqueletos em branco, **os 92 exercícios reprovam**.
Um teste que passa sem código escrito não testa nada.
