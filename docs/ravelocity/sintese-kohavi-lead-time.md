# RAVelocity — Reduzir o lead-time de experimentação de 30 para 15 dias

**Síntese analítica da Parte IV de *Trustworthy Online Controlled Experiments* (Kohavi, Tang & Xu), aplicada ao contexto do RAVelocity**

Documento de trabalho · versão 1 · setembro/2026
Base bibliográfica: capítulos 12 a 16 ("Advanced Topics for Building an Experimentation Platform")

---

## Como usar este documento

Ele tem três camadas, e cada uma serve a um propósito diferente:

1. **Diagnóstico e tese** (seções 1–3) — o argumento central sobre o que realmente move o lead-time, e por que a meta de 15 dias é atingível mas *não* pela via que parece óbvia. É o material para o discurso ao diretor.
2. **Estratégias** (seções 4–6) — o desdobramento dos dois grupos (reativas e estruturantes), com a evidência do Kohavi anexada a cada item e os anti-padrões que sabotam a meta.
3. **Instrumentos de execução** (seções 7–9) — o OEC do próprio programa, o roteiro de entrevista, e o **checklist de cruzamento com a estrutura atual do RAVelocity**, que é o insumo direto para a TO-DO list.

A seção 9 é a que você leva para a próxima sessão, junto do mapa do repositório, para gerar a lista de tarefas priorizada.

---

## 0. Uma ressalva honesta sobre a fonte

A Parte IV do livro é a parte *de engenharia de plataforma*: client-side, instrumentação, unidade de randomização, ramp e escalonamento da análise. Ela não é, à primeira vista, um capítulo sobre "velocidade de aprendizado organizacional". Mas é justamente aí que está o valor para o RAVelocity: **quase todo o tempo perdido entre hipótese e decisão é tempo de plataforma, não tempo de gente.** Fila de instrumentação, ramp mal calibrado, scorecard que demora, teste subdimensionado que não conclui, decisão que trava porque ninguém confia no número — todos esses são problemas que o Kohavi trata nesses cinco capítulos, e todos são endereçáveis por *feature de produto*, não por comunicado interno.

Três avisos de escopo:

- O capítulo 15 (Ramping / SQR) é o mais diretamente aplicável e é o coração deste documento.
- Vários pontos aqui referenciam capítulos **fora** deste PDF (cap. 3 SRM e SUTVA, cap. 5 métricas de velocidade, cap. 8 memória institucional, cap. 17 múltiplos testes e stopping rules, cap. 20 análise triggered, cap. 22 redução de variância/CUPED, cap. 23 efeitos de longo prazo). Onde eu uso algo que vem de fora do excerto, está marcado como **[fora do excerto]**. Vale muito ler o 17, o 20 e o 22 antes de fechar o roadmap — são os três que mais afetam a meta.
- Onde eu extrapolo do livro para o seu contexto, está marcado como **[extrapolação]**.

---

## 1. Passo zero: definir com precisão o relógio que estamos tentando encurtar

Antes de qualquer estratégia, é preciso fechar a definição operacional da métrica. Hoje ela está ambígua na formulação "tempo entre a hipótese e o experimento", e a ambiguidade muda completamente o plano de ação.

**Leitura A — hipótese → *início* do experimento.** Mede fila de design e implementação. Aqui a meta de 15 dias é confortável e o problema é quase todo organizacional/ferramental.

**Leitura B — hipótese → *decisão* (experimento concluído e lido).** Inclui o tempo de execução. É a leitura consistente com a sua preocupação de que "experimentos underpowered acabam rodando por muito tempo e extrapolando a meta" — se o tempo de execução não estivesse dentro do relógio, um teste underpowered não estouraria a meta.

**Este documento assume a Leitura B**, porque é a mais restritiva e a que corresponde à sua descrição do problema. Se a definição oficial for a Leitura A, tudo aqui continua válido, e a meta fica ainda mais folgada. **Confirme isso antes de apresentar — é a primeira pergunta que um diretor faz.**

### 1.1 A decomposição em estágios

Um número agregado de 30 dias não diz onde está a fila. O primeiro entregável de plataforma é **carimbar o tempo de cada estágio**:

| # | Estágio | Do evento | Ao evento | Natureza |
|---|---------|-----------|-----------|----------|
| S1 | Formulação | hipótese registrada | design aprovado / escopo fechado | humano, comprimível |
| S2 | Instrumentação | design aprovado | eventos disponíveis e validados | engenharia, comprimível |
| S3 | Implementação | eventos ok | variante pronta atrás de flag | engenharia, comprimível |
| S4 | Fila / liberação | variante pronta | primeira exposição real | processo, comprimível |
| S5 | Ramp pré-MPR | primeira exposição | atingir alocação de medição | **parcialmente irredutível** |
| S6 | Execução em MPR | alocação de medição | fim da janela de medição | **irredutível (~7 dias)** |
| S7 | Leitura | fim da janela | scorecard confiável disponível | plataforma, comprimível |
| S8 | Decisão | scorecard | decisão registrada (launch/kill/iterate) | humano, comprimível |

Sem esses oito carimbos, qualquer plano de redução é chute. **Este é provavelmente o item nº 1 da TO-DO list**, e é barato: são campos de timestamp e transições de estado num modelo de dados que o RAVelocity quase certamente já tem em alguma forma.

### 1.2 A aritmética dos 15 dias

O livro dá números concretos para os estágios irredutíveis:

- **S6 = 7 dias.** "We want to highlight our recommendation to keep experiments at MPR for a week, and longer if novelty or primacy effects are present" (cap. 15). A razão é dupla: capturar fatores dependentes do tempo (dia de semana vs. fim de semana) e evitar o viés de heavy users — "an experiment that runs for only one day will have results biased towards heavy users". O ganho de precisão *depois* de uma semana é pequeno na ausência de novidade/primazia; **antes** de uma semana, o custo em viés é grande.
- **S5 = horas a poucos dias.** Pré-MPR são "short ramps": anéis de exposição e dial automático de tráfego. O livro é explícito sobre a ordem de grandeza: "taking an extra hour to reach 5% can help limit the impact of bad bugs without adding much delay".
- **S7 = do dia para horas.** Historicamente Bing/Google/LinkedIn tinham scorecard diário com ~24h de atraso; hoje operam caminhos near-real-time. E o livro conecta isso diretamente ao nosso problema: "any delay in experiment scorecard generation can add delay to decision making".

Ou seja, o **núcleo irredutível de um experimento bem desenhado é da ordem de 9 a 11 dias** (1–3 de pré-MPR + 7 de MPR + ~1 de leitura). Dentro de uma meta de 15 dias, sobram **4 a 6 dias para tudo o que é humano: formular, instrumentar, implementar, esperar na fila e decidir.**

Essa conta é o argumento central para o diretor, e ela tem duas consequências que precisam ser ditas em voz alta:

> **A meta de 15 dias é atingível, mas apenas se ela for perseguida em S1–S4, S7 e S8. Perseguir a meta em S6 — isto é, rodando testes por menos de uma semana — troca lead-time por decisões erradas, e decisões erradas custam mais do que 15 dias.**

> **Com 4 a 6 dias de folga total, não existe espaço para retrabalho.** Um único ciclo de "descobri no dia 8 que o evento não estava instrumentado" estoura a meta sozinho. É por isso que os *gates* de pré-registro (seção 5.1 e 5.2) não são burocracia: eles são o mecanismo que protege o orçamento de tempo.

---

## 2. A tensão central da tese: escopo menor **não** implica experimento mais rápido

Esta é a parte contraintuitiva, e é a que mais precisa aparecer na apresentação, porque é onde a iniciativa pode falhar silenciosamente.

A tese de negócio — "escopo menor, incremental, aprendizado mais acelerado, mais experimentos" — está correta na direção, mas tem um efeito colateral estatístico direto:

**Escopo menor → efeito esperado menor → tamanho de amostra necessário maior → mais tempo de execução, não menos.**

O tamanho de amostra necessário cresce com o *quadrado* do inverso do efeito **[fora do excerto — regra padrão do cap. 17]**: detectar um efeito de 0,5% exige aproximadamente **quatro vezes** mais amostra que detectar 1%. Um squad que fatia uma tese grande em quatro incrementos pequenos pode, sem perceber, transformar um experimento de 10 dias em quatro experimentos de 30 dias cada.

**É exatamente esse o mecanismo que produz o sintoma que você já observou:** testes underpowered que rodam indefinidamente porque nunca alcançam significância, e estouram a meta. O squad não está sendo lento — ele está sendo lento *por causa da* decisão de reduzir escopo, tomada sem a compensação correspondente de sensibilidade.

### 2.1 As cinco compensações de sensibilidade

Se a empresa vai reduzir escopo, a plataforma precisa devolver poder estatístico por outras vias. Todas as cinco estão nos capítulos lidos ou são referenciadas por eles:

1. **Alocação em MPR (Maximum Power Ramp).** Um teste 50/50 é o ponto de máxima sensibilidade. A variância no teste t de duas amostras é proporcional a `1/(q(1-q))`, minimizada em `q = 0,5` (cap. 15, nota de rodapé 1). Rodar 10/90 "por segurança" durante toda a execução é a forma mais comum e mais cara de desperdiçar tempo. **Se hoje o RAVelocity permite ou incentiva alocações assimétricas prolongadas, essa é uma correção de altíssimo retorno e baixíssimo custo.**
2. **Análise triggered.** Medir apenas sobre a população que efetivamente poderia ser afetada pela mudança remove a diluição causada por usuários que nunca viram o tratamento (cap. 12, implicação #4; cap. 20 **[fora do excerto]**). Para experimentos de escopo pequeno — que por definição afetam uma fração pequena da jornada — este é **o** maior multiplicador de sensibilidade disponível. O cap. 16 lembra de sempre reportar o impacto *overall* ao lado do impacto na população triggered, para não superestimar o efeito no negócio.
3. **Unidade de randomização mais fina, quando válida** (cap. 14, detalhado na seção 5.3). Mais unidades → menor variância da média → mais poder.
4. **Métricas mais sensíveis e de menor variância.** O cap. 16 é explícito: "metrics with high variance such as revenue... having a more sensitive, lower variance version such as trimmed revenue or other indicators, allows more informed decisions". Instrumentação server-side também ajuda: "because it is not impacted by the network, the data tend to have lower variance, allowing for more sensitive metrics" (cap. 13).
5. **Redução de variância (CUPED e afins)** **[fora do excerto — cap. 22, referenciado no cap. 15]**. É a alavanca de maior impacto por unidade de esforço de engenharia depois do triggering, e vale um spike técnico dedicado.

### 2.2 A consequência de produto

O gate de desenho de experimento que você já imaginou tem, portanto, uma função mais precisa do que "melhorar a qualidade da hipótese". Ele é o lugar onde a plataforma pergunta:

> *Você reduziu o escopo. O efeito que você espera agora é menor. Você compensou isso com triggering, alocação e métrica adequados — ou você acabou de desenhar um teste que vai rodar 40 dias sem concluir nada?*

Uma calculadora de amostra mínima que apenas devolve um número está incompleta. A calculadora útil devolve um **veredito com saídas**: "com o desenho atual, este experimento precisa de 26 dias para detectar o efeito que você declarou. Opções: (a) restringir a análise à população triggered → 11 dias; (b) usar a métrica X, de menor variância, como indicador primário → 9 dias; (c) subir a alocação para 50/50 → 14 dias; (d) aumentar o escopo da mudança; (e) declarar explicitamente que este é um experimento de aprendizado, não de decisão."

---

## 3. Mapa: o que cada capítulo entrega para a meta

| Cap. | Tema | Alavanca de lead-time | Onde entra |
|------|------|------------------------|------------|
| 12 | Client-Side Experiments | O relógio do experimento em app **não começa** quando você liga a flag. Parametrização substitui ciclo de release. | §4.2, §5.5 |
| 13 | Instrumentation | "Nada sobe sem instrumentação" — elimina a causa nº 1 de retrabalho tardio. | §5.2 |
| 14 | Choosing a Randomization Unit | Granularidade é um botão de poder estatístico, com restrições de validade que a plataforma pode checar. | §5.3 |
| 15 | Ramping (SQR) | O framework de referência: velocidade, qualidade e risco como um trade-off explícito e *templatizável*. | §5.4 |
| 16 | Scaling Experiment Analyses | Latência de scorecard, confiança na leitura, taxonomia de métricas, notificação e aprovação como fluxo de produto. | §5.6, §5.7 |

---

## 4. Grupo I — Estratégias reativas (estancar o sangramento)

O plano de identificar os squads com maior gap e entrevistá-los está correto e é de fato o *low-hanging fruit*. Três refinamentos o tornam muito mais forte.

### 4.1 Localize com dados, explique com entrevista

Entrevista é um instrumento caro e enviesado para *localizar* um gargalo — as pessoas relatam a dor mais recente, não a mais custosa. Use a decomposição S1–S8 (§1.1) para localizar, e a entrevista para explicar.

Na prática: para cada squad outlier, monte o histograma de tempo por estágio antes da conversa e entre na sala com uma pergunta específica ("seus experimentos passam em média 11 dias entre design aprovado e primeira exposição — o que acontece nesses 11 dias?") em vez de uma pergunta aberta. Isso muda a qualidade da evidência coletada e, principalmente, torna a evidência **agregável** entre squads, que é o que alimenta o Grupo II.

Se a decomposição por estágio ainda não existir na plataforma, ela vira pré-requisito do Grupo I — e isso reordena o roadmap: **um pedaço pequeno do trabalho estruturante precisa vir antes do trabalho reativo.**

### 4.2 Segmente antes de comparar — nem todo gap é cultural

O cap. 12 é um alerta direto contra o "naming and shaming" acidental. Experimentos client-side têm um piso estrutural de lead-time que nenhuma mudança de comportamento remove:

- A variante precisa **já estar no build** — "all experiments, including all variants for each of these experiments, need to be coded and shipped with the current app build. Any new variants, including bug fixes on any existing variant, must wait for the next release."
- A configuração pode não chegar ao device (offline, banda limitada), e quando chega, "the new assignment may not take effect until the next session" — para usuários leves, isso é uma semana.
- A adoção da nova versão "takes about a week to reach a more stable adoption rate".
- Nos primeiros dias o sinal é fraco e **enviesado** para usuários frequentes e de Wi-Fi.

**Consequência operacional:** um squad de app pode ter processo impecável e ainda assim aparecer como outlier. Antes de qualquer entrevista, segmente o painel por **plataforma (server / web / app)** e verifique se o gap sobrevive à segmentação. Se não sobreviver, o problema não é do squad — é a meta que precisa ser diferenciada por plataforma, e essa é uma recomendação legítima para levar ao diretor.

**Consequência de medição:** a plataforma deveria registrar o **início efetivo** do experimento (primeiro evento real de exposição/triggering) e não apenas o início nominal (quando alguém apertou o botão). Sem isso, o lead-time de app é medido errado — e, pior, o cap. 12 alerta que Controle e Tratamento podem ter *effective starting times* diferentes (especialmente com Controle compartilhado, que pode estar no ar antes, com cache aquecido e população selecionada distinta), o que é uma ameaça de validade, não só de métrica de processo.

### 4.3 Cuidado com regressão à média na avaliação do próprio programa

Selecionar os squads com pior desempenho, intervir, e medir a melhora **produz melhora mesmo que a intervenção não faça nada** — os extremos regridem naturalmente. É o mesmo raciocínio de replicação que o cap. 15 recomenda para resultados surpreendentes ("rerun the experiment with a different set of users... replication is a simple yet effective way to eliminate spurious errors").

Três defesas práticas:
1. Avalie o programa pela **distribuição do portfólio inteiro** (p50 e p75/p90 de todos os squads), não só pela melhora dos outliers.
2. Se possível, escalone as intervenções no tempo entre squads comparáveis — os primeiros a receber viram tratamento, os últimos viram controle temporário. É um experimento sobre a plataforma, e é a demonstração cultural mais forte que a área de experimentação pode dar. **[extrapolação]**
3. Registre a linha de base *antes* da entrevista, com pelo menos um trimestre de histórico.

### 4.4 Taxonomia de causas para o roteiro

Suas três hipóteses (conhecimento insuficiente, escopo grande demais, ausência de pressão) são boas, mas os capítulos sugerem mais cinco candidatas de peso, e o roteiro deveria conseguir distingui-las:

| # | Causa candidata | Sintoma no painel | Fonte |
|---|-----------------|-------------------|-------|
| C1 | Conhecimento/confiança de desenho | S1 longo; muitas revisões de desenho | cap. 15 (necessidade de princípios de ramp) |
| C2 | Escopo/tese grande demais | S3 longo; efeito declarado impreciso | §2 |
| C3 | Falta de pressão / ownership difuso | S7→S8 longo; experimentos "esquecidos" no ar | cap. 16 (assinatura de métricas, aprovação) |
| C4 | **Instrumentação ausente ou quebrada** | S2 longo; retrabalho após início | cap. 13 |
| C5 | **Ciclo de release / client-side** | S4 e S5 longos, concentrados em squads de app | cap. 12 |
| C6 | **Desenho underpowered** | S6 muito acima de 7 dias; extensões sucessivas | cap. 15, §2 |
| C7 | **Latência de análise / falta de confiança no scorecard** | S7 longo; pedidos de análise ad hoc | cap. 16 |
| C8 | **Ausência de regra de decisão pré-registrada** | S8 longo; discussão sobre o que o resultado significa | cap. 16 (visualização para decisores) |

C4, C6 e C7 são as três que mais provavelmente estão escondidas dentro do que hoje se lê como "cultura", e as três são **corrigíveis por feature**. Vale entrar na entrevista já com perguntas desenhadas para separá-las (roteiro na §8).

### 4.5 Ações reativas de retorno imediato

Independentemente do que as entrevistas revelarem, três coisas podem ser feitas no primeiro mês:

- **Auditoria dos experimentos hoje no ar.** Quantos passaram de 7 dias em MPR? Quantos estão em alocação assimétrica sem justificativa? Quantos nunca tiveram scorecard aberto? Quantos falharam SRM e continuam rodando? Cada um desses é lead-time queimando agora.
- **Limpeza pós-ramp.** O cap. 15 alerta para o passivo dos experimentos concluídos e nunca encerrados: código morto em caminhos de variante que "can be disastrous when a dead code path that is not being maintained for a while is accidentally executed". Um relatório de experimentos em 100% sem cleanup é fácil de gerar e reduz risco operacional.
- **Sessão de leitura assistida de scorecard** com os 2–3 squads outliers, feita por alguém da plataforma. Ela serve simultaneamente como intervenção (destrava decisões paradas) e como pesquisa de usuário para as features de interpretação da §5.6.

---

## 5. Grupo II — Estratégias estruturantes (mudar o piso, não o teto)

Organizadas pelo estágio do funil que atacam.

### 5.1 Gate de hipótese e escopo (ataca S1, C1, C2, C6, C8)

Você já tinha essa ideia; os capítulos ajudam a dar-lhe forma e, principalmente, a decidir **onde travar e onde apenas avisar**.

O que o gate deve exigir antes de permitir o start:

1. **Hipótese com efeito declarado.** Não "acreditamos que melhora o engajamento", e sim "esperamos +X% em [métrica primária]". Sem um efeito declarado não existe cálculo de amostra, e sem cálculo de amostra não existe previsão de lead-time. Esta é a informação que destrava tudo o mais.
2. **Métrica primária escolhida de um catálogo, não digitada em texto livre.** O cap. 16 é categórico: "have a way to define common metrics and definitions so that everyone shares a standard vocabulary... and you can discuss the interesting product questions rather than re-litigating definitions".
3. **Guard-rails obrigatórios pré-selecionados por tipo de experimento.** O usuário não deve *escolher* seus guard-rails do zero — a plataforma propõe o conjunto padrão e ele justifica remoções. O cap. 12 dá a lista mínima para app (crash rate, tamanho do app, bateria, CPU/latência, consumo de banda, desativação de notificações) e o cap. 16 dá a taxonomia de agrupamento (qualidade de dados / OEC / guard-rail / diagnóstico local).
4. **Previsão de duração calculada pela plataforma**, com as saídas descritas em §2.2. Este é o coração do gate.
5. **Regra de decisão pré-registrada.** "Se a métrica primária subir mais que X com significância, lançamos; se cair mais que Y, matamos; caso contrário, iteramos." Pré-registrar a regra é o que impede S8 de virar uma negociação de duas semanas — e é também a defesa contra o *peeking* que a pressão por velocidade vai inevitavelmente incentivar.
6. **Unidade de randomização escolhida com validação automática** (ver §5.3).

**Sobre travar o usuário:** trave em (1), (2) e (6), porque são condições de *validade* — sem elas o experimento não é analisável e o tempo gasto é perdido de qualquer forma. Em (4), não trave: **mostre a consequência**. Um aviso do tipo "com este desenho, previsão de 26 dias — acima da meta de 15" com as opções de correção ao lado é mais eficaz e menos ressentido do que um bloqueio, e preserva o caso legítimo do experimento longo consciente. A regra prática: **travar o que é inválido, tornar visível o que é caro.**

**Sobre o "detector de má hipótese":** comece por heurísticas verificáveis, não por julgamento subjetivo — hipótese sem efeito declarado, sem métrica do catálogo, com mais de N mudanças simultâneas na mesma variante, com métrica primária que não pode ser computada na unidade de randomização escolhida (§5.3), com duração prevista acima da meta. São todas checáveis por código e todas explicáveis ao usuário. Julgamento sobre qualidade de tese é revisão humana, e cabe melhor num rito leve de peer review do que num validador.

### 5.2 Instrumentação como pré-requisito, não como etapa (ataca S2, C4)

Este é o capítulo 13 e é, na minha leitura, **a fonte de retrabalho mais subestimada no seu contexto** — porque ela não aparece como atraso, aparece como "o experimento precisou ser refeito".

O livro diagnostica a causa raiz com precisão: o problema é uma **dissociação funcional** — "a time lag (time from when the code is written to when the results are examined), as well as a functional difference (i.e., the engineer creating the feature is often not the one analyzing the logs)". Quem instrumenta não é quem sofre a consequência de instrumentar mal, e sofre semanas depois. É estrutural, não é desleixo.

As três recomendações do livro, traduzidas em features:

- **"Nothing ships without instrumentation."** No RAVelocity: o gate de start verifica que os eventos exigidos pela métrica primária e pelos guard-rails **existem e estão chegando** — não que alguém marcou uma caixinha. Uma checagem automática de "este evento recebeu volume não-nulo nas últimas 24h, nas dimensões que o experimento vai usar" é barata e mata C4.
- **"Invest in testing instrumentation during development."** Um modo de validação que o squad roda antes de subir, com feedback imediato sobre os eventos que a análise vai precisar.
- **"Monitor the raw logs for quality"** — contagens por dimensão-chave, invariantes (timestamps dentro de faixa esperada), detecção de outliers. Com correção tratada como bug de produção: "ensure that broken instrumentation has the same priority as a broken feature".

Dois detalhes técnicos do capítulo que valem virar requisito de plataforma:
- **Chave de join comum a todos os logs**, na granularidade da unidade de randomização, mais chaves por evento quando for preciso casar um evento client-side com o server-side que o explica.
- **Nunca subtrair timestamp de cliente e de servidor** — "they could be significantly off even after adjusting for time zones", porque o relógio do cliente pode ser alterado. Se alguma métrica de duração do RAVelocity faz isso hoje, é um bug silencioso de confiabilidade.

### 5.3 Unidade de randomização como botão de poder — com trava de validade (ataca S6, C6)

O cap. 14 é o mais diretamente "acionável como feature" dos cinco, porque descreve uma decisão que hoje quase certamente está implícita no RAVelocity e que tem efeito de primeira ordem sobre duração.

**O trade-off:** granularidade mais fina (página, sessão) cria mais unidades → menor variância da média → mais poder → **experimento mais curto**. Mas o livro impõe três restrições duras:

1. **Consistência da experiência.** "The more the user will notice the Treatment, the more important it is to use a coarser granularity." Uma feature que aparece e some entre páginas é uma experiência ruim e contamina as métricas.
2. **Independência.** Se há personalização ou dependência entre páginas, randomizar por página é inválido — o exemplo do livro é direto: primeira query no Tratamento com resultado ruim leva o usuário a reformular, e a segunda query cai no Controle.
3. **Compatibilidade entre unidade de randomização e unidade de análise.** A regra: **a unidade de randomização deve ser igual ou mais grossa que a unidade de análise.** Randomizar por página e reportar "sessões por usuário" não é apenas impreciso — não é interpretável: "you cannot use user-level metrics to evaluate an experiment when the randomization is by page. If these metrics are part of your OEC, then you cannot use the finer levels of granularity for randomization."

**A feature que isso sugere:** um seletor de unidade de randomização que, ao ser combinado com a métrica primária escolhida no catálogo, **bloqueia combinações inválidas e mostra o ganho de duração das combinações válidas.** É uma trava de validade (portanto, travar de verdade — §5.1) que ao mesmo tempo entrega velocidade. Difícil pensar num item com melhor relação entre esforço e impacto na meta.

Complementos do capítulo que vale internalizar:
- Randomização por usuário permanece o padrão (consistência + medição de retenção). Escolha do identificador — logado, cookie/pseudônimo, device ID — tem consequência de escopo (cross-device) e de estabilidade longitudinal.
- Randomização mais grossa que a análise (usuário randomizado, métrica por página) **funciona**, mas exige delta method ou bootstrap para a variância, e fica exposta a bots com um único ID e 10.000 pageviews. Mitigação: limitar a contribuição individual ou usar a versão por usuário da métrica. Se o RAVelocity calcula CTR por página sob randomização por usuário com fórmula de variância ingênua, **os p-values estão errados** — e isso é um achado de trustworthiness com prioridade acima da meta de lead-time.
- IP como unidade: só quando não houver alternativa (mudanças de infraestrutura). Granularidade instável e baixo poder.

### 5.4 Ramp padronizado SQR como *template* do produto (ataca S4, S5, C1, C3)

O cap. 15 entrega o framework pronto; o trabalho de produto é transformá-lo em **caminho padrão com poucos cliques**, em vez de decisão livre a cada experimento. As quatro fases:

| Fase | Objetivo primário | Trade-off | Duração de referência |
|------|-------------------|-----------|------------------------|
| 1. Pré-MPR | Mitigar risco | velocidade × risco | horas a poucos dias |
| 2. MPR (ex.: 50/50) | Medir com precisão | velocidade × qualidade | **~1 semana** |
| 3. Pós-MPR | Operacional (carga) | — | ≤ 1 dia, opcional |
| 4. Holdout longo | Aprender efeito de longo prazo | — | opcional, **não default** |

Da fase 1, três mecanismos concretos:
- **Anéis de exposição**: whitelist do time → funcionários → beta users/insiders → data center isolado (Bing usa 0,5–2% em um único DC para pegar vazamento de memória e uso indevido de recurso). O livro avisa que medições dos primeiros anéis são enviesadas ("those users are likely the insiders") — servem para bug, não para decisão.
- **Dial automático de tráfego** até a alocação-alvo. É a diferença entre "o squad lembra de subir o tráfego na segunda-feira" e "o sistema sobe sozinho às 3h". Elimina uma fatia inteira de S5, que é puro tempo de espera humana.
- **Guard-rails em tempo real ou quase-real**: "the sooner you can get a read on whether an experiment is risky, the faster you can decide to go to the next ramp phase". Velocidade e segurança aqui não são opostos — a medição rápida é o que *autoriza* ir rápido.

Da fase 4, um alerta importante para quem está com pressa: **holdout longo não deve ser passo padrão.** O livro é firme, inclusive eticamente: "it could be unethical when we know there is a superior experience but deliberately delay the delivery". Use só nos três casos listados (suspeita de novidade/primazia, efeito de curto prazo grande demais para ser assumido sustentável, ou indicador antecedente com true-north de longo prazo). E, quando o efeito de curto prazo já é pequeno, mantenha o holdout em MPR em vez de 90/10 — "the statistical sensitivity gained by running longer is usually not enough to offset the sensitivity loss by going from MPR to 90%".

**O holdout global merece consideração à parte, e é um bom argumento para o diretor.** O livro descreve empresas que mantêm uma fatia de tráfego fora de *qualquer* lançamento por um trimestre, para medir o impacto cumulativo (o Bing usa 10%). Numa cultura que vai passar a rodar muitos experimentos pequenos e incrementais, **essa é a única forma de responder à pergunta "a soma dos ganhos declarados corresponde ao ganho real?"** — pergunta que um diretor faz cedo ou tarde, e que é constrangedora sem instrumento. Custo baixo, valor institucional alto.

E, para experimentos de resultado surpreendente, o livro recomenda **replicação** com outra amostra ou re-randomização ortogonal, lembrando que "when there have been many iterations of an experiment, the results from the final iteration may be biased upwards" — relevante justamente numa cultura de iteração incremental rápida.

### 5.5 Client-side: parametrizar para descolar do ciclo de release (ataca S3, S4, C5)

Se parte relevante do portfólio é app, este é o maior lever estrutural disponível, porque ataca um piso e não uma média.

- **Feature flags e dark features**: features incompletas sobem desligadas e são ativadas depois, sem novo release.
- **Configurabilidade server-side de features do cliente**: além de permitir A/B test, funciona como rede de segurança — "if a feature does not perform well, we can instantly revert by shutting down the feature... without having to go through a lengthy client release cycle".
- **Parametrização fina** é o ponto mais forte: "even though new code cannot be pushed to the client easily, new configurations can be passed, which effectively creates a new variant if the client understands how to parse the configurations". O exemplo do Windows 10 (texto da caixa de busca parametrizado, experimentos rodados mais de um ano após o envio, variante vencedora com ganho de milhões em engajamento e receita) é a melhor ilustração de que **antecipar o que será parametrizado é o que separa um ciclo de experimentação de semanas de um de meses.**

Isso sugere uma feature de plataforma mais ambiciosa e provavelmente de alto valor **[extrapolação]**: um **inventário de parâmetros experimentáveis por superfície** — o que já está parametrizado hoje e, portanto, pode virar experimento *sem release*. Um squad que consulta esse inventário no momento de formular a hipótese pode escolher, entre duas hipóteses de valor semelhante, aquela que não depende de release. Isso é redução de lead-time em S1, na origem, e é o tipo de coisa que só a plataforma pode oferecer.

Dois cuidados do capítulo que precisam existir na plataforma: **failsafe** (cachear a atribuição para o caso de o device estar offline; variante default quando o servidor não responde; ID de randomização estável antes e depois do login) e **tracking de atribuição no uso, não no fetch** — como as atribuições costumam ser buscadas todas de uma vez na abertura do app, usar o fetch como sinal de trigger causa **over-triggering** e destrói o ganho de sensibilidade da análise triggered.

### 5.6 Leitura do resultado: da latência à interpretação (ataca S7, S8, C7, C8)

Duas coisas diferentes moram aqui, e vale não confundi-las.

**(a) Latência do scorecard** — "any delay in experiment scorecard generation can add delay to decision making, which can be costly as experimentation becomes more common". A arquitetura recomendada é de dois caminhos:
- **NRT (near-real-time)**: métricas simples (somas e contagens), sem filtro de spam, mínimo de testes estatísticos, operando quase direto no log cru. Serve para monitorar problemas graves — experimento mal configurado ou com bug — e **disparar alerta e desligamento automático**.
- **Batch**: o caminho confiável, com o processamento completo (sort/join, limpeza, enriquecimento) para decisão.

A limpeza tem uma armadilha que vale explicitar no produto: "some filtering may unintentionally remove more events from one variant than another, potentially causing a sample ratio mismatch (SRM)". O filtro anti-bot pode *criar* o problema que ele parece detectar.

**(b) Interpretação** — sua ideia de comunicar inferência visualmente está exatamente alinhada ao cap. 16, que quer o scorecard acessível "to people with various technical backgrounds, from Marketers to Data Scientists and Engineers to Product Managers", inclusive escondendo métricas de debug do público menos técnico. As diretrizes concretas:

- **Testes de confiança em destaque, com poder de veto.** "Microsoft's experimentation platform (ExP) hides the scorecard if key tests fail" — no caso do SRM, esconder é mais correto do que exibir com um aviso, porque um número inválido lido por um decisor não volta atrás.
- **Mudança relativa, significância explícita, código de cor e filtros.**
- **Taxonomia de métricas** (qualidade de dados / OEC / guard-rail / diagnóstico local, ou os três tiers do LinkedIn: companywide / produto / feature), com navegação por grupo.
- **Múltiplos testes**: com muitas métricas, movimentos "irrelevantes" significantes viram a pergunta recorrente dos experimentadores. Solução simples e eficaz do livro: limiar de p-value mais rigoroso que 0,05 para filtrar rapidamente; formalmente, Benjamini-Hochberg **[cap. 17, fora do excerto]**.
- **Métricas relacionadas** — "when CTR is up, is it because clicks are up or because page views are down? The reason for the movement may lead to different launch decisions". Modelar relações entre métricas no catálogo permite que a plataforma *explique* um movimento em vez de só reportá-lo. É a forma mais direta de atacar C1/C8 sem exigir que o PM aprenda variância.
- **Drill-down por segmento**, com destaque automático dos segmentos interessantes.

**Sobre "comunicar inferência de forma visual":** o objetivo certo não é ensinar intervalo de confiança — é fazer o decisor tomar a decisão correta. Duas heurísticas de desenho que decorrem do capítulo **[extrapolação]**: mostrar o **intervalo contra a região de indiferença** (o efeito mínimo que importa para o negócio, declarado no gate da §5.1) em vez de contra zero, porque "não significante" e "significantemente irrelevante" são decisões diferentes; e traduzir o resultado em **linguagem de decisão pré-registrada** ("o critério que você registrou foi +2%; o intervalo observado é [+0,3%, +1,1%] — abaixo do seu critério"), o que fecha o loop com a regra de decisão e reduz S8 a minutos.

### 5.7 Awareness, ownership e prazos (ataca S8, C3)

Sua ideia do MCP com Google Chat tem respaldo direto — o cap. 16 lista, entre as features que "cultivam um processo de decisão saudável":

1. **Assinatura de métricas com digest**: "allow individuals to subscribe to metrics they care about and get an email digest with the top experiments impacting these metrics."
2. **Processo de aprovação acionado por impacto negativo**: "if an experiment has a negative impact, the platform can initiate an approval process, where it forces the experiment owner to start a conversation with the metrics owners before the experiment can be ramped up. Not only does this drive transparency regarding experiment launch decisions, it encourages discussion, which increases the overall knowledge of experimentation in the company."

Repare no que esse segundo mecanismo faz pelo seu objetivo: ele **fabrica ownership** ligando o dono do experimento ao dono da métrica no momento exato em que a conversa importa, e o efeito colateral declarado é aumento de conhecimento de experimentação na empresa — que é exatamente o C1 que você quer atacar. E o *dono da métrica* passa a ser um segundo par de olhos com incentivo próprio para não deixar o experimento parado.

**Desenho recomendado das notificações** para não virar ruído **[extrapolação]**:
- Notifique **eventos e decisões pendentes**, não passagem de tempo. "Seu experimento atingiu a janela de medição e o scorecard está pronto — decisão pendente há 2 dias" é acionável; "seu experimento está no ar há 10 dias" não é.
- Cada notificação carrega **a ação e o link direto** para executá-la (encerrar, promover, estender com justificativa).
- **Escalonamento explícito e previsível**: dono → dono + líder do squad → painel de portfólio. Sem escalonamento a notificação vira ignorável; com escalonamento surpresa, vira política.
- **Alertas de risco (NRT) são de outra classe** e merecem canal separado, com desligamento automático conforme o cap. 16.
- **Meça o próprio mecanismo**: taxa de ação por notificação enviada. Se cair, é ruído — e ruído em canal de risco custa caro.

### 5.8 Memória institucional (ataca S1, C1)

O cap. 16 registra que a ferramenta de visualização "can also be a gateway to accessing institutional memory" **[cap. 8, fora do excerto]**. No seu contexto isso é uma alavanca de lead-time no estágio mais caro de comprimir, o S1: um squad que consegue buscar "o que já testamos nesta superfície, com que efeito, e o que aprendemos" formula mais rápido e formula melhor. E é o antídoto mais barato para C1 — conhecimento insuficiente se resolve mais por acesso a precedente do que por treinamento.

Requisito mínimo: todo experimento concluído tem hipótese, desenho, resultado e **decisão tomada** persistidos e buscáveis, incluindo os negativos — que são os mais informativos e os que ninguém documenta.

---

## 6. Anti-padrões: as sete maneiras de bater a meta e piorar a empresa

Esta seção é curta de propósito, e deve estar na apresentação. Uma meta de velocidade sem guard-rails é um convite a otimizações locais que destroem confiabilidade — e "trustworthy" é a primeira palavra do título do livro por um motivo.

1. **Encurtar o MPR para menos de uma semana.** Viés de dia da semana e de heavy users. O livro é explícito.
2. **Espiar e parar quando dá significância** (*peeking*). Infla drasticamente o falso positivo. A defesa é a regra de decisão pré-registrada (§5.1) e, se houver apetite, testes sequenciais **[cap. 17, fora do excerto]**.
3. **Randomizar mais fino para acelerar, ignorando SUTVA e a compatibilidade com a unidade de análise.** Ganha-se poder e perde-se validade — e a perda é invisível no scorecard. Por isso a trava do §5.3 é trava, não aviso.
4. **Declarar vitória em métrica secundária** depois de ver os resultados. Com dezenas de métricas, sempre haverá uma verde. Defesa: métrica primária pré-registrada + tratamento de múltiplos testes.
5. **Iniciar o relógio tarde.** Se o lead-time é medido a partir do registro da hipótese no RAVelocity, a resposta racional a uma meta apertada é registrar a hipótese depois de já tê-la trabalhado por duas semanas. Defesa: medir também o volume de experimentos e o tempo desde a *primeira* aparição da ideia em qualquer artefato; e, sobretudo, não usar a métrica para avaliar pessoas.
6. **Transformar gates em fila.** Se o gate exigir aprovação humana centralizada, ele desloca a espera de S3 para S1 e o lead-time não melhora — piora, porque agora tem fila e ressentimento. Gates devem ser **automáticos e instantâneos**; revisão humana só no caso excepcional.
7. **Confundir "mais experimentos" com "mais aprendizado".** Cinquenta experimentos underpowered ensinam menos que dez bem desenhados. O contrapeso está no OEC do programa (§7): número de experimentos **conclusivos**, não número de experimentos.

---

## 7. O OEC do próprio programa

Trate a iniciativa como um experimento: ela tem uma métrica primária, guard-rails e uma regra de decisão.

**Métrica primária**
- Lead-time hipótese → decisão, reportado como **p50 e p75** (não média — a média esconde a cauda que é justamente o problema), segmentado por plataforma (server/web/app) e por tipo de experimento.

**Métricas de diagnóstico (as que dizem *onde* melhorou)**
- Tempo por estágio S1–S8, mesma estatística.
- % de experimentos com duração prevista ≤ 15 dias **no momento do desenho** — indicador antecedente, mexe antes da métrica primária e é o melhor sinal de que os gates estão funcionando.

**Guard-rails (nenhum ganho de lead-time vale degradá-los)**
- % de experimentos **conclusivos** (atingiram o poder declarado antes de encerrar) — sobe ou fica estável.
- % de experimentos com SRM ou falha em teste de confiança — não sobe.
- % de experimentos encerrados antes de 7 dias em MPR — não sobe.
- % de experimentos com métrica primária alterada após o início — não sobe (detector de #4 acima).
- % de experimentos com instrumentação incompleta detectada após o início — cai (efeito direto do §5.2).
- Qualidade da decisão: % de lançamentos que sobrevivem à verificação do holdout global (§5.4), se ele existir.

**Métrica de volume**
- Experimentos conclusivos por squad por trimestre. É a métrica que traduz a tese de negócio ("a empresa aprende mais") e a única defesa contra o anti-padrão #7.

---

## 8. Roteiro de entrevista (Grupo I)

Estrutura sugerida: 45 minutos, com o painel de estágios do squad aberto na tela. Entrar com dado, sair com hipótese classificada em C1–C8.

**Abertura — ancorar no caso concreto (10 min)**
1. Vamos pegar o seu último experimento concluído. Me conta a linha do tempo dele, do momento em que a ideia apareceu até a decisão.
2. Em que ponto dessa linha você sentiu que estava esperando por algo?

**Formulação e escopo — C1, C2 (10 min)**
3. Quando vocês formularam a hipótese, vocês tinham um número em mente para o efeito esperado? De onde veio esse número?
4. Como vocês decidiram o tamanho do recorte? O que foi deixado de fora e por quê?
5. Vocês procuraram experimentos anteriores sobre essa superfície? Onde procuraram? Acharam? *(sonda de C1 e §5.8)*

**Instrumentação — C4 (5 min)**
6. Os eventos de que vocês precisavam já existiam? Como vocês descobriram que existiam (ou que não existiam)?
7. Alguma vez vocês precisaram refazer ou estender um experimento por causa de dado faltando ou errado?

**Execução e ramp — C5, C6 (10 min)**
8. Como vocês decidiram a alocação de tráfego? Ela mudou ao longo do experimento? Quem mudou?
9. O experimento rodou pelo tempo que vocês planejaram? Se estendeu, por quê?
10. Alguma parte do que vocês queriam testar dependia de um release de app? *(sonda de C5)*

**Leitura e decisão — C3, C7, C8 (10 min)**
11. Quando o resultado saiu, quanto tempo levou até a decisão? O que aconteceu nesse intervalo?
12. Ao abrir o scorecard, qual foi a primeira coisa que você olhou? Teve alguma coisa que você não soube interpretar?
13. Vocês pediram alguma análise adicional fora da plataforma? Qual e por quê? *(sonda forte de C7)*
14. Antes de começar, vocês tinham combinado o que fariam com cada resultado possível? *(sonda de C8)*
15. Se o experimento tivesse ficado parado sem decisão por duas semanas, alguém teria notado? Quem? *(sonda de C3)*

**Fechamento**
16. Se você pudesse mudar uma coisa na plataforma para o próximo experimento sair mais rápido, qual seria?

Registre cada resposta já classificada em C1–C8 — é isso que permite agregar entre squads e priorizar o Grupo II por evidência, e não por intuição.

---

## 9. Checklist de cruzamento com a estrutura atual do RAVelocity

Esta é a seção operacional: as perguntas a fazer ao repositório/arquitetura na próxima etapa. Para cada linha, o resultado esperado é **existe / existe parcialmente / não existe**, e daí sai a TO-DO list.

### 9.1 Modelo de dados e ciclo de vida

- [ ] Existe uma entidade `Experimento` com **máquina de estados** explícita? Quais estados?
- [ ] Existem timestamps por transição de estado suficientes para reconstruir S1–S8? Quais faltam?
- [ ] Existe a entidade `Hipótese` separada do experimento, com efeito esperado, métrica primária e escopo?
- [ ] Existe campo de **decisão** (launch/kill/iterate) preenchido no encerramento? É obrigatório?
- [ ] O **início efetivo** (primeira exposição real) é registrado além do início nominal? *(§4.2)*
- [ ] Existe registro de **alterações de configuração durante o experimento** (mudança de alocação, de métrica, extensão de prazo)? *(insumo dos guard-rails da §7)*

### 9.2 Desenho e gates

- [ ] Existe catálogo central de métricas com definição única, ou métricas são texto livre? *(cap. 16)*
- [ ] Existe cálculo de amostra mínima / duração prevista? Ele é exibido antes do start?
- [ ] Existe seleção de unidade de randomização? É explícita ou implícita no código?
- [ ] Existe validação de compatibilidade entre unidade de randomização e unidade de análise da métrica primária? *(§5.3 — trava)*
- [ ] Existem guard-rails obrigatórios por tipo de experimento? Existe o conjunto de guard-rails de app do cap. 12?
- [ ] Existe regra de decisão pré-registrada?
- [ ] O gate é automático e instantâneo, ou envolve aprovação humana? *(anti-padrão #6)*

### 9.3 Instrumentação

- [ ] Existe verificação automática de que os eventos exigidos estão chegando, antes do start? *(§5.2)*
- [ ] Existe chave de join comum na granularidade da unidade de randomização?
- [ ] Existe monitoramento de qualidade de log cru (contagens por dimensão, invariantes, outliers)?
- [ ] Existe algum cálculo que subtrai timestamp de cliente e de servidor? *(bug latente — cap. 13)*

### 9.4 Ramp e exposição

- [ ] Existem templates de ramp, ou cada experimento configura tráfego livremente?
- [ ] Existe **dial automático** de tráfego? *(§5.4 — corte direto em S5)*
- [ ] Existem anéis de exposição (whitelist / funcionários / beta / data center)?
- [ ] A alocação padrão sugerida é MPR (50/50)? Qual é a distribuição real de alocações hoje? *(§2.1 — auditoria de retorno imediato)*
- [ ] Existe desligamento automático por guard-rail em NRT?
- [ ] Existe relatório de experimentos em 100% sem cleanup de código morto? *(§4.5)*
- [ ] Existe suporte a holdout longo? Ele é default? *(deveria não ser — §5.4)*
- [ ] Existe holdout global de portfólio? *(§5.4)*

### 9.5 Análise e scorecard

- [ ] Qual é a latência real do scorecard (fim da janela → número disponível)? Existe caminho NRT separado do batch?
- [ ] Existe teste de SRM? Ele **esconde** o scorecard quando falha, ou apenas avisa?
- [ ] Existe análise triggered? Ela reporta também o impacto overall? *(§2.1 — maior multiplicador de sensibilidade)*
- [ ] Como a variância é calculada quando a unidade de análise é mais fina que a de randomização? Delta method / bootstrap / fórmula ingênua? *(§5.3 — risco de p-value incorreto)*
- [ ] Existe limitação da contribuição individual (bots / outliers)?
- [ ] Existe taxonomia/agrupamento de métricas no scorecard?
- [ ] Existe tratamento de múltiplos testes (limiar mais rigoroso ou BH)?
- [ ] Existe modelagem de métricas relacionadas? *(§5.6)*
- [ ] Existe drill-down por segmento?
- [ ] Existe versão de baixa variância das métricas de alta variância (ex.: receita trimada)?
- [ ] Existe redução de variância tipo CUPED? *(spike técnico — §2.1)*

### 9.6 Notificação, ownership e memória

- [ ] Existe conceito de **dono de métrica**, distinto de dono de experimento? *(pré-requisito do fluxo de aprovação — §5.7)*
- [ ] Existe assinatura de métricas com digest?
- [ ] Existe fluxo de aprovação disparado por impacto negativo em métrica de terceiros?
- [ ] Existe canal de notificação ativo (o MCP do Google Chat entra aqui) e ele é orientado a *ação pendente*?
- [ ] Existe busca sobre experimentos passados com hipótese, resultado e decisão? Inclui os negativos?

### 9.7 Client-side

- [ ] Que fração do portfólio é client-side? Ela tem lead-time estruturalmente maior? *(§4.2 — pode exigir meta segmentada)*
- [ ] Existe inventário de parâmetros já experimentáveis sem release? *(§5.5 — alta alavancagem)*
- [ ] O tracking de atribuição é enviado no **uso** ou no **fetch**? *(§5.5 — risco de over-triggering)*
- [ ] Existe failsafe offline (cache de atribuição, variante default, ID estável antes/depois do login)?

### 9.8 Formato sugerido para a TO-DO list final

| Item | Estágio atacado (S) | Causa atacada (C) | Evidência (cap.) | Existe hoje? | Esforço | Dependências | Impacto esperado em lead-time |
|---|---|---|---|---|---|---|---|

Sugestão de leitura da priorização quando a tabela estiver preenchida: **primeiro o que é pré-requisito de medição** (timestamps por estágio, início efetivo), **depois as travas de validade que também dão velocidade** (compatibilidade randomização×análise, verificação de instrumentação, alocação MPR default), **depois os multiplicadores de sensibilidade** (triggering, métricas de baixa variância, CUPED), **depois a camada de decisão** (scorecard, notificação, aprovação por dono de métrica), e por último os itens de fundo cultural (memória institucional, inventário de parâmetros) — que rendem menos no trimestre e mais no ano.

---

## 10. Resumo em cinco frases (para o slide)

1. O núcleo irredutível de um bom experimento é de 9 a 11 dias; a meta de 15 dias é atingível, mas só atacando o que está **fora** da janela de medição.
2. Reduzir escopo, sozinho, **aumenta** o lead-time — efeitos menores exigem mais amostra; a plataforma precisa devolver sensibilidade via triggering, alocação em MPR, unidade de randomização e métricas de menor variância.
3. A maior fonte oculta de atraso é retrabalho por instrumentação: "nada sobe sem instrumentação" é uma feature de gate, não um valor de parede.
4. Ramp padronizado com dial automático e guard-rails em tempo quase-real é o que permite ir rápido **com** segurança — velocidade e risco não são opostos quando a medição é rápida.
5. Ownership se fabrica ligando dono de experimento a dono de métrica no momento da decisão; a meta precisa dos seus próprios guard-rails, ou será batida às custas da confiabilidade.

---

### Fontes

Kohavi, R., Tang, D., & Xu, Y. *Trustworthy Online Controlled Experiments: A Practical Guide to A/B Testing*, Part IV — cap. 12 (Client-Side Experiments), 13 (Instrumentation), 14 (Choosing a Randomization Unit), 15 (Ramping Experiment Exposure: Trading Off Speed, Quality, and Risk), 16 (Scaling Experiment Analyses).

Leituras complementares recomendadas antes de fechar o roadmap: cap. 17 (múltiplos testes e stopping rules), cap. 20 (análise triggered), cap. 22 (redução de variância e interferência), cap. 3 (SRM e SUTVA), cap. 8 (memória institucional).
