/** A dieta do aluno, pela mão do João.
 *
 *  Uma tela por aluno: o protocolo em vigor, editável, e os anteriores em
 *  lista. Os antigos ficam guardados — trocar o protocolo não é motivo para
 *  perder o que o aluno seguia mês passado.
 */

import { useCallback, useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

import { api, ErroDaApi } from "../api/cliente";
import type { Aluno, Protocolo, ProtocoloNaLista } from "../api/tipos";
import { EditorDeProtocolo } from "../componentes/EditorDeProtocolo";
import "./dieta.css";
import "./paginas.css";

function data(iso: string): string {
  return new Date(iso).toLocaleDateString("pt-BR", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  });
}

export function ProtocoloAlimentar() {
  const { id } = useParams<{ id: string }>();
  const alunoId = id === undefined ? null : Number(id);

  const [aluno, definirAluno] = useState<Aluno | null>(null);
  const [protocolo, definirProtocolo] = useState<Protocolo | null>(null);
  const [anteriores, definirAnteriores] = useState<ProtocoloNaLista[]>([]);
  const [carregando, definirCarregando] = useState(true);
  const [erro, definirErro] = useState<string | null>(null);
  const [aviso, definirAviso] = useState<string | null>(null);

  const carregar = useCallback(async (quem: number) => {
    definirAluno(await api.verAluno(quem));
    try {
      definirProtocolo(await api.protocoloDoAluno(quem));
    } catch (falha) {
      // 404 aqui é o caso normal do primeiro protocolo, não erro.
      if (!(falha instanceof ErroDaApi && falha.status === 404)) throw falha;
      definirProtocolo(null);
    }
    definirAnteriores(await api.listarProtocolos(quem));
  }, []);

  useEffect(() => {
    if (alunoId === null) return;
    definirCarregando(true);
    carregar(alunoId)
      .catch((falha) =>
        definirErro(
          falha instanceof ErroDaApi ? falha.message : "Não foi possível carregar.",
        ),
      )
      .finally(() => definirCarregando(false));
  }, [alunoId, carregar]);

  async function abrir(protocoloId: number) {
    definirErro(null);
    definirAviso(null);
    try {
      definirProtocolo(await api.verProtocolo(protocoloId));
    } catch (falha) {
      definirErro(falha instanceof ErroDaApi ? falha.message : "Não foi possível abrir.");
    }
  }

  function comecarDoZero() {
    definirAviso(null);
    definirProtocolo(null);
  }

  if (erro !== null && aluno === null) {
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

  if (carregando || alunoId === null) {
    return (
      <main className="conteudo">
        <p className="carregando">Carregando…</p>
      </main>
    );
  }

  const guardados = anteriores.filter((item) => item.id !== protocolo?.id);

  return (
    <main className="conteudo pilha">
      <div className="titulo-da-pagina">
        <div>
          <p className="rotulo">
            <Link to={`/alunos/${alunoId}`}>{aluno?.nome ?? "Aluno"}</Link>
          </p>
          <h1>Protocolo alimentar</h1>
        </div>
        {protocolo !== null && (
          <button type="button" className="botao secundario" onClick={comecarDoZero}>
            Novo protocolo
          </button>
        )}
      </div>

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

      <EditorDeProtocolo
        // Trocar de protocolo troca o rascunho inteiro: sem a chave, o React
        // manteria o estado do editor anterior dentro do novo.
        key={protocolo?.id ?? "novo"}
        alunoId={alunoId}
        protocolo={protocolo}
        aoSalvar={(salvo) => {
          definirProtocolo(salvo);
          definirAviso(`“${salvo.nome}” salvo e em vigor para o aluno.`);
          api.listarProtocolos(alunoId).then(definirAnteriores).catch(() => undefined);
        }}
      />

      {guardados.length > 0 && (
        <section className="pilha">
          <h2 className="rotulo">Protocolos anteriores</h2>
          <ul className="lista-de-blocos">
            {guardados.map((item) => (
              <li key={item.id}>
                <button type="button" className="como-link" onClick={() => abrir(item.id)}>
                  <span className="bloco-nome">{item.nome}</span>
                  <span className="prescricao-detalhe">
                    {data(item.criado_em)}
                    {item.ativo && " · em vigor"}
                  </span>
                </button>
              </li>
            ))}
          </ul>
        </section>
      )}
    </main>
  );
}
