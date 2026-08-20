/** Uma linha de exercício nas listagens (plano do dia, catálogo, revisão). */

import { Link } from "react-router-dom";

import type { Resumo } from "../api/tipos";
import { Nivel } from "./Nivel";

const MARCA: Record<Resumo["estado"], string> = {
  novo: "",
  em_andamento: "•",
  resolvido: "✓",
};

export function LinhaDoExercicio({ ex, nota }: { ex: Resumo; nota?: string }) {
  return (
    <Link to={`/exercicio/${ex.id}`} className={`linha ${ex.estado}`}>
      <span className="marca" aria-hidden="true">
        {MARCA[ex.estado]}
      </span>
      <span className="id mono">{ex.id}</span>
      <span className="titulo">{ex.titulo}</span>
      <Nivel nivel={ex.nivel} />
      <span className="nota fraco">{nota ?? `~${ex.tempo_min} min`}</span>
    </Link>
  );
}
