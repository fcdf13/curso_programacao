# A estrutura do case

O que avaliam, segundo o guia e o relato do blog:

- **estrutura vale mais que complexidade do modelo**;
- ligar os dados ao valor de negócio;
- pensar como consultor, não só como engenheiro de algoritmo;
- entender de verdade o modelo que você propõe: por que ele, o que ele assume, como avaliá-lo.

Você não precisa "resolver" o case. Precisa mostrar um caminho lógico, com escolhas justificadas
e alternativas descartadas **em voz alta**.

---

## Os 8 passos

Esta é a espinha do blog (a "estrutura de nota alta"). Acrescentei o passo 0, que o guia oficial
cobra: esclarecer antes de começar.

| # | passo | tempo em 45 min | pergunta que você responde |
|---|---|---|---|
| 0 | Escutar e esclarecer | 3–4 min | O que exatamente me pediram? |
| 1 | Enquadrar o problema | 5 min | Qual decisão isso destrava, e como mediremos sucesso? |
| 2 | Dados: o que existe e os problemas | 5 min | Com o que eu conto, e onde isso pode me enganar? |
| 3 | Abordagem de EDA | 4 min | O que quero ver antes de modelar? |
| 4 | Feature engineering | 5 min | Que sinais explicam o alvo, a partir das hipóteses? |
| 5 | Escolha do modelo | 6 min | Baseline → modelo, e por quê |
| 6 | Métrica de avaliação | 5 min | Como sei que funciona, offline e no mundo real? |
| 7 | Implantação e monitoramento | 4 min | Como vira decisão no dia a dia do cliente? |
| 8 | Riscos e alinhamento com stakeholders | 3 min | O que pode dar errado, e quem precisa concordar? |
| — | Síntese e recomendação | 2 min | Resumo em 30 segundos e próximos passos |

Não recite os passos como uma lista decorada. Anuncie a estrutura **uma vez**, no começo, e
depois conduza a conversa por ela. O entrevistador vai puxar você para um ponto específico:
responda, e depois **volte ao mapa** ("isso fecha a parte de métrica; o próximo ponto é como
isso entra em produção").

---

### 0. Escutar e esclarecer (não pule!)

Repita o problema com as suas palavras e faça **2 a 4 perguntas que mudam a solução**. Diga
**por que** você está perguntando: o guia pede isso explicitamente.

Boas perguntas de esclarecimento:
- **Decisão e usuário:** quem vai usar o resultado e o que vai fazer com ele? ("Um gerente
  vai priorizar uma lista? Um sistema vai precificar automaticamente?")
- **Escopo:** quais produtos, regiões ou segmentos? Qual horizonte de tempo?
- **Restrições:** orçamento de ação (quantas pessoas dá para contatar ou inspecionar), prazo,
  regulação, necessidade de explicar a decisão.
- **Estado atual:** como decidem hoje? Esse é o baseline de negócio que você precisa superar.

> *"Before I structure this, let me make sure I understand the objective. I'd like to ask a
> couple of questions because the answers change the approach: …"*

Depois das respostas, **peça 30–60 segundos para organizar as ideias**. É esperado e bem visto.

### 1. Enquadrar o problema

Traduza **negócio → decisão → problema analítico → métrica de negócio**.

- **Objetivo de negócio:** aumentar receita, reduzir custo, reduzir risco, melhorar experiência.
- **Alavanca:** o que o cliente pode de fato mudar (preço, estoque, contato, inspeção)?
- **Tipo de problema:** classificação, regressão, previsão de série, ranking/recomendação,
  otimização, inferência causal ou, às vezes, **nenhum modelo** (uma análise descritiva ou
  uma regra resolve).
- **Alvo, definido com precisão:** "churn = não renovar em até 60 dias após o vencimento do
  contrato", "demanda = unidades vendidas por SKU × loja × semana".
- **KPI de sucesso:** o número de negócio que vai mudar (R$ retido, ruptura de estoque, perdas
  com fraude), não o AUC.

> **O teste de ouro:** o problema é **prever** ("quem vai sair?") ou **intervir** ("em quem a
> ação muda o resultado?")? Se for intervir, diga isso cedo. Leva a uplift modeling ou a
> experimento, e é o tipo de sacada que diferencia o candidato.

### 2. Dados: o que existe e os problemas

Liste as fontes pelas **hipóteses**, não aleatoriamente. Monte uma mini árvore de fatores:
"o alvo depende de A (comportamento), B (produto/preço), C (contexto externo)" e, para cada
ramo, diga que dado o testaria.

Problemas que você deve **nomear proativamente**:
- **Vazamento de informação (leakage):** variáveis que só existem depois do evento
  (ex.: "ligou para cancelar" prevendo churn).
- **Granularidade e junção:** tabelas em níveis diferentes (cliente × transação × dia) e o risco
  de duplicar linhas ao juntar.
- **Qualidade:** nulos, duplicatas, mudanças de definição ao longo do tempo, sistemas legados.
- **Viés de seleção:** só temos rótulo para quem foi inspecionado, aprovado ou contatado.
- **Volume de histórico e sazonalidade:** há ciclos completos suficientes?
- **Acesso e privacidade:** LGPD/GDPR, dados sensíveis, consentimento.

### 3. Abordagem de EDA

Diga **o que** você quer descobrir, não "vou fazer uns gráficos":
- taxa-base do alvo e desbalanceamento;
- distribuição no tempo (tendência, sazonalidade, quebras);
- cortes por segmento (onde o problema se concentra, o bom e velho Pareto 80/20);
- qualidade (nulos, outliers, valores impossíveis);
- relação univariada entre os principais fatores e o alvo, para validar as hipóteses do passo 2.

### 4. Feature engineering

Organize por família de hipótese. Assim fica estruturado e fácil de acompanhar:
- **Recência, frequência e valor (RFM)**, tendências (últimos 30 dias contra os 90 anteriores),
  variação e volatilidade;
- **atributos da entidade** (perfil do cliente, características do ativo ou do produto);
- **contexto** (sazonalidade, feriados, preço de concorrentes, clima, macroeconomia);
- **interações e agregações de grupo** (desvio em relação à média do segmento).

Sempre cite a **janela de observação** e o **corte temporal**: as features são calculadas só
com dados anteriores à data de previsão.

### 5. Escolha do modelo

A sequência que sempre cai bem:
1. **Baseline de negócio:** a regra atual ou uma heurística. É o que você precisa superar.
2. **Modelo simples e interpretável:** regressão logística ou linear com regularização.
   Rápido, explicável e ótimo para calibrar a expectativa.
3. **Modelo mais forte:** gradient boosting (XGBoost/LightGBM) para dados tabulares; é o
   padrão de mercado.
4. **Só se o problema pedir:** modelos específicos de série temporal, sobrevivência,
   deep learning (imagem, texto, sensores de alta frequência), otimização em cima da previsão.

Justifique pelo **trade-off**: desempenho × interpretabilidade × volume de dados × latência ×
manutenção pelo time do cliente. E diga o que descartou: *"I'd avoid a deep learning model
here: tabular data, ~50k rows, and the client needs to explain decisions to regulators."*

### 6. Métrica de avaliação

Separe três níveis e mencione os três:
1. **Métrica do modelo (offline):**
   - classificação: AUC-PR se for desbalanceado, precision@k se houver orçamento de ação,
     recall se o custo do erro for alto;
   - regressão ou previsão: MAE/MAPE/WAPE, com viés sob controle.
2. **Métrica de decisão:** converta a matriz de confusão em dinheiro. Custo de um falso positivo
   × custo de um falso negativo leva ao **limiar ótimo**.
3. **Métrica de negócio (online):** o KPI do passo 1, medido num **piloto com grupo de controle**
   (teste A/B).

Validação: **divisão temporal** (treinar no passado, testar no futuro), nunca aleatória
quando há tempo. Validação cruzada por janelas. Checar a **calibração** se as probabilidades
forem usadas para decidir.

### 7. Implantação e monitoramento

- **Como o resultado é consumido:** lista em lote semanal no CRM, API em tempo real,
  painel para o gerente. A resposta depende do passo 0.
- **Monitoramento:** drift dos dados de entrada, drift de desempenho (quando o rótulo chegar),
  métricas de negócio.
- **Retreino:** periodicidade ou gatilho por drift; versionamento do modelo.
- **Adoção:** o modelo que ninguém usa tem valor zero. Treinar os usuários, explicar
  as previsões (SHAP), feedback loop.
- **MLOps em uma frase:** pipeline reprodutível, testes de dados, CI/CD. A QuantumBlack tem
  a própria ferramenta para isso (o **Kedro**); citar pode ajudar, mas não é obrigatório.

### 8. Riscos e alinhamento com stakeholders

- **Riscos técnicos:** dados insuficientes, drift, loops de feedback (o modelo altera os
  dados futuros).
- **Riscos de negócio:** adoção, mudança de processo, efeitos colaterais (desconto
  canibalizando margem).
- **Ética e regulação:** viés contra grupos, explicabilidade, privacidade.
- **Stakeholders:** quem é o dono do KPI, quem opera, quem fornece dados (TI), jurídico.
  Proponha checkpoints: validar a definição do alvo com o negócio **antes** de modelar.

### Síntese (feche sempre assim)

> *"To summarise: the objective is X, measured by Y. I'd start with a baseline of Z, build
> a [model] on [key data], evaluate with [metric] and validate in a pilot against a control
> group. Main risks are A and B. As next steps, I'd first confirm [critical assumption] with
> the client."*

---

## Contas no meio do case

O guia pede: **explique a montagem da conta antes de calcular** e depois faça no papel.
Não pode usar calculadora.

Estrutura típica do dimensionamento de impacto:
```
valor = população afetada × taxa do evento × fração que o modelo captura
        × fração que a ação converte × valor por evento − custo da ação
```
Exemplo (churn): 1M de clientes × 2%/mês de churn = 20k saídas por mês. Contatamos os 5%
de maior risco (50k), com precision de 20%: 10k são churners reais. A ação retém 25% deles
(2,5k) × R$1.200 de valor anual = R$3M/ano por mês de campanha. O custo é de 50k contatos ×
R$10 = R$0,5M. Arredonde sem medo e diga que é uma estimativa de ordem de grandeza.

---

## Frases de transição (em inglês, caso a entrevista seja em inglês)

- Pedir tempo: *"Could I take a minute to structure my thoughts?"*
- Anunciar a estrutura: *"I'd like to approach this in four parts: first…, then…"*
- Pedir dado explicando o porquê: *"Do we know X? It would tell me whether Y, which changes how I…"*
- Descartar uma alternativa: *"I considered X, but I'd rule it out because…"*
- Resumir no meio: *"Let me step back for a second: so far we have…, which implies…"*
- Voltar ao mapa: *"That covers evaluation. Next I'd like to talk about how this gets used."*
- Quando não souber: *"I'm not sure about the details of X, but the way I'd reason about it is…"*
- Discordância do "cliente": *"That's a fair concern. What would make you comfortable? One
  option is to run a small pilot and let the results speak."*

---

## Erros que reprovam

1. Pular para o modelo ("usaria XGBoost") antes de entender a decisão.
2. Falar só de AUC e nunca de dinheiro, clientes ou operação.
3. Divisão aleatória em problema temporal; vazamento de informação que passa despercebido.
4. Não definir o alvo com precisão.
5. Monólogo: não checar com o entrevistador nem incorporar as dicas dele. **As dicas são
   intencionais**: se ele perguntar "e o orçamento da equipe?", isso deve mudar sua métrica.
6. Não sintetizar. Terminar sem recomendação.
7. Propor algo que você não sabe defender tecnicamente. Eles vão perguntar.

---

## Folha de uma página (para revisar na terça de manhã, e depois fechar)

```
0 ESCUTAR    repetir o problema · 2–4 perguntas que mudam a solução · pedir 1 min
1 ENQUADRAR  negócio → decisão → tipo de problema → alvo preciso → KPI
             prever ou intervir? (uplift / experimento)
2 DADOS      árvore de hipóteses → fontes · leakage · granularidade · viés de seleção
3 EDA        taxa-base · tempo · segmentos · qualidade · hipóteses univariadas
4 FEATURES   RFM/tendência · entidade · contexto · relativo ao grupo · corte temporal
5 MODELO     baseline de negócio → logística → GBM · trade-offs · o que descartei
6 MÉTRICA    offline (AUC-PR, p@k, MAE) · decisão (custo FP × FN → limiar) · piloto A/B
             divisão TEMPORAL
7 PRODUÇÃO   como é consumido · drift · retreino · adoção/explicabilidade
8 RISCOS     técnicos · negócio · ética/regulação · quem precisa concordar
→ SÍNTESE    objetivo, abordagem, validação, riscos, próximo passo
```
