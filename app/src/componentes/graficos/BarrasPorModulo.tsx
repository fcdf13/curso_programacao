/** Quanto de cada módulo você já fechou.
 *
 *  Magnitude com um rótulo por linha: aqui o número é o assunto, então ele é
 *  rotulado direto em vez de ficar só no tooltip.
 */

import type { ModuloNoPainel } from "../../api/tipos";

export function BarrasPorModulo({ modulos }: { modulos: ModuloNoPainel[] }) {
  const porBloco = new Map<string, ModuloNoPainel[]>();
  for (const m of modulos) {
    porBloco.set(m.nome_do_bloco, [...(porBloco.get(m.nome_do_bloco) ?? []), m]);
  }

  return (
    <div className="grafico">
      <h3 className="grafico-titulo">Progresso por módulo</h3>
      <p className="grafico-nota">exercícios resolvidos ao menos uma vez</p>
      <div className="barras-de-modulo">
        {[...porBloco.entries()].map(([bloco, lista]) => (
          <div className="grupo-de-bloco" key={bloco}>
            <h4 className="titulo-secao">{bloco}</h4>
            {lista.map((m) => {
              const fracao = m.total === 0 ? 0 : m.feitos / m.total;
              return (
                <div className="barra-linha" key={m.modulo}>
                  <span className="barra-nome" title={m.nome_do_modulo}>
                    {m.nome_do_modulo}
                  </span>
                  <div
                    className="barra-trilho"
                    role="img"
                    aria-label={`${m.nome_do_modulo}: ${m.feitos} de ${m.total}`}
                  >
                    <div
                      className={`barra-preenchida ${fracao === 1 ? "completa" : ""}`}
                      style={{ width: `${Math.max(fracao * 100, fracao > 0 ? 2 : 0)}%` }}
                    />
                  </div>
                  <span className="barra-contagem">
                    {m.feitos}/{m.total}
                  </span>
                </div>
              );
            })}
          </div>
        ))}
      </div>
    </div>
  );
}
