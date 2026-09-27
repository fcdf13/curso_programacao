# Perguntas técnicas do meio do case

O guia diz: *"We will look for evidence that you understand the model(s) you propose."* As
perguntas vêm do contexto do case. Por isso, **só proponha o que você sabe defender**. Cada
resposta abaixo cabe em ~30 segundos. Treine dizendo em voz alta, não lendo.

---

## A. Enquadramento e dados

**Como você detecta vazamento de informação (leakage)?**
Features que não existiriam no momento da previsão. Sinais de alerta: desempenho bom demais,
uma feature dominando a importância. Previna com um corte temporal rígido (features calculadas
só com dados anteriores à data de referência) e divisão temporal ou agrupada por entidade.

**Por que divisão temporal e não aleatória?**
Em produção, sempre prevemos o futuro com o passado. A divisão aleatória mistura períodos,
vaza tendência e sazonalidade e superestima o desempenho. Com várias linhas por entidade,
também é preciso agrupar (group k-fold), para não ter a mesma pessoa em treino e em teste.

**O que é viés de seleção nos rótulos?**
Quando só temos o rótulo de uma amostra escolhida por um critério (empréstimos aprovados, casos
investigados). O modelo aprende a população errada. Mitigação: amostra aleatória
(exploração), reject inference, modelos de propensão para reponderar.

**Como tratar dados faltantes?**
Primeiro entender o **porquê** (aleatório? informativo?). Opções: imputar (mediana, modelo) com
um indicador de "estava faltando"; GBMs lidam nativamente com nulos. Faltar pode ser o próprio
sinal: um cliente sem uso de dados, por exemplo.

**Demanda censurada?**
Quando a venda é limitada pelo estoque, ela subestima a demanda. Trate os dias de ruptura como
censurados ou exclua-os.

---

## B. Modelos

**Por que gradient boosting em dados tabulares?**
Captura não-linearidades e interações sem feature engineering manual, lida com nulos e escalas
diferentes, é robusto a outliers nas features e costuma ganhar em dados tabulares. Contras: menos
interpretável que um modelo linear, precisa de ajuste de hiperparâmetros, extrapola mal fora do
intervalo de treino.

**Random forest × gradient boosting?**
RF: árvores independentes em paralelo (bagging), reduz variância, difícil de fazer overfitting,
pouco ajuste. GBM: árvores sequenciais corrigindo o erro das anteriores (boosting), reduz viés,
normalmente é mais preciso, mas é mais sensível a hiperparâmetros e a overfitting (learning
rate, early stopping).

**Quando usar regressão logística?**
Como baseline, quando a interpretabilidade e a regulação importam (crédito), com poucos dados, ou
quando a relação é aproximadamente linear. Os coeficientes são explicáveis e as probabilidades
tendem a vir bem calibradas.

**Trade-off viés × variância?**
Viés = erro por um modelo simples demais (underfitting). Variância = sensibilidade demais ao
treino (overfitting). Modelos mais complexos têm menos viés e mais variância. Controle com
regularização, mais dados, validação cruzada e early stopping.

**Regularização L1 × L2?**
L1 (Lasso) zera coeficientes, fazendo seleção de variáveis. L2 (Ridge) encolhe os coeficientes
sem zerar e lida bem com a colinearidade. Elastic net combina as duas.

**Como lidar com classes desbalanceadas?**
Primeiro, a métrica certa (AUC-PR, precision@k, não acurácia). Depois: ponderar as classes na
perda, reamostrar (undersampling da maioria; SMOTE com cuidado), ajustar o limiar pelo custo.
Se reamostrar, recalibre as probabilidades.

**Como escolher o número de clusters (segmentação)?**
Método do cotovelo, silhueta, mas sobretudo a **utilidade para o negócio**: os segmentos são
acionáveis, estáveis no tempo e diferentes em comportamento?

**Série temporal: modelo clássico ou ML?**
Poucas séries e padrões estáveis: ARIMA/ETS/Prophet. Muitas séries relacionadas com
covariáveis (preço, promoção): um modelo global de GBM com lags. Backtesting com janelas
móveis, sempre.

**Análise de sobrevivência, quando?**
Quando importa **quando** o evento acontece e há censura (quem ainda não saiu, ou a máquina
que ainda não falhou). Kaplan-Meier para descrever; Cox ou modelos de GBM de sobrevivência para
prever.

**Uplift ou modelo de resposta?**
O modelo de resposta prevê o resultado; o uplift prevê a **mudança causada pela ação**. Precisa
de dados de um tratamento aleatorizado. Métodos: T-learner, S-learner, X-learner, causal
forest. Avaliação pela curva Qini ou curva de uplift.

**Como estimar um efeito causal sem experimento?**
Diferença-em-diferenças (tendências paralelas), controle sintético, pareamento/propensity score,
regressão descontínua, variáveis instrumentais. Todos têm hipóteses. O padrão-ouro, quando
possível, é um teste A/B.

---

## C. Avaliação

**Precision × recall?**
Precision = dos que eu apontei, quantos são mesmo positivos. Recall = dos positivos reais,
quantos eu peguei. O trade-off é controlado pelo limiar. A escolha vem do custo relativo entre
falso positivo e falso negativo, e da capacidade de ação.

**AUC-ROC × AUC-PR?**
ROC mede a ordenação geral e não é sensível à taxa-base. Em classes raras, pode parecer ótima
mesmo com uma precision baixa. AUC-PR é mais informativa quando os positivos são raros.

**Como escolher o limiar?**
Maximize o valor esperado: para cada limiar, (VP × ganho) − (FP × custo) − (FN × perda), sujeito
à capacidade (k contatos, inspeções). Na prática, ordene pelo score e pegue o top-k.

**O que é calibração e quando importa?**
Uma probabilidade prevista de 0,2 deve corresponder a ~20% de eventos. Importa quando o valor da
probabilidade entra numa conta (valor esperado, preço, provisão). Verifique com a curva de
calibração; corrija com Platt/isotônica.

**MAE × RMSE × MAPE?**
MAE: erro médio absoluto, robusto e fácil de explicar. RMSE: penaliza erros grandes. MAPE: em
%, mas explode com valores próximos de zero. Para demanda, prefira WAPE (soma dos erros /
soma das vendas).

**Como provar o valor do modelo para o cliente?**
Um piloto com grupo de controle aleatório, medindo o KPI de negócio, não a métrica do modelo.
Defina de antemão o tamanho da amostra (poder estatístico) e a duração.

**Teste A/B — o que pode dar errado?**
Amostra pequena (falta de poder), olhar o resultado todo dia e parar cedo (*peeking*),
contaminação entre grupos, efeito de novidade, métricas múltiplas (falsos positivos), unidade de
aleatorização errada.

---

## D. Produção e explicabilidade

**O que é drift e como monitorar?**
*Data drift*: a distribuição das entradas muda (PSI, teste KS). *Concept drift*: a relação entre
as entradas e o alvo muda, e aparece quando o rótulo chega e o desempenho cai. Monitore os dois
e retreine por calendário ou por gatilho.

**Como explicar um modelo de caixa-preta?**
Global: importância das features, dependência parcial. Local: SHAP (a contribuição de cada
feature para aquela previsão). Na comunicação com o negócio: 2–3 motivos principais em linguagem
simples.

**Batch ou tempo real?**
Depende da decisão. Lista de campanha mensal: batch. Aprovação de uma transação ou fraude no
momento do pagamento: tempo real (latência, disponibilidade, features calculadas online).

**Loop de feedback?**
Quando as ações do modelo alteram os dados futuros (retemos quem o modelo apontou e o churn
deles some dos dados). Mantenha grupos de controle e registre as intervenções.

**Viés e justiça (fairness)?**
Verifique o desempenho e as taxas de decisão por grupo; atenção a proxies de atributos
protegidos (CEP, nome). Documentação, revisão humana nas decisões de alto impacto.

---

## E. Estatística rápida (pode aparecer como pergunta solta)

- **Valor-p:** a probabilidade de observar um resultado tão extremo **se a hipótese nula for
  verdadeira**. Não é a probabilidade de a hipótese ser verdadeira.
- **Intervalo de confiança de 95%:** o procedimento que, repetido, cobre o valor real em 95% das
  vezes.
- **Teorema de Bayes:** P(A|B) = P(B|A)·P(A)/P(B). O clássico: um teste 99% preciso para uma
  doença com 1% de prevalência dá ~50% de positivos verdadeiros. **A taxa-base importa** (é o
  mesmo raciocínio da precision em classes raras).
- **Correlação não é causalidade:** confusão, causalidade reversa, viés de seleção.
- **Paradoxo de Simpson:** uma tendência que se inverte quando se agrega os grupos. Sempre
  segmente.
