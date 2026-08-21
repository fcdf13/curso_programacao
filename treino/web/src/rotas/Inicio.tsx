/** A tela do aluno. Na fase 0 é a boas-vindas com o perfil; o check-in semanal
 *  ocupa este lugar na fase 1. */

import { useEffect, useState } from "react";

import { api, ErroDaApi } from "../api/cliente";
import type { Aluno } from "../api/tipos";
import { useSessao } from "../sessao";
import "./paginas.css";

export function Inicio() {
  const { eu } = useSessao();
  const [aluno, definirAluno] = useState<Aluno | null>(null);
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
  }, [alunoId]);

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

      <div className="vazio">
        <p>
          <strong>Seu treino ainda não foi montado.</strong>
        </p>
        <p>
          Assim que o João publicar a periodização, ela aparece aqui. O check-in semanal —
          peso, sono, medidas — entra na próxima fase.
        </p>
      </div>

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
