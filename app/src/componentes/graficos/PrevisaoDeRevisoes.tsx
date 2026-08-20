/** Quantos exercícios voltam para revisão em cada um dos próximos 30 dias.
 *
 *  Uma série só, magnitude ao longo do tempo → colunas. Sem legenda (o título
 *  nomeia a série) e sem rótulo em cada barra: os números vivem no tooltip, e o
 *  eixo marca de 7 em 7 dias.
 */

import type { DiaDaPrevisao } from "../../api/tipos";

const LARGURA = 620;
const ALTURA = 130;
const TOPO = 10;
const BASE = ALTURA - 22;
const VAO = 2; // respiro entre colunas, como manda a especificação de marcas

function rotulo(iso: string, indice: number): string {
  if (indice === 0) return "hoje";
  const [, mes, dia] = iso.split("-");
  return `${Number(dia)}/${Number(mes)}`;
}

function porExtenso(iso: string): string {
  const [ano, mes, dia] = iso.split("-").map(Number);
  return new Date(ano, mes - 1, dia).toLocaleDateString("pt-BR", {
    day: "numeric",
    month: "long",
  });
}

export function PrevisaoDeRevisoes({ dias }: { dias: DiaDaPrevisao[] }) {
  const total = dias.reduce((soma, d) => soma + d.quantidade, 0);
  const maximo = Math.max(1, ...dias.map((d) => d.quantidade));
  const largura = LARGURA / dias.length;

  if (total === 0) {
    return (
      <div className="grafico">
        <h3 className="grafico-titulo">Revisões nos próximos 30 dias</h3>
        <p className="grafico-vazio">
          Nada agendado ainda — o primeiro exercício que você acertar aparece aqui.
        </p>
      </div>
    );
  }

  return (
    <div className="grafico">
      <h3 className="grafico-titulo">Revisões nos próximos 30 dias</h3>
      <p className="grafico-nota">
        {total} {total === 1 ? "revisão agendada" : "revisões agendadas"} · pico de{" "}
        {maximo} num dia
      </p>
      <svg
        viewBox={`0 0 ${LARGURA} ${ALTURA}`}
        className="svg-grafico"
        role="img"
        aria-label={`Previsão de revisões: ${total} agendadas nos próximos 30 dias`}
      >
        <line
          x1="0"
          y1={BASE}
          x2={LARGURA}
          y2={BASE}
          className="eixo"
        />
        {dias.map((dia, i) => {
          const altura =
            dia.quantidade === 0 ? 0 : ((BASE - TOPO) * dia.quantidade) / maximo;
          return (
            <g key={dia.data} className="coluna">
              {/* Alvo de mouse maior que a marca, para o tooltip pegar fácil. */}
              <rect
                x={i * largura}
                y={TOPO}
                width={largura}
                height={BASE - TOPO}
                className="alvo"
              />
              {altura > 0 && (
                <rect
                  x={i * largura + VAO / 2}
                  y={BASE - altura}
                  width={largura - VAO}
                  height={altura}
                  rx="2"
                  className="marca"
                />
              )}
              <title>
                {porExtenso(dia.data)}: {dia.quantidade}{" "}
                {dia.quantidade === 1 ? "revisão" : "revisões"}
              </title>
            </g>
          );
        })}
        {dias.map((dia, i) =>
          i % 7 === 0 ? (
            <text
              key={`r-${dia.data}`}
              x={i * largura + largura / 2}
              y={ALTURA - 6}
              className="rotulo-eixo"
              textAnchor="middle"
            >
              {rotulo(dia.data, i)}
            </text>
          ) : null,
        )}
      </svg>
    </div>
  );
}
