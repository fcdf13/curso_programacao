/** A calculadora de carga — a ferramenta do João.
 *
 *  Ele informa uma série que o aluno fez de verdade (carga × repetições) e
 *  recebe o 1RM estimado e a carga para cada faixa. A escolha da equação é
 *  dele, e as três aparecem lado a lado: comparar é o argumento de por que a
 *  proposta é melhor que a tabela impressa.
 */

import { useEffect, useState } from "react";
import type { FormEvent } from "react";

import { api, ErroDaApi } from "../api/cliente";
import type {
  Equacao,
  Exercicio,
  RespostaDaCalculadora,
  Tecnica,
} from "../api/tipos";
import "./calculadora.css";
import "./paginas.css";

const EQUACOES: { valor: Equacao; nome: string }[] = [
  { valor: "proposta", nome: "Marzagão (2026)" },
  { valor: "epley", nome: "Epley (1985)" },
  { valor: "brzycki", nome: "Brzycki (1993)" },
];

const kg = (valor: number) =>
  valor.toLocaleString("pt-BR", { maximumFractionDigits: 1 });

export function Calculadora() {
  const [exercicios, definirExercicios] = useState<Exercicio[]>([]);
  const [tecnicas, definirTecnicas] = useState<Tecnica[]>([]);

  const [exercicioId, definirExercicioId] = useState("");
  const [carga, definirCarga] = useState("80");
  const [reps, definirReps] = useState("8");
  const [rir, definirRir] = useState("1");
  const [equacao, definirEquacao] = useState<Equacao>("proposta");
  const [escolhidas, definirEscolhidas] = useState<number[]>([]);

  const [resultado, definirResultado] = useState<RespostaDaCalculadora | null>(null);
  const [erro, definirErro] = useState<string | null>(null);
  const [calculando, definirCalculando] = useState(false);

  useEffect(() => {
    api.listarExercicios().then(definirExercicios).catch(() => definirExercicios([]));
    // Só as que mudam o que uma série significa importam para a estimativa;
    // as de agrupamento vivem na prescrição, não aqui.
    api
      .tecnicas()
      .then((todas) => definirTecnicas(todas.filter((t) => t.escopo !== "agrupamento")))
      .catch(() => definirTecnicas([]));
  }, []);

  const exercicio = exercicios.find((e) => String(e.id) === exercicioId) ?? null;

  function alternarTecnica(id: number) {
    definirEscolhidas((atual) =>
      atual.includes(id) ? atual.filter((x) => x !== id) : [...atual, id],
    );
  }

  async function calcular(evento: FormEvent) {
    evento.preventDefault();
    definirErro(null);
    definirCalculando(true);
    try {
      definirResultado(
        await api.calcular({
          carga_kg: Number(carga),
          reps: Number(reps),
          rir: rir === "" ? null : Number(rir),
          equacao,
          exercicio_id: exercicio?.id ?? null,
          tecnica_ids: escolhidas,
        }),
      );
    } catch (falha) {
      definirResultado(null);
      definirErro(falha instanceof ErroDaApi ? falha.message : "Não foi possível calcular.");
    } finally {
      definirCalculando(false);
    }
  }

  return (
    <main className="conteudo pilha">
      <div className="titulo-da-pagina">
        <div>
          <p className="rotulo">Ferramenta do treinador</p>
          <h1>Calculadora de carga</h1>
        </div>
      </div>

      <form className="painel pilha" onSubmit={calcular}>
        <p className="dica">
          Informe uma série que o aluno fez até <strong>perto da falha</strong>. A
          equação foi calibrada nesse tipo de série; com muita reserva o 1RM real
          fica acima do estimado.
        </p>

        <label className="campo">
          <span>Exercício (opcional — define o arredondamento)</span>
          <select
            value={exercicioId}
            onChange={(evento) => definirExercicioId(evento.target.value)}
          >
            <option value="">Sem exercício — arredonda de 2,5 em 2,5 kg</option>
            {exercicios.map((item) => (
              <option key={item.id} value={item.id}>
                {item.nome}
              </option>
            ))}
          </select>
        </label>

        {exercicio?.convencao_de_carga === "por_halter" && (
          <p className="aviso" role="status">
            <strong>{exercicio.nome}</strong> registra o peso de <strong>um</strong>{" "}
            halter, mesmo usando dois.
          </p>
        )}

        <div className="linha-de-campos">
          <label className="campo">
            <span>Carga (kg)</span>
            <input
              type="number"
              inputMode="decimal"
              step="0.5"
              min="0.5"
              value={carga}
              onChange={(evento) => definirCarga(evento.target.value)}
              required
            />
          </label>
          <label className="campo">
            <span>Repetições</span>
            <input
              type="number"
              inputMode="numeric"
              min="1"
              max="30"
              value={reps}
              onChange={(evento) => definirReps(evento.target.value)}
              required
            />
          </label>
          <label className="campo">
            <span>RIR (reserva)</span>
            <input
              type="number"
              inputMode="numeric"
              min="0"
              max="10"
              value={rir}
              onChange={(evento) => definirRir(evento.target.value)}
            />
          </label>
          <label className="campo">
            <span>Equação</span>
            <select
              value={equacao}
              onChange={(evento) => definirEquacao(evento.target.value as Equacao)}
            >
              {EQUACOES.map((item) => (
                <option key={item.valor} value={item.valor}>
                  {item.nome}
                </option>
              ))}
            </select>
          </label>
        </div>

        {tecnicas.length > 0 && (
          <fieldset className="tecnicas">
            <legend>Técnica usada na série</legend>
            <div className="tecnicas-lista">
              {tecnicas.map((tecnica) => (
                <label
                  key={tecnica.id}
                  className={`tecnica-chip ${escolhidas.includes(tecnica.id) ? "marcada" : ""}`}
                  title={tecnica.descricao}
                >
                  <input
                    type="checkbox"
                    checked={escolhidas.includes(tecnica.id)}
                    onChange={() => alternarTecnica(tecnica.id)}
                  />
                  {tecnica.nome}
                  {tecnica.distorce_estimativa && <span aria-hidden="true"> ⚠</span>}
                </label>
              ))}
            </div>
            <p className="dica">
              As marcadas com ⚠ mudam o que uma série significa — um cluster de 3×3
              não é uma série de 9 repetições corridas — e por isso invalidam a
              estimativa.
            </p>
          </fieldset>
        )}

        {erro !== null && (
          <p className="aviso erro" role="alert">
            {erro}
          </p>
        )}

        <button type="submit" className="botao" disabled={calculando}>
          {calculando ? "Calculando…" : "Calcular"}
        </button>
      </form>

      {resultado !== null && <Resultado resultado={resultado} />}
    </main>
  );
}

function Resultado({ resultado }: { resultado: RespostaDaCalculadora }) {
  return (
    <>
      <div className={`resultado ${resultado.confiavel ? "" : "com-ressalva"}`}>
        <p className="rotulo">1RM estimado</p>
        <p className="resultado-numero">
          {kg(resultado.um_rm)} <span>kg</span>
        </p>
        <p className="resultado-equacao">por {resultado.nome_da_equacao}</p>
        {resultado.ressalva !== null && (
          <p className="resultado-ressalva" role="status">
            {resultado.ressalva}
          </p>
        )}
      </div>

      <section className="painel pilha">
        <div>
          <h2 className="rotulo">Carga por faixa de repetições</h2>
          <p className="dica">
            Arredondada de {kg(resultado.incremento_kg)} em {kg(resultado.incremento_kg)}{" "}
            kg. Repare que o percentual <strong>não</strong> é fixo por número de
            repetições — é isso que a tabela impressa erra.
          </p>
        </div>
        <div className="rolagem">
          <table className="tabela-de-cargas">
            <thead>
              <tr>
                <th>Reps</th>
                <th>Carga</th>
                <th>Exato</th>
                <th>% do 1RM</th>
              </tr>
            </thead>
            <tbody>
              {resultado.tabela.map((linha) => (
                <tr key={linha.reps}>
                  <td className="num forte">{linha.reps}</td>
                  <td className="num forte">{kg(linha.carga_arredondada_kg)} kg</td>
                  <td className="num fraco">{kg(linha.carga_kg)}</td>
                  <td className="num">{kg(linha.percentual)}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section className="painel pilha">
        <div>
          <h2 className="rotulo">A mesma série pelas três equações</h2>
          <p className="dica">
            Elas concordam nas cargas altas e discordam nas leves, onde as clássicas
            subestimam o quanto cada repetição vale.
          </p>
        </div>
        <ul className="comparacao">
          {Object.entries(resultado.comparacao).map(([nome, valor]) => (
            <li key={nome} className={nome === resultado.nome_da_equacao ? "usada" : ""}>
              <span>{nome}</span>
              <span className="num">{kg(valor)} kg</span>
            </li>
          ))}
        </ul>
      </section>
    </>
  );
}
