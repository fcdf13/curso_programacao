/** O plano do dia: o que venceu de revisão, e o que vem de novo. */

import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { api } from "../api/cliente";
import type { PlanoDoDia } from "../api/tipos";
import { LinhaDoExercicio } from "../componentes/LinhaDoExercicio";
import "../componentes/lista.css";

export function Hoje() {
  const [plano, setPlano] = useState<PlanoDoDia | null>(null);
  const [erro, setErro] = useState("");
  const navegar = useNavigate();

  useEffect(() => {
    api.hoje(6).then(setPlano).catch((e: Error) => setErro(e.message));
  }, []);

  if (erro) return <div className="pagina erro-global">{erro}</div>;
  if (!plano) return <p className="carregando">carregando…</p>;

  const primeiro = plano.revisoes[0] ?? plano.novos[0];
  const atrasoDe = (dias: number | null) =>
    dias === null || dias >= 0 ? "vence hoje" : `${-dias} dia(s) de atraso`;

  return (
    <div className="pagina">
      <header className="topo-da-pagina">
        <h1>Plano de hoje</h1>
        {plano.sequencia > 0 && (
          <p className="suave">
            <strong>{plano.sequencia}</strong>{" "}
            {plano.sequencia === 1 ? "dia seguido" : "dias seguidos"} de prática.
          </p>
        )}
      </header>

      {primeiro && (
        <button
          className="principal comecar"
          onClick={() => navegar(`/exercicio/${primeiro.id}`)}
        >
          Começar por {primeiro.id} · {primeiro.titulo}
        </button>
      )}

      {plano.revisoes.length > 0 && (
        <section className="secao">
          <h2 className="titulo-secao">Revisar ({plano.revisoes.length})</h2>
          <div className="lista">
            {plano.revisoes.map((ex) => (
              <LinhaDoExercicio key={ex.id} ex={ex} nota={atrasoDe(ex.dias_ate_revisao)} />
            ))}
          </div>
        </section>
      )}

      <section className="secao">
        <h2 className="titulo-secao">Aprender ({plano.novos.length})</h2>
        {plano.novos.length > 0 ? (
          <div className="lista">
            {plano.novos.map((ex) => (
              <LinhaDoExercicio key={ex.id} ex={ex} />
            ))}
          </div>
        ) : (
          <div className="lista">
            <p className="lista-vazia">
              Você resolveu tudo que existe hoje. <Link to="/revisao">Revisar</Link> ou{" "}
              <Link to="/catalogo">rever o catálogo</Link>.
            </p>
          </div>
        )}
      </section>
    </div>
  );
}
