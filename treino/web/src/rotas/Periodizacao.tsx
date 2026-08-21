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
import { useSessao } from "../sessao";
import "../componentes/prescricao.css";
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
        {podeEditar && !abertoAqui && (
          <button
            type="button"
            className="botao secundario"
            onClick={() => definirEditando({ sessaoId: treino.id })}
          >
            Adicionar exercício
          </button>
        )}
      </div>

      {treino.prescricoes.length > 0 && (
        <div className="lista-de-prescricoes">
          {treino.prescricoes.map((prescricao) => (
            <Linha
              key={prescricao.id}
              prescricao={prescricao}
              podeEditar={podeEditar}
              aoEditar={() => definirEditando({ sessaoId: treino.id, prescricao })}
              aoApagar={() => apagar(prescricao)}
            />
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

function Linha({
  prescricao,
  podeEditar,
  aoEditar,
  aoApagar,
}: {
  prescricao: Prescricao;
  podeEditar: boolean;
  aoEditar: () => void;
  aoApagar: () => void;
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

        <span className="prescricao-carga">
          {prescricao.series} × {faixa}
          {prescricao.carga_alvo_kg !== null && ` · ${numero(prescricao.carga_alvo_kg, 1)} kg`}
        </span>

        {podeEditar && (
          <div className="prescricao-acoes">
            <button type="button" className="botao discreto" onClick={aoEditar}>
              Editar
            </button>
            <button type="button" className="botao discreto" onClick={aoApagar}>
              Remover
            </button>
          </div>
        )}
      </div>

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
