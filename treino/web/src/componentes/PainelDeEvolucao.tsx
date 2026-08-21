/** A evolução do aluno em gráfico. A mesma tela para os dois lados.
 *
 *  O peso vem primeiro e ocupa a linha inteira: é o número que oscila mais e o
 *  que mais se interpreta errado sem a média móvel.
 */

import { useEffect, useState } from "react";

import { api, ErroDaApi } from "../api/cliente";
import type { Evolucao } from "../api/tipos";
import { GraficoDeLinha } from "./graficos/GraficoDeLinha";
import "./graficos/graficos.css";

/** Séries de 1 a 5 recebem faixa fixa: deixar a escala automática faria uma
 *  variação de 3 para 4 parecer um salto do chão ao teto. */
const FAIXA_FIXA: Record<string, [number, number]> = {
  qualidade_do_sono: [1, 5],
  disposicao: [1, 5],
  recuperacao: [1, 5],
  aderencia_dieta: [0, 100],
  aderencia_treino: [0, 100],
};

const CASAS: Record<string, number> = {
  peso_kg: 1,
  horas_de_sono: 1,
  passos_por_dia: 0,
  qualidade_do_sono: 0,
  disposicao: 0,
  recuperacao: 0,
  aderencia_dieta: 0,
  aderencia_treino: 0,
};

export function PainelDeEvolucao({ alunoId }: { alunoId: number }) {
  const [evolucao, definirEvolucao] = useState<Evolucao | null>(null);
  const [erro, definirErro] = useState<string | null>(null);

  useEffect(() => {
    definirEvolucao(null);
    api
      .evolucao(alunoId)
      .then(definirEvolucao)
      .catch((falha) =>
        definirErro(
          falha instanceof ErroDaApi ? falha.message : "Não foi possível carregar.",
        ),
      );
  }, [alunoId]);

  if (erro !== null) {
    return (
      <p className="aviso erro" role="alert">
        {erro}
      </p>
    );
  }

  if (evolucao === null) return <p className="carregando">Carregando…</p>;

  if (evolucao.series.length === 0) {
    return (
      <div className="vazio">
        <p>
          <strong>Ainda não há check-in.</strong>
        </p>
        <p>
          O gráfico aparece a partir do primeiro. A média móvel do peso pede quatro
          semanas — antes disso o que se vê é ruído, não tendência.
        </p>
      </div>
    );
  }

  const peso = evolucao.series.find((serie) => serie.chave === "peso_kg");
  const resto = evolucao.series.filter((serie) => serie.chave !== "peso_kg");

  return (
    <div className="pilha">
      <Placas evolucao={evolucao} />

      <div className="grade-de-graficos">
        {peso && (
          <div className="cartao-de-grafico largo">
            <GraficoDeLinha
              titulo="Peso"
              unidade="kg"
              pontos={peso.pontos}
              tendencia={peso.tendencia}
              casas={1}
              altura={210}
            />
          </div>
        )}

        {resto.map((serie) => {
          const faixa = FAIXA_FIXA[serie.chave];
          return (
            <div className="cartao-de-grafico" key={serie.chave}>
              <GraficoDeLinha
                titulo={serie.rotulo}
                unidade={serie.unidade}
                pontos={serie.pontos}
                minimo={faixa?.[0]}
                maximo={faixa?.[1]}
                casas={CASAS[serie.chave] ?? 1}
                largura={340}
              />
            </div>
          );
        })}
      </div>
    </div>
  );
}

function Placas({ evolucao }: { evolucao: Evolucao }) {
  const comVariacao = evolucao.series.filter(
    (serie) => evolucao.variacao[serie.chave] !== undefined,
  );
  if (comVariacao.length === 0) return null;

  return (
    <div className="placas">
      {comVariacao.map((serie) => {
        const primeiro = serie.pontos[0]!.valor;
        const ultimo = serie.pontos[serie.pontos.length - 1]!.valor;
        const delta = evolucao.variacao[serie.chave]!;
        const casas = CASAS[serie.chave] ?? 1;
        const formatar = (valor: number) =>
          valor.toLocaleString("pt-BR", {
            minimumFractionDigits: casas,
            maximumFractionDigits: casas,
          });

        return (
          <div className="placa" key={serie.chave}>
            <p className="rotulo">{serie.rotulo}</p>
            <p className="placa-valor">
              {formatar(ultimo)}
              {serie.unidade !== "1–5" && (
                <span className="placa-unidade"> {serie.unidade}</span>
              )}
            </p>
            <span className="placa-variacao">
              {/* Seta neutra: peso caindo num corte é o objetivo, sono caindo
                  não é. Pintar de verde e vermelho decidiria pelo João. */}
              <span className="seta" aria-hidden="true">
                {delta > 0 ? "↑" : delta < 0 ? "↓" : "="}
              </span>{" "}
              de {formatar(primeiro)} em {serie.pontos.length} semanas
            </span>
          </div>
        );
      })}
    </div>
  );
}
