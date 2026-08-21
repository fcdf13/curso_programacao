/** O catálogo de exercícios, com a convenção de carga de cada um à vista.
 *
 *  A convenção não é detalhe de banco: é o que decide se "25" quer dizer um
 *  halter de 25 kg ou dois. A estimativa de 1RM da fase 3 depende disso estar
 *  combinado, então a informação fica visível desde já.
 */

import { useEffect, useMemo, useState } from "react";

import { api, ErroDaApi } from "../api/cliente";
import type { ConvencaoDeCarga, Exercicio } from "../api/tipos";
import "./paginas.css";

const CONVENCAO: Record<ConvencaoDeCarga, string> = {
  total: "carga total",
  por_halter: "por halter",
  peso_corporal: "peso corporal",
};

const EXPLICACAO: Record<ConvencaoDeCarga, string> = {
  total: "Registre o peso total, incluindo a barra.",
  por_halter: "Registre o peso de um halter, mesmo usando dois.",
  peso_corporal: "Registre só a carga adicional, se houver.",
};

export function Catalogo() {
  const [exercicios, definirExercicios] = useState<Exercicio[] | null>(null);
  const [erro, definirErro] = useState<string | null>(null);
  const [busca, definirBusca] = useState("");
  const [grupo, definirGrupo] = useState("");
  const [grupos, definirGrupos] = useState<string[]>([]);

  useEffect(() => {
    api.gruposMusculares().then(definirGrupos).catch(() => definirGrupos([]));
  }, []);

  useEffect(() => {
    // Espera o usuário parar de digitar antes de consultar.
    const relogio = setTimeout(() => {
      api
        .listarExercicios({ busca: busca || undefined, grupo: grupo || undefined })
        .then(definirExercicios)
        .catch((falha) =>
          definirErro(
            falha instanceof ErroDaApi ? falha.message : "Não foi possível carregar.",
          ),
        );
    }, 250);
    return () => clearTimeout(relogio);
  }, [busca, grupo]);

  const porGrupo = useMemo(() => {
    const mapa = new Map<string, Exercicio[]>();
    for (const exercicio of exercicios ?? []) {
      const lista = mapa.get(exercicio.grupo_muscular) ?? [];
      lista.push(exercicio);
      mapa.set(exercicio.grupo_muscular, lista);
    }
    return [...mapa.entries()];
  }, [exercicios]);

  return (
    <main className="conteudo pilha">
      <div className="titulo-da-pagina">
        <div>
          <p className="rotulo">Catálogo</p>
          <h1>Exercícios</h1>
        </div>
      </div>

      <div className="linha-de-campos">
        <label className="campo">
          <span>Buscar</span>
          <input
            type="search"
            value={busca}
            onChange={(evento) => definirBusca(evento.target.value)}
            placeholder="supino, agachamento…"
          />
        </label>
        <label className="campo">
          <span>Grupo muscular</span>
          <select value={grupo} onChange={(evento) => definirGrupo(evento.target.value)}>
            <option value="">Todos</option>
            {grupos.map((nome) => (
              <option key={nome} value={nome}>
                {nome}
              </option>
            ))}
          </select>
        </label>
      </div>

      {erro !== null && (
        <p className="aviso erro" role="alert">
          {erro}
        </p>
      )}

      {exercicios === null && erro === null && <p className="carregando">Carregando…</p>}

      {exercicios !== null && exercicios.length === 0 && (
        <div className="vazio">
          <p>Nenhum exercício com esse filtro.</p>
        </div>
      )}

      {porGrupo.map(([nome, lista]) => (
        <section key={nome} className="grupo-de-exercicios">
          <h2 className="rotulo">{nome}</h2>
          <ul className="lista-de-exercicios">
            {lista.map((exercicio) => (
              <li key={exercicio.id}>
                <span className="exercicio-nome">{exercicio.nome}</span>
                <span
                  className={`etiqueta convencao-${exercicio.convencao_de_carga}`}
                  title={EXPLICACAO[exercicio.convencao_de_carga]}
                >
                  {CONVENCAO[exercicio.convencao_de_carga]}
                </span>
                <span className="exercicio-incremento">
                  +{exercicio.incremento_kg.toLocaleString("pt-BR")} kg
                </span>
              </li>
            ))}
          </ul>
        </section>
      ))}
    </main>
  );
}
