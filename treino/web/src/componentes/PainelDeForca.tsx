/** A força estimada por exercício, e como ela mudou.
 *
 *  É o gráfico que só existe porque o aluno registra as séries: cada ponto é o
 *  1RM estimado do melhor conjunto daquele dia. Vem com a série de origem à
 *  vista — "100,5 kg (5 × 85)" — porque um número estimado que não deixa
 *  conferir de onde veio pede mais fé do que o aluno deve ter num app.
 */

import { useEffect, useState } from "react";

import { api, ErroDaApi } from "../api/cliente";
import type { ForcaDoExercicio } from "../api/tipos";
import { GraficoDeLinha } from "./graficos/GraficoDeLinha";
import "./forca.css";

const numero = (valor: number) =>
  valor.toLocaleString("pt-BR", { maximumFractionDigits: 1 });

function Variacao({ kg }: { kg: number | null }) {
  if (kg === null) {
    // Um treino não é uma tendência, e fingir que é seria pior que calar.
    return <span className="prescricao-detalhe">um registro só</span>;
  }
  if (kg === 0) return <span className="prescricao-detalhe">sem mudança</span>;

  const subiu = kg > 0;
  return (
    <span className={`variacao ${subiu ? "subiu" : "caiu"}`}>
      {subiu ? "↑" : "↓"} {numero(Math.abs(kg))} kg
    </span>
  );
}

export function PainelDeForca({ alunoId }: { alunoId: number }) {
  const [exercicios, definirExercicios] = useState<ForcaDoExercicio[] | null>(null);
  const [aberto, definirAberto] = useState<number | null>(null);
  const [erro, definirErro] = useState<string | null>(null);

  useEffect(() => {
    api
      .forcaDoAluno(alunoId)
      .then(definirExercicios)
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

  if (exercicios === null) return <p className="carregando">Carregando…</p>;

  if (exercicios.length === 0) {
    return (
      <div className="vazio">
        <p>
          <strong>Ainda não há série registrada.</strong>
        </p>
        <p>
          O 1RM estimado aparece aqui assim que o treino for registrado no modo
          academia — é do que foi levantado de verdade que ele sai.
        </p>
      </div>
    );
  }

  return (
    <div className="pilha">
      {exercicios.map((exercicio) => {
        const escancarado = aberto === exercicio.exercicio_id;
        return (
          <div key={exercicio.exercicio_id} className="painel pilha">
            <button
              type="button"
              className="linha-de-forca"
              onClick={() =>
                definirAberto(escancarado ? null : exercicio.exercicio_id)
              }
              aria-expanded={escancarado}
            >
              <span className="forca-nome">{exercicio.exercicio}</span>
              <span className="forca-numero">
                {exercicio.atual === null ? "—" : `${numero(exercicio.atual.e1rm)} kg`}
              </span>
              <Variacao kg={exercicio.variacao_kg} />
            </button>

            {exercicio.atual !== null && (
              <p className="prescricao-detalhe">
                De {exercicio.atual.reps} × {numero(exercicio.atual.carga_kg)} kg
                {" · "}
                {exercicio.pontos.length} registro
                {exercicio.pontos.length === 1 ? "" : "s"}
              </p>
            )}

            {exercicio.atual?.ressalva != null && (
              <p className="dica">{exercicio.atual.ressalva}</p>
            )}

            {escancarado && exercicio.pontos.length > 1 && (
              <GraficoDeLinha
                titulo="1RM estimado"
                unidade="kg"
                pontos={exercicio.pontos.map((ponto) => ({
                  semana: ponto.dia,
                  valor: ponto.e1rm,
                }))}
              />
            )}
          </div>
        );
      })}
    </div>
  );
}
