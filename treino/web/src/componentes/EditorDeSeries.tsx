/** A progressão de carga dentro do exercício, série por série.
 *
 *  O caminho principal é preencher à mão: uma linha por série, com reps, carga
 *  e técnica próprias. Colar o texto é atalho, para quem já tem o treino
 *  escrito — ele preenche estas mesmas linhas, que continuam editáveis.
 */

import { useState } from "react";

import { api, ErroDaApi } from "../api/cliente";
import type { NovaSerie, Prescricao, Tecnica, TipoDeSerie } from "../api/tipos";
import "./series.css";

const TIPOS: { valor: TipoDeSerie; nome: string; dica: string }[] = [
  { valor: "valida", nome: "Válida", dica: "Série de trabalho. Conta no volume." },
  {
    valor: "up_set",
    nome: "Up set",
    dica: "Rampa até a carga de trabalho. Não conta no volume.",
  },
  {
    valor: "aquecimento",
    nome: "Aquecimento",
    dica: "Preparação. Não conta no volume.",
  },
  { valor: "back_off", nome: "Back off", dica: "Mais leve depois da pesada. Conta." },
];

/** O estado de edição é tudo string: campo numérico vazio precisa continuar
 *  vazio enquanto se digita, e `Number("")` seria zero. */
interface Rascunho {
  chave: string;
  tipo: TipoDeSerie;
  reps: string;
  carga_kg: string;
  carga_ate_kg: string;
  rir: string;
  observacao: string;
  tecnica_ids: number[];
}

let contador = 0;
const novaChave = () => `s${(contador += 1)}`;

function vazia(): Rascunho {
  return {
    chave: novaChave(),
    tipo: "valida",
    reps: "",
    carga_kg: "",
    carga_ate_kg: "",
    rir: "",
    observacao: "",
    tecnica_ids: [],
  };
}

function daPrescricao(prescricao: Prescricao): Rascunho[] {
  return prescricao.series_detalhadas.map((serie) => ({
    chave: novaChave(),
    tipo: serie.tipo,
    reps: serie.reps === null ? "" : String(serie.reps),
    carga_kg: serie.carga_kg === null ? "" : String(serie.carga_kg),
    carga_ate_kg: serie.carga_ate_kg === null ? "" : String(serie.carga_ate_kg),
    rir: serie.rir === null ? "" : String(serie.rir),
    observacao: serie.observacao ?? "",
    tecnica_ids: serie.tecnicas.map((t) => t.id),
  }));
}

const numeroOuNulo = (valor: string) =>
  valor.trim() === "" ? null : Number(valor.replace(",", "."));

function paraApi(rascunhos: Rascunho[]): NovaSerie[] {
  return rascunhos.map((linha, posicao) => ({
    ordem: posicao,
    tipo: linha.tipo,
    reps: numeroOuNulo(linha.reps),
    carga_kg: numeroOuNulo(linha.carga_kg),
    carga_ate_kg: numeroOuNulo(linha.carga_ate_kg),
    rir: numeroOuNulo(linha.rir),
    observacao: linha.observacao.trim() || null,
    tecnica_ids: linha.tecnica_ids,
  }));
}

function tonelagemDe(linhas: Rascunho[]): number {
  let total = 0;
  for (const linha of linhas) {
    if (linha.tipo === "up_set" || linha.tipo === "aquecimento") continue;
    const reps = numeroOuNulo(linha.reps);
    const de = numeroOuNulo(linha.carga_kg);
    if (reps === null || de === null) continue;
    const ate = numeroOuNulo(linha.carga_ate_kg);
    // Numa rampa vale o ponto médio, como no servidor.
    total += reps * (ate === null ? de : (de + ate) / 2);
  }
  return total;
}

interface Props {
  prescricao: Prescricao;
  tecnicas: Tecnica[];
  aoSalvar: () => Promise<void> | void;
}

export function EditorDeSeries({ prescricao, tecnicas, aoSalvar }: Props) {
  const [linhas, definirLinhas] = useState<Rascunho[]>(() => {
    const existentes = daPrescricao(prescricao);
    return existentes.length > 0 ? existentes : [vazia()];
  });
  const [erro, definirErro] = useState<string | null>(null);
  const [salvando, definirSalvando] = useState(false);

  const [colando, definirColando] = useState(false);
  // Qual série está com o seletor de técnicas aberto. Só uma por vez: com as
  // 24 técnicas repetidas em toda linha, cinco séries viravam uma parede.
  const [expandida, definirExpandida] = useState<string | null>(null);
  const [texto, definirTexto] = useState("");
  const [aviso, definirAviso] = useState<string | null>(null);

  const doExercicio = tecnicas.filter((t) => t.escopo !== "agrupamento");

  function alterar(chave: string, campo: keyof Rascunho, valor: string) {
    definirLinhas((atual) =>
      atual.map((linha) => (linha.chave === chave ? { ...linha, [campo]: valor } : linha)),
    );
  }

  function alternarTecnica(chave: string, id: number) {
    definirLinhas((atual) =>
      atual.map((linha) =>
        linha.chave === chave
          ? {
              ...linha,
              tecnica_ids: linha.tecnica_ids.includes(id)
                ? linha.tecnica_ids.filter((x) => x !== id)
                : [...linha.tecnica_ids, id],
            }
          : linha,
      ),
    );
  }

  function acrescentar() {
    // Copia a última: a série seguinte quase sempre parte da anterior, e
    // digitar tudo de novo a cada linha seria o trabalho que o app deve poupar.
    definirLinhas((atual) => {
      const ultima = atual[atual.length - 1];
      return [...atual, ultima ? { ...ultima, chave: novaChave() } : vazia()];
    });
  }

  function remover(chave: string) {
    definirLinhas((atual) => atual.filter((linha) => linha.chave !== chave));
  }

  function mover(indice: number, passo: number) {
    definirLinhas((atual) => {
      const destino = indice + passo;
      if (destino < 0 || destino >= atual.length) return atual;
      const copia = [...atual];
      const [movida] = copia.splice(indice, 1);
      if (movida) copia.splice(destino, 0, movida);
      return copia;
    });
  }

  async function lerColado() {
    definirErro(null);
    definirAviso(null);
    try {
      const leitura = await api.lerTexto(texto);
      const entendidas = leitura.linhas.filter((linha) => linha.entendida);

      if (entendidas.length === 0) {
        definirAviso("Não entendi nenhuma linha. Confira o formato ou preencha à mão.");
        return;
      }

      definirLinhas(
        entendidas.map((linha) => ({
          chave: novaChave(),
          tipo: linha.tipo,
          reps: linha.reps === null ? "" : String(linha.reps),
          carga_kg: linha.carga_kg === null ? "" : String(linha.carga_kg),
          carga_ate_kg: linha.carga_ate_kg === null ? "" : String(linha.carga_ate_kg),
          rir: "",
          observacao: linha.observacao ?? "",
          tecnica_ids: linha.tecnica_ids,
        })),
      );

      const perdidas = leitura.linhas.filter((linha) => !linha.entendida);
      definirAviso(
        perdidas.length === 0
          ? `${entendidas.length} séries lidas. Confira antes de salvar.`
          : `${entendidas.length} séries lidas. Não entendi: ${perdidas
              .map((linha) => `"${linha.texto.trim()}"`)
              .join(", ")}.`,
      );
      definirColando(false);
    } catch (falha) {
      definirErro(falha instanceof ErroDaApi ? falha.message : "Não foi possível ler.");
    }
  }

  async function salvar() {
    definirErro(null);
    definirSalvando(true);
    try {
      await api.definirSeries(prescricao.id, paraApi(linhas));
      await aoSalvar();
    } catch (falha) {
      definirErro(falha instanceof ErroDaApi ? falha.message : "Não foi possível salvar.");
    } finally {
      definirSalvando(false);
    }
  }

  const tonelagem = tonelagemDe(linhas);

  return (
    <div className="editor-de-series">
      <div className="series-topo">
        <div>
          <p className="rotulo">Séries do exercício</p>
          <p className="dica">
            Uma linha por série. Preencha reps e carga de cada uma quando houver
            progressão; deixe iguais quando não houver.
          </p>
        </div>
        <button
          type="button"
          className="botao discreto"
          onClick={() => definirColando((aberto) => !aberto)}
        >
          {colando ? "Fechar" : "Colar texto"}
        </button>
      </div>

      {colando && (
        <div className="colar">
          <label className="campo">
            <span>Cole a prescrição como você escreve</span>
            <textarea
              rows={5}
              value={texto}
              onChange={(evento) => definirTexto(evento.target.value)}
              placeholder={"Up set de 40 a 100kg\n10x100kg\n12x100kg cluster set"}
            />
          </label>
          <button
            type="button"
            className="botao secundario"
            onClick={lerColado}
            disabled={texto.trim() === ""}
          >
            Ler e preencher
          </button>
          <p className="dica">
            Isto substitui as linhas abaixo — elas continuam editáveis depois.
          </p>
        </div>
      )}

      {aviso !== null && (
        <p className="aviso" role="status">
          {aviso}
        </p>
      )}

      <div className="series-lista">
        {linhas.map((linha, indice) => {
          const rampa = linha.carga_ate_kg.trim() !== "";
          const escolhidas = doExercicio.filter((tecnica) =>
            linha.tecnica_ids.includes(tecnica.id),
          );
          const aberta = expandida === linha.chave;

          return (
            <div key={linha.chave} className={`serie-linha tipo-${linha.tipo}`}>
              <div className="serie-numero">
                <span>{indice + 1}</span>
                <div className="serie-mover">
                  <button
                    type="button"
                    className="botao discreto"
                    onClick={() => mover(indice, -1)}
                    disabled={indice === 0}
                    aria-label={`Subir a série ${indice + 1}`}
                  >
                    ↑
                  </button>
                  <button
                    type="button"
                    className="botao discreto"
                    onClick={() => mover(indice, 1)}
                    disabled={indice === linhas.length - 1}
                    aria-label={`Descer a série ${indice + 1}`}
                  >
                    ↓
                  </button>
                </div>
              </div>

              <div className="serie-corpo">
                <div className="serie-campos">
                  <label className="campo estreito tipo">
                    <span>Tipo</span>
                    <select
                      value={linha.tipo}
                      onChange={(evento) =>
                        alterar(linha.chave, "tipo", evento.target.value)
                      }
                    >
                      {TIPOS.map((tipo) => (
                        <option key={tipo.valor} value={tipo.valor} title={tipo.dica}>
                          {tipo.nome}
                        </option>
                      ))}
                    </select>
                  </label>

                  <label className="campo estreito">
                    <span>Reps</span>
                    <input
                      type="number"
                      inputMode="numeric"
                      min="1"
                      max="100"
                      value={linha.reps}
                      onChange={(evento) =>
                        alterar(linha.chave, "reps", evento.target.value)
                      }
                      placeholder={linha.tipo === "up_set" ? "—" : ""}
                    />
                  </label>

                  <label className="campo estreito">
                    <span>Carga</span>
                    <input
                      type="number"
                      inputMode="decimal"
                      step="0.5"
                      min="0"
                      value={linha.carga_kg}
                      onChange={(evento) =>
                        alterar(linha.chave, "carga_kg", evento.target.value)
                      }
                    />
                  </label>

                  <label className="campo estreito">
                    <span>Até</span>
                    <input
                      type="number"
                      inputMode="decimal"
                      step="0.5"
                      min="0"
                      value={linha.carga_ate_kg}
                      onChange={(evento) =>
                        alterar(linha.chave, "carga_ate_kg", evento.target.value)
                      }
                      placeholder="—"
                    />
                  </label>

                  <label className="campo estreito">
                    <span>RIR</span>
                    <input
                      type="number"
                      inputMode="numeric"
                      min="0"
                      max="10"
                      value={linha.rir}
                      onChange={(evento) =>
                        alterar(linha.chave, "rir", evento.target.value)
                      }
                    />
                  </label>

                  <div className="serie-botoes">
                    <button
                      type="button"
                      className={`botao discreto ${aberta ? "ativo" : ""}`}
                      onClick={() =>
                        definirExpandida(aberta ? null : linha.chave)
                      }
                      aria-expanded={aberta}
                    >
                      Técnica
                      {escolhidas.length > 0 && ` (${escolhidas.length})`}
                    </button>
                    <button
                      type="button"
                      className="botao discreto"
                      onClick={() => remover(linha.chave)}
                      disabled={linhas.length === 1}
                      aria-label={`Remover a série ${indice + 1}`}
                    >
                      Remover
                    </button>
                  </div>
                </div>

                {/* Fechado, mostra só o que foi escolhido — clicar tira. */}
                {!aberta && escolhidas.length > 0 && (
                  <div className="serie-tecnicas">
                    {escolhidas.map((tecnica) => (
                      <button
                        key={tecnica.id}
                        type="button"
                        className="tecnica-chip miudo marcada"
                        title={`${tecnica.descricao} Clique para tirar.`}
                        onClick={() => alternarTecnica(linha.chave, tecnica.id)}
                      >
                        {tecnica.nome}
                        {tecnica.distorce_estimativa && <span aria-hidden="true"> ⚠</span>}
                      </button>
                    ))}
                  </div>
                )}

                {aberta && (
                  <div className="serie-expandida">
                    <div className="serie-tecnicas">
                      {doExercicio.map((tecnica) => (
                        <label
                          key={tecnica.id}
                          className={`tecnica-chip miudo ${
                            linha.tecnica_ids.includes(tecnica.id) ? "marcada" : ""
                          }`}
                          title={tecnica.descricao}
                        >
                          <input
                            type="checkbox"
                            checked={linha.tecnica_ids.includes(tecnica.id)}
                            onChange={() => alternarTecnica(linha.chave, tecnica.id)}
                          />
                          {tecnica.nome}
                          {tecnica.distorce_estimativa && (
                            <span aria-hidden="true"> ⚠</span>
                          )}
                        </label>
                      ))}
                    </div>
                    <label className="campo">
                      <span>Observação desta série</span>
                      <input
                        value={linha.observacao}
                        onChange={(evento) =>
                          alterar(linha.chave, "observacao", evento.target.value)
                        }
                        placeholder="Pausa de 2s no fundo"
                        maxLength={200}
                      />
                    </label>
                  </div>
                )}

                {!aberta && linha.observacao.trim() !== "" && (
                  <p className="dica italico">{linha.observacao}</p>
                )}

                {rampa && (
                  <p className="dica">
                    Rampa: a carga não é um número só, então esta série não serve para
                    estimar 1RM e entra no volume pelo ponto médio.
                  </p>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {erro !== null && (
        <p className="aviso erro" role="alert">
          {erro}
        </p>
      )}

      <div className="series-rodape">
        <button type="button" className="botao secundario" onClick={acrescentar}>
          Adicionar série
        </button>
        <span className="tonelagem-viva">
          Tonelagem:{" "}
          <strong>{tonelagem.toLocaleString("pt-BR", { maximumFractionDigits: 0 })} kg</strong>{" "}
          <span>· só as séries que contam no volume</span>
        </span>
        <button
          type="button"
          className="botao"
          onClick={salvar}
          disabled={salvando}
        >
          {salvando ? "Salvando…" : "Salvar séries"}
        </button>
      </div>
    </div>
  );
}
