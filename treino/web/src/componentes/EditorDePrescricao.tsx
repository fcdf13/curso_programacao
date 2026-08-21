/** Montar um exercício do treino: séries × repetições × carga, mais técnicas.
 *
 *  Os três escopos de técnica aparecem em campos diferentes de propósito.
 *  Bi-set e tri-set ligam exercícios, então vivem no bloco; dead stop e cadência
 *  descrevem como cada repetição é feita, então vivem no exercício. A API recusa
 *  quem trocar os campos — aqui a tela só evita que a pessoa tente.
 */

import { useMemo, useState } from "react";
import type { FormEvent } from "react";

import { api, ErroDaApi } from "../api/cliente";
import type { Exercicio, NovaPrescricao, Prescricao, Tecnica } from "../api/tipos";
import "./prescricao.css";

interface Props {
  sessaoId: number;
  exercicios: Exercicio[];
  tecnicas: Tecnica[];
  inicial?: Prescricao;
  aoSalvar: () => void;
  aoCancelar: () => void;
}

function estadoInicial(inicial: Prescricao | undefined) {
  return {
    exercicio_id: inicial ? String(inicial.exercicio.id) : "",
    series: String(inicial?.series ?? 3),
    reps_min: String(inicial?.reps_min ?? 8),
    reps_max: String(inicial?.reps_max ?? 12),
    rir_alvo: inicial?.rir_alvo === null ? "" : String(inicial?.rir_alvo ?? 2),
    carga_alvo_kg: inicial?.carga_alvo_kg == null ? "" : String(inicial.carga_alvo_kg),
    descanso_s: inicial?.descanso_s === null ? "" : String(inicial?.descanso_s ?? 90),
    cadencia: inicial?.cadencia ?? "",
    bloco: inicial?.bloco ?? "",
    agrupamento_id: inicial?.agrupamento ? String(inicial.agrupamento.id) : "",
    observacao: inicial?.observacao ?? "",
  };
}

export function EditorDePrescricao({
  sessaoId,
  exercicios,
  tecnicas,
  inicial,
  aoSalvar,
  aoCancelar,
}: Props) {
  const [campos, definirCampos] = useState(() => estadoInicial(inicial));
  const [escolhidas, definirEscolhidas] = useState<number[]>(
    () => inicial?.tecnicas.map((t) => t.id) ?? [],
  );
  const [erro, definirErro] = useState<string | null>(null);
  const [salvando, definirSalvando] = useState(false);

  const doExercicio = useMemo(
    () => tecnicas.filter((t) => t.escopo !== "agrupamento"),
    [tecnicas],
  );
  const deAgrupamento = useMemo(
    () => tecnicas.filter((t) => t.escopo === "agrupamento"),
    [tecnicas],
  );

  const exercicio = exercicios.find((e) => String(e.id) === campos.exercicio_id) ?? null;

  // A tonelagem acompanha o que está sendo digitado: o João vê o volume da
  // prescrição mudar enquanto decide, em vez de descobrir depois de salvar.
  const tonelagem = useMemo(() => {
    const series = Number(campos.series);
    const carga = Number(campos.carga_alvo_kg);
    const media = (Number(campos.reps_min) + Number(campos.reps_max)) / 2;
    if (!series || !carga || !media) return null;
    return series * media * carga;
  }, [campos.series, campos.reps_min, campos.reps_max, campos.carga_alvo_kg]);

  function alterar(campo: keyof typeof campos, valor: string) {
    definirCampos((atual) => ({ ...atual, [campo]: valor }));
  }

  const numeroOuNulo = (valor: string) => (valor === "" ? null : Number(valor));

  async function salvar(evento: FormEvent) {
    evento.preventDefault();
    definirErro(null);
    definirSalvando(true);

    const dados: NovaPrescricao = {
      exercicio_id: Number(campos.exercicio_id),
      series: Number(campos.series),
      reps_min: Number(campos.reps_min),
      reps_max: Number(campos.reps_max),
      rir_alvo: numeroOuNulo(campos.rir_alvo),
      carga_alvo_kg: numeroOuNulo(campos.carga_alvo_kg),
      descanso_s: numeroOuNulo(campos.descanso_s),
      cadencia: campos.cadencia || null,
      bloco: campos.bloco || null,
      agrupamento_id: numeroOuNulo(campos.agrupamento_id),
      observacao: campos.observacao || null,
      ordem: inicial?.ordem ?? 0,
      tecnica_ids: escolhidas,
    };

    try {
      if (inicial) await api.editarPrescricao(inicial.id, dados);
      else await api.criarPrescricao(sessaoId, dados);
      aoSalvar();
    } catch (falha) {
      definirErro(falha instanceof ErroDaApi ? falha.message : "Não foi possível salvar.");
    } finally {
      definirSalvando(false);
    }
  }

  return (
    <form className="editor-de-prescricao" onSubmit={salvar}>
      <label className="campo">
        <span>Exercício</span>
        <select
          value={campos.exercicio_id}
          onChange={(evento) => alterar("exercicio_id", evento.target.value)}
          required
        >
          <option value="">Escolha…</option>
          {exercicios.map((item) => (
            <option key={item.id} value={item.id}>
              {item.nome}
            </option>
          ))}
        </select>
      </label>

      {exercicio?.convencao_de_carga === "por_halter" && (
        <p className="dica destaque">
          Registre o peso de <strong>um</strong> halter, mesmo usando dois.
        </p>
      )}

      <div className="linha-de-campos">
        <label className="campo">
          <span>Séries</span>
          <input
            type="number"
            inputMode="numeric"
            min="1"
            max="20"
            value={campos.series}
            onChange={(evento) => alterar("series", evento.target.value)}
            required
          />
        </label>
        <label className="campo">
          <span>Reps (mín.)</span>
          <input
            type="number"
            inputMode="numeric"
            min="1"
            value={campos.reps_min}
            onChange={(evento) => alterar("reps_min", evento.target.value)}
            required
          />
        </label>
        <label className="campo">
          <span>Reps (máx.)</span>
          <input
            type="number"
            inputMode="numeric"
            min="1"
            value={campos.reps_max}
            onChange={(evento) => alterar("reps_max", evento.target.value)}
            required
          />
        </label>
        <label className="campo">
          <span>Carga (kg)</span>
          <input
            type="number"
            inputMode="decimal"
            step="0.5"
            min="0"
            value={campos.carga_alvo_kg}
            onChange={(evento) => alterar("carga_alvo_kg", evento.target.value)}
            placeholder="—"
          />
        </label>
      </div>

      <div className="linha-de-campos">
        <label className="campo">
          <span>RIR alvo</span>
          <input
            type="number"
            inputMode="numeric"
            min="0"
            max="10"
            value={campos.rir_alvo}
            onChange={(evento) => alterar("rir_alvo", evento.target.value)}
          />
        </label>
        <label className="campo">
          <span>Descanso (s)</span>
          <input
            type="number"
            inputMode="numeric"
            min="0"
            max="900"
            step="15"
            value={campos.descanso_s}
            onChange={(evento) => alterar("descanso_s", evento.target.value)}
          />
        </label>
        <label className="campo">
          <span>Cadência</span>
          <input
            value={campos.cadencia}
            onChange={(evento) => alterar("cadencia", evento.target.value)}
            placeholder="3-1-1-0"
            maxLength={15}
          />
        </label>
      </div>

      {tonelagem !== null && (
        <p className="tonelagem-viva">
          Tonelagem prevista:{" "}
          <strong>{tonelagem.toLocaleString("pt-BR", { maximumFractionDigits: 0 })} kg</strong>{" "}
          <span>· séries × reps × carga, o volume de trabalho — não a força</span>
        </p>
      )}

      <fieldset className="tecnicas">
        <legend>Técnica de execução</legend>
        <div className="tecnicas-lista">
          {doExercicio.map((tecnica) => (
            <label
              key={tecnica.id}
              className={`tecnica-chip ${escolhidas.includes(tecnica.id) ? "marcada" : ""}`}
              title={tecnica.descricao}
            >
              <input
                type="checkbox"
                checked={escolhidas.includes(tecnica.id)}
                onChange={() =>
                  definirEscolhidas((atual) =>
                    atual.includes(tecnica.id)
                      ? atual.filter((x) => x !== tecnica.id)
                      : [...atual, tecnica.id],
                  )
                }
              />
              {tecnica.nome}
              {tecnica.distorce_estimativa && <span aria-hidden="true"> ⚠</span>}
            </label>
          ))}
        </div>
      </fieldset>

      <fieldset className="tecnicas">
        <legend>Bloco — para ligar com outro exercício</legend>
        <div className="linha-de-campos">
          <label className="campo">
            <span>Letra do bloco</span>
            <input
              value={campos.bloco}
              onChange={(evento) => alterar("bloco", evento.target.value.toUpperCase())}
              placeholder="A"
              maxLength={4}
            />
          </label>
          <label className="campo">
            <span>Agrupamento</span>
            <select
              value={campos.agrupamento_id}
              onChange={(evento) => alterar("agrupamento_id", evento.target.value)}
            >
              <option value="">Exercício isolado</option>
              {deAgrupamento.map((tecnica) => (
                <option key={tecnica.id} value={tecnica.id} title={tecnica.descricao}>
                  {tecnica.nome}
                </option>
              ))}
            </select>
          </label>
        </div>
        <p className="dica">
          Exercícios com a mesma letra são executados juntos. Um bi-set são dois
          registros no bloco A; um tri-set, três.
        </p>
      </fieldset>

      <label className="campo">
        <span>Observação</span>
        <input
          value={campos.observacao}
          onChange={(evento) => alterar("observacao", evento.target.value)}
          placeholder="Última série até a falha"
          maxLength={300}
        />
      </label>

      {erro !== null && (
        <p className="aviso erro" role="alert">
          {erro}
        </p>
      )}

      <div className="editor-acoes">
        <button type="submit" className="botao" disabled={salvando}>
          {salvando ? "Salvando…" : inicial ? "Salvar" : "Adicionar"}
        </button>
        <button type="button" className="botao secundario" onClick={aoCancelar}>
          Cancelar
        </button>
      </div>
    </form>
  );
}
