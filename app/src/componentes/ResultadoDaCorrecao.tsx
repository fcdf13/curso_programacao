/** O painel que aparece depois de `corrigir`.
 *
 *  Quando a falha traz dados estruturados, o texto do terminal dá lugar a uma
 *  explicação curta mais as tabelas. Quando não traz (erro de sintaxe, laço
 *  infinito, exceção do aluno), a mensagem de texto do motor já é boa — e ela
 *  aparece como está.
 */

import { ehTabela, type DadosDaFalha, type ResultadoDaCorrecao } from "../api/tipos";
import { ComparacaoDeTabelas } from "./ComparacaoDeTabelas";
import "./resultado.css";

const EXPLICACAO: Record<DadosDaFalha["tipo"], string> = {
  sem_retorno: "A função não devolveu nada.",
  valor_escalar: "O valor devolvido não bate.",
  tamanho_da_lista: "A lista tem tamanho diferente do esperado.",
  item_da_lista: "A lista tem o tamanho certo, mas um item difere.",
  conjunto: "O conjunto tem itens a mais ou a menos.",
  chaves_do_dicionario: "As chaves do dicionário não batem.",
  valor_do_dicionario: "As chaves estão certas, mas um valor difere.",
  tipo_errado: "O tipo do resultado não é o que o exercício pede.",
  esperava_dataframe: "O exercício pede um DataFrame.",
  esperava_series: "O exercício pede uma Series.",
  colunas_diferentes: "As colunas do resultado não batem.",
  ordem_das_colunas: "As colunas certas estão lá, mas fora de ordem.",
  numero_de_linhas: "O número de linhas não bate.",
  indice_diferente: "As linhas batem, mas o índice não.",
  valores_diferentes: "A forma da tabela está certa, mas há valores diferentes.",
  tipo_da_coluna: "Os valores estão certos, mas o tipo da coluna não.",
  tempo_esgotado: "Seu código demorou demais e foi interrompido.",
};

function Tabelas({ dados }: { dados: DadosDaFalha }) {
  if (!ehTabela(dados.esperado) || !ehTabela(dados.obtido)) return null;
  return (
    <ComparacaoDeTabelas
      esperado={dados.esperado}
      obtido={dados.obtido}
      celulas={dados.celulas}
      semOrdem={dados.comparado_sem_ordem}
    />
  );
}

function Detalhe({ dados }: { dados: DadosDaFalha }) {
  switch (dados.tipo) {
    case "valor_escalar":
      return (
        <dl className="par">
          <div>
            <dt>esperado</dt>
            <dd className="ok">{JSON.stringify(dados.esperado)}</dd>
          </div>
          <div>
            <dt>o seu</dt>
            <dd className="nao">{JSON.stringify(dados.obtido)}</dd>
          </div>
        </dl>
      );

    case "tamanho_da_lista":
    case "item_da_lista":
      return (
        <dl className="par">
          <div>
            <dt>esperado</dt>
            <dd className="ok">{JSON.stringify(dados.esperado)}</dd>
          </div>
          <div>
            <dt>o seu</dt>
            <dd className="nao">{JSON.stringify(dados.obtido)}</dd>
          </div>
        </dl>
      );

    case "colunas_diferentes":
      return (
        <>
          {!!dados.faltando?.length && (
            <p className="linha-de-detalhe">
              colunas que faltam: <code className="nao">{dados.faltando.join(", ")}</code>
            </p>
          )}
          {!!dados.sobrando?.length && (
            <p className="linha-de-detalhe">
              colunas a mais: <code className="nao">{dados.sobrando.join(", ")}</code>
            </p>
          )}
          <Tabelas dados={dados} />
        </>
      );

    case "conjunto":
    case "chaves_do_dicionario":
      return (
        <>
          {!!dados.faltando?.length && (
            <p className="linha-de-detalhe">
              faltando: <code className="nao">{JSON.stringify(dados.faltando)}</code>
            </p>
          )}
          {!!dados.sobrando?.length && (
            <p className="linha-de-detalhe">
              sobrando: <code className="nao">{JSON.stringify(dados.sobrando)}</code>
            </p>
          )}
        </>
      );

    case "tipo_da_coluna":
      return (
        <p className="linha-de-detalhe">
          coluna <code>{dados.coluna}</code>: esperado{" "}
          <code className="ok">{dados.tipo_esperado}</code>, obtido{" "}
          <code className="nao">{dados.tipo_obtido}</code>
        </p>
      );

    case "tipo_errado":
    case "esperava_dataframe":
    case "esperava_series":
      return (
        <>
          <p className="linha-de-detalhe">
            esperado <code className="ok">{dados.tipo_esperado ?? "tabela"}</code>, obtido{" "}
            <code className="nao">{dados.tipo_obtido ?? "outra coisa"}</code>
          </p>
          <Tabelas dados={dados} />
        </>
      );

    default:
      return <Tabelas dados={dados} />;
  }
}

interface Props {
  resultado: ResultadoDaCorrecao;
  onVerSolucao?: () => void;
  onPedirDica?: () => void;
  dicasRestantes?: number;
}

export function PainelDoResultado({
  resultado,
  onVerSolucao,
  onPedirDica,
  dicasRestantes = 0,
}: Props) {
  if (resultado.ok) {
    const { intervalo_dias, proxima_revisao, revisoes, tentativas_ate_acertar } =
      resultado.ficha;
    const quando = intervalo_dias === 1 ? "amanhã" : `em ${intervalo_dias} dias`;
    return (
      <div className="resultado certo" role="status">
        <div className="resultado-topo">
          <span className="selo">Passou</span>
          <span className="suave">
            {resultado.passaram} {resultado.passaram === 1 ? "teste verde" : "testes verdes"}
          </span>
        </div>
        <p className="resultado-frase">
          {revisoes > 0
            ? "Revisão em dia."
            : `Resolvido em ${tentativas_ate_acertar} ${
                tentativas_ate_acertar === 1 ? "tentativa" : "tentativas"
              }.`}{" "}
          Volta para revisão <strong>{quando}</strong>{" "}
          <span className="fraco">({proxima_revisao})</span>.
        </p>
      </div>
    );
  }

  const dados = resultado.dados;
  return (
    <div className="resultado errado" role="alert">
      <div className="resultado-topo">
        <span className="selo">Ainda não</span>
        <span className="fraco mono">falhou em {resultado.nome_da_falha}</span>
      </div>

      {dados ? (
        <>
          <p className="resultado-frase">{EXPLICACAO[dados.tipo] ?? "O resultado não bate."}</p>
          <Detalhe dados={dados} />
        </>
      ) : (
        <pre className="mensagem-crua">{resultado.mensagem}</pre>
      )}

      <div className="resultado-acoes">
        {dicasRestantes > 0 && onPedirDica && (
          <button onClick={onPedirDica}>
            Dica ({dicasRestantes} {dicasRestantes === 1 ? "restante" : "restantes"})
          </button>
        )}
        {onVerSolucao && <button onClick={onVerSolucao}>Ver a solução</button>}
      </div>
    </div>
  );
}
