/** A tela onde o estudo acontece: enunciado à esquerda, editor à direita.
 *
 *  Ctrl+Enter corrige. O que você digita é salvo sozinho depois de 800 ms parado,
 *  no mesmo arquivo de `respostas/` que o CLI usa — dá para alternar entre os dois
 *  no meio de um exercício sem perder nada.
 */

import { useCallback, useEffect, useRef, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import { api, ErroDaApi } from "../api/cliente";
import type { Detalhe, ResultadoDaCorrecao, Solucao } from "../api/tipos";
import { Dicas } from "../componentes/Dicas";
import { Editor } from "../componentes/Editor";
import { Markdown } from "../componentes/Markdown";
import { Nivel } from "../componentes/Nivel";
import { PainelDoResultado } from "../componentes/ResultadoDaCorrecao";
import "./resolver.css";

const ATRASO_DO_AUTOSAVE_MS = 800;

type Aba = "enunciado" | "teoria";

export function Resolver() {
  const { id = "" } = useParams();
  const navegar = useNavigate();

  const [exercicio, setExercicio] = useState<Detalhe | null>(null);
  const [codigo, setCodigo] = useState("");
  const [resultado, setResultado] = useState<ResultadoDaCorrecao | null>(null);
  const [solucao, setSolucao] = useState<Solucao | null>(null);
  const [dicas, setDicas] = useState<string[]>([]);
  const [aba, setAba] = useState<Aba>("enunciado");
  const [corrigindo, setCorrigindo] = useState(false);
  const [salvo, setSalvo] = useState(true);
  const [erro, setErro] = useState("");

  const relogioDoAutosave = useRef<number>();
  const areaDoResultado = useRef<HTMLDivElement>(null);
  const codigoAtual = useRef("");
  codigoAtual.current = codigo;

  // ------------------------------------------------------------- carregar --
  useEffect(() => {
    let cancelado = false;
    setExercicio(null);
    setResultado(null);
    setSolucao(null);
    setErro("");

    api
      .detalhar(id)
      .then((dados) => {
        if (cancelado) return;
        setExercicio(dados);
        setCodigo(dados.codigo);
        setDicas(dados.dicas_liberadas);
        setAba("enunciado");
        setSalvo(true);
      })
      .catch((e: Error) => !cancelado && setErro(e.message));

    return () => {
      cancelado = true;
    };
  }, [id]);

  // ------------------------------------------------------------- autosave --
  const agendarSalvamento = useCallback(
    (texto: string) => {
      window.clearTimeout(relogioDoAutosave.current);
      setSalvo(false);
      relogioDoAutosave.current = window.setTimeout(() => {
        api
          .salvar(id, texto)
          .then(() => setSalvo(true))
          .catch((e: Error) => setErro(e.message));
      }, ATRASO_DO_AUTOSAVE_MS);
    },
    [id],
  );

  const mudarCodigo = useCallback(
    (texto: string) => {
      setCodigo(texto);
      agendarSalvamento(texto);
    },
    [agendarSalvamento],
  );

  // Salva o que estiver pendente ao sair da tela, para não perder o último trecho.
  useEffect(
    () => () => {
      window.clearTimeout(relogioDoAutosave.current);
    },
    [],
  );

  // ------------------------------------------------------------- corrigir --
  const corrigir = useCallback(async () => {
    if (corrigindo) return;
    window.clearTimeout(relogioDoAutosave.current);
    setCorrigindo(true);
    setErro("");
    try {
      const saida = await api.corrigir(id, codigoAtual.current);
      setSalvo(true);
      setResultado(saida);
      if (saida.ok) setSolucao(null);
      // O editor é alto: sem isto, o resultado pode nascer fora da tela.
      window.requestAnimationFrame(() =>
        areaDoResultado.current?.scrollIntoView({ behavior: "smooth", block: "nearest" }),
      );
    } catch (e) {
      setErro((e as Error).message);
    } finally {
      setCorrigindo(false);
    }
  }, [corrigindo, id]);

  // Ctrl+Enter também funciona fora do editor.
  useEffect(() => {
    const aoTeclar = (evento: KeyboardEvent) => {
      if ((evento.ctrlKey || evento.metaKey) && evento.key === "Enter") {
        evento.preventDefault();
        void corrigir();
      }
    };
    window.addEventListener("keydown", aoTeclar);
    return () => window.removeEventListener("keydown", aoTeclar);
  }, [corrigir]);

  // ---------------------------------------------------------------- dicas --
  const pedirDica = async () => {
    try {
      const nova = await api.dica(id);
      setDicas((anteriores) => [...anteriores, nova.texto]);
    } catch (e) {
      setErro((e as Error).message);
    }
  };

  const verSolucao = async (forcar = false) => {
    try {
      setSolucao(await api.solucao(id, forcar));
    } catch (e) {
      if (e instanceof ErroDaApi && e.status === 409) {
        setErro(`${e.message} Tente corrigir ao menos uma vez.`);
      } else {
        setErro((e as Error).message);
      }
    }
  };

  // ----------------------------------------------------------------- vista --
  if (erro && !exercicio) return <div className="pagina erro-global">{erro}</div>;
  if (!exercicio) return <p className="carregando">carregando…</p>;

  const revisao = exercicio.estado === "resolvido";

  return (
    <div className="resolver">
      <aside className="coluna-esquerda">
        <header className="cabecalho-do-exercicio">
          <div className="identificacao">
            <span className="id mono">{exercicio.id}</span>
            <Nivel nivel={exercicio.nivel} />
          </div>
          <h1>{exercicio.titulo}</h1>
          <div className="meta">
            <span className="fraco">~{exercicio.tempo_min} min</span>
            <div className="tags">
              {exercicio.tags.map((t) => (
                <span key={t} className="tag">
                  #{t}
                </span>
              ))}
            </div>
          </div>
          {revisao && <p className="aviso-revisao">Você já resolveu isto — é revisão.</p>}
        </header>

        <div className="abas">
          <button
            className={aba === "enunciado" ? "ativa" : ""}
            onClick={() => setAba("enunciado")}
          >
            Enunciado
          </button>
          <button
            className={aba === "teoria" ? "ativa" : ""}
            onClick={() => setAba("teoria")}
            disabled={!exercicio.teoria}
          >
            Teoria do módulo
          </button>
        </div>

        <div className="painel-de-leitura">
          <Markdown texto={aba === "enunciado" ? exercicio.enunciado : exercicio.teoria} />
        </div>

        {aba === "enunciado" && (
          <Dicas
            dicas={dicas}
            total={exercicio.total_de_dicas}
            onPedir={pedirDica}
            ocupado={corrigindo}
          />
        )}
      </aside>

      <main className="coluna-direita">
        <div className="barra-do-editor">
          <span className="fraco mono">
            {exercicio.linguagem === "sql" ? "SQL · DuckDB" : "Python"}
          </span>
          <span className={`estado-do-salvamento ${salvo ? "" : "pendente"}`}>
            {salvo ? "salvo" : "salvando…"}
          </span>
          <div className="espaco" />
          <button onClick={() => void corrigir()} disabled={corrigindo} className="principal">
            {corrigindo ? "Corrigindo…" : "Corrigir"}
            <kbd>Ctrl ↵</kbd>
          </button>
        </div>

        <Editor
          codigo={codigo}
          linguagem={exercicio.linguagem}
          onMudar={mudarCodigo}
          onCorrigir={() => void corrigir()}
        />

        <div className="area-de-resultado" ref={areaDoResultado}>
          {erro && <div className="erro-global">{erro}</div>}

          {resultado && (
            <PainelDoResultado
              resultado={resultado}
              dicasRestantes={exercicio.total_de_dicas - dicas.length}
              onPedirDica={pedirDica}
              onVerSolucao={() => void verSolucao(true)}
            />
          )}

          {resultado?.ok && (
            <div className="depois-de-acertar">
              <button className="principal" onClick={() => navegar("/")}>
                Próximo exercício
              </button>
              {!solucao && (
                <button onClick={() => void verSolucao(true)}>
                  Comparar com o gabarito
                </button>
              )}
            </div>
          )}

          {solucao && (
            <section className="gabarito">
              <h2 className="titulo-secao">Gabarito comentado</h2>
              <pre>
                <code>{solucao.codigo}</code>
              </pre>
            </section>
          )}
        </div>
      </main>
    </div>
  );
}
