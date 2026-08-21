/** O protocolo alimentar, do jeito que o João monta.
 *
 *  O caminho principal é preencher aqui: grupos de substituição, refeições e
 *  suplementos, linha a linha. Colar o texto é atalho para quem já tem o
 *  protocolo escrito — ele preenche estas mesmas linhas, que continuam
 *  editáveis, e mostra o que não foi entendido em vez de engolir.
 *
 *  Grava o protocolo inteiro numa chamada só: gravar por partes deixaria a
 *  dieta do aluno pela metade se uma delas falhasse.
 */

import { useState } from "react";

import { api, ErroDaApi } from "../api/cliente";
import type {
  GrupoNovo,
  Protocolo,
  ProtocoloNovo,
  RefeicaoNova,
  SuplementoNovo,
} from "../api/tipos";
import "./protocolo.css";

let contador = 0;
const novaChave = () => `p${(contador += 1)}`;

/** Tudo string enquanto se edita: campo numérico vazio precisa continuar vazio,
 *  e `Number("")` seria zero — 0 kcal de meta é uma afirmação, não um branco. */
interface ItemDeGrupo {
  chave: string;
  descricao: string;
  quantidade: string;
  unidade: string;
}

interface Grupo {
  chave: string;
  nome: string;
  itens: ItemDeGrupo[];
}

interface ItemDeRefeicao {
  chave: string;
  descricao: string;
  quantidade: string;
  unidade: string;
  a_gosto: boolean;
  opcional: boolean;
}

interface RefeicaoRascunho {
  chave: string;
  nome: string;
  horario: string;
  itens: ItemDeRefeicao[];
}

interface SuplementoRascunho {
  chave: string;
  nome: string;
  dose: string;
  momento: string;
}

interface Rascunho {
  nome: string;
  kcal_alvo: string;
  deficit_kcal: string;
  proteina_g: string;
  carboidrato_g: string;
  gordura_g: string;
  observacoes: string;
  grupos: Grupo[];
  refeicoes: RefeicaoRascunho[];
  suplementos: SuplementoRascunho[];
}

const numeroOuNulo = (valor: string) =>
  valor.trim() === "" ? null : Number(valor.replace(",", "."));

const inteiroOuNulo = (valor: string) => {
  const numero = numeroOuNulo(valor);
  return numero === null || Number.isNaN(numero) ? null : Math.round(numero);
};

function itemDeGrupoVazio(): ItemDeGrupo {
  return { chave: novaChave(), descricao: "", quantidade: "", unidade: "g" };
}

function itemDeRefeicaoVazio(): ItemDeRefeicao {
  return {
    chave: novaChave(),
    descricao: "",
    quantidade: "",
    unidade: "",
    a_gosto: false,
    opcional: false,
  };
}

function vazio(): Rascunho {
  return {
    nome: "Protocolo alimentar",
    kcal_alvo: "",
    deficit_kcal: "",
    proteina_g: "",
    carboidrato_g: "",
    gordura_g: "",
    observacoes: "",
    grupos: [],
    refeicoes: [],
    suplementos: [],
  };
}

function doServidor(protocolo: Protocolo): Rascunho {
  return {
    nome: protocolo.nome,
    kcal_alvo: protocolo.kcal_alvo === null ? "" : String(protocolo.kcal_alvo),
    deficit_kcal: protocolo.deficit_kcal === null ? "" : String(protocolo.deficit_kcal),
    proteina_g: protocolo.proteina_g === null ? "" : String(protocolo.proteina_g),
    carboidrato_g: protocolo.carboidrato_g === null ? "" : String(protocolo.carboidrato_g),
    gordura_g: protocolo.gordura_g === null ? "" : String(protocolo.gordura_g),
    observacoes: protocolo.observacoes ?? "",
    grupos: protocolo.grupos.map((grupo) => ({
      chave: novaChave(),
      nome: grupo.nome,
      itens: grupo.itens.map((item) => ({
        chave: novaChave(),
        descricao: item.descricao,
        quantidade: item.quantidade === null ? "" : String(item.quantidade),
        unidade: item.unidade ?? "",
      })),
    })),
    refeicoes: protocolo.refeicoes.map((refeicao) => ({
      chave: novaChave(),
      nome: refeicao.nome,
      horario: refeicao.horario ?? "",
      itens: refeicao.itens.map((item) => ({
        chave: novaChave(),
        descricao: item.descricao ?? "",
        quantidade: item.quantidade === null ? "" : String(item.quantidade),
        unidade: item.unidade ?? "",
        a_gosto: item.a_gosto,
        opcional: item.opcional,
      })),
    })),
    suplementos: protocolo.suplementos.map((suplemento) => ({
      chave: novaChave(),
      nome: suplemento.nome,
      dose: suplemento.dose ?? "",
      momento: suplemento.momento ?? "",
    })),
  };
}

function doLido(lido: ProtocoloNovo): Rascunho {
  const base = vazio();
  return {
    ...base,
    nome: lido.nome,
    deficit_kcal: lido.deficit_kcal === null ? "" : String(lido.deficit_kcal),
    grupos: lido.grupos.map((grupo: GrupoNovo) => ({
      chave: novaChave(),
      nome: grupo.nome,
      itens: grupo.itens.map((item) => ({
        chave: novaChave(),
        descricao: item.descricao,
        quantidade: item.quantidade === null ? "" : String(item.quantidade),
        unidade: item.unidade ?? "",
      })),
    })),
    refeicoes: lido.refeicoes.map((refeicao: RefeicaoNova) => ({
      chave: novaChave(),
      nome: refeicao.nome,
      horario: refeicao.horario ?? "",
      itens: refeicao.itens.map((item) => ({
        chave: novaChave(),
        descricao: item.descricao ?? "",
        quantidade: item.quantidade === null ? "" : String(item.quantidade),
        unidade: item.unidade ?? "",
        a_gosto: item.a_gosto,
        opcional: item.opcional,
      })),
    })),
    suplementos: lido.suplementos.map((suplemento: SuplementoNovo) => ({
      chave: novaChave(),
      nome: suplemento.nome,
      dose: suplemento.dose ?? "",
      momento: suplemento.momento ?? "",
    })),
  };
}

function paraApi(rascunho: Rascunho): ProtocoloNovo {
  return {
    nome: rascunho.nome.trim() || "Protocolo alimentar",
    kcal_alvo: inteiroOuNulo(rascunho.kcal_alvo),
    deficit_kcal: inteiroOuNulo(rascunho.deficit_kcal),
    proteina_g: inteiroOuNulo(rascunho.proteina_g),
    carboidrato_g: inteiroOuNulo(rascunho.carboidrato_g),
    gordura_g: inteiroOuNulo(rascunho.gordura_g),
    observacoes: rascunho.observacoes.trim() || null,
    ativo: true,
    grupos: rascunho.grupos
      .filter((grupo) => grupo.nome.trim() !== "")
      .map((grupo) => ({
        nome: grupo.nome.trim(),
        itens: grupo.itens
          .filter((item) => item.descricao.trim() !== "")
          .map((item) => ({
            descricao: item.descricao.trim(),
            quantidade: numeroOuNulo(item.quantidade),
            unidade: item.unidade.trim() || null,
          })),
      })),
    refeicoes: rascunho.refeicoes
      .filter((refeicao) => refeicao.nome.trim() !== "")
      .map((refeicao) => ({
        nome: refeicao.nome.trim(),
        horario: refeicao.horario.trim() || null,
        itens: refeicao.itens
          .filter((item) => item.descricao.trim() !== "")
          .map((item) => ({
            descricao: item.descricao.trim(),
            quantidade: numeroOuNulo(item.quantidade),
            unidade: item.unidade.trim() || null,
            a_gosto: item.a_gosto,
            opcional: item.opcional,
          })),
      })),
    suplementos: rascunho.suplementos
      .filter((suplemento) => suplemento.nome.trim() !== "")
      .map((suplemento) => ({
        nome: suplemento.nome.trim(),
        dose: suplemento.dose.trim() || null,
        momento: suplemento.momento.trim() || null,
      })),
  };
}

interface Props {
  alunoId: number;
  protocolo: Protocolo | null;
  aoSalvar: (salvo: Protocolo) => void;
}

export function EditorDeProtocolo({ alunoId, protocolo, aoSalvar }: Props) {
  const [rascunho, definirRascunho] = useState<Rascunho>(() =>
    protocolo === null ? vazio() : doServidor(protocolo),
  );
  const [erro, definirErro] = useState<string | null>(null);
  const [aviso, definirAviso] = useState<string | null>(null);
  const [perdidas, definirPerdidas] = useState<string[]>([]);
  const [salvando, definirSalvando] = useState(false);

  const [colando, definirColando] = useState(false);
  const [texto, definirTexto] = useState("");
  const [lendo, definirLendo] = useState(false);

  function mudar<C extends keyof Rascunho>(campo: C, valor: Rascunho[C]) {
    definirRascunho((atual) => ({ ...atual, [campo]: valor }));
  }

  async function lerColado() {
    definirErro(null);
    definirAviso(null);
    definirPerdidas([]);
    definirLendo(true);
    try {
      const leitura = await api.lerProtocolo(texto);
      const lido = leitura.protocolo;

      if (lido.grupos.length === 0 && lido.refeicoes.length === 0) {
        definirAviso("Não entendi nada do texto. Confira o formato ou preencha à mão.");
        return;
      }

      definirRascunho(doLido(lido));
      definirPerdidas(leitura.nao_entendidas);
      definirAviso(
        `${lido.grupos.length} grupo(s), ${lido.refeicoes.length} refeição(ões) e ` +
          `${lido.suplementos.length} suplemento(s) lidos. Confira antes de salvar.`,
      );
      definirColando(false);
    } catch (falha) {
      definirErro(falha instanceof ErroDaApi ? falha.message : "Não foi possível ler.");
    } finally {
      definirLendo(false);
    }
  }

  async function salvar() {
    definirErro(null);
    definirAviso(null);
    definirSalvando(true);
    try {
      const dados = paraApi(rascunho);
      const salvo =
        protocolo === null
          ? await api.criarProtocolo(alunoId, dados)
          : await api.editarProtocolo(protocolo.id, dados);
      // Quem confirma é a página: salvar um protocolo novo troca a `key` deste
      // componente, e um aviso posto aqui morreria na remontagem sem ninguém
      // ver que deu certo.
      aoSalvar(salvo);
    } catch (falha) {
      definirErro(falha instanceof ErroDaApi ? falha.message : "Não foi possível salvar.");
    } finally {
      definirSalvando(false);
    }
  }

  // ------------------------------------------------------------- grupos

  function mudarGrupo(chave: string, nome: string) {
    definirRascunho((atual) => ({
      ...atual,
      grupos: atual.grupos.map((g) => (g.chave === chave ? { ...g, nome } : g)),
    }));
  }

  function mudarItemDeGrupo(
    grupo: string,
    item: string,
    campo: keyof ItemDeGrupo,
    valor: string,
  ) {
    definirRascunho((atual) => ({
      ...atual,
      grupos: atual.grupos.map((g) =>
        g.chave === grupo
          ? {
              ...g,
              itens: g.itens.map((i) => (i.chave === item ? { ...i, [campo]: valor } : i)),
            }
          : g,
      ),
    }));
  }

  function acrescentarItemDeGrupo(grupo: string) {
    definirRascunho((atual) => ({
      ...atual,
      grupos: atual.grupos.map((g) =>
        // Herda a unidade da última: uma lista de carboidratos é toda em gramas,
        // e escolher "g" de novo a cada linha é trabalho que o app deve poupar.
        g.chave === grupo
          ? {
              ...g,
              itens: [
                ...g.itens,
                { ...itemDeGrupoVazio(), unidade: g.itens[g.itens.length - 1]?.unidade ?? "g" },
              ],
            }
          : g,
      ),
    }));
  }

  function removerItemDeGrupo(grupo: string, item: string) {
    definirRascunho((atual) => ({
      ...atual,
      grupos: atual.grupos.map((g) =>
        g.chave === grupo ? { ...g, itens: g.itens.filter((i) => i.chave !== item) } : g,
      ),
    }));
  }

  // ---------------------------------------------------------- refeições

  function mudarRefeicao(chave: string, campo: "nome" | "horario", valor: string) {
    definirRascunho((atual) => ({
      ...atual,
      refeicoes: atual.refeicoes.map((r) =>
        r.chave === chave ? { ...r, [campo]: valor } : r,
      ),
    }));
  }

  function mudarItemDeRefeicao(
    refeicao: string,
    item: string,
    campo: keyof ItemDeRefeicao,
    valor: string | boolean,
  ) {
    definirRascunho((atual) => ({
      ...atual,
      refeicoes: atual.refeicoes.map((r) =>
        r.chave === refeicao
          ? {
              ...r,
              itens: r.itens.map((i) => (i.chave === item ? { ...i, [campo]: valor } : i)),
            }
          : r,
      ),
    }));
  }

  function acrescentarItemDeRefeicao(refeicao: string) {
    definirRascunho((atual) => ({
      ...atual,
      refeicoes: atual.refeicoes.map((r) =>
        r.chave === refeicao ? { ...r, itens: [...r.itens, itemDeRefeicaoVazio()] } : r,
      ),
    }));
  }

  function removerItemDeRefeicao(refeicao: string, item: string) {
    definirRascunho((atual) => ({
      ...atual,
      refeicoes: atual.refeicoes.map((r) =>
        r.chave === refeicao ? { ...r, itens: r.itens.filter((i) => i.chave !== item) } : r,
      ),
    }));
  }

  const nomesDosGrupos = rascunho.grupos
    .map((grupo) => grupo.nome.trim())
    .filter((nome) => nome !== "");

  return (
    <div className="pilha editor-de-protocolo">
      {erro !== null && (
        <p className="aviso erro" role="alert">
          {erro}
        </p>
      )}
      {aviso !== null && (
        <p className="aviso certo" role="status">
          {aviso}
        </p>
      )}

      {perdidas.length > 0 && (
        <div className="aviso" role="status">
          <p>
            <strong>Estas linhas ficaram de fora:</strong>
          </p>
          <ul className="perdidas">
            {perdidas.map((linha, indice) => (
              <li key={indice}>{linha}</li>
            ))}
          </ul>
          <p className="dica">
            Acrescente à mão o que for comida; o resto pode ser título ou recado.
          </p>
        </div>
      )}

      <div className="painel pilha">
        <div className="linha-de-campos">
          <label className="campo">
            <span>Nome</span>
            <input
              value={rascunho.nome}
              onChange={(evento) => mudar("nome", evento.target.value)}
              maxLength={120}
              placeholder="Corte — bloco 1"
            />
          </label>
          <label className="campo">
            <span>Meta (kcal)</span>
            <input
              type="number"
              inputMode="numeric"
              value={rascunho.kcal_alvo}
              onChange={(evento) => mudar("kcal_alvo", evento.target.value)}
            />
          </label>
          <label className="campo">
            <span>Déficit</span>
            <input
              type="number"
              inputMode="numeric"
              value={rascunho.deficit_kcal}
              onChange={(evento) => mudar("deficit_kcal", evento.target.value)}
            />
          </label>
        </div>

        <div className="linha-de-campos">
          <label className="campo">
            <span>Proteína (g)</span>
            <input
              type="number"
              inputMode="numeric"
              value={rascunho.proteina_g}
              onChange={(evento) => mudar("proteina_g", evento.target.value)}
            />
          </label>
          <label className="campo">
            <span>Carboidrato (g)</span>
            <input
              type="number"
              inputMode="numeric"
              value={rascunho.carboidrato_g}
              onChange={(evento) => mudar("carboidrato_g", evento.target.value)}
            />
          </label>
          <label className="campo">
            <span>Gordura (g)</span>
            <input
              type="number"
              inputMode="numeric"
              value={rascunho.gordura_g}
              onChange={(evento) => mudar("gordura_g", evento.target.value)}
            />
          </label>
        </div>

        <button
          type="button"
          className="botao secundario alinhado"
          onClick={() => definirColando((aberto) => !aberto)}
          aria-expanded={colando}
        >
          {colando ? "Fechar" : "Colar protocolo escrito"}
        </button>

        {colando && (
          <div className="pilha">
            <label className="campo">
              <span>Cole o protocolo como você já escreve</span>
              <textarea
                rows={10}
                value={texto}
                onChange={(evento) => definirTexto(evento.target.value)}
                placeholder={
                  "Carboidratos substituição\nArroz branco: 200g\nCuscuz: 225g\n\n" +
                  "1° refeição café\nOvos\nPão francês\n(Azeite)"
                }
              />
            </label>
            <p className="dica">
              Isto <strong>substitui</strong> o que está na tela — e não salva nada
              até você conferir e clicar em salvar.
            </p>
            <button
              type="button"
              className="botao secundario"
              onClick={lerColado}
              disabled={lendo || texto.trim() === ""}
            >
              {lendo ? "Lendo…" : "Ler o texto"}
            </button>
          </div>
        )}
      </div>

      {/* ------------------------------------------------------- grupos */}

      <section className="pilha">
        <div className="titulo-de-secao">
          <h2 className="rotulo">Grupos de substituição</h2>
          <button
            type="button"
            className="botao discreto"
            onClick={() =>
              mudar("grupos", [
                ...rascunho.grupos,
                { chave: novaChave(), nome: "", itens: [itemDeGrupoVazio()] },
              ])
            }
          >
            + Grupo
          </button>
        </div>

        {rascunho.grupos.length === 0 && (
          <p className="dica">
            É aqui que mora a equivalência: as quantidades diferem entre os itens
            de propósito, e é isso que torna a troca justa.
          </p>
        )}

        {rascunho.grupos.map((grupo) => (
          <div key={grupo.chave} className="painel pilha">
            <div className="cabecalho-de-secao">
              <label className="campo">
                <span>Grupo</span>
                <input
                  value={grupo.nome}
                  onChange={(evento) => mudarGrupo(grupo.chave, evento.target.value)}
                  placeholder="Carboidratos"
                  maxLength={80}
                />
              </label>
              <button
                type="button"
                className="botao discreto"
                onClick={() =>
                  mudar(
                    "grupos",
                    rascunho.grupos.filter((g) => g.chave !== grupo.chave),
                  )
                }
              >
                Remover grupo
              </button>
            </div>

            {grupo.itens.map((item) => (
              <div key={item.chave} className="linha-de-item">
                <input
                  className="descricao"
                  value={item.descricao}
                  onChange={(evento) =>
                    mudarItemDeGrupo(grupo.chave, item.chave, "descricao", evento.target.value)
                  }
                  placeholder="Arroz branco"
                  maxLength={120}
                  aria-label="Alimento"
                />
                <input
                  className="quantidade"
                  type="number"
                  inputMode="decimal"
                  value={item.quantidade}
                  onChange={(evento) =>
                    mudarItemDeGrupo(grupo.chave, item.chave, "quantidade", evento.target.value)
                  }
                  placeholder="200"
                  aria-label="Quantidade"
                />
                <input
                  className="unidade"
                  value={item.unidade}
                  onChange={(evento) =>
                    mudarItemDeGrupo(grupo.chave, item.chave, "unidade", evento.target.value)
                  }
                  placeholder="g"
                  maxLength={20}
                  aria-label="Unidade"
                />
                <button
                  type="button"
                  className="botao discreto"
                  onClick={() => removerItemDeGrupo(grupo.chave, item.chave)}
                  aria-label={`Remover ${item.descricao || "item"}`}
                >
                  ×
                </button>
              </div>
            ))}

            <button
              type="button"
              className="botao discreto alinhado"
              onClick={() => acrescentarItemDeGrupo(grupo.chave)}
            >
              + Alimento
            </button>
          </div>
        ))}
      </section>

      {/* ---------------------------------------------------- refeições */}

      <section className="pilha">
        <div className="titulo-de-secao">
          <h2 className="rotulo">Refeições</h2>
          <button
            type="button"
            className="botao discreto"
            onClick={() =>
              mudar("refeicoes", [
                ...rascunho.refeicoes,
                {
                  chave: novaChave(),
                  nome: `${rascunho.refeicoes.length + 1}ª refeição`,
                  horario: "",
                  itens: [itemDeRefeicaoVazio()],
                },
              ])
            }
          >
            + Refeição
          </button>
        </div>

        <p className="dica">
          Deixe a quantidade em branco quando o alimento já estiver num grupo: o
          app acha a porção sozinho e mostra as trocas para o aluno.
        </p>

        {rascunho.refeicoes.map((refeicao) => (
          <div key={refeicao.chave} className="painel pilha">
            <div className="cabecalho-de-secao">
              <label className="campo">
                <span>Refeição</span>
                <input
                  value={refeicao.nome}
                  onChange={(evento) =>
                    mudarRefeicao(refeicao.chave, "nome", evento.target.value)
                  }
                  placeholder="1ª refeição — café"
                  maxLength={80}
                />
              </label>
              <label className="campo horario">
                <span>Horário</span>
                <input
                  value={refeicao.horario}
                  onChange={(evento) =>
                    mudarRefeicao(refeicao.chave, "horario", evento.target.value)
                  }
                  placeholder="7h"
                  maxLength={20}
                />
              </label>
              <button
                type="button"
                className="botao discreto"
                onClick={() =>
                  mudar(
                    "refeicoes",
                    rascunho.refeicoes.filter((r) => r.chave !== refeicao.chave),
                  )
                }
              >
                Remover
              </button>
            </div>

            {refeicao.itens.map((item) => (
              <div key={item.chave} className="pilha-de-item">
                <div className="linha-de-item">
                  <input
                    className="descricao"
                    list="alimentos-do-protocolo"
                    value={item.descricao}
                    onChange={(evento) =>
                      mudarItemDeRefeicao(
                        refeicao.chave,
                        item.chave,
                        "descricao",
                        evento.target.value,
                      )
                    }
                    placeholder="Ovos"
                    maxLength={120}
                    aria-label="Alimento"
                  />
                  <input
                    className="quantidade"
                    type="number"
                    inputMode="decimal"
                    value={item.quantidade}
                    onChange={(evento) =>
                      mudarItemDeRefeicao(
                        refeicao.chave,
                        item.chave,
                        "quantidade",
                        evento.target.value,
                      )
                    }
                    placeholder="—"
                    aria-label="Quantidade"
                    disabled={item.a_gosto}
                  />
                  <input
                    className="unidade"
                    value={item.unidade}
                    onChange={(evento) =>
                      mudarItemDeRefeicao(
                        refeicao.chave,
                        item.chave,
                        "unidade",
                        evento.target.value,
                      )
                    }
                    placeholder=""
                    maxLength={20}
                    aria-label="Unidade"
                    disabled={item.a_gosto}
                  />
                  <button
                    type="button"
                    className="botao discreto"
                    onClick={() => removerItemDeRefeicao(refeicao.chave, item.chave)}
                    aria-label={`Remover ${item.descricao || "item"}`}
                  >
                    ×
                  </button>
                </div>
                <div className="marcas-do-item">
                  <label>
                    <input
                      type="checkbox"
                      checked={item.a_gosto}
                      onChange={(evento) =>
                        mudarItemDeRefeicao(
                          refeicao.chave,
                          item.chave,
                          "a_gosto",
                          evento.target.checked,
                        )
                      }
                    />
                    <span>à gosto</span>
                  </label>
                  <label>
                    <input
                      type="checkbox"
                      checked={item.opcional}
                      onChange={(evento) =>
                        mudarItemDeRefeicao(
                          refeicao.chave,
                          item.chave,
                          "opcional",
                          evento.target.checked,
                        )
                      }
                    />
                    <span>opcional</span>
                  </label>
                </div>
              </div>
            ))}

            <button
              type="button"
              className="botao discreto alinhado"
              onClick={() => acrescentarItemDeRefeicao(refeicao.chave)}
            >
              + Alimento
            </button>
          </div>
        ))}
      </section>

      {/* --------------------------------------------------- suplementos */}

      <section className="pilha">
        <div className="titulo-de-secao">
          <h2 className="rotulo">Suplementos</h2>
          <button
            type="button"
            className="botao discreto"
            onClick={() =>
              mudar("suplementos", [
                ...rascunho.suplementos,
                { chave: novaChave(), nome: "", dose: "", momento: "" },
              ])
            }
          >
            + Suplemento
          </button>
        </div>

        {rascunho.suplementos.length > 0 && (
          <div className="painel pilha">
            {rascunho.suplementos.map((suplemento) => (
              <div key={suplemento.chave} className="linha-de-item">
                <input
                  className="descricao"
                  value={suplemento.nome}
                  onChange={(evento) =>
                    mudar(
                      "suplementos",
                      rascunho.suplementos.map((s) =>
                        s.chave === suplemento.chave
                          ? { ...s, nome: evento.target.value }
                          : s,
                      ),
                    )
                  }
                  placeholder="Ioimbina"
                  maxLength={80}
                  aria-label="Suplemento"
                />
                <input
                  className="dose"
                  value={suplemento.dose}
                  onChange={(evento) =>
                    mudar(
                      "suplementos",
                      rascunho.suplementos.map((s) =>
                        s.chave === suplemento.chave
                          ? { ...s, dose: evento.target.value }
                          : s,
                      ),
                    )
                  }
                  placeholder="5 mg"
                  maxLength={80}
                  aria-label="Dose"
                />
                <input
                  className="dose"
                  value={suplemento.momento}
                  onChange={(evento) =>
                    mudar(
                      "suplementos",
                      rascunho.suplementos.map((s) =>
                        s.chave === suplemento.chave
                          ? { ...s, momento: evento.target.value }
                          : s,
                      ),
                    )
                  }
                  placeholder="em jejum"
                  maxLength={80}
                  aria-label="Momento"
                />
                <button
                  type="button"
                  className="botao discreto"
                  onClick={() =>
                    mudar(
                      "suplementos",
                      rascunho.suplementos.filter((s) => s.chave !== suplemento.chave),
                    )
                  }
                  aria-label={`Remover ${suplemento.nome || "suplemento"}`}
                >
                  ×
                </button>
              </div>
            ))}
          </div>
        )}
      </section>

      <label className="campo">
        <span>Observações</span>
        <textarea
          rows={3}
          value={rascunho.observacoes}
          onChange={(evento) => mudar("observacoes", evento.target.value)}
          placeholder="O que o aluno precisa saber além da lista."
          maxLength={4000}
        />
      </label>

      {/* Sugere no campo da refeição o que já está nos grupos: digitar "Arroz
          branko" quebraria a ligação com a substituição sem avisar ninguém. */}
      <datalist id="alimentos-do-protocolo">
        {rascunho.grupos.flatMap((grupo) =>
          grupo.itens
            .filter((item) => item.descricao.trim() !== "")
            .map((item) => <option key={item.chave} value={item.descricao} />),
        )}
      </datalist>

      <div className="acoes-do-protocolo">
        <button type="button" className="botao" onClick={salvar} disabled={salvando}>
          {salvando ? "Salvando…" : protocolo === null ? "Criar protocolo" : "Salvar"}
        </button>
        {nomesDosGrupos.length > 0 && (
          <p className="dica">
            {nomesDosGrupos.length} grupo(s) · {rascunho.refeicoes.length} refeição(ões)
          </p>
        )}
      </div>
    </div>
  );
}
