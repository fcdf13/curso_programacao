/** A ficha de um aluno. Na fase 0 mostra o perfil; check-in, treino e dieta
 *  entram como abas aqui nas fases seguintes. */

import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

import { api, ErroDaApi } from "../api/cliente";
import type { Aluno } from "../api/tipos";
import "./paginas.css";

const SEXO: Record<string, string> = {
  masculino: "Masculino",
  feminino: "Feminino",
  outro: "Outro",
};

function idade(nascimento: string | null): string | null {
  if (nascimento === null) return null;
  const data = new Date(`${nascimento}T00:00:00`);
  if (Number.isNaN(data.getTime())) return null;

  const hoje = new Date();
  let anos = hoje.getFullYear() - data.getFullYear();
  // Ainda não fez aniversário este ano.
  const mes = hoje.getMonth() - data.getMonth();
  if (mes < 0 || (mes === 0 && hoje.getDate() < data.getDate())) anos -= 1;

  return `${anos} anos`;
}

export function FichaDoAluno() {
  const { id } = useParams<{ id: string }>();
  const [aluno, definirAluno] = useState<Aluno | null>(null);
  const [erro, definirErro] = useState<string | null>(null);

  useEffect(() => {
    if (id === undefined) return;
    definirAluno(null);
    definirErro(null);
    api
      .verAluno(Number(id))
      .then(definirAluno)
      .catch((falha) =>
        definirErro(
          falha instanceof ErroDaApi ? falha.message : "Não foi possível carregar.",
        ),
      );
  }, [id]);

  if (erro !== null) {
    return (
      <main className="conteudo pilha">
        <p className="aviso erro" role="alert">
          {erro}
        </p>
        <p>
          <Link to="/alunos">Voltar para a lista</Link>
        </p>
      </main>
    );
  }

  if (aluno === null) {
    return (
      <main className="conteudo">
        <p className="carregando">Carregando…</p>
      </main>
    );
  }

  const fichas: [string, string | null][] = [
    ["Email", aluno.email],
    ["Idade", idade(aluno.nascimento)],
    ["Sexo", aluno.sexo === null ? null : (SEXO[aluno.sexo] ?? null)],
    ["Altura", aluno.altura_cm === null ? null : `${aluno.altura_cm} cm`],
    ["Objetivo", aluno.objetivo],
  ];

  return (
    <main className="conteudo pilha">
      <div className="titulo-da-pagina">
        <div>
          <p className="rotulo">
            <Link to="/alunos">Alunos</Link>
          </p>
          <h1>{aluno.nome}</h1>
        </div>
      </div>

      <div className="painel">
        <dl className="ficha">
          {fichas.map(([nome, valor]) => (
            <div key={nome}>
              <dt>{nome}</dt>
              <dd className={valor === null ? "ausente" : undefined}>
                {valor ?? "não informado"}
              </dd>
            </div>
          ))}
        </dl>
      </div>

      <div className="vazio">
        <p>
          <strong>Ainda não há histórico.</strong>
        </p>
        <p>
          O check-in semanal e os gráficos de evolução entram na fase 1; a prescrição de
          treino, na fase 2.
        </p>
      </div>
    </main>
  );
}
