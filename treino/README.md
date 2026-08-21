# JF Treino

App de acompanhamento entre o treinador **João Filho** e seus alunos. O aluno
registra como a semana foi, o João prescreve o treino, e os dois veem a mesma
evolução. O plano completo está em [`PLANO.md`](PLANO.md); para publicar, veja
[`DEPLOY.md`](DEPLOY.md).

**Fases 0 a 4 estão prontas, a 2 fechou com o modo academia, a 3 fechou de
verdade (a carga sugerida agora sai do que o aluno levantou), e a 5 ganhou o
painel de alertas do João.** O aluno faz o check-in semanal e os dois veem a
evolução em gráfico; o João monta a periodização com a progressão de carga série
a série, usa a calculadora para escolher a carga e monta o protocolo alimentar
com os grupos de substituição — que o aluno abre no celular e marca refeição a
refeição.

---

## Rodar

Com Docker, um comando:

```bash
cd treino
docker compose run --rm app jf demonstracao   # opcional: banco com um treino dentro
docker compose up --build                     # http://localhost:8770
```

Sem Docker, também um comando (precisa de Python 3.11+ e Node 20+):

```bash
cd treino
./comecar.sh          # instala, compila o PWA, monta a demonstração e serve
./comecar.sh --limpo  # apaga o banco e recomeça
```

A demonstração cria duas contas com senha conhecida:

| | |
|---|---|
| treinador | `joao@jftreino.com.br` / `demonstracao-2026` |
| aluno | `filipe@jftreino.com.br` / `demonstracao-2026` |

Dentro dela já existem dez semanas de check-in, dois treinos montados e o
protocolo alimentar completo, para os gráficos, a progressão e a dieta terem o
que mostrar. `jf demonstracao` se recusa a rodar
com `JF_PRODUCAO=1` e num banco que já tenha conta.

Para começar do zero, sem dado de brinquedo:

```bash
jf preparar                                 # tabelas + catálogos
jf treinador "João Filho" joao@exemplo.com  # pede a senha sem eco
jf servir
```

Para mexer no front com recarga automática, deixe `jf servir` rodando numa aba e
`npm run dev` noutra: o Vite sobe em `:5180` e repassa `/api` para o uvicorn.

Sem `JF_CHAVE_SECRETA` o app sorteia uma chave a cada início — serve para
desenvolver, derruba a sessão a cada reinício. Em produção (`JF_PRODUCAO=1`) ela
é obrigatória e o servidor se recusa a subir sem ela.

## Verificar

```bash
cd treino && python3 -m pytest      # 490 testes
cd treino/web && npm run verificar  # tsc
```

Dois arquivos carregam o peso. `testes/teste_forca.py` confere a equação de 1RM
contra os números publicados no paper — é o tipo de erro que não quebra nenhum
teste de rota e sai como carga errada na academia. E `testes/teste_permissoes.py`
existe porque uma rota que esquece de filtrar por dono passa em todo teste feliz
e só falha quando alguém troca o número na URL.

## Como está organizado

```
jf/
  backup.py       cópia do banco, e o agendamento que a faz sozinha
  progresso.py    e1RM ao longo do tempo, a partir das séries executadas
  alertas.py      os sinais que colocam um aluno no topo da lista do João
  validacao.py    traduz o 422 do Pydantic para uma frase que o aluno entenda
  forca.py        a equação de 1RM e o cálculo de carga (puro, sem I/O)
  leitura.py      lê a prescrição escrita à mão (puro, sem I/O)
  dieta_texto.py  lê o protocolo alimentar escrito à mão (puro, sem I/O)
  alimentos.py    importa a TACO / Open Food Facts para o catálogo
  privacidade.py  o termo e a versão dele (o hash do próprio texto)
  diagnostico.py  o `jf doutor` — confere a configuração antes de subir
  migracoes/      Alembic: uma revisão por mudança de esquema
  modelos.py      Usuario, Aluno, Exercicio, Tecnica, Periodizacao,
                  SessaoModelo, Prescricao, SerieDaPrescricao,
                  CheckinSemanal, MedidaCorporal, Consentimento,
                  ProtocoloAlimentar, GrupoDeSubstituicao, Refeicao,
                  Suplemento, AderenciaDaRefeicao, Alimento
  auth.py         senha, sessão e quem-pode-ver-o-quê
  banco.py        engine e sessão do SQLAlchemy
  esquemas.py     o que entra e sai da API (Pydantic)
  api/            sessao · alunos · exercicios · treinos · execucao ·
                  checkins · dieta · privacidade · calculadora
  dados/          catálogos de exercícios e técnicas, semeadura e a
                  demonstração
  servidor.py     a API em /api e o PWA no resto
  cli.py          jf preparar · jf treinador · jf demonstracao ·
                  jf importar-alimentos · jf doutor · jf backup · jf servir
web/
  src/estilo/     tokens da marca (preto, vermelho-sangue, osso)
  src/api/        cliente e tipos, espelhando jf/esquemas.py
  src/api/fila.ts o que ainda não subiu, guardado em IndexedDB
  src/rotas/      Entrar · Alunos · FichaDoAluno · Periodizacao ·
                  Calculadora · Checkin · MeusDados · Inicio · Catalogo ·
                  Dieta · ProtocoloAlimentar · Treinar
  src/componentes/EditorDePrescricao.tsx · EditorDeSeries.tsx ·
                  EditorDeProtocolo.tsx · PainelDeEvolucao.tsx ·
                  PainelDeForca.tsx · CronometroDeDescanso.tsx ·
                  graficos/GraficoDeLinha.tsx
  gerar-icones.py desenha os ícones do PWA a partir do monograma
```

## Catorze decisões que valem saber

**A convenção de carga é dado de primeira classe.** Cada exercício declara se a
carga é registrada como peso total (barra, incluindo a barra), por halter (o peso
de *um* halter, mesmo usando dois) ou como adicional ao peso corporal. Não é
preciosismo: a estimativa de 1RM da fase 3 recebe a carga como número puro, e sem
essa convenção combinada de antemão a conta erra sem dar nenhum sinal. A tela do
catálogo mostra a etiqueta de propósito.

**O 404 em vez do 403.** Pedir um aluno de outro treinador responde 404, não 403 —
um 403 confirmaria que aquele id existe, o que já é informação sobre a base de
alunos de outra pessoa. O corpo é idêntico ao de um id inexistente, e há teste
para isso.

**Técnica tem escopo, e o escopo muda onde ela vive.** *Dead Stop* e *Super Slow*
descrevem como cada repetição é feita, então ficam no exercício. *Cluster set* e
*rest-pause* mudam o que uma série é, então também ficam no exercício — mas
marcadas como distorcendo a estimativa. *Bi-set* e *tri-set* ligam exercícios
diferentes, então vivem no bloco, e a API recusa quem tentar informá-las como
técnica de um exercício só. Sem essa separação não dá para saber, olhando o dado,
se uma prescrição é um bloco ou um exercício solto.

**A série é a unidade, não o exercício.** `12x20kg / 10x30kg / 8x40kg` não cabe
num "3 × 8–12 @ 30 kg": a progressão de carga dentro do exercício é a regra, não
a exceção, e a técnica costuma ser de uma série só — no `10x100kg / 12x100kg
cluster set`, só a segunda é cluster. Por isso `SerieDaPrescricao` guarda reps,
carga e técnicas próprias, e `TipoDeSerie` separa trabalho de preparação:
aquecimento e up set sobem até a carga de trabalho e **não entram na tonelagem**,
porque somá-los inflaria o volume sem o aluno ter treinado mais. Quando todas as
séries são iguais, o resumo da prescrição continua bastando.

**A semana do check-in é sempre a segunda-feira.** O servidor normaliza qualquer
data para a segunda correspondente, e um índice único por `(aluno, semana)`
impede dois check-ins da mesma semana — sem isso, quem responde no domingo e
quem responde na terça cairiam em linhas diferentes do gráfico, e um envio
duplicado viraria um degrau falso. Semana sem resposta **some** da série em vez
de virar zero: quem não pesou não pesa zero, e uma linha caindo até o eixo seria
mentira.

**O painel de alertas é regra explicável, não aprendizado de máquina.** Cinco
sinais — sem check-in, sono baixo, peso subindo em fase de déficit, força caindo
duas vezes seguidas no mesmo exercício, aderência à dieta em queda — cada um
dando para resumir numa frase. Um alerta que ninguém entende por que disparou é
um alerta que se aprende a ignorar, e é por isso que `jf/alertas.py` é função
pura e testável, não um modelo estatístico por cima do histórico.

**A comparação da equação é por valor, não por identidade.** `Periodizacao.
equacao` é uma coluna de texto — `"proposta"`, não `Equacao.PROPOSTA` — e o
código comparava com `is`. A string nunca casava com nenhum ramo e caía calada
no último `if` do arquivo: toda estimativa que passasse pelo banco em vez de
vir direto do enum saía de Brzycki achando que era a equação do paper. Foi um
teste do e1RM que achou isso, comparando o número que o gráfico mostrava com a
conta feita à mão — é o tipo de erro que não quebra teste de rota nenhum e sai
como carga errada na academia.

**Trocar a senha derruba os outros aparelhos.** O cookie de sessão é assinado,
mas o servidor não guarda lista de sessões abertas — então, sozinho, ele não é
revogável, e trocar a senha não expulsaria ninguém. O login carimba o instante
no cookie e `Usuario.senha_alterada_em` guarda a última troca; quem tiver um
carimbo mais velho cai. É o que faz a troca servir para o motivo pelo qual
alguém troca a senha: tirar de dentro quem sabia a antiga.

**A versão do termo de consentimento é o hash do próprio texto.** Editar o
termo muda a versão sozinho, o consentimento anterior deixa de valer, e o app
volta a perguntar — que é o que a LGPD pede, já que o consentimento é específico
para uma finalidade (art. 8º §4º). Um número que alguém precisa lembrar de
incrementar acabaria esquecido, e consentimentos antigos passariam a valer para
um texto que ninguém leu.

**Sincronizar não pode duplicar nem apagar.** Subsolo de academia não tem sinal,
então o celular grava a série primeiro em IndexedDB e só depois envia — a tela
nunca espera a rede para confirmar. Cada série carrega uma chave gerada no
aparelho, e a rota é um *upsert* por essa chave: mandar a mesma fila dez vezes dá
o mesmo resultado que mandar uma. E a ausência de uma série no envio **nunca**
vale como remoção — um aparelho que ficou offline no meio do treino tem visão
parcial e apagaria o que foi registrado de outro lugar. A tela conta a fila junto
com o que o servidor confirmou, mas com marca diferente: prometer "enviado"
quando não foi é como se perde a confiança no app.

**O histórico executado sobrevive ao treino que o gerou.** `SessaoRealizada`
guarda o nome copiado e aponta para o modelo com `SET NULL`, não `CASCADE`: o
João reorganiza a periodização, apaga um bloco de março, e a carga que o aluno
levantou em março continua sendo verdade. É o dado mais difícil de recriar do
app — ninguém lembra quanto puxou numa terça qualquer.

**A substituição é o protocolo, não um enfeite dele.** O João não escreve "coma
200 g de arroz", escreve "coma um carboidrato — e arroz 200 g, cuscuz 225 g e pão
francês 2 unidades valem o mesmo". As quantidades diferem *de propósito*: é o que
torna a troca justa. Guardar o protocolo como texto, ou guardar só o nome do
alimento, jogaria fora exatamente a conta que ele fez. Por isso cada grupo é uma
tabela, cada item guarda a sua porção, e o item da refeição aponta para o grupo a
que pertence — é isso que faz o botão **Trocar** existir na tela do aluno.

**O catálogo nutricional nasce vazio, e continua vazio até alguém importar.**
Nenhum kcal ou macro vem embutido no repositório. `jf importar-alimentos` lê a
TACO ou o Open Food Facts em CSV e casa as colunas por apelido, porque as versões
que circulam não combinam nos cabeçalhos; `Tr` e `NA` viram `None`, não zero —
zero é uma afirmação, "não medido" não é. Chutar macro num app que alguém usa
para cortar peso é dano, não aproximação. **Nada do protocolo depende dessa
tabela**: as equivalências são do João, e a dieta funciona inteira sem ela.

**A equação proposta tem um piso que o paper não menciona.** O guard `k(w) ≥ 0,5`
publicado impede a divisão por zero, mas abaixo de ~4,74 kg a equação *inverte de
sentido*: 2 kg por 8 repetições estima 18,7 kg de 1RM e 3 kg pelas mesmas 8
estima 9,3 kg. Como cargas assim existem — elevação lateral com halter de 3 kg —,
o app cai para Epley nesse trecho e diz que caiu. Ver `CARGA_MINIMA_PROPOSTA` em
`jf/forca.py`, com a derivada que justifica o valor.

## O que fica em aberto

- **Não há "esqueci minha senha" automático.** O app não manda email, e mandar
  link de redefinição sem provedor configurado seria promessa que ele não
  cumpre. Quem redefine é o João, na ficha do aluno; a senha nasce marcada como
  provisória e o aluno é avisado, em toda tela, de que outra pessoa consegue
  entrar na conta dele até que ele troque.
- **Limite de tentativas de login.** O freio em `auth.py` vive na memória do
  processo: segura o roteiro ingênuo, mas não sobrevive a reinício nem cobre um
  deploy com vários workers. Precisa de um limite no proxy ou de uma contagem
  compartilhada.
- **As cópias de backup ficam no mesmo volume do banco.** O backup automático
  protege contra erro de software e engano humano; o volume inteiro se perder é
  outro risco, e levar uma cópia para fora ainda é manual (`jf backup`).
- **A calculadora manual e a carga sugerida na prescrição são caminhos
  separados.** O João continua podendo digitar carga × reps na calculadora para
  simular um cenário; a carga automática (`GET /sessoes/{id}/cargas-sugeridas`)
  só aparece quando a prescrição pede `percentual_1rm` **e** o aluno já tem
  série registrada naquele exercício. As duas convivem de propósito — nem toda
  prescrição precisa depender do histórico.
- **O modo academia só abre treino que foi prescrito.** Treinar algo fora do
  plano não tem tela; o registro parte sempre de uma sessão da periodização.
- **O painel de alertas olha 8 a 12 semanas para trás, não o histórico
  inteiro.** Um aluno que treina há dois anos não deveria carregar para sempre
  um mês ruim de 2024. As janelas (`jf/alertas.py` e `resumo_de_forca`) são fixas
  e ainda não configuráveis pelo João.
- **`Prescricao.ordem` não é reordenável pela tela.** Os exercícios saem na ordem
  em que foram criados; as séries dentro de um exercício, sim, sobem e descem.
- **O leitor de texto entende as séries, não o treino inteiro.** Colar
  `12x50kg` funciona; colar o bloco com os nomes dos exercícios não, porque
  casar "Cadeira abdutora vermelha" com o catálogo pede busca aproximada. As
  linhas que ele não entende voltam com o motivo, em vez de sumirem.
- **O termo precisa passar por um advogado.** O texto em `jf/dados/termo.md`
  cobre o que a LGPD exige e está em português claro, mas foi escrito por quem
  não é advogado. O mecanismo (pedir, registrar, exportar, apagar) está testado;
  o texto é um ponto de partida.
- **O aviso de campo numérico fora da faixa vem do navegador, não do app.**
  Um `<input max="400">` é barrado antes do envio, e o texto do balãozinho sai
  no idioma do navegador — em português num aparelho em português. As mensagens
  do servidor (`jf/validacao.py`) cobrem o resto: datas, email, regras entre
  campos e qualquer cliente que não seja o formulário.
- **O catálogo de alimentos não está preenchido.** O esquema, a importação e a
  busca existem e estão testados, mas nenhuma tabela nutricional acompanha o
  repositório — é preciso rodar `jf importar-alimentos` com a TACO ou o Open
  Food Facts. Nada do protocolo depende disso.
- **O protocolo não soma kcal nem macro.** Depende do catálogo acima, e um
  total somado por cima de valores incompletos seria pior que não somar.
- **Sem gráfico de medidas.** O check-in guarda as medidas de fita (cintura,
  quadril, tórax, braço, coxa, panturrilha), mas ainda não há gráfico para elas —
  o e1RM já tem o dele (`PainelDeForca.tsx`).
