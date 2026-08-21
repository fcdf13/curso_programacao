/** Uma série ao longo das semanas, em SVG à mão.
 *
 *  Convenção do repositório: sem biblioteca de gráfico. Mantém o bundle pequeno
 *  e as cores presas aos tokens do tema, que é o que faz o mesmo gráfico
 *  funcionar no claro e no escuro.
 *
 *  Duas marcas quando há tendência: o ponto de cada semana e a média móvel. Sob
 *  protanopia o vermelho da linha e o cinza dos pontos ficam a ΔE 6,7 — perto
 *  demais para a cor sozinha resolver. Por isso a diferença é de *forma*
 *  (linha contínua contra pontos soltos) e há legenda: a cor é reforço, não o
 *  único sinal.
 */

import { useId, useMemo, useState } from "react";
import type { PontoDaSerie } from "../../api/tipos";
import "./graficos.css";

interface Props {
  titulo: string;
  unidade: string;
  pontos: PontoDaSerie[];
  tendencia?: PontoDaSerie[];
  /** Faixa fixa, para escalas como 1–5 não esticarem por causa do ruído. */
  minimo?: number;
  maximo?: number;
  casas?: number;
  altura?: number;
  /** Largura do viewBox. Precisa acompanhar o tamanho real do cartão: o texto
   *  do eixo é dado em unidades do viewBox, então um viewBox de 640 dentro de
   *  um cartão de 300px renderiza a fonte pela metade do tamanho pedido. */
  largura?: number;
}

const MARGEM = { topo: 14, direita: 14, base: 26, esquerda: 44 };

const semanaCurta = (iso: string) => {
  const data = new Date(`${iso}T00:00:00`);
  return data.toLocaleDateString("pt-BR", { day: "2-digit", month: "2-digit" });
};

export function GraficoDeLinha({
  titulo,
  unidade,
  pontos,
  tendencia = [],
  minimo,
  maximo,
  casas = 1,
  altura = 190,
  largura: LARGURA = 640,
}: Props) {
  const idBase = useId();
  const [ativo, definirAtivo] = useState<number | null>(null);

  const escala = useMemo(() => {
    const valores = [...pontos, ...tendencia].map((p) => p.valor);
    const cru = { min: Math.min(...valores), max: Math.max(...valores) };

    // Uma folga de 8% impede que o menor e o maior ponto encostem na moldura.
    const folga = (cru.max - cru.min) * 0.08 || 1;
    const min = minimo ?? cru.min - folga;
    const max = maximo ?? cru.max + folga;

    const semanas = pontos.map((p) => p.semana);
    const x = (semana: string) => {
      const indice = semanas.indexOf(semana);
      const largura = LARGURA - MARGEM.esquerda - MARGEM.direita;
      // Uma semana só fica no meio, em vez de dividir por zero.
      if (semanas.length < 2) return MARGEM.esquerda + largura / 2;
      return MARGEM.esquerda + (indice / (semanas.length - 1)) * largura;
    };
    const y = (valor: number) => {
      const alturaUtil = altura - MARGEM.topo - MARGEM.base;
      const fracao = max === min ? 0.5 : (valor - min) / (max - min);
      return MARGEM.topo + (1 - fracao) * alturaUtil;
    };
    return { min, max, x, y };
  }, [pontos, tendencia, minimo, maximo, altura, LARGURA]);

  if (pontos.length === 0) return null;

  const caminho = (lista: PontoDaSerie[]) =>
    lista
      .map((p, i) => `${i === 0 ? "M" : "L"} ${escala.x(p.semana)} ${escala.y(p.valor)}`)
      .join(" ");

  const formatar = (valor: number) =>
    valor.toLocaleString("pt-BR", {
      minimumFractionDigits: casas,
      maximumFractionDigits: casas,
    });

  const destacado = ativo === null ? null : pontos[ativo];
  // Só três rótulos no eixo: um por semana viraria uma faixa ilegível.
  const rotulos = [0, Math.floor((pontos.length - 1) / 2), pontos.length - 1].filter(
    (indice, posicao, lista) => lista.indexOf(indice) === posicao,
  );

  return (
    <figure className="grafico">
      <figcaption>
        <h3>{titulo}</h3>
        <span className="grafico-unidade">{unidade}</span>
        {tendencia.length > 0 && (
          <span className="grafico-legenda">
            <span className="marca-linha" aria-hidden="true" /> média de 4 semanas
            <span className="marca-ponto" aria-hidden="true" /> semana
          </span>
        )}
      </figcaption>

      <svg
        viewBox={`0 0 ${LARGURA} ${altura}`}
        className="grafico-svg"
        role="img"
        aria-label={`${titulo}: de ${formatar(pontos[0]!.valor)} a ${formatar(
          pontos[pontos.length - 1]!.valor,
        )} ${unidade}`}
        onPointerLeave={() => definirAtivo(null)}
        onPointerMove={(evento) => {
          const caixa = evento.currentTarget.getBoundingClientRect();
          // O SVG escala, então a posição do ponteiro precisa voltar para as
          // coordenadas do viewBox antes de virar índice.
          const emViewBox = ((evento.clientX - caixa.left) / caixa.width) * LARGURA;
          const util = LARGURA - MARGEM.esquerda - MARGEM.direita;
          const fracao = (emViewBox - MARGEM.esquerda) / util;
          const indice = Math.round(fracao * Math.max(pontos.length - 1, 1));
          definirAtivo(Math.min(Math.max(indice, 0), pontos.length - 1));
        }}
      >
        {/* Grade: três linhas horizontais, hairline e sólidas. */}
        {[0, 0.5, 1].map((fracao) => {
          const y = MARGEM.topo + fracao * (altura - MARGEM.topo - MARGEM.base);
          const valor = escala.max - fracao * (escala.max - escala.min);
          return (
            <g key={fracao}>
              <line
                x1={MARGEM.esquerda}
                x2={LARGURA - MARGEM.direita}
                y1={y}
                y2={y}
                className="grade"
              />
              <text x={MARGEM.esquerda - 8} y={y + 4} className="eixo" textAnchor="end">
                {formatar(valor)}
              </text>
            </g>
          );
        })}

        {rotulos.map((indice) => (
          <text
            key={indice}
            x={escala.x(pontos[indice]!.semana)}
            y={altura - 8}
            className="eixo"
            textAnchor={indice === 0 ? "start" : indice === pontos.length - 1 ? "end" : "middle"}
          >
            {semanaCurta(pontos[indice]!.semana)}
          </text>
        ))}

        {/* Sem tendência, a própria série vira a linha. */}
        {tendencia.length === 0 && pontos.length > 1 && (
          <path d={caminho(pontos)} className="linha" />
        )}

        {tendencia.length > 0 && <path d={caminho(tendencia)} className="linha" />}

        {pontos.map((ponto, indice) => (
          <circle
            key={ponto.semana}
            cx={escala.x(ponto.semana)}
            cy={escala.y(ponto.valor)}
            r={indice === ativo ? 5 : 3.5}
            className={`ponto ${tendencia.length > 0 ? "cru" : ""} ${
              indice === ativo ? "ativo" : ""
            }`}
          />
        ))}

        {destacado && (
          <line
            x1={escala.x(destacado.semana)}
            x2={escala.x(destacado.semana)}
            y1={MARGEM.topo}
            y2={altura - MARGEM.base}
            className="cursor"
          />
        )}
      </svg>

      <p className="grafico-leitura" aria-live="polite" id={idBase}>
        {destacado ? (
          <>
            <strong>{formatar(destacado.valor)}</strong> {unidade} · semana de{" "}
            {semanaCurta(destacado.semana)}
          </>
        ) : (
          <>
            Último: <strong>{formatar(pontos[pontos.length - 1]!.valor)}</strong> {unidade}
          </>
        )}
      </p>
    </figure>
  );
}
