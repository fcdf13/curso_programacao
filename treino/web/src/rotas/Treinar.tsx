/** Modo academia: o treino aberto no celular, série por série.
 *
 *  A tela é feita para uma mão suada e um minuto de descanso: número grande,
 *  botão grande, e o registro **nunca espera a rede**. Cada série vai primeiro
 *  para a fila no aparelho e depois para o servidor; se o sinal cair no meio do
 *  agachamento, o aluno não descobre isso — descobre quando reconectar, e nada
 *  se perdeu.
 *
 *  Os campos já vêm preenchidos com o que foi prescrito, porque no caso comum o
 *  aluno fez exatamente aquilo e só precisa confirmar.
 */

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { Link, useParams } from "react-router-dom";

import { api, ErroDaApi } from "../api/cliente";
import * as fila from "../api/fila";
import type {
  Prescricao,
  Serie,
  SerieParaEnviar,
  SessaoModelo,
  TreinoRealizado,
} from "../api/tipos";
import { CronometroDeDescanso } from "../componentes/CronometroDeDescanso";
import { useSessao } from "../sessao";
import "./treinar.css";
import "./paginas.css";

/** Chave da série, gerada aqui. `randomUUID` não existe em http:// antigo. */
function novaChave(): string {
  if (typeof crypto !== "undefined" && "randomUUID" in crypto) {
    return crypto.randomUUID();
  }
  return `s-${Date.now()}-${Math.random().toString(36).slice(2, 10)}`;
}

/** A carga que a série prescrita pede. Numa rampa, o alvo é o topo. */
function cargaPrescrita(serie: Serie): number | null {
  return serie.carga_ate_kg ?? serie.carga_kg;
}

interface Rascunho {
  reps: string;
  carga: string;
  rir: string;
}

function doPrescrito(serie: Serie, prescricao: Prescricao): Rascunho {
  const carga = cargaPrescrita(serie);
  return {
    reps: serie.reps === null ? "" : String(serie.reps),
    carga: carga === null ? "" : String(carga),
    rir: String(serie.rir ?? prescricao.rir_alvo ?? ""),
  };
}

const numeroOuNulo = (valor: string) =>
  valor.trim() === "" ? null : Number(valor.replace(",", "."));

export function Treinar() {
  const { id } = useParams<{ id: string }>();
  const { eu } = useSessao();
  const alunoId = eu?.aluno_id ?? null;

  const [modelo, definirModelo] = useState<SessaoModelo | null>(null);
  const [treino, definirTreino] = useState<TreinoRealizado | null>(null);
  const [erro, definirErro] = useState<string | null>(null);
  // A fila do aparelho, e não só o tamanho dela: sem sinal, é ela que sabe o
  // que o aluno já registrou — e é justamente sem sinal que ele mais precisa
  // ver o que já fez para não repetir a série.
  const [naFila, definirNaFila] = useState<fila.Pendente[]>([]);
  const [online, definirOnline] = useState(
    typeof navigator === "undefined" ? true : navigator.onLine,
  );
  const [descanso, definirDescanso] = useState<number | null>(null);
  const [encerrando, definirEncerrando] = useState(false);
  const [observacoes, definirObservacoes] = useState("");

  // Um rascunho por série prescrita, chaveado por `prescricao:serie`.
  const [rascunhos, definirRascunhos] = useState<Record<string, Rascunho>>({});

  const sincronizando = useRef(false);

  const lerFila = useCallback(async (treinoId: number) => {
    if (!fila.disponivel()) return;
    definirNaFila(await fila.pendentes(treinoId));
  }, []);

  /** Manda o que está na fila. Silenciosa: falhar aqui é normal, não é erro. */
  const escoar = useCallback(
    async (treinoId: number) => {
      if (!fila.disponivel() || sincronizando.current) return;
      sincronizando.current = true;
      try {
        const espera = await fila.pendentes(treinoId);
        if (espera.length === 0) return;

        const atualizado = await api.sincronizarSeries(
          treinoId,
          espera.map((item) => item.serie),
        );
        definirTreino(atualizado);
        // Só sai da fila o que voltou confirmado pelo servidor.
        const confirmadas = new Set(atualizado.series.map((s) => s.chave_local));
        await fila.confirmar(
          treinoId,
          espera.map((i) => i.serie.chave_local).filter((c) => confirmadas.has(c)),
        );
      } catch {
        // Sem rede, ou servidor fora: a fila continua onde está e tenta depois.
      } finally {
        sincronizando.current = false;
        await lerFila(treinoId);
      }
    },
    [lerFila],
  );

  useEffect(() => {
    if (alunoId === null || id === undefined) return;

    let vivo = true;
    (async () => {
      const sessao = await api.verSessao(Number(id));
      if (!vivo) return;
      definirModelo(sessao);

      const aberto = await api.abrirTreino(alunoId, sessao.id);
      if (!vivo) return;
      definirTreino(aberto);
      definirObservacoes(aberto.observacoes ?? "");
      await escoar(aberto.id);
    })().catch((falha) =>
      definirErro(
        falha instanceof ErroDaApi ? falha.message : "Não foi possível abrir o treino.",
      ),
    );

    return () => {
      vivo = false;
    };
  }, [alunoId, id, escoar]);

  // Voltou o sinal: tenta escoar sem o aluno pedir.
  useEffect(() => {
    function voltou() {
      definirOnline(true);
      if (treino !== null) void escoar(treino.id);
    }
    function caiu() {
      definirOnline(false);
    }
    window.addEventListener("online", voltou);
    window.addEventListener("offline", caiu);
    return () => {
      window.removeEventListener("online", voltou);
      window.removeEventListener("offline", caiu);
    };
  }, [treino, escoar]);

  const registradas = useMemo(() => {
    const mapa = new Map<number, TreinoRealizado["series"][number]>();
    for (const serie of treino?.series ?? []) {
      if (serie.serie_id !== null) mapa.set(serie.serie_id, serie);
    }
    return mapa;
  }, [treino]);

  /** O que está no aparelho esperando envio, por série prescrita. */
  const esperando = useMemo(() => {
    const mapa = new Map<number, SerieParaEnviar>();
    for (const item of naFila) {
      if (item.serie.serie_id != null) mapa.set(item.serie.serie_id, item.serie);
    }
    return mapa;
  }, [naFila]);

  function rascunho(prescricao: Prescricao, serie: Serie): Rascunho {
    const chave = `${prescricao.id}:${serie.id}`;
    const existente = rascunhos[chave];
    if (existente !== undefined) return existente;

    // Já registrada: mostra o que foi feito, não o que foi pedido. A fila do
    // aparelho ganha do servidor — é ela que tem o valor mais recente.
    const feita = esperando.get(serie.id) ?? registradas.get(serie.id);
    if (feita !== undefined) {
      return {
        reps: feita.reps === null ? "" : String(feita.reps),
        carga: feita.carga_kg === null ? "" : String(feita.carga_kg),
        rir: feita.rir == null ? "" : String(feita.rir),
      };
    }
    return doPrescrito(serie, prescricao);
  }

  function mudar(prescricao: Prescricao, serie: Serie, campo: keyof Rascunho, valor: string) {
    const chave = `${prescricao.id}:${serie.id}`;
    definirRascunhos((atual) => ({
      ...atual,
      [chave]: { ...rascunho(prescricao, serie), [campo]: valor },
    }));
  }

  async function registrar(prescricao: Prescricao, serie: Serie, ordem: number) {
    if (treino === null) return;
    definirErro(null);

    const atual = rascunho(prescricao, serie);
    const feita = esperando.get(serie.id) ?? registradas.get(serie.id);
    const paraEnviar: SerieParaEnviar = {
      // Corrigir uma série reaproveita a chave: o servidor atualiza em vez de
      // criar uma segunda.
      chave_local: feita?.chave_local ?? novaChave(),
      ordem,
      exercicio_id: prescricao.exercicio.id,
      prescricao_id: prescricao.id,
      serie_id: serie.id,
      reps: numeroOuNulo(atual.reps),
      carga_kg: numeroOuNulo(atual.carga),
      rir: numeroOuNulo(atual.rir),
      tipo: serie.tipo,
    };

    // Grava no aparelho antes de tentar a rede. Se o app morrer agora, a série
    // está salva; se a rede morrer, ela sai depois.
    if (fila.disponivel()) {
      await fila.enfileirar(treino.id, paraEnviar);
      await lerFila(treino.id);
      await escoar(treino.id);
    } else {
      try {
        definirTreino(await api.sincronizarSeries(treino.id, [paraEnviar]));
      } catch (falha) {
        definirErro(
          falha instanceof ErroDaApi
            ? falha.message
            : "Não deu para registrar, e este navegador não guarda fila offline.",
        );
        return;
      }
    }

    if (prescricao.descanso_s !== null && prescricao.descanso_s > 0) {
      definirDescanso(prescricao.descanso_s);
    }
  }

  async function encerrar() {
    if (treino === null) return;
    definirErro(null);
    try {
      await escoar(treino.id);
      definirTreino(await api.encerrarTreino(treino.id, observacoes.trim() || null));
      definirEncerrando(false);
    } catch (falha) {
      definirErro(
        falha instanceof ErroDaApi ? falha.message : "Não foi possível encerrar.",
      );
    }
  }

  async function reabrir() {
    if (treino === null) return;
    try {
      definirTreino(await api.reabrirTreino(treino.id));
    } catch (falha) {
      definirErro(falha instanceof ErroDaApi ? falha.message : "Não foi possível reabrir.");
    }
  }

  if (erro !== null && treino === null) {
    return (
      <main className="conteudo pilha">
        <p className="aviso erro" role="alert">
          {erro}
        </p>
        <p>
          <Link to="/inicio">Voltar</Link>
        </p>
      </main>
    );
  }

  if (modelo === null || treino === null) {
    return (
      <main className="conteudo">
        <p className="carregando">Abrindo o treino…</p>
      </main>
    );
  }

  // Conta o que o aluno fez, não o que o servidor confirmou: sem sinal, os
  // dois números são diferentes, e o que interessa a ele é o primeiro.
  const confirmadas = new Set(treino.series.map((s) => s.serie_id));
  const feitas =
    treino.series.length +
    naFila.filter((item) => !confirmadas.has(item.serie.serie_id ?? null)).length;
  const totais = modelo.prescricoes.reduce(
    (soma, p) => soma + (p.series_detalhadas.length || p.series),
    0,
  );

  return (
    <main className="conteudo pilha treinar">
      <div className="titulo-da-pagina">
        <div>
          <p className="rotulo">Modo academia</p>
          <h1>{modelo.nome}</h1>
        </div>
      </div>

      <div className="painel placar">
        <div>
          <p className="rotulo">Séries</p>
          <p className="placar-valor">
            {feitas}
            <span className="placar-de">/{totais}</span>
          </p>
        </div>
        <div>
          <p className="rotulo">Levantado</p>
          <p className="placar-valor">
            {Math.round(treino.tonelagem).toLocaleString("pt-BR")}
            <span className="placar-de"> kg</span>
          </p>
        </div>
        {(naFila.length > 0 || !online) && (
          <div>
            <p className="rotulo">Fila</p>
            <p className="placar-valor pendente">
              {naFila.length}
              <span className="placar-de">{online ? " enviando" : " sem sinal"}</span>
            </p>
          </div>
        )}
      </div>

      {!online && (
        <p className="aviso" role="status">
          <strong>Sem sinal.</strong> Pode continuar: o que você registrar fica
          guardado no celular e sobe sozinho quando a conexão voltar.
        </p>
      )}

      {erro !== null && (
        <p className="aviso erro" role="alert">
          {erro}
        </p>
      )}

      {treino.encerrada && (
        <div className="painel pilha">
          <p>
            <strong>Treino encerrado.</strong> {treino.observacoes ?? ""}
          </p>
          <div className="acoes">
            <button type="button" className="botao secundario" onClick={reabrir}>
              Reabrir para corrigir
            </button>
          </div>
        </div>
      )}

      {modelo.prescricoes.map((prescricao) => {
        const series =
          prescricao.series_detalhadas.length > 0 ? prescricao.series_detalhadas : [];
        return (
          <section key={prescricao.id} className="painel pilha exercicio-do-treino">
            <header>
              <h2>{prescricao.exercicio.nome}</h2>
              <p className="prescricao-detalhe">
                {prescricao.series} × {prescricao.reps_min}–{prescricao.reps_max}
                {prescricao.rir_alvo !== null && ` · RIR ${prescricao.rir_alvo}`}
                {prescricao.descanso_s !== null && ` · ${prescricao.descanso_s}s`}
                {prescricao.tecnicas.length > 0 &&
                  ` · ${prescricao.tecnicas.map((t) => t.nome).join(", ")}`}
              </p>
              {prescricao.observacao !== null && (
                <p className="dica">{prescricao.observacao}</p>
              )}
            </header>

            {series.length === 0 ? (
              <p className="dica">
                Sem séries detalhadas. Peça ao João para preencher a progressão.
              </p>
            ) : (
              series.map((serie, indice) => {
                const atual = rascunho(prescricao, serie);
                const confirmada = registradas.get(serie.id) !== undefined;
                const naEspera = esperando.has(serie.id);
                const feita = confirmada || naEspera;
                return (
                  <div
                    key={serie.id}
                    className={
                      "serie-da-academia" +
                      (confirmada ? " feita" : naEspera ? " na-fila" : "")
                    }
                  >
                    <span className="serie-numero">{indice + 1}</span>

                    <label className="campo-grande">
                      <span>reps</span>
                      <input
                        type="number"
                        inputMode="numeric"
                        value={atual.reps}
                        onChange={(e) => mudar(prescricao, serie, "reps", e.target.value)}
                        disabled={treino.encerrada}
                      />
                    </label>
                    <label className="campo-grande">
                      <span>kg</span>
                      <input
                        type="number"
                        inputMode="decimal"
                        value={atual.carga}
                        onChange={(e) => mudar(prescricao, serie, "carga", e.target.value)}
                        disabled={treino.encerrada}
                      />
                    </label>
                    <label className="campo-grande estreito">
                      <span>RIR</span>
                      <input
                        type="number"
                        inputMode="numeric"
                        value={atual.rir}
                        onChange={(e) => mudar(prescricao, serie, "rir", e.target.value)}
                        disabled={treino.encerrada}
                      />
                    </label>

                    <button
                      type="button"
                      className={`botao registrar${feita ? " secundario" : ""}`}
                      onClick={() => registrar(prescricao, serie, indice)}
                      disabled={treino.encerrada}
                      title={
                        naEspera && !confirmada
                          ? "Registrada no celular, aguardando sinal"
                          : undefined
                      }
                    >
                      {/* Sem sinal a série está guardada, mas ainda não chegou:
                          "✓" ali prometeria o que não aconteceu. */}
                      {confirmada ? "✓" : naEspera ? "⋯" : "OK"}
                    </button>
                  </div>
                );
              })
            )}
          </section>
        );
      })}

      {!treino.encerrada && (
        <section className="painel pilha">
          {!encerrando ? (
            <div className="acoes">
              <button
                type="button"
                className="botao"
                onClick={() => definirEncerrando(true)}
              >
                Encerrar o treino
              </button>
            </div>
          ) : (
            <>
              <label className="campo">
                <span>Como foi? (opcional)</span>
                <textarea
                  rows={3}
                  value={observacoes}
                  onChange={(evento) => definirObservacoes(evento.target.value)}
                  placeholder="ombro incomodou na última série"
                  maxLength={2000}
                />
              </label>
              <div className="acoes">
                <button type="button" className="botao" onClick={encerrar}>
                  Encerrar
                </button>
                <button
                  type="button"
                  className="botao secundario"
                  onClick={() => definirEncerrando(false)}
                >
                  Voltar
                </button>
              </div>
            </>
          )}
        </section>
      )}

      {descanso !== null && (
        <CronometroDeDescanso
          key={`${descanso}-${feitas}`}
          segundos={descanso}
          aoFechar={() => definirDescanso(null)}
        />
      )}
    </main>
  );
}
