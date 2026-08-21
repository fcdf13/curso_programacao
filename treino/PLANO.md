# JF Treino — plano de construção

App de acompanhamento entre o treinador **João Filho** e seus alunos: o aluno registra
como a semana foi (peso, sono, medidas, dieta), o João prescreve o treino, e os dois
veem a mesma evolução em gráfico. A calculadora estima o 1RM a partir das séries que o
aluno já fez e devolve a carga para a fase da periodização.

---

## 1. Contexto

Hoje o protocolo do João sai como PDF solto no WhatsApp (o `Protocolo Filipe` anexado é
o exemplo: refeições, listas de substituição de carboidrato e proteína, suplementos e um
déficit de 500 kcal/dia). O que se perde nesse formato:

- **não tem histórico** — ninguém consegue olhar 12 semanas atrás e dizer se funcionou;
- **não tem retorno do aluno** — peso, sono e aderência ficam no chat, sem série temporal;
- **a carga é escolhida no olho** — sem estimativa de 1RM, "aumenta um pouquinho" é o método;
- **não escala** — cada aluno é um PDF editado à mão.

O objetivo é uma plataforma onde o histórico fica salvo, os dois lados enxergam a mesma
evolução, e a prescrição de carga vira uma conta com base no que o aluno de fato levantou.

## 2. Decisões de stack

| Decisão | Escolha | Por quê |
|---|---|---|
| Cliente | **PWA** (React 18 + Vite + TS) | Instala na tela de início do iPhone/Android, sem App Store, sem os US$ 99/ano da Apple, atualização instantânea. É a stack que já existe em `app/`. |
| Servidor | **FastAPI** + SQLite (dev) / Postgres (prod) | Mesma convenção de `curso/api.py` e `curso/servidor.py`. Sem dependência de serviço externo. |
| Auth | Sessão em cookie `httpOnly` + CSRF, senha com Argon2 | Mesma origem que o SPA, então cookie é mais simples e mais seguro que guardar JWT em `localStorage`. |
| Gráficos | SVG escrito à mão | `app/src/componentes/graficos/` já faz assim, sem biblioteca de chart. Mantém o bundle pequeno e o controle do tema. |
| Idioma do código | Português | Convenção do repositório inteiro (`teste_*.py`, `Resolver.tsx`, `--fundo-painel`). |

## 3. Layout

Projeto Python próprio, para não acoplar o app ao curso (o `pyproject.toml` da raiz só
empacota `curso*`, `dados*`, `autoria*`):

```
treino/
  pyproject.toml            # projeto "jf-treino", independente da raiz
  jf/
    forca.py                # ← equação de 1RM e calculadora (núcleo puro, sem I/O)
    modelos.py              # SQLAlchemy
    banco.py                # sessão, migrações
    auth.py                 # senha, sessão, dependências de permissão
    api/                    # routers: alunos, checkins, treinos, dieta, painel
    servidor.py             # sobe a API e serve o SPA compilado
    dados/taco.csv          # tabela TACO (alimentos brasileiros), embarcada
  testes/
    teste_forca.py          # ← vetores do paper, testes de propriedade
    teste_permissoes.py     # aluno A não lê aluno B
  web/                      # React + Vite + TS (PWA)
    src/{api,rotas,componentes,estilo}/
```

`forca.py` fica **puro**: recebe números, devolve números, não conhece banco nem HTTP.
É o que permite testá-lo contra o paper.

## 4. Modelo de dados

**Pessoas** — `usuario` (nome, email, senha_hash, papel `treinador|aluno`),
`aluno` (perfil: nascimento, sexo, altura, treinador_id, objetivo).

**Semana do aluno** — `checkin_semanal` (semana, peso_kg, horas_de_sono_media,
qualidade_do_sono 1‑5, passos_media, fadiga, dor_muscular, estresse,
aderencia_dieta_pct, aderencia_treino_pct, observacoes) e `medida_corporal`
(cintura, quadril, braço, coxa, tórax, pescoço).

**Treino** — `exercicio` (catálogo com grupo muscular, equipamento e
`incremento_kg`), `periodizacao` (mesociclo: objetivo, início, fim, semanas),
`sessao_modelo` ("Treino A — segunda"), `prescricao` (séries, reps alvo min/max,
RIR alvo, carga alvo, descanso, técnica), `sessao_realizada`, `serie_realizada`
(carga_kg, reps, **rir**, falha).

O `rir` em `serie_realizada` não é enfeite: é o que decide se a série entra ou não no
cálculo de 1RM (ver §5).

**Dieta** — `protocolo_alimentar` (kcal alvo, macros, déficit),
`refeicao_do_protocolo`, `grupo_de_substituicao` + `item_de_substituicao`,
`suplemento`, `registro_alimentar` (diário), `alimento` (TACO + Open Food Facts).

O `grupo_de_substituicao` é a modelagem direta do PDF do João — "Arroz branco 200 g ≡
Mandioca 200 g ≡ Cuscuz 225 g ≡ Batata doce 225 g". Na tela a refeição mostra
`Carboidrato: [Arroz 200 g ▾]` e trocar o item mantém os macros. É a parte do protocolo
dele que o papel representa mal e o app representa bem.

## 5. A calculadora — o que o paper dá e o que ele não dá

Fonte: Marzagão, T. (2026), *A Weight-Dependent 1RM Prediction Equation Optimized on
303,494 Near-Failure Sets Across 388 Exercises*, arXiv:2603.17495v1.

### A equação (conferida no PDF, §"The complete formula")

```
k(w) = max(0.5, a + b × ln(w))          a = −2.55   b = 4.58
1RM  = w × (1 + (r − 1)^α / k(w))       α = 0.85
```

Pontos que mudam a implementação:

- **`w` está em quilos.** O paper fixa `w₀ = 1 kg` e diz que em libras o intercepto `a`
  deslocaria em `b × ln(2,205) ≈ 3,61`. Como o João treina em kg, usamos os coeficientes
  publicados direto — mas `forca.py` guarda a unidade explicitamente, porque essa é
  exatamente a troca silenciosa que produz números errados sem quebrar nada.
- **O guard `k(w) ≥ 0,5` é do paper**, não invenção nossa. Sem ele o denominador zera em
  `w ≈ 1,74 kg`. Ativa abaixo de 1,95 kg (0,06% da amostra do autor).
- **`r = 1` devolve `w`**, por construção.
- **Halteres contam por unidade** (o paper: "dois halteres de 25 kg registram '25 kg'") e
  **barra conta o peso total, com a barra**. A UI precisa impor isso, senão a estimativa
  vira lixo silenciosamente.

Vetores conferidos contra o texto do paper, que viram `testes/teste_forca.py`:

| Caso | Nossa conta | Paper |
|---|---|---|
| `k(12)` | 8,83 | "≈ 8,8" |
| Rosca 13 kg × 10 | 22,1 kg | "cerca de 22 kg" |
| Brzycki, mesmo caso | 17,3 kg | "cerca de 17 kg" |
| 12 kg × 15 | 24,8 kg | "roughly 25 kg" |
| Guard ativa abaixo de | 1,95 kg | "abaixo de 2 kg" |

### O que a calculadora faz

1. **e1RM por exercício ao longo do tempo.** De cada `sessao_realizada`, pega a melhor
   série *perto da falha* e estima o 1RM. Esse é o gráfico que importa: mostra ganho de
   força mesmo quando o esquema de séries muda, coisa que "carga máxima" não mostra.
2. **Carga sugerida.** Dado o e1RM e a faixa de reps da fase, devolve a carga. Como `k`
   depende de `w`, a equação é **implícita em `w`** — resolve por bisseção (monótona,
   converge em ~40 iterações). É o trabalho de engenharia de verdade dessa parte.
3. **Arredondamento para o que existe na academia.** `incremento_kg` por exercício
   (barra 2,5 kg; halteres 2 kg; máquina por pino).

### O achado que justifica a calculadora

A inversão mostra por que a tabela clássica de %1RM não serve para todo exercício:

| Exercício | 10 reps até quase a falha corresponde a |
|---|---|
| Rosca com halter, 13 kg | **59%** do 1RM |
| Supino, 86 kg | **73%** do 1RM |

Ou seja: "10 repetições = 70% do 1RM" está errado nos dois casos, e erra para lados
opostos. É precisamente isso que a equação com `k(w)` corrige, e é o argumento para
o João de por que a conta do app é melhor que a tabela impressa.

### O que o paper NÃO dá — e isso precisa estar claro

O paper prevê **1RM**. Ele **não prescreve séries, volume nem periodização** — a palavra
"sets" aparece lá como unidade de dado, não como recomendação. Então a camada de
"carga × reps × séries ótima" é:

```
paper  →  e1RM (conta, validada)
João   →  fase, faixa de reps, RIR alvo, séries por grupo muscular (parâmetro, editável)
app    →  carga = inverte a equação no e1RM e na faixa de reps da fase
```

Os padrões de fase entram como **valores editáveis pelo João**, não como constante no
código — acumulação 65‑75% / 8‑12 reps / RIR 2‑3, intensificação 80‑90% / 3‑6 / RIR 1‑2,
deload −50% de volume. Ele discorda de algum, ele muda. O app não finge que a ciência
decidiu o que a experiência dele decide.

Duas restrições de validade que viram regra no código:

- **Só série perto da falha entra no e1RM** (RIR ≤ 2). O paper calibrou em sets
  near-failure e avisa que série com reserva enviesa a estimativa para baixo.
- **Acima de ~10 reps a precisão cai** (achado consistente na literatura revisada).
  Séries longas entram no gráfico marcadas como estimativa fraca.

## 6. Gráficos

Seguindo `app/src/componentes/graficos/`: SVG à mão, cor por token, legível nos dois temas.

- **Peso × tempo** com média móvel de 7 dias — peso oscila com água e sal; a tendência é o dado, o ponto é ruído.
- **Sono** — barras semanais com linha de meta.
- **e1RM por exercício** — linha, o gráfico principal do treinador.
- **Volume semanal por grupo muscular** — barras empilhadas.
- **Medidas** — small multiples.
- **Aderência** — heatmap de calendário (o `CalendarioDePratica.tsx` já resolve esse formato).
- **Painel do João** — um cartão por aluno, ordenado por sinal de alerta: sem check-in há
  10 dias, sono < 6 h, peso subindo em fase de corte, e1RM caindo 2 semanas seguidas.

## 7. Dieta

- **Protocolo** — o PDF vira tela, com os grupos de substituição de §4.
- **Base de alimentos** — TACO (UNICAMP, alimentos brasileiros, domínio público)
  embarcada no repo; Open Food Facts por código de barras, com cache local. OFF é ODbL e
  **exige atribuição** na tela.
- **MyFitnessPal fica de fora.** Não existe API pública — o acesso é só para parceiros
  comerciais aprovados. O caminho honesto é importar o CSV que o MFP exporta, e isso fica
  para depois da v1.

## 8. Marca

Amostrada do logo em anexo:

```
--preto:      #101010        (texto e fundo do tema escuro)
--vermelho:   #AD0101        (acento; gradiente até #7A0C10)
--osso:       #F5F3F4        (fundo do tema claro)
```

Tema **escuro por padrão** — o app é usado na academia, à noite. Títulos em sans
condensada pesada em itálico (o estilo esportivo do logo), corpo em sans normal. Ícone do
PWA e splash saem do monograma JF. Os tokens ficam em `web/src/estilo/tokens.css` no
mesmo formato de `app/src/estilo/tokens.css` — claro como base, escuro só redefinindo.

## 9. Segurança e LGPD

- Peso, sono, medidas e dieta são **dado pessoal sensível de saúde** (LGPD art. 5º, II).
  Consentimento no cadastro, exportar e apagar os próprios dados, sem foto sem consentimento explícito.
- **Toda** consulta filtrada por dono, numa dependência única (`aluno_permitido()`).
  O risco real aqui é IDOR — `/api/alunos/7/checkins` responder para quem não é o 7 nem o
  treinador do 7. Por isso `teste_permissoes.py` é obrigatório, não opcional.
- Backup diário. É o histórico de treino de um atleta; perder é inaceitável.

## 10. Fases

| Fase | Entrega | Fecha quando |
|---|---|---|
| 0 ✅ | Estrutura, banco, auth, papéis, catálogo de exercícios, tokens da marca, casca do PWA | ~~João entra, cria um aluno, aluno faz login~~ — feito; ver [`README.md`](README.md) |
| 1 | Check-in semanal + medidas + gráficos | Aluno registra a semana, os dois veem o gráfico |
| 2 ◐ | ~~Periodização, prescrição~~ (feito), **modo academia**, registro de séries | Aluno treina lendo do celular e registra carga/reps/RIR |
| 3 ◐ | ~~`forca.py`, carga sugerida, arredondamento~~ (feito), gráfico de e1RM | Testes do paper passam; João aceita a carga sugerida |
| 4 | Protocolo alimentar, substituições, TACO/OFF, diário | O PDF do Filipe existe inteiro dentro do app |
| 5 | Painel com alertas, sincronização offline, export LGPD, deploy | Rodando no domínio dele, com backup |

**Modo academia** (fase 2) merece atenção: tela grande, botão grande, cronômetro de
descanso, carga em destaque — e fila de sincronização em IndexedDB, porque subsolo de
academia não tem sinal e perder a série registrada mata a confiança no app.

## 11. Verificação

```bash
cd treino && pytest                    # forca.py contra os vetores do paper + permissões
cd treino/web && npm run verificar     # tsc
cd treino/web && npm run e2e           # Playwright: check-in e modo academia
```

- `teste_forca.py`: os cinco vetores da tabela em §5, mais propriedades — `1RM(w,1) == w`,
  monotonicidade em `r` e em `w`, `inverter(1RM(w,r), r) ≈ w` para uma grade de `(w, r)`,
  guard ativando abaixo de 1,95 kg.
- `teste_permissoes.py`: com `TestClient`, aluno A recebe 403/404 em todo endpoint do aluno B.
- E2E: João cria periodização → aluno registra sessão → e1RM aparece no gráfico dos dois.

## 12. Em aberto

1. **Onde hospedar.** Fly.io e Render têm tier barato que serve. Decidir na fase 5, junto com o domínio.
2. **Repositório.** Isto aqui é um curso de Python; o app convive, mas separar em repo
   próprio fica mais limpo quando for para produção.
3. **Quantos alunos.** Muda pouco até ~200; acima disso o painel do treinador precisa de paginação e índice.
4. **Foto de progresso.** Alto valor para fisiculturismo, mas é o dado mais sensível do app.
   Fora da v1 de propósito — entra com consentimento próprio e storage separado.
