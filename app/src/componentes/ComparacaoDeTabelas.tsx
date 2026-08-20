/** Esperado × obtido, lado a lado, com as células divergentes marcadas.
 *
 *  É o componente que justifica o app existir: no terminal essa mesma informação
 *  sai truncada e sem alinhamento; aqui as duas tabelas rolam e as diferenças
 *  saltam à vista.
 */

import type { CelulaDivergente, Tabela } from "../api/tipos";
import "./comparacao.css";

type Valor = string | number | boolean | null;

function formatar(valor: Valor): string {
  if (valor === null) return "—";
  if (typeof valor === "boolean") return valor ? "True" : "False";
  if (typeof valor === "number") {
    // Inteiros ficam inteiros; decimais longos são cortados para não estourar a coluna.
    return Number.isInteger(valor) ? String(valor) : String(Number(valor.toFixed(6)));
  }
  return valor;
}

function classeDoValor(valor: Valor): string {
  if (valor === null) return "nulo";
  if (typeof valor === "number") return "numero";
  if (typeof valor === "boolean") return "booleano";
  return "";
}

interface PropsDaTabela {
  titulo: string;
  tabela: Tabela;
  lado: "esperado" | "obtido";
  divergentes: Set<string>;
}

function Quadro({ titulo, tabela, lado, divergentes }: PropsDaTabela) {
  const escondidas = tabela.total - tabela.linhas.length;
  return (
    <div className={`quadro ${lado}`}>
      <div className="quadro-topo">
        <span className="quadro-titulo">{titulo}</span>
        <span className="quadro-contagem">
          {tabela.total} {tabela.total === 1 ? "linha" : "linhas"}
        </span>
      </div>
      <div className="quadro-rolagem">
        <table>
          <thead>
            <tr>
              <th className="indice" scope="col">
                #
              </th>
              {tabela.colunas.map((coluna) => (
                <th key={coluna} scope="col">
                  {coluna}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {tabela.linhas.map((linha, i) => (
              <tr key={i}>
                <td className="indice">{i}</td>
                {linha.map((valor, j) => {
                  const marcada = divergentes.has(`${i}:${tabela.colunas[j]}`);
                  return (
                    <td
                      key={j}
                      className={`${classeDoValor(valor)} ${marcada ? "divergente" : ""}`}
                    >
                      {formatar(valor)}
                    </td>
                  );
                })}
              </tr>
            ))}
            {tabela.linhas.length === 0 && (
              <tr>
                <td className="vazia" colSpan={tabela.colunas.length + 1}>
                  nenhuma linha
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
      {escondidas > 0 && (
        <p className="quadro-rodape">+{escondidas} linhas não mostradas</p>
      )}
    </div>
  );
}

interface Props {
  esperado: Tabela;
  obtido: Tabela;
  celulas?: CelulaDivergente[];
  semOrdem?: boolean;
}

export function ComparacaoDeTabelas({ esperado, obtido, celulas, semOrdem }: Props) {
  const divergentes = new Set((celulas ?? []).map((c) => `${c.linha}:${c.coluna}`));

  return (
    <div className="comparacao">
      {semOrdem && (
        <p className="aviso-ordem">
          As duas tabelas foram ordenadas antes da comparação — neste exercício a ordem
          das linhas não importa.
        </p>
      )}
      <div className="quadros">
        <Quadro
          titulo="esperado"
          tabela={esperado}
          lado="esperado"
          divergentes={divergentes}
        />
        <Quadro titulo="o seu" tabela={obtido} lado="obtido" divergentes={divergentes} />
      </div>

      {celulas && celulas.length > 0 && (
        <ul className="lista-de-celulas">
          {celulas.map((c, i) => (
            <li key={i}>
              linha <strong>{c.linha}</strong>, coluna <code>{c.coluna}</code>:
              esperado <code className="ok">{formatar(c.esperado as Valor)}</code>,
              obtido <code className="nao">{formatar(c.obtido as Valor)}</code>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
