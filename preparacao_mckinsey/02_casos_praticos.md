# Casos para praticar

**Como usar:**
1. Leia só o **enunciado** e comece o cronômetro de 45 min.
2. Resolva em voz alta, com papel e caneta, seguindo os 8 passos.
3. Quando você fizer uma pergunta de esclarecimento, consulte as **respostas do "cliente"**.
4. As **perguntas do entrevistador** são as interrupções que ele fará. Se tiver alguém
   ajudando, essa pessoa as lê no meio da sua fala; se estiver sozinho, pare aos 15 e aos 30
   minutos e responda-as.
5. Só no fim abra a **resposta-modelo** e anote o que faltou (não o que você falou diferente;
   há várias respostas boas).

Os casos estão em ordem de "tipo de problema". Juntos, cobrem os padrões que mais aparecem:
classificação com orçamento de ação, previsão de demanda, manutenção preditiva, causalidade
de preço e promoção, fraude e recomendação.

---

## Caso 1 — Churn numa operadora de telecom

**Enunciado.** *"Our client is a mobile telecom operator with 8 million postpaid customers.
Churn has increased over the last year and the CEO wants to use data to reduce it. How would
you approach this?"*

**Respostas do "cliente" (se perguntar):**
- Churn mensal subiu de 1,5% para 2,0%. Ticket médio de R$80/mês.
- Hoje o time de retenção liga para quem pede cancelamento e oferece desconto. A capacidade é
  de 100 mil contatos proativos por mês.
- Dados disponíveis: cadastro, faturamento, uso (dados, voz), chamadas ao call center,
  reclamações na Anatel, qualidade de rede por antena, portabilidade.
- A oferta de retenção custa, em média, R$15/mês de desconto por 6 meses.

**Perguntas do entrevistador:**
1. "What exactly would you predict? Define the target."
2. "The retention team says your top-risk list is full of people who would leave anyway
   whatever we offer. How do you respond?"
3. "Your model has AUC 0.85. Is it good? How would you tell the CEO it works?"
4. "Quick calculation: what's the monthly value at stake if we reduce churn by 10% relative?"

<details>
<summary><b>Resposta-modelo</b></summary>

**Esclarecer:** qual é a alavanca (contato proativo com oferta)? Capacidade (100 mil/mês)?
Churn voluntário ou involuntário (inadimplência)? São problemas diferentes. Proponho focar no
voluntário.

**Enquadrar:** decisão = *quem* contatar a cada mês e *qual oferta* dar. Primeiro vem uma
classificação: alvo = "portabilidade ou cancelamento voluntário nos próximos 60 dias",
excluindo quem já tem o pedido aberto (leakage). O KPI de negócio é a receita retida líquida
do custo da oferta.

**A sacada (pergunta 2):** o risco de churn não é a mesma coisa que o ganho da ação. Há
clientes "perdidos" (saem de qualquer jeito), "fiéis" (ficam de qualquer jeito, e aí o desconto é
desperdício) e "persuadíveis". O certo é **uplift modeling**: estimar P(ficar | oferta) −
P(ficar | sem oferta). Para isso preciso de dados de tratamento aleatorizado. Proponho uma
campanha com grupo de controle aleatório: ela gera o rótulo para o modelo de uplift. Os métodos
podem ser T-learner, X-learner ou causal forest.

**Dados e hipóteses:** a árvore de fatores tem (a) qualidade do serviço: quedas de rede na
antena mais usada, reclamações; (b) preço: aumento de fatura, fim do período de fidelidade,
oferta de concorrente; (c) engajamento: queda de uso, mudança de padrão; (d) ciclo de vida:
tempo de casa, fim de contrato. Riscos nos dados: a junção de dados de rede por antena com o
cliente exige geolocalização; histórico de ofertas passadas enviesado (só quem pediu para
sair recebeu).

**EDA:** churn por safra, plano, região, fim de fidelidade; o salto de 1,5 para 2,0% está
concentrado em algum lugar? Pode ser uma causa única, como uma queda de rede numa região ou uma
oferta agressiva de um concorrente. Nesse caso, a ação não é um modelo.

**Features:** variação de uso nos últimos 30 dias contra os 90 anteriores, meses até o fim da
fidelidade, reclamações nos últimos 90 dias, percentual de chamadas caídas, aumento de fatura,
contatos com o SAC.

**Modelo:** baseline = regra "fim de fidelidade + reclamação". Depois regressão logística e
LightGBM. Para uplift, um T-learner com dois GBMs ou causal forest.

**Métrica (pergunta 3):** AUC 0,85 sozinho não diz nada. Como a capacidade é de 100 mil,
importa a **precision@100k** e o **lift no decil superior** (por exemplo, 5× a taxa-base).
Para uplift, a curva Qini. Divisão temporal. Para provar ao CEO: um **piloto A/B** com
tratados (lista do modelo), controle aleatório e a abordagem atual, medindo o churn e a receita
líquida em 60–90 dias.

**Conta (pergunta 4):** 8M × 2% = 160 mil saídas/mês. Redução relativa de 10% = 16 mil
clientes. × R$80 = R$1,28M/mês de receita mensal recorrente preservada, e cada cliente retido
vale vários meses (se ficar ~12 meses a mais, ~R$15M por safra mensal). Custo: 100 mil ofertas
× R$15 × 6 = R$9M se todos aceitarem. Esse é o argumento para mirar só os persuadíveis.

**Produção:** a lista mensal vai para o CRM, com o motivo principal por cliente (SHAP), o que
ajuda o atendente a escolher a oferta. Monitorar drift e sempre manter um grupo de controle
aleatório de ~5%, para continuar medindo o impacto e gerando dados para o uplift.

**Riscos:** canibalização (ensinar clientes que ameaçar sair dá desconto), adoção pelo time de
retenção, LGPD no uso dos dados de localização.
</details>

---

## Caso 2 — Previsão de demanda para uma rede de supermercados

**Enunciado.** *"A grocery retailer with 300 stores has high waste in fresh products and, at
the same time, frequent stock-outs. They want to improve replenishment using analytics."*

**Respostas do "cliente":**
- ~5 mil SKUs perecíveis por loja. O pedido de reposição é diário, feito pelo gerente da loja
  com base na intuição e na média das últimas semanas.
- 3 anos de vendas diárias por SKU × loja, promoções, preços, estoque diário (com falhas),
  calendário de feriados.
- Desperdício de ~4% da receita de perecíveis; ruptura estimada em 8% dos SKUs-dia.

**Perguntas do entrevistador:**
1. "Sales data only shows what was sold, not what customers wanted. Does that matter?"
2. "How would you handle 1.5 million store–SKU combinations? One model each?"
3. "Which metric would you report to the operations director?"
4. "A store manager doesn't trust the forecast and keeps overriding it. What do you do?"

<details>
<summary><b>Resposta-modelo</b></summary>

**Enquadrar:** o problema final é de **decisão de estoque** (quanto pedir), não só de previsão.
A previsão de demanda alimenta uma regra de pedido que equilibra o custo de sobra (desperdício)
e o custo de falta (venda perdida mais insatisfação). Para perecíveis, é o problema clássico do
**newsvendor**: o quantil ótimo é custo de falta / (custo de falta + custo de sobra). Então eu
preveria **quantis ou uma distribuição**, não só a média. KPI de negócio: desperdício % e
ruptura % em conjunto (os dois precisam cair, ou pelo menos um não pode piorar).

**Demanda censurada (pergunta 1):** sim, importa muito. Em dia de ruptura, a venda é menor que
a demanda. Se eu treinar direto, o modelo aprende a subestimar e perpetua a ruptura. Soluções:
marcar os dias com estoque zero e excluí-los ou tratá-los como censurados; estimar a demanda
perdida por padrão intradiário ou lojas similares.

**Dados:** qualidade do estoque (falhas), mudanças de sortimento, produtos novos (cold start),
efeito de promoções e canibalização entre SKUs.

**EDA:** padrões semanais (dia da semana é enorme em supermercado), sazonalidade anual,
feriados, efeito de promoção, intermitência (muitos SKUs com vendas zero).

**Features:** lags e médias móveis (7/14/28 dias), dia da semana, feriados e véspera, preço e
desconto, promoção, clima (para alguns itens), eventos locais, atributos do SKU e da loja.

**Modelo (pergunta 2):** um modelo **global** de gradient boosting (LightGBM) treinado em todas
as combinações, com identificadores de loja, SKU e categoria como features. Isso escala, compartilha
informação entre séries e resolve o cold start melhor que 1,5 milhão de ARIMAs. Com objetivo
quantílico ou modelo de distribuição. Baseline: média móvel sazonal (o que o gerente faz).
Alternativas: previsão hierárquica com reconciliação; modelos de deep learning (DeepAR/TFT)
se houver ganho claro, mas custam mais para manter.

**Métrica (pergunta 3):** tecnicamente, WAPE e viés (pinball loss para quantis), com
backtesting em janelas móveis. Para o diretor de operações: **desperdício % e ruptura %**
simulados no histórico ("com esta regra, no último trimestre, o desperdício teria sido 3,1% em
vez de 4%, e a ruptura 6% em vez de 8%"). Depois, piloto em ~20 lojas contra 20 lojas-controle
pareadas.

**Produção:** batch diário antes do horário de pedido, integrado ao sistema de reposição, com
limites de sanidade. Monitoramento do erro por categoria e retreino semanal.

**Adoção (pergunta 4):** é o ponto mais importante. Mostrar ao gerente por que a previsão está
assim (promoção, feriado), deixar que ele ajuste com um motivo registrado, e medir quem
acertou mais (modelo ou ajuste). Começar com o modelo como sugestão, e envolver os gerentes que
mais aderirem como campeões internos. Um override com justificativa também é dado útil (por
exemplo, um evento local que o modelo não conhece).

**Conta rápida:** se a receita de perecíveis é de R$3 bi/ano, 4% de desperdício = R$120M.
Cortar ¼ disso = R$30M/ano, antes de contar a venda recuperada com menos ruptura.
</details>

---

## Caso 3 — Manutenção preditiva numa mineradora

**Enunciado.** *"A mining company operates a fleet of 120 haul trucks. Unplanned breakdowns are
very costly. They have sensor data and want to predict failures."*

**Respostas do "cliente":**
- Cada hora de caminhão parado custa ~R$20 mil em produção perdida. Hoje a manutenção é por
  calendário (a cada X horas de operação).
- Sensores de motor e transmissão (temperatura, pressão, vibração) a cada 10 segundos, desde
  2 anos atrás. As ordens de serviço de manutenção estão num sistema separado, com texto livre.
- ~300 falhas graves registradas nos 2 anos, de ~15 tipos diferentes.

**Perguntas do entrevistador:**
1. "How do you create the labels?"
2. "You have only 300 failures. Is that enough?"
3. "The maintenance planner says too many false alarms make him ignore the system. How do you
   set the alert threshold?"

<details>
<summary><b>Resposta-modelo</b></summary>

**Enquadrar:** decisão = programar a manutenção antes da falha, na próxima janela de parada.
Então o alvo útil é "falha grave do componente X nos próximos N dias", e N depende do tempo de
que a manutenção precisa para agir (peças, equipe). Isso é mais útil que prever o instante exato.
KPI: horas de parada não planejada, disponibilidade da frota, custo de manutenção.

**Rótulos (pergunta 1):** juntar as ordens de serviço aos sensores por caminhão e tempo. O texto
livre precisa de classificação por tipo de falha (regras ou NLP simples, validadas com os
técnicos). Distinguir manutenção corretiva de preventiva. Cuidado com o carimbo de hora: a
ordem de serviço é aberta depois que a falha começou. Definir janelas: positivo = N dias antes
da falha; excluir o período logo antes e depois (zona ambígua, pós-reparo).

**Poucos eventos (pergunta 2):** 300 eventos em 15 tipos = ~20 por tipo, o que é pouco. Opções:
agrupar por sistema (motor, transmissão, pneus) e focar nos 2–3 modos de falha mais caros
(Pareto); ter muitas janelas negativas por caminhão; **detecção de anomalia** não
supervisionada (desvio do comportamento normal do caminhão, como um autoencoder ou isolation
forest) como complemento, sem precisar de rótulos; análise de sobrevivência (tempo até a falha,
com censura) em vez de classificação binária; regras de física e conhecimento dos engenheiros
como features.

**Dados e EDA:** sensores com falhas, calibração diferente entre caminhões, condições de operação
(carga, rota, clima) que mudam as leituras. Normalizar por condição de operação. Visualizar
sinais antes das falhas conhecidas com os engenheiros.

**Features:** agregados em janelas (média, máximo, tendência, desvio-padrão) de 1h, 24h, 7d;
tempo desde a última manutenção; horas de operação; carga média; quantidade de alertas do
próprio equipamento.

**Modelo:** baseline = a regra de calendário atual e os limiares de alarme do fabricante. Depois
GBM sobre as features em janela, e o modelo de sobrevivência como alternativa.

**Limiar (pergunta 3):** definir pelo custo. Falso negativo = falha não prevista ≈ ~10h de
parada × R$20 mil = R$200 mil mais o reparo maior. Falso positivo = uma inspeção desnecessária
(~2h + mão de obra ≈ R$40 mil, menos se feita numa parada já programada). Isso justifica um
limiar que tolera vários falsos positivos por falha evitada. Mas a capacidade da oficina e a
confiança do planejador limitam o número de alertas por semana: fixar um orçamento (por exemplo,
5 alertas/semana) e maximizar a precision dentro dele. Avaliar no tempo (backtest por período) e
por caminhão (validação agrupada por caminhão, para não vazar).

**Produção:** o scoring diário alimenta uma lista priorizada para o planejador, com o sinal que
disparou o alerta. Cada alerta recebe o feedback do técnico ("encontrou desgaste?"), o que gera
rótulos novos.

**Riscos:** o modelo muda o próprio dado (falhas evitadas somem dos rótulos; é preciso registrar
as intervenções); caminhões novos ou de outra marca; mudança de sensores.
</details>

---

## Caso 4 — Efetividade de promoções num fabricante de bens de consumo

**Enunciado.** *"A consumer goods company spends 20% of its revenue on trade promotions with
retailers. The CFO suspects much of it is wasted. How would you determine which promotions work?"*

**Respostas do "cliente":**
- Dados semanais de sell-out por varejista × SKU × região (3 anos), calendário de promoções,
  preço, mídia.
- Promoções não são aleatórias: o time comercial promove mais nos períodos de alta e nos
  produtos que vendem mais.

**Perguntas do entrevistador:**
1. "Sales go up 40% in promotion weeks. So promotions work, right?"
2. "How do you estimate what would have happened without the promotion?"
3. "What would you recommend the CFO actually do next year?"

<details>
<summary><b>Resposta-modelo</b></summary>

**Enquadrar:** é uma pergunta **causal**, não preditiva: qual é o **ganho incremental** de cada
promoção, e qual o **ROI**? ROI = (margem da venda incremental − custo da promoção) / custo.
Decisão: realocar o orçamento entre tipos de promoção, SKUs, varejistas e frequência.

**A armadilha (pergunta 1):** os 40% são brutos. É preciso descontar: (a) **baseline**: a venda
teria subido de qualquer jeito, porque a promoção cai na alta; (b) **antecipação e estoque em
casa**: o consumidor antecipa a compra e a semana seguinte cai (*pull-forward*/*post-promo dip*);
(c) **canibalização**: roubo de venda de outros SKUs da própria empresa; (d) *forward buying*
do varejista. Promoção não é aleatória, então há **viés de confusão**.

**Contrafactual (pergunta 2):** um modelo de baseline de vendas, sem promoção (ex.: regressão
ou GBM com sazonalidade, tendência, preço regular, distribuição e mídia), treinado nas semanas
sem promoção. O incremental é a venda real menos o baseline. Complementos: comparar regiões
ou varejistas com e sem a mesma promoção (**diferença-em-diferenças**, controle sintético),
modelar a elasticidade-preço, incluir as semanas depois e os SKUs vizinhos para capturar dip e
canibalização. O mais forte é **testar**: promoções aleatorizadas por loja ou região.

**Dados e EDA:** verificar se a variável "promoção" é bem registrada; mudanças de distribuição;
falta de estoque; efeito de mídia concomitante (atribuição).

**Métrica:** a precisão do modelo de baseline nas semanas sem promoção (MAPE/WAPE em backtest);
depois o ROI por evento, com intervalo de confiança. Validar com um teste em campo.

**Recomendação (pergunta 3):** ranking das promoções por ROI; tipicamente uma parte relevante tem
ROI negativo, e cortar ou redesenhar o quartil pior libera orçamento para o quartil melhor. Plano:
(1) cortar o grupo claramente negativo, (2) testar de forma controlada os casos incertos, (3)
institucionalizar o pós-evento de cada promoção num painel para o time comercial. Dimensionamento:
se a receita é R$10 bi, promoções = R$2 bi; realocar 10% dos gastos com ROI negativo = R$200M
reaproveitados.

**Stakeholders:** o time comercial vai resistir (a promoção também é moeda de negociação com o
varejista). Envolvê-lo na definição e na metodologia desde o início.
</details>

---

## Caso 5 — Fraude em sinistros de seguro

**Enunciado.** *"An auto insurer believes 5–10% of claims involve some fraud. They have a team
of 20 investigators. How can data science help?"*

**Respostas do "cliente":**
- 200 mil sinistros/ano. Cada investigador analisa ~500/ano (10 mil no total, 5%).
- Os rótulos existem só para os casos investigados: ~30% dos investigados confirmam fraude.
- Dados: apólice, histórico do segurado, descrição do sinistro (texto), oficina, prestadores,
  fotos, tempo entre contratação e sinistro.
- Um sinistro fraudulento médio custa R$15 mil.

**Perguntas do entrevistador:**
1. "Your labels only exist for claims that were investigated. Problem?"
2. "Which metric do you optimise?"
3. "The legal team says you cannot deny a claim because 'the model said so'. Implications?"

<details>
<summary><b>Resposta-modelo</b></summary>

**Enquadrar:** decisão = quais 10 mil sinistros enviar para investigação (**ranking com orçamento
fixo**). O modelo prioriza, o humano decide. KPI: valor de fraude detectada (e evitada) por
investigador; tempo de pagamento dos sinistros legítimos (não atrasar o cliente honesto).

**Viés de seleção (pergunta 1):** sim. Os rótulos refletem os critérios antigos de quem era
investigado. O modelo aprende "o que os investigadores acham suspeito" e não enxerga fraudes de
tipo novo. Mitigações: reservar uma **amostra aleatória** de investigações (ex.: 5–10% do
orçamento) para ter rótulos não enviesados e medir a taxa real; técnicas de semi-supervisão ou
PU-learning; **detecção de anomalia** e **análise de rede** (a mesma oficina, o mesmo advogado ou
o mesmo telefone ligando muitos sinistros: redes de fraude organizada) como fontes
complementares.

**Features:** tempo entre a apólice e o sinistro, alteração recente de cobertura, histórico de
sinistros, horário e local, sinais do texto (inconsistências, palavras-chave), grau na rede de
prestadores, valor contra o esperado para o tipo de dano.

**Modelo:** baseline = as regras atuais (red flags). Depois GBM supervisionado, somado a scores
de anomalia e de rede. Explicabilidade é obrigatória (pergunta 3).

**Métrica (pergunta 2):** com orçamento fixo, **precision@k** (k = 10 mil), ou melhor, **valor
recuperado@k**: ponderar pelo valor do sinistro, porque é melhor investigar uma fraude de
R$80 mil do que uma de R$2 mil. AUC-PR como métrica geral (classe rara). Divisão temporal.
Hoje: 10 mil investigações × 30% = 3 mil fraudes. Se o modelo levar a precision a 45% = 4,5 mil,
são +1,5 mil fraudes × R$15 mil = **R$22,5M/ano** a mais, com a mesma equipe.

**Explicabilidade e regulação (pergunta 3):** o modelo serve para **triagem**, e a decisão de
negar é do investigador, com evidência. Cada score vem com os motivos (SHAP/regras). Verificar
se o modelo não discrimina por atributos protegidos ou por proxies (CEP, por exemplo). Documentar
o modelo e manter a trilha de auditoria.

**Produção:** score em tempo real na abertura do sinistro (fast-track para os de baixo risco, o
que também melhora a experiência), fila priorizada para os investigadores, com feedback do
resultado da investigação. Os fraudadores se adaptam, então o drift é esperado: retreino
frequente e monitoramento dos padrões novos.
</details>

---

## Caso 6 — Próxima melhor oferta num banco

**Enunciado.** *"A retail bank wants to increase product holding per customer: today customers
have 1.8 products on average. They'd like to personalise offers across the app, email and branch."*

**Respostas do "cliente":**
- 5 milhões de clientes, 12 produtos (cartões, empréstimo pessoal, investimentos, seguros…).
- As campanhas atuais são por segmento, com uma taxa de conversão de ~1%.
- Há limite de contatos por cliente (no máximo 2 ofertas por mês) e restrições de crédito
  (risco) para alguns produtos.

**Perguntas do entrevistador:**
1. "How do you choose which product to offer each customer?"
2. "Should the bank always offer the product with the highest probability of purchase?"
3. "How do you know the personalisation beat the segment campaigns?"

<details>
<summary><b>Resposta-modelo</b></summary>

**Enquadrar:** decisão = para cada cliente e mês, qual oferta (ou nenhuma), em qual canal. KPI:
produtos por cliente e, principalmente, **valor** (margem incremental ao longo do tempo), mais
a satisfação (não incomodar).

**Abordagem (pergunta 1):** um modelo de propensão por produto (P(contrata o produto j |
cliente)), treinado com "clientes parecidos que compraram o produto j nos meses seguintes",
excluindo quem já tem. Ou um modelo multiclasse/ranking. Alternativas: filtragem colaborativa
("clientes com carteira parecida têm…"), bandits contextuais para aprender com as respostas
às ofertas (exploração × aproveitamento).

**Não é só probabilidade (pergunta 2):** não. A oferta ótima maximiza o **valor esperado
incremental**: P(converter | oferta) − P(converter | sem oferta), × margem do produto − custo
do contato, e dentro das **restrições**: risco de crédito (não ofertar crédito a quem não pode
pagar, que é também uma questão de adequação e de regulação), limite de 2 contatos por mês e
prioridades do banco. Isso vira um **problema de otimização** (atribuição com restrições) em cima
dos scores. Também considerar a sequência: cartão antes de investimento, por exemplo.

**Dados:** transações (sinais de eventos de vida: salário novo, mudança de cidade), produtos
atuais, interações no app, respostas a campanhas anteriores (para uplift), dados de crédito.
Consentimento de uso para marketing (LGPD).

**Métrica (pergunta 3):** offline, precision@k e AUC por produto, e a calibração (importa para o
valor esperado). Online, um **teste A/B**: um grupo com as ofertas do modelo, um grupo com as
campanhas por segmento e um grupo de controle sem oferta, medindo a conversão incremental, a
margem e o descadastramento (opt-out). Conversão de 1% para 2% em 5M × 2 contatos/mês = 100
mil produtos extras/mês. Com margem anual de R$200 por produto, ~R$20M de valor anual por mês
de campanha.

**Produção:** scores em batch diário, o motor de regras e otimização decide, os canais consomem
por API; o gerente de agência vê a sugestão com o motivo. Monitoramento de fadiga de contato.

**Riscos:** venda inadequada (mis-selling), reputação, viés; loop de feedback (o modelo só aprende
com as ofertas que ele mesmo fez), daí a importância de manter exploração.
</details>

---

## Depois de cada caso: auto-avaliação

Marque de 1 a 5:

| critério | nota |
|---|---|
| Fiz 2–4 perguntas de esclarecimento, dizendo por que as fazia? | |
| Anunciei a estrutura no início e voltei a ela depois das interrupções? | |
| Defini o alvo com precisão (evento, janela, população)? | |
| Perguntei a mim mesmo "prever ou intervir?" | |
| Citei um risco de dados concreto (leakage, viés de seleção, censura)? | |
| Propus um baseline antes do modelo, e disse o que descartei? | |
| Liguei a métrica técnica ao dinheiro e ao limiar de decisão? | |
| Propus a validação no mundo real (piloto/A/B)? | |
| Falei de adoção e dos stakeholders? | |
| Terminei com uma síntese de 30 segundos? | |
| Fiquei dentro de 45 minutos? | |
