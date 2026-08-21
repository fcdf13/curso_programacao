/** A ficha de um aluno. Na fase 0 mostra o perfil; check-in, treino e dieta
 *  entram como abas aqui nas fases seguintes. */

import { useCallback, useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

import { api, ErroDaApi } from "../api/cliente";
import type { Aluno, FaseDaPeriodizacao, PeriodizacaoNaLista } from "../api/tipos";
import { PainelDeEvolucao } from "../componentes/PainelDeEvolucao";
import "../componentes/prescricao.css";
import "./paginas.css";

const SEXO: Record<string, string> = {
  masculino: "Masculino",
  feminino: "Feminino",
  outro: "Outro",
};

function idade(nascimento: string | null): string | null {
  if (nascimento === null) return null;
  const data = new Date(`${nascimento}T00:00:00`);
  if (Number.isNaN(data.getTime())) return null;

  const hoje = new Date();
  let anos = hoje.getFullYear() - data.getFullYear();
  // Ainda não fez aniversário este ano.
  const mes = hoje.getMonth() - data.getMonth();
  if (mes < 0 || (mes === 0 && hoje.getDate() < data.getDate())) anos -= 1;

  return `${anos} anos`;
}

const FASES: { valor: FaseDaPeriodizacao; nome: string }[] = [
  { valor: "acumulacao", nome: "Acumulação" },
  { valor: "intensificacao", nome: "Intensificação" },
  { valor: "pico", nome: "Pico" },
  { valor: "deload", nome: "Deload" },
  { valor: "manutencao", nome: "Manutenção" },
];

export function FichaDoAluno() {
  const { id } = useParams<{ id: string }>();
  const [aluno, definirAluno] = useState<Aluno | null>(null);
  const [erro, definirErro] = useState<string | null>(null);
  const [blocos, definirBlocos] = useState<PeriodizacaoNaLista[]>([]);
  const [nomeDoBloco, definirNomeDoBloco] = useState("");
  const [fase, definirFase] = useState<FaseDaPeriodizacao>("acumulacao");
  const [semanas, definirSemanas] = useState("4");
  const [criando, definirCriando] = useState(false);

  const carregarBlocos = useCallback(async (alunoId: number) => {
    definirBlocos(await api.listarPeriodizacoes(alunoId));
  }, []);

  useEffect(() => {
    if (id === undefined) return;
    definirAluno(null);
    definirErro(null);
    api
      .verAluno(Number(id))
      .then(definirAluno)
      .catch((falha) =>
        definirErro(
          falha instanceof ErroDaApi ? falha.message : "Não foi possível carregar.",
        ),
      );
    void carregarBlocos(Number(id)).catch(() => definirBlocos([]));
  }, [id, carregarBlocos]);

  async function criarBloco() {
    if (id === undefined || nomeDoBloco.trim() === "") return;
    definirCriando(true);
    try {
      await api.criarPeriodizacao(Number(id), {
        nome: nomeDoBloco.trim(),
        fase,
        semanas: Number(semanas),
      });
      definirNomeDoBloco("");
      await carregarBlocos(Number(id));
    } catch (falha) {
      definirErro(falha instanceof ErroDaApi ? falha.message : "Não foi possível criar.");
    } finally {
      definirCriando(false);
    }
  }

  if (erro !== null) {
    return (
      <main className="conteudo pilha">
        <p className="aviso erro" role="alert">
          {erro}
        </p>
        <p>
          <Link to="/alunos">Voltar para a lista</Link>
        </p>
      </main>
    );
  }

  if (aluno === null) {
    return (
      <main className="conteudo">
        <p className="carregando">Carregando…</p>
      </main>
    );
  }

  const fichas: [string, string | null][] = [
    ["Email", aluno.email],
    ["Idade", idade(aluno.nascimento)],
    ["Sexo", aluno.sexo === null ? null : (SEXO[aluno.sexo] ?? null)],
    ["Altura", aluno.altura_cm === null ? null : `${aluno.altura_cm} cm`],
    ["Objetivo", aluno.objetivo],
  ];

  return (
    <main className="conteudo pilha">
      <div className="titulo-da-pagina">
        <div>
          <p className="rotulo">
            <Link to="/alunos">Alunos</Link>
          </p>
          <h1>{aluno.nome}</h1>
        </div>
      </div>

      <div className="painel">
        <dl className="ficha">
          {fichas.map(([nome, valor]) => (
            <div key={nome}>
              <dt>{nome}</dt>
              <dd className={valor === null ? "ausente" : undefined}>
                {valor ?? "não informado"}
              </dd>
            </div>
          ))}
        </dl>
      </div>

      <section className="pilha">
        <h2 className="rotulo">Evolução</h2>
        <PainelDeEvolucao alunoId={Number(id)} />
      </section>

      <section className="pilha">
        <h2 className="rotulo">Blocos de treino</h2>

        {blocos.length === 0 ? (
          <div className="vazio">
            <p>
              <strong>Nenhum bloco montado ainda.</strong>
            </p>
            <p>Crie o primeiro abaixo e comece a prescrever os treinos.</p>
          </div>
        ) : (
          <ul className="lista-de-blocos">
            {blocos.map((bloco) => (
              <li key={bloco.id}>
                <Link
                  to={`/periodizacoes/${bloco.id}`}
                  className={bloco.ativa ? "ativa" : ""}
                >
                  <span className="bloco-nome">{bloco.nome}</span>
                  <span className="prescricao-detalhe">
                    {FASES.find((f) => f.valor === bloco.fase)?.nome ?? bloco.fase} ·{" "}
                    {bloco.semanas} semanas
                    {!bloco.ativa && " · encerrado"}
                  </span>
                </Link>
              </li>
            ))}
          </ul>
        )}

        <div className="painel novo-treino">
          <label className="campo">
            <span>Novo bloco</span>
            <input
              value={nomeDoBloco}
              onChange={(evento) => definirNomeDoBloco(evento.target.value)}
              placeholder="Corte — bloco 1"
              maxLength={120}
            />
          </label>
          <label className="campo">
            <span>Fase</span>
            <select
              value={fase}
              onChange={(evento) => definirFase(evento.target.value as FaseDaPeriodizacao)}
            >
              {FASES.map((item) => (
                <option key={item.valor} value={item.valor}>
                  {item.nome}
                </option>
              ))}
            </select>
          </label>
          <label className="campo">
            <span>Semanas</span>
            <input
              type="number"
              inputMode="numeric"
              min="1"
              max="52"
              value={semanas}
              onChange={(evento) => definirSemanas(evento.target.value)}
            />
          </label>
          <button
            type="button"
            className="botao"
            onClick={criarBloco}
            disabled={criando || nomeDoBloco.trim() === ""}
          >
            {criando ? "Criando…" : "Criar bloco"}
          </button>
        </div>
      </section>
    </main>
  );
}
