/** O índice inteiro, com busca e filtro por bloco. */

import { useEffect, useMemo, useState } from "react";

import { api } from "../api/cliente";
import type { Resumo } from "../api/tipos";
import { LinhaDoExercicio } from "../componentes/LinhaDoExercicio";
import "../componentes/lista.css";

const BLOCOS = [
  { chave: "", rotulo: "Tudo" },
  { chave: "A", rotulo: "Python" },
  { chave: "B", rotulo: "Pandas" },
  { chave: "C", rotulo: "SQL" },
  { chave: "D", rotulo: "Ponte" },
];

export function Catalogo() {
  const [todos, setTodos] = useState<Resumo[]>([]);
  const [busca, setBusca] = useState("");
  const [bloco, setBloco] = useState("");
  const [erro, setErro] = useState("");

  useEffect(() => {
    api.listar().then(setTodos).catch((e: Error) => setErro(e.message));
  }, []);

  // Filtrar no cliente evita uma ida ao servidor a cada tecla digitada.
  const visiveis = useMemo(() => {
    const alvo = busca.trim().toLowerCase();
    return todos.filter(
      (ex) =>
        (!bloco || ex.bloco === bloco) &&
        (!alvo ||
          ex.id.toLowerCase().includes(alvo) ||
          ex.titulo.toLowerCase().includes(alvo) ||
          ex.tags.some((t) => t.includes(alvo))),
    );
  }, [todos, busca, bloco]);

  const porModulo = useMemo(() => {
    const grupos = new Map<string, Resumo[]>();
    for (const ex of visiveis) {
      const chave = `${ex.nome_do_bloco} · ${ex.nome_do_modulo}`;
      grupos.set(chave, [...(grupos.get(chave) ?? []), ex]);
    }
    return [...grupos.entries()];
  }, [visiveis]);

  if (erro) return <div className="pagina erro-global">{erro}</div>;

  return (
    <div className="pagina">
      <header className="topo-da-pagina">
        <h1>Catálogo</h1>
        <p className="suave">
          {visiveis.length} de {todos.length} exercícios
        </p>
      </header>

      <div className="filtros">
        <input
          type="search"
          placeholder="buscar por título, id ou tag…"
          value={busca}
          onChange={(e) => setBusca(e.target.value)}
        />
        <div className="botoes-de-bloco">
          {BLOCOS.map((b) => (
            <button
              key={b.chave}
              className={bloco === b.chave ? "principal" : ""}
              onClick={() => setBloco(b.chave)}
            >
              {b.rotulo}
            </button>
          ))}
        </div>
      </div>

      {porModulo.map(([nome, exercicios]) => (
        <section className="secao" key={nome}>
          <h2 className="titulo-secao">
            {nome} <span className="fraco">· {exercicios.length}</span>
          </h2>
          <div className="lista">
            {exercicios.map((ex) => (
              <LinhaDoExercicio key={ex.id} ex={ex} />
            ))}
          </div>
        </section>
      ))}

      {visiveis.length === 0 && todos.length > 0 && (
        <div className="lista">
          <p className="lista-vazia">Nada encontrado.</p>
        </div>
      )}
    </div>
  );
}
