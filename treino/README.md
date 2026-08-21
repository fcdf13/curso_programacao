# JF Treino

App de acompanhamento entre o treinador **João Filho** e seus alunos. O aluno
registra como a semana foi, o João prescreve o treino, e os dois veem a mesma
evolução. O plano completo está em [`PLANO.md`](PLANO.md).

**Fase 0 — fundação — está pronta.** O João entra, cadastra um aluno, e o aluno
entra. As fases seguintes (check-in, treino, calculadora, dieta) ainda não.

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
cd treino && python3 -m pytest      # 36 testes
cd treino/web && npm run verificar  # tsc
```

O arquivo que mais importa é `testes/teste_permissoes.py`. Ele existe porque o
erro que ele pega é silencioso: uma rota que esquece de filtrar por dono passa em
todo teste feliz e só falha quando alguém troca o número na URL.

## Como está organizado

```
jf/
  modelos.py      Usuario, Aluno, Exercicio
  auth.py         senha, sessão e quem-pode-ver-o-quê
  banco.py        engine e sessão do SQLAlchemy
  esquemas.py     o que entra e sai da API (Pydantic)
  api/            sessao.py, alunos.py, exercicios.py
  dados/          o catálogo de exercícios e a semeadura
  servidor.py     a API em /api e o PWA no resto
  cli.py          jf preparar · jf treinador · jf servir
web/
  src/estilo/     tokens da marca (preto, vermelho-sangue, osso)
  src/api/        cliente e tipos, espelhando jf/esquemas.py
  src/rotas/      Entrar, Alunos, FichaDoAluno, Inicio, Catalogo
  gerar-icones.py desenha os ícones do PWA a partir do monograma
```

## Duas decisões que valem saber

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

## O que a fase 0 deixou em aberto

- **Troca e recuperação de senha.** Hoje o João cria a senha e passa ao aluno;
  não há tela para trocá-la nem fluxo de "esqueci minha senha".
- **Limite de tentativas de login.** O freio em `auth.py` vive na memória do
  processo: segura o roteiro ingênuo, mas não sobrevive a reinício nem cobre um
  deploy com vários workers. A fase 5 precisa de um limite no proxy ou de uma
  contagem compartilhada.
- **Migrações.** `criar_tabelas()` só cria o que falta. A partir da fase 1, quando
  houver dado real de aluno para preservar, entra Alembic.
- **Consentimento LGPD, exportar e apagar os próprios dados.** Peso, sono e
  medidas são dado sensível de saúde; isso entra junto com o check-in, na fase 1.
