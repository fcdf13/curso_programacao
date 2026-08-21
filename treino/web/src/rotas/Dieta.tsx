/** A dieta do aluno: o que comer hoje, o que dá para trocar, e o que ele seguiu.
 *
 *  O protocolo do João não diz "coma 200 g de arroz", diz "coma um carboidrato,
 *  e estes aqui equivalem" — então a tela mostra a porção junto do alimento e
 *  deixa a lista de trocas a um toque. Sem isso o aluno abre o PDF no WhatsApp.
 */

import { useCallback, useEffect, useMemo, useState } from "react";

import { api, ErroDaApi } from "../api/cliente";
import type { Aderencia, GrupoDeSubstituicao, ItemDaRefeicao, Protocolo } from "../api/tipos";
import { useSessao } from "../sessao";
import "./dieta.css";
import "./paginas.css";

/** Compara nome de alimento como gente: sem acento, sem caixa. */
export function chave(texto: string): string {
  return texto
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .trim()
    .toLowerCase();
}

/** A porção do item — a dele, ou a que está no grupo.
 *
 *  Na refeição o João escreve só "Ovos": a quantidade mora no grupo, porque é
 *  lá que ela vale como equivalência. Mostrar "Ovos" sem "5 und" deixaria o
 *  aluno com metade da instrução.
 */
export function porcaoDoItem(
  item: ItemDaRefeicao,
  grupos: GrupoDeSubstituicao[],
): string | null {
  if (item.a_gosto) return "à vontade";
  if (item.quantidade !== null) {
    return `${item.quantidade}${item.unidade ? ` ${item.unidade}` : ""}`;
  }

  const grupo = grupos.find((g) => g.id === item.grupo_id);
  if (grupo === undefined || item.descricao === null) return null;

  const igual = grupo.itens.find((i) => chave(i.descricao) === chave(item.descricao ?? ""));
  if (igual === undefined || igual.quantidade === null) return null;
  return `${igual.quantidade}${igual.unidade ? ` ${igual.unidade}` : ""}`;
}

function hoje(): string {
  // Data local, não UTC: `toISOString()` joga quem está em UTC-3 para o dia
  // anterior a partir das 21h — e é justamente aí que se marca a última refeição.
  const agora = new Date();
  const mes = String(agora.getMonth() + 1).padStart(2, "0");
  const dia = String(agora.getDate()).padStart(2, "0");
  return `${agora.getFullYear()}-${mes}-${dia}`;
}

function Trocas({ grupo, exceto }: { grupo: GrupoDeSubstituicao; exceto: string | null }) {
  const outros = grupo.itens.filter((i) => chave(i.descricao) !== chave(exceto ?? ""));
  if (outros.length === 0) return null;

  return (
    <div className="trocas">
      <p className="rotulo">No lugar, qualquer um destes</p>
      <ul>
        {outros.map((item) => (
          <li key={item.id}>{item.porcao}</li>
        ))}
      </ul>
    </div>
  );
}

export function Dieta() {
  const { eu } = useSessao();
  const alunoId = eu?.aluno_id ?? null;

  const [protocolo, definirProtocolo] = useState<Protocolo | null>(null);
  const [marcacoes, definirMarcacoes] = useState<Aderencia[]>([]);
  const [semProtocolo, definirSemProtocolo] = useState(false);
  const [erro, definirErro] = useState<string | null>(null);
  const [aberto, definirAberto] = useState<number | null>(null);

  const dia = hoje();

  const carregar = useCallback(async (id: number) => {
    try {
      definirProtocolo(await api.protocoloDoAluno(id));
      definirSemProtocolo(false);
    } catch (falha) {
      if (falha instanceof ErroDaApi && falha.status === 404) {
        definirSemProtocolo(true);
        return;
      }
      throw falha;
    }
    definirMarcacoes(await api.listarAderencia(id, 7));
  }, []);

  useEffect(() => {
    if (alunoId === null) return;
    carregar(alunoId).catch((falha) =>
      definirErro(falha instanceof ErroDaApi ? falha.message : "Não foi possível carregar."),
    );
  }, [alunoId, carregar]);

  const seguidas = useMemo(() => {
    const doDia = marcacoes.filter((m) => m.dia === dia && m.seguiu);
    return new Set(doDia.map((m) => m.refeicao_id));
  }, [marcacoes, dia]);

  async function marcar(refeicaoId: number, seguiu: boolean) {
    definirErro(null);
    try {
      const marcacao = await api.marcarRefeicao(refeicaoId, { dia, seguiu });
      definirMarcacoes((atuais) => [
        ...atuais.filter((m) => !(m.refeicao_id === refeicaoId && m.dia === dia)),
        marcacao,
      ]);
    } catch (falha) {
      definirErro(
        falha instanceof ErroDaApi ? falha.message : "Não foi possível marcar.",
      );
    }
  }

  if (semProtocolo) {
    return (
      <main className="conteudo pilha">
        <div className="titulo-da-pagina">
          <div>
            <p className="rotulo">Sua dieta</p>
            <h1>Protocolo alimentar</h1>
          </div>
        </div>
        <div className="vazio">
          <p>
            <strong>Sua dieta ainda não foi montada.</strong>
          </p>
          <p>Assim que o João passar o protocolo, ele aparece aqui.</p>
        </div>
      </main>
    );
  }

  if (protocolo === null) {
    return (
      <main className="conteudo">
        {erro !== null ? (
          <p className="aviso erro" role="alert">
            {erro}
          </p>
        ) : (
          <p className="carregando">Carregando…</p>
        )}
      </main>
    );
  }

  const metas: [string, string][] = [
    ...(protocolo.kcal_alvo !== null
      ? ([["Meta", `${protocolo.kcal_alvo} kcal`]] as [string, string][])
      : []),
    ...(protocolo.deficit_kcal !== null
      ? ([["Déficit", `${protocolo.deficit_kcal} kcal/dia`]] as [string, string][])
      : []),
    ...(protocolo.proteina_g !== null
      ? ([["Proteína", `${protocolo.proteina_g} g`]] as [string, string][])
      : []),
  ];

  return (
    <main className="conteudo pilha">
      <div className="titulo-da-pagina">
        <div>
          <p className="rotulo">Sua dieta</p>
          <h1>{protocolo.nome}</h1>
        </div>
      </div>

      {erro !== null && (
        <p className="aviso erro" role="alert">
          {erro}
        </p>
      )}

      {metas.length > 0 && (
        <div className="painel metas">
          {metas.map(([nome, valor]) => (
            <div key={nome}>
              <p className="rotulo">{nome}</p>
              <p className="meta-valor">{valor}</p>
            </div>
          ))}
        </div>
      )}

      <section className="pilha">
        <h2 className="rotulo">Hoje — {seguidas.size} de {protocolo.refeicoes.length} refeições</h2>

        {protocolo.refeicoes.map((refeicao) => (
          <article key={refeicao.id} className="painel refeicao">
            <header className="refeicao-topo">
              <div>
                <h3>{refeicao.nome}</h3>
                {refeicao.horario !== null && (
                  <p className="prescricao-detalhe">{refeicao.horario}</p>
                )}
              </div>
              <label className="marcar">
                <input
                  type="checkbox"
                  checked={seguidas.has(refeicao.id)}
                  onChange={(evento) => marcar(refeicao.id, evento.target.checked)}
                />
                <span>Segui</span>
              </label>
            </header>

            <ul className="itens">
              {refeicao.itens.map((item) => {
                const porcao = porcaoDoItem(item, protocolo.grupos);
                const grupo = protocolo.grupos.find((g) => g.id === item.grupo_id);
                // Grupo de um item só não tem troca a oferecer, e o botão que
                // abre um painel vazio custa mais que a ausência dele.
                const temTroca =
                  grupo !== undefined &&
                  grupo.itens.some((i) => chave(i.descricao) !== chave(item.descricao ?? ""));
                return (
                  <li key={item.id}>
                    <div className="item-linha">
                      <span className="item-nome">
                        {item.descricao}
                        {item.opcional && <span className="etiqueta">opcional</span>}
                      </span>
                      {porcao !== null && <span className="item-porcao">{porcao}</span>}
                      {temTroca && (
                        <button
                          type="button"
                          className="botao discreto"
                          onClick={() =>
                            definirAberto((atual) => (atual === item.id ? null : item.id))
                          }
                          aria-expanded={aberto === item.id}
                        >
                          Trocar
                        </button>
                      )}
                    </div>
                    {item.observacao !== null && (
                      <p className="prescricao-detalhe">{item.observacao}</p>
                    )}
                    {aberto === item.id && grupo !== undefined && (
                      <Trocas grupo={grupo} exceto={item.descricao} />
                    )}
                  </li>
                );
              })}
            </ul>

            {refeicao.observacoes !== null && (
              <p className="dica">{refeicao.observacoes}</p>
            )}
          </article>
        ))}
      </section>

      {protocolo.suplementos.length > 0 && (
        <section className="pilha">
          <h2 className="rotulo">Suplementos</h2>
          <ul className="painel lista-simples">
            {protocolo.suplementos.map((suplemento) => (
              <li key={suplemento.id}>
                <span className="item-nome">{suplemento.nome}</span>
                <span className="item-porcao">
                  {[suplemento.dose, suplemento.momento].filter(Boolean).join(" · ")}
                </span>
              </li>
            ))}
          </ul>
        </section>
      )}

      {protocolo.grupos.length > 0 && (
        <section className="pilha">
          <h2 className="rotulo">Tabela de substituições</h2>
          {protocolo.grupos.map((grupo) => (
            <div key={grupo.id} className="painel">
              <p className="rotulo">{grupo.nome}</p>
              <ul className="porcoes">
                {grupo.itens.map((item) => (
                  <li key={item.id}>{item.porcao}</li>
                ))}
              </ul>
              {grupo.observacao !== null && <p className="dica">{grupo.observacao}</p>}
            </div>
          ))}
        </section>
      )}

      {protocolo.observacoes !== null && (
        <div className="painel">
          <p className="rotulo">Observações do João</p>
          <p className="objetivo-texto">{protocolo.observacoes}</p>
        </div>
      )}
    </main>
  );
}
