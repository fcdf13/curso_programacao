# JF Treino

App de acompanhamento entre o treinador **João Filho** e seus alunos. O aluno
registra como a semana foi, o João prescreve o treino, e os dois veem a mesma
evolução. O plano completo está em [`PLANO.md`](PLANO.md).

**Fases 0, 2 e 3 estão prontas.** O João entra, cadastra um aluno, monta a
periodização com a progressão de carga série a série e as técnicas de cada uma,
e usa a calculadora para escolher a carga. Falta o check-in semanal com gráficos
(fase 1) e a dieta (fase 4).

---

## Rodar

```bash
pip install -e "treino[dev]"                    # instala o comando `jf`

export JF_CHAVE_SECRETA="$(python3 -c 'import secrets; print(secrets.token_hex(32))')"
cd treino
jf preparar                                     # cria as tabelas e semeia 76 exercícios
jf treinador "João Filho" joao@exemplo.com      # pede a senha sem eco

cd web && npm install && npm run build && cd ..
jf servir                                       # http://127.0.0.1:8770
```

Para mexer no front com recarga automática, deixe `jf servir` rodando numa aba e
`npm run dev` noutra: o Vite sobe em `:5180` e repassa `/api` para o uvicorn.

Sem `JF_CHAVE_SECRETA` o app sorteia uma chave a cada início — serve para
desenvolver, derruba a sessão a cada reinício. Em produção (`JF_PRODUCAO=1`) ela
é obrigatória e o servidor se recusa a subir sem ela.

## Verificar

```bash
cd treino && python3 -m pytest      # 244 testes
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
  modelos.py      Usuario, Aluno, Exercicio, Tecnica, Periodizacao,
                  SessaoModelo, Prescricao, SerieDaPrescricao
  auth.py         senha, sessão e quem-pode-ver-o-quê
  banco.py        engine e sessão do SQLAlchemy
  esquemas.py     o que entra e sai da API (Pydantic)
  api/            sessao · alunos · exercicios · treinos · calculadora
  dados/          catálogos de exercícios e técnicas, e a semeadura
  servidor.py     a API em /api e o PWA no resto
  cli.py          jf preparar · jf treinador · jf servir
web/
  src/estilo/     tokens da marca (preto, vermelho-sangue, osso)
  src/api/        cliente e tipos, espelhando jf/esquemas.py
  src/rotas/      Entrar · Alunos · FichaDoAluno · Periodizacao ·
                  Calculadora · Inicio · Catalogo
  src/componentes/EditorDePrescricao.tsx · EditorDeSeries.tsx
  gerar-icones.py desenha os ícones do PWA a partir do monograma
```

## Cinco decisões que valem saber

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
  deploy com vários workers. A fase 5 precisa de um limite no proxy ou de uma
  contagem compartilhada.
- **Migrações.** `criar_tabelas()` só cria o que falta. Quando houver dado real
  de aluno para preservar, entra Alembic.
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
- **Consentimento LGPD, exportar e apagar os próprios dados.** Peso, sono e
  medidas são dado sensível de saúde; isso entra junto com o check-in, na fase 1.
