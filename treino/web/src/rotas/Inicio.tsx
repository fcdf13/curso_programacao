/** A tela do aluno: o treino em andamento, a dieta, o check-in e a evolução. */

import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { api, ErroDaApi } from "../api/cliente";
import type { Aluno, PeriodizacaoNaLista } from "../api/tipos";
import { PainelDeEvolucao } from "../componentes/PainelDeEvolucao";
import { useSessao } from "../sessao";
import "../componentes/prescricao.css";
import "./paginas.css";

export function Inicio() {
  const { eu } = useSessao();
  const [aluno, definirAluno] = useState<Aluno | null>(null);
  const [blocos, definirBlocos] = useState<PeriodizacaoNaLista[]>([]);
  const [erro, definirErro] = useState<string | null>(null);

  const alunoId = eu?.aluno_id ?? null;

  useEffect(() => {
    if (alunoId === null) return;
    api
      .verAluno(alunoId)
      .then(definirAluno)
      .catch((falha) =>
        definirErro(
          falha instanceof ErroDaApi ? falha.message : "Não foi possível carregar.",
        ),
      );
    api.listarPeriodizacoes(alunoId).then(definirBlocos).catch(() => definirBlocos([]));
  }, [alunoId]);

  const ativos = blocos.filter((bloco) => bloco.ativa);

  const primeiroNome = eu?.usuario.nome.split(" ")[0] ?? "";

  return (
    <main className="conteudo pilha">
      <div className="titulo-da-pagina">
        <div>
          <p className="rotulo">Seu acompanhamento</p>
          <h1>Olá, {primeiroNome}</h1>
        </div>
      </div>

      {erro !== null && (
        <p className="aviso erro" role="alert">
          {erro}
        </p>
      )}

      {aluno?.objetivo != null && (
        <div className="painel objetivo">
          <p className="rotulo">Objetivo</p>
          <p className="objetivo-texto">{aluno.objetivo}</p>
        </div>
      )}

      {ativos.length === 0 ? (
        <div className="vazio">
          <p>
            <strong>Seu treino ainda não foi montado.</strong>
          </p>
          <p>
            Assim que o João publicar o bloco, ele aparece aqui. Enquanto isso, o
            check-in semanal e a dieta já funcionam.
          </p>
        </div>
      ) : (
        <section className="pilha">
          <h2 className="rotulo">Seu treino</h2>
          <ul className="lista-de-blocos">
            {ativos.map((bloco) => (
              <li key={bloco.id}>
                <Link to={`/periodizacoes/${bloco.id}`} className="ativa">
                  <span className="bloco-nome">{bloco.nome}</span>
                  <span className="prescricao-detalhe">{bloco.semanas} semanas</span>
                </Link>
              </li>
            ))}
          </ul>
        </section>
      )}

      <div className="painel chamada-de-checkin">
        <div>
          <p className="rotulo">Sua dieta</p>
          <p className="dica" style={{ marginTop: 4 }}>
            O que comer hoje, o que dá para trocar, e o que você já seguiu.
          </p>
        </div>
        <Link to="/dieta" className="botao">
          Ver a dieta
        </Link>
      </div>

      <div className="painel chamada-de-checkin">
        <div>
          <p className="rotulo">Esta semana</p>
          <p className="dica" style={{ marginTop: 4 }}>
            Peso, sono e como o corpo respondeu. Leva um minuto.
          </p>
        </div>
        <Link to="/checkin" className="botao">
          Fazer o check-in
        </Link>
      </div>

      {alunoId !== null && (
        <section className="pilha">
          <h2 className="rotulo">Sua evolução</h2>
          <PainelDeEvolucao alunoId={alunoId} />
        </section>
      )}

      <div className="painel">
        <p className="rotulo">Instalar no celular</p>
        <p className="dica" style={{ marginTop: 8 }}>
          No iPhone, toque em Compartilhar e depois em <strong>Adicionar à Tela de
          Início</strong>. No Android, no menu do navegador, <strong>Instalar
          app</strong>. Ele passa a abrir como aplicativo, em tela cheia.
        </p>
      </div>
    </main>
  );
}
