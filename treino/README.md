# JF Treino

App de acompanhamento entre o treinador **João Filho** e seus alunos. O aluno
registra como a semana foi, o João prescreve o treino, e os dois veem a mesma
evolução. O plano completo está em [`PLANO.md`](PLANO.md); para publicar, veja
[`DEPLOY.md`](DEPLOY.md).

**Fases 0 a 3 estão prontas.** O aluno faz o check-in semanal e os dois veem a
evolução em gráfico; o João monta a periodização com a progressão de carga série
a série e usa a calculadora para escolher a carga. Falta a dieta (fase 4).

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

Dentro dela já existem dez semanas de check-in e dois treinos montados, para os
gráficos e a progressão terem o que mostrar. `jf demonstracao` se recusa a rodar
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
cd treino && python3 -m pytest      # 296 testes
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
  forca.py        a equação de 1RM e o cálculo de carga (puro, sem I/O)
  leitura.py      lê a prescrição escrita à mão (puro, sem I/O)
  privacidade.py  o termo e a versão dele (o hash do próprio texto)
  diagnostico.py  o `jf doutor` — confere a configuração antes de subir
  migracoes/      Alembic: uma revisão por mudança de esquema
  modelos.py      Usuario, Aluno, Exercicio, Tecnica, Periodizacao,
                  SessaoModelo, Prescricao, SerieDaPrescricao,
                  CheckinSemanal, MedidaCorporal
  auth.py         senha, sessão e quem-pode-ver-o-quê
  banco.py        engine e sessão do SQLAlchemy
  esquemas.py     o que entra e sai da API (Pydantic)
  api/            sessao · alunos · exercicios · treinos · checkins ·
                  privacidade · calculadora
  dados/          catálogos de exercícios e técnicas, semeadura e a
                  demonstração
  servidor.py     a API em /api e o PWA no resto
  cli.py          jf preparar · jf treinador · jf demonstracao ·
                  jf doutor · jf backup · jf servir
web/
  src/estilo/     tokens da marca (preto, vermelho-sangue, osso)
  src/api/        cliente e tipos, espelhando jf/esquemas.py
  src/rotas/      Entrar · Alunos · FichaDoAluno · Periodizacao ·
                  Calculadora · Checkin · MeusDados · Inicio · Catalogo
  src/componentes/EditorDePrescricao.tsx · EditorDeSeries.tsx ·
                  PainelDeEvolucao.tsx · graficos/GraficoDeLinha.tsx
  gerar-icones.py desenha os ícones do PWA a partir do monograma
```

## Sete decisões que valem saber

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

**A versão do termo de consentimento é o hash do próprio texto.** Editar o
termo muda a versão sozinho, o consentimento anterior deixa de valer, e o app
volta a perguntar — que é o que a LGPD pede, já que o consentimento é específico
para uma finalidade (art. 8º §4º). Um número que alguém precisa lembrar de
incrementar acabaria esquecido, e consentimentos antigos passariam a valer para
um texto que ninguém leu.

**A equação proposta tem um piso que o paper não menciona.** O guard `k(w) ≥ 0,5`
publicado impede a divisão por zero, mas abaixo de ~4,74 kg a equação *inverte de
sentido*: 2 kg por 8 repetições estima 18,7 kg de 1RM e 3 kg pelas mesmas 8
estima 9,3 kg. Como cargas assim existem — elevação lateral com halter de 3 kg —,
o app cai para Epley nesse trecho e diz que caiu. Ver `CARGA_MINIMA_PROPOSTA` em
`jf/forca.py`, com a derivada que justifica o valor.

## O que fica em aberto

- **Troca e recuperação de senha.** Hoje o João cria a senha e passa ao aluno;
  não há tela para trocá-la nem fluxo de "esqueci minha senha".
- **Limite de tentativas de login.** O freio em `auth.py` vive na memória do
  processo: segura o roteiro ingênuo, mas não sobrevive a reinício nem cobre um
  deploy com vários workers. Precisa de um limite no proxy ou de uma contagem
  compartilhada.
- **Backup automático.** `jf backup` existe e faz cópia consistente, mas
  ninguém o chama sozinho.
- **A carga sugerida ainda não volta sozinha para a prescrição.** A calculadora é
  uma tela à parte: o João lê o número e digita. Ligar as duas depende do e1RM do
  aluno, que só existe quando ele registrar as séries executadas — fase 2 do lado
  do aluno, ainda não feita. O campo `percentual_1rm` já está no banco esperando.
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
- **As mensagens de validação saem em inglês.** Um peso fora da faixa devolve o
  texto padrão do Pydantic ("Input should be less than 400"), não uma frase em
  português. A tela mostra o que o servidor manda.
- **Sem gráfico de e1RM nem de medidas.** O check-in guarda as medidas de fita,
  mas ainda não há gráfico para elas; o e1RM depende do aluno registrar as séries
  executadas, que é o lado do treino ainda não feito.
