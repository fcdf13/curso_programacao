/** Um bloco de treino: os treinos dentro dele e os exercícios de cada um.
 *
 *  O João edita; o aluno lê a mesma tela sem os botões. Manter uma tela só
 *  garante que os dois vejam exatamente a mesma prescrição.
 */

import { useCallback, useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

import { api, ErroDaApi } from "../api/cliente";
import type { Exercicio, Periodizacao as Bloco, Prescricao, SessaoModelo, Tecnica } from "../api/tipos";
import { EditorDePrescricao } from "../componentes/EditorDePrescricao";
import { EditorDeSeries } from "../componentes/EditorDeSeries";
import { useSessao } from "../sessao";
import "../componentes/prescricao.css";
import "../componentes/series.css";
import "./paginas.css";

const DIAS = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"];

const FASES: Record<string, string> = {
  acumulacao: "Acumulação",
  intensificacao: "Intensificação",
  pico: "Pico",
  deload: "Deload",
  manutencao: "Manutenção",
};

const numero = (valor: number, casas = 0) =>
  valor.toLocaleString("pt-BR", { maximumFractionDigits: casas });

export function Periodizacao() {
  const { id } = useParams<{ id: string }>();
  const { eu } = useSessao();
  const podeEditar = eu?.usuario.papel === "treinador";

  const [bloco, definirBloco] = useState<Bloco | null>(null);
  const [erro, definirErro] = useState<string | null>(null);
  const [exercicios, definirExercicios] = useState<Exercicio[]>([]);
  const [tecnicas, definirTecnicas] = useState<Tecnica[]>([]);

  const [editando, definirEditando] = useState<{ sessaoId: number; prescricao?: Prescricao } | null>(null);
  const [novoTreino, definirNovoTreino] = useState("");

  const recarregar = useCallback(async () => {
    if (id === undefined) return;
    try {
      definirBloco(await api.verPeriodizacao(Number(id)));
    } catch (falha) {
      definirErro(falha instanceof ErroDaApi ? falha.message : "Não foi possível carregar.");
    }
  }, [id]);

  useEffect(() => {
    void recarregar();
  }, [recarregar]);

  useEffect(() => {
    if (!podeEditar) return;
    api.listarExercicios().then(definirExercicios).catch(() => definirExercicios([]));
    api.tecnicas().then(definirTecnicas).catch(() => definirTecnicas([]));
  }, [podeEditar]);

  async function criarTreino() {
    if (bloco === null || novoTreino.trim() === "") return;
    await api.criarSessao(bloco.id, { nome: novoTreino.trim(), ordem: bloco.sessoes.length });
    definirNovoTreino("");
    await recarregar();
  }

  if (erro !== null) {
    return (
      <main className="conteudo pilha">
        <p className="aviso erro" role="alert">
          {erro}
        </p>
      </main>
    );
  }

  if (bloco === null) {
    return (
      <main className="conteudo">
        <p className="carregando">Carregando…</p>
      </main>
    );
  }

  return (
    <main className="conteudo pilha">
      <div className="titulo-da-pagina">
        <div>
          <p className="rotulo">
            {podeEditar ? <Link to={`/alunos/${bloco.aluno_id}`}>Voltar ao aluno</Link> : "Seu treino"}
          </p>
          <h1>{bloco.nome}</h1>
        </div>
      </div>

      <div className="painel resumo-do-bloco">
        <div>
          <p className="rotulo">Fase</p>
          <p className="resumo-valor">{FASES[bloco.fase] ?? bloco.fase}</p>
        </div>
        <div>
          <p className="rotulo">Semanas</p>
          <p className="resumo-valor">{bloco.semanas}</p>
        </div>
        <div>
          <p className="rotulo">Treinos</p>
          <p className="resumo-valor">{bloco.sessoes.length}</p>
        </div>
        <div>
          <p className="rotulo">Tonelagem por volta</p>
          <p className="resumo-valor">{numero(bloco.tonelagem_prevista)} kg</p>
        </div>
      </div>

      {bloco.sessoes.length === 0 && (
        <div className="vazio">
          <p>
            <strong>Nenhum treino neste bloco ainda.</strong>
          </p>
          {podeEditar && <p>Crie o Treino A abaixo e comece a montar.</p>}
        </div>
      )}

      {bloco.sessoes.map((treino) => (
        <Treino
          key={treino.id}
          treino={treino}
          podeEditar={podeEditar}
          exercicios={exercicios}
          tecnicas={tecnicas}
          editando={editando}
          definirEditando={definirEditando}
          recarregar={recarregar}
        />
      ))}

      {podeEditar && (
        <div className="painel novo-treino">
          <label className="campo">
            <span>Novo treino</span>
            <input
              value={novoTreino}
              onChange={(evento) => definirNovoTreino(evento.target.value)}
              placeholder="Treino A — peito e tríceps"
              maxLength={120}
            />
          </label>
          <button
            type="button"
            className="botao secundario"
            onClick={criarTreino}
            disabled={novoTreino.trim() === ""}
          >
            Criar treino
          </button>
        </div>
      )}
    </main>
  );
}

interface TreinoProps {
  treino: SessaoModelo;
  podeEditar: boolean;
  exercicios: Exercicio[];
  tecnicas: Tecnica[];
  editando: { sessaoId: number; prescricao?: Prescricao } | null;
  definirEditando: (valor: { sessaoId: number; prescricao?: Prescricao } | null) => void;
  recarregar: () => Promise<void>;
}

function Treino({
  treino,
  podeEditar,
  exercicios,
  tecnicas,
  editando,
  definirEditando,
  recarregar,
}: TreinoProps) {
  const abertoAqui = editando?.sessaoId === treino.id;
  const [seriesDe, definirSeriesDe] = useState<number | null>(null);

  async function apagar(prescricao: Prescricao) {
    await api.apagarPrescricao(prescricao.id);
    await recarregar();
  }

  return (
    <section className="painel pilha">
      <div className="titulo-do-treino">
        <div>
          <h2>{treino.nome}</h2>
          <p className="prescricao-detalhe">
            {treino.dia_da_semana !== null && `${DIAS[treino.dia_da_semana]} · `}
            {treino.prescricoes.length} exercício
            {treino.prescricoes.length === 1 ? "" : "s"}
            {treino.tonelagem_prevista > 0 &&
              ` · ${numero(treino.tonelagem_prevista)} kg de tonelagem`}
            {treino.prescricoes_sem_carga > 0 &&
              ` · ${treino.prescricoes_sem_carga} sem carga definida`}
          </p>
        </div>
        {podeEditar ? (
          !abertoAqui && (
            <button
              type="button"
              className="botao secundario"
              onClick={() => definirEditando({ sessaoId: treino.id })}
            >
              Adicionar exercício
            </button>
          )
        ) : (
          treino.prescricoes.length > 0 && (
            <Link to={`/treinar/${treino.id}`} className="botao">
              Treinar
            </Link>
          )
        )}
      </div>

      {treino.prescricoes.length > 0 && (
        <div className="lista-de-prescricoes">
          {treino.prescricoes.map((prescricao) => (
            <div key={prescricao.id}>
              <Linha
                prescricao={prescricao}
                podeEditar={podeEditar}
                editandoSeries={seriesDe === prescricao.id}
                aoEditar={() => definirEditando({ sessaoId: treino.id, prescricao })}
                aoApagar={() => apagar(prescricao)}
                aoAbrirSeries={() =>
                  definirSeriesDe((atual) =>
                    atual === prescricao.id ? null : prescricao.id,
                  )
                }
              />
              {seriesDe === prescricao.id && (
                <div className="encaixe-do-editor">
                  <EditorDeSeries
                    prescricao={prescricao}
                    tecnicas={tecnicas}
                    aoSalvar={async () => {
                      definirSeriesDe(null);
                      await recarregar();
                    }}
                  />
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {abertoAqui && (
        <EditorDePrescricao
          sessaoId={treino.id}
          exercicios={exercicios}
          tecnicas={tecnicas}
          inicial={editando?.prescricao}
          aoSalvar={async () => {
            definirEditando(null);
            await recarregar();
          }}
          aoCancelar={() => definirEditando(null)}
        />
      )}
    </section>
  );
}

const TIPO_CURTO: Record<string, string> = {
  up_set: "up set",
  aquecimento: "aquec.",
  back_off: "back off",
  valida: "",
};

/** Como a série se lê na academia: "12x50kg", "12x50 a 92kg", "up set 40 a 100kg". */
function textoDaSerie(serie: Prescricao["series_detalhadas"][number]): string {
  const carga =
    serie.carga_kg === null
      ? "—"
      : serie.carga_ate_kg !== null
        ? `${numero(serie.carga_kg, 1)} a ${numero(serie.carga_ate_kg, 1)} kg`
        : `${numero(serie.carga_kg, 1)} kg`;

  const rotulo = TIPO_CURTO[serie.tipo];
  if (serie.reps === null) return `${rotulo || "rampa"} ${carga}`.trim();
  return `${serie.reps}× ${carga}${rotulo ? ` (${rotulo})` : ""}`;
}

function Linha({
  prescricao,
  podeEditar,
  editandoSeries,
  aoEditar,
  aoApagar,
  aoAbrirSeries,
}: {
  prescricao: Prescricao;
  podeEditar: boolean;
  editandoSeries: boolean;
  aoEditar: () => void;
  aoApagar: () => void;
  aoAbrirSeries: () => void;
}) {
  const faixa =
    prescricao.reps_min === prescricao.reps_max
      ? `${prescricao.reps_min}`
      : `${prescricao.reps_min}–${prescricao.reps_max}`;

  return (
    <div className={`linha-de-prescricao ${prescricao.bloco ? "em-bloco" : ""}`}>
      <div className="prescricao-principal">
        {prescricao.bloco !== null && (
          <span className="selo-de-bloco">
            {prescricao.bloco}
            {prescricao.agrupamento && ` · ${prescricao.agrupamento.nome}`}
          </span>
        )}

        <span className="prescricao-nome">{prescricao.exercicio.nome}</span>

        {/* Com progressão o resumo mente por omissão, então some. */}
        {!prescricao.tem_progressao && (
          <span className="prescricao-carga">
            {prescricao.series} × {faixa}
            {prescricao.carga_alvo_kg !== null &&
              ` · ${numero(prescricao.carga_alvo_kg, 1)} kg`}
          </span>
        )}

        {podeEditar && (
          <div className="prescricao-acoes">
            <button type="button" className="botao discreto" onClick={aoAbrirSeries}>
              {editandoSeries ? "Fechar séries" : "Séries"}
            </button>
            <button type="button" className="botao discreto" onClick={aoEditar}>
              Editar
            </button>
            <button type="button" className="botao discreto" onClick={aoApagar}>
              Remover
            </button>
          </div>
        )}
      </div>

      {prescricao.series_detalhadas.length > 0 && (
        <ol className="progressao">
          {prescricao.series_detalhadas.map((serie) => (
            <li
              key={serie.id}
              className={`serie-pastilha tipo-${serie.tipo}`}
              title={serie.tecnicas.map((t) => t.nome).join(", ") || undefined}
            >
              {textoDaSerie(serie)}
              {serie.tecnicas.map((t) => (
                <span key={t.id} className="serie-tecnica">
                  {t.nome}
                  {t.distorce_estimativa && <span aria-hidden="true"> ⚠</span>}
                </span>
              ))}
            </li>
          ))}
        </ol>
      )}

      <div className="prescricao-secundaria">
        <span className="prescricao-detalhe">
          {[
            prescricao.rir_alvo !== null ? `RIR ${prescricao.rir_alvo}` : null,
            prescricao.descanso_s !== null ? `${prescricao.descanso_s}s` : null,
            prescricao.cadencia,
            prescricao.tonelagem_prevista !== null
              ? `${numero(prescricao.tonelagem_prevista)} kg`
              : null,
          ]
            .filter(Boolean)
            .join(" · ")}
        </span>

        {prescricao.tecnicas.map((tecnica) => (
          <span
            key={tecnica.id}
            className={`etiqueta ${tecnica.distorce_estimativa ? "distorce" : ""}`}
            title={
              tecnica.distorce_estimativa
                ? `${tecnica.descricao} Esta série não entra na estimativa de 1RM.`
                : tecnica.descricao
            }
          >
            {tecnica.nome}
          </span>
        ))}

        {prescricao.observacao !== null && (
          <span className="prescricao-detalhe italico">{prescricao.observacao}</span>
        )}
      </div>
    </div>
  );
}
