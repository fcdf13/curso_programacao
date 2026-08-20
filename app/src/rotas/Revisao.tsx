/** A fila de revisões vencidas.
 *
 *  Entrar numa revisão arquiva a resposta anterior e devolve o esqueleto — é o
 *  mesmo comportamento de `curso revisar`, e é o que faz revisar ser resolver de
 *  novo em vez de reler.
 */

import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { api } from "../api/cliente";
import type { Resumo } from "../api/tipos";
import { LinhaDoExercicio } from "../componentes/LinhaDoExercicio";
import "../componentes/lista.css";

export function Revisao() {
  const [fila, setFila] = useState<Resumo[] | null>(null);
  const [erro, setErro] = useState("");
  const [preparando, setPreparando] = useState(false);
  const navegar = useNavigate();

  useEffect(() => {
    api.revisao().then(setFila).catch((e: Error) => setErro(e.message));
  }, []);

  const comecar = async (id: string) => {
    setPreparando(true);
    try {
      await api.prepararRevisao(id);
      navegar(`/exercicio/${id}`);
    } catch (e) {
      setErro((e as Error).message);
      setPreparando(false);
    }
  };

  if (erro) return <div className="pagina erro-global">{erro}</div>;
  if (!fila) return <p className="carregando">carregando…</p>;

  return (
    <div className="pagina">
      <header className="topo-da-pagina">
        <h1>Revisão</h1>
        <p className="suave">
          {fila.length === 0
            ? "Nada vencido hoje."
            : `${fila.length} ${fila.length === 1 ? "exercício venceu" : "exercícios venceram"}.`}
        </p>
      </header>

      {fila.length > 0 && (
        <>
          <p className="explicacao">
            Ao começar, sua resposta anterior é guardada em <code>.curso/historico/</code> e
            o exercício volta em branco. Revisar aqui é resolver de novo, do zero.
          </p>
          <button
            className="principal comecar"
            disabled={preparando}
            onClick={() => void comecar(fila[0].id)}
          >
            {preparando ? "Preparando…" : `Revisar ${fila[0].id} · ${fila[0].titulo}`}
          </button>
          <div className="lista">
            {fila.map((ex) => (
              <LinhaDoExercicio
                key={ex.id}
                ex={ex}
                nota={
                  ex.dias_ate_revisao !== null && ex.dias_ate_revisao < 0
                    ? `${-ex.dias_ate_revisao} dia(s) de atraso`
                    : "vence hoje"
                }
              />
            ))}
          </div>
        </>
      )}
    </div>
  );
}
