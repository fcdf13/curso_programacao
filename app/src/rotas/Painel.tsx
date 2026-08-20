/** O painel: onde você está, o que vem, e se está mantendo o ritmo. */

import { useEffect, useState } from "react";

import { api } from "../api/cliente";
import type { PainelDeProgresso } from "../api/tipos";
import { BarrasPorModulo } from "../componentes/graficos/BarrasPorModulo";
import { CalendarioDePratica } from "../componentes/graficos/CalendarioDePratica";
import { PrevisaoDeRevisoes } from "../componentes/graficos/PrevisaoDeRevisoes";
import "../componentes/graficos/graficos.css";
import "./painel.css";

function Numero({ valor, rotulo }: { valor: number | string; rotulo: string }) {
  return (
    <div className="numero-grande">
      <strong>{valor}</strong>
      <span>{rotulo}</span>
    </div>
  );
}

export function Painel() {
  const [dados, setDados] = useState<PainelDeProgresso | null>(null);
  const [erro, setErro] = useState("");

  useEffect(() => {
    api.progresso().then(setDados).catch((e: Error) => setErro(e.message));
  }, []);

  if (erro) return <div className="pagina erro-global">{erro}</div>;
  if (!dados) return <p className="carregando">carregando…</p>;

  const percentual = dados.total === 0 ? 0 : Math.round((dados.feitos / dados.total) * 100);

  return (
    <div className="pagina">
      <header className="topo-da-pagina">
        <h1>Progresso</h1>
      </header>

      <section className="numeros">
        <Numero valor={`${dados.feitos}/${dados.total}`} rotulo={`exercícios · ${percentual}%`} />
        <Numero
          valor={dados.sequencia}
          rotulo={dados.sequencia === 1 ? "dia seguido" : "dias seguidos"}
        />
        <Numero valor={dados.vencidas} rotulo="a revisar hoje" />
        <Numero valor={dados.agendados} rotulo="agendados" />
      </section>

      <div className="grade-de-graficos">
        <PrevisaoDeRevisoes dias={dados.previsao} />
        <CalendarioDePratica dias={dados.dias_praticados} />
      </div>

      <div className="grade-de-graficos uma-coluna">
        <BarrasPorModulo modulos={dados.modulos} />
      </div>
    </div>
  );
}
