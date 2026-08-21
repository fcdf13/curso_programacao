# Publicar o JF Treino

O app é um **PWA**: ele não vem da App Store nem da Play Store. Quem tem o link
instala pela tela de início e passa a ter um ícone no celular, com push
notification funcionando no iPhone (iOS 16.4+) e no Android.

Para isso, só é preciso o app estar num endereço **com HTTPS**. Sem HTTPS o PWA
não instala e o push não funciona — não é preferência, é requisito do navegador.

---

## Antes de subir

```bash
cd treino
cd web && npm install && npm run build && cd ..
jf doutor
```

O `jf doutor` confere o que costuma passar despercebido num deploy e sai com
código 1 se algo impedir. As três coisas que ele pega:

| | |
|---|---|
| **A chave de sessão** | Se for a de exemplo, qualquer pessoa que leia este repositório assina um cookie válido e entra como quem quiser. |
| **O disco do banco** | SQLite dentro do contêiner some no próximo deploy, com o histórico do aluno junto. |
| **O PWA compilado** | Sem `web/dist`, o servidor só responde a `/api` — a tela fica em branco. |

Gere a chave assim, e guarde num lugar que não seja o repositório:

```bash
python3 -c 'import secrets; print(secrets.token_hex(32))'
```

## Fly.io

O `fly.toml` já está pronto. Ajuste `app` para um nome livre e rode:

```bash
cd treino
fly launch --no-deploy --copy-config
fly volumes create dados --size 1 --region gru
fly secrets set JF_CHAVE_SECRETA="$(python3 -c 'import secrets; print(secrets.token_hex(32))')"
fly secrets set JF_DOMINIOS="seu-app.fly.dev"
fly deploy

fly ssh console -C "jf treinador 'João Filho' joao@exemplo.com --senha 'trocar-no-primeiro-acesso'"
```

O `[[mounts]]` monta o volume em `/dados` e o `JF_BANCO` aponta para lá. É isso
que faz o histórico sobreviver ao deploy.

## Render

Suba o repositório, aponte um Blueprint para `treino/render.yaml` e defina
`JF_CHAVE_SECRETA` e `JF_DOMINIOS` no painel — o `render.yaml` marca a chave
como `sync: false` justamente para ela nunca ficar escrita aqui.

O **plano gratuito não tem disco persistente**; o `render.yaml` já vem no
`starter` por isso. Depois de subir, use o Shell do serviço:

```bash
jf treinador "João Filho" joao@exemplo.com
```

## Qualquer outro lugar com Docker

```bash
cd treino
docker build -t jf-treino .
docker run -d -p 8770:8770 \
  -v jf-dados:/dados \
  -e JF_PRODUCAO=1 \
  -e JF_BANCO="sqlite:////dados/jf.db" \
  -e JF_CHAVE_SECRETA="..." \
  -e JF_DOMINIOS="treino.seudominio.com.br" \
  jf-treino
```

Ponha um proxy com HTTPS na frente (Caddy resolve com duas linhas). O contêiner
roda `jf preparar` no início, que aplica as migrações pendentes.

## As variáveis

| Variável | Para quê |
|---|---|
| `JF_CHAVE_SECRETA` | Assina o cookie de sessão. **Obrigatória** em produção; o servidor se recusa a subir sem ela. |
| `JF_PRODUCAO` | `1` liga o cookie `Secure`, o HSTS, e fecha `/docs` e `/openapi.json`. |
| `JF_BANCO` | URL do banco. Padrão: SQLite ao lado do código — troque por um caminho dentro do volume. |
| `JF_DOMINIOS` | Domínios que o app aceita no `Host`, separados por vírgula. Sem isso ele responde a qualquer um. |

## O banco

SQLite num volume é adequado aqui, e não é gambiarra: um treinador com algumas
centenas de alunos está muito longe de qualquer limite do SQLite. O que ele
custa é **uma instância só** — o volume não se compartilha entre máquinas.

Para Postgres, instale o extra e troque a URL:

```bash
pip install -e "treino[postgres]"
export JF_BANCO="postgresql+psycopg://usuario:senha@host/jf"
jf preparar
```

## Backup

O histórico de treino de um atleta não tem como ser recriado. Copiar o arquivo
com `cp` enquanto há escrita produz um banco corrompido que só se descobre na
hora de restaurar, então use o comando — ele usa a API de backup do SQLite:

```bash
jf backup /caminho/backup-$(date +%F).db
```

No Fly:

```bash
fly ssh console -C "jf backup /dados/backup.db"
fly sftp get /dados/backup.db
```

Vale um cron semanal. **Ainda não existe backup automático** — é o item mais
importante em aberto depois que o primeiro aluno real entrar.

## Migrações

`jf preparar` aplica o que estiver pendente e é seguro rodar num banco já em
dia. Quando alterar um modelo, gere a revisão:

```bash
python3 -c "
from alembic import command
from jf.migracoes import _configuracao
command.revision(_configuracao(), message='o que mudou', autogenerate=True)
"
```

Leia o arquivo gerado antes de aplicar — o `autogenerate` acerta o esquema, mas
não sabe o que fazer com o dado que já está lá. Há um teste
(`teste_diagnostico.py`) que falha se os modelos saírem de sincronia com as
migrações, para ninguém descobrir isso no deploy.

## O que ainda falta antes de um aluno real

1. **Consentimento LGPD e exportar/apagar os próprios dados.** Peso, sono e
   medidas são dado sensível de saúde, e o app já os guarda.
2. **Backup automático.** Hoje é manual.
3. **Limite de tentativas de login que sobreviva a reinício.** O de hoje vive
   na memória do processo.
