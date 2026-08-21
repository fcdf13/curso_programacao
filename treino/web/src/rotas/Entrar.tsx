import { useState } from "react";
import type { FormEvent } from "react";
import { Navigate, useLocation } from "react-router-dom";

import { ErroDaApi } from "../api/cliente";
import { Marca } from "../componentes/Marca";
import { useSessao } from "../sessao";
import "./entrar.css";

export function Entrar() {
  const { eu, carregando, entrar } = useSessao();
  const local = useLocation();

  const [email, definirEmail] = useState("");
  const [senha, definirSenha] = useState("");
  const [erro, definirErro] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);

  if (carregando) return null;

  if (eu !== null) {
    // Volta para onde a pessoa tentou ir antes de ser mandada para cá.
    const destino = (local.state as { de?: string } | null)?.de ?? "/";
    return <Navigate to={destino} replace />;
  }

  async function enviar(evento: FormEvent) {
    evento.preventDefault();
    definirErro(null);
    definirEnviando(true);
    try {
      await entrar(email, senha);
    } catch (falha) {
      definirErro(
        falha instanceof ErroDaApi
          ? falha.message
          : "Não foi possível conectar. Verifique sua internet.",
      );
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <main className="entrar">
      <form className="entrar-cartao" onSubmit={enviar}>
        <div className="entrar-marca">
          <Marca tamanho={52} />
          <h1 className="marca-texto">JF Treino</h1>
          <p>Acompanhamento com o João Filho</p>
        </div>

        {erro !== null && (
          <p className="aviso erro" role="alert">
            {erro}
          </p>
        )}

        <label className="campo">
          <span>Email</span>
          <input
            type="email"
            value={email}
            onChange={(evento) => definirEmail(evento.target.value)}
            autoComplete="username"
            autoCapitalize="none"
            required
          />
        </label>

        <label className="campo">
          <span>Senha</span>
          <input
            type="password"
            value={senha}
            onChange={(evento) => definirSenha(evento.target.value)}
            autoComplete="current-password"
            required
          />
        </label>

        <button type="submit" className="botao" disabled={enviando}>
          {enviando ? "Entrando…" : "Entrar"}
        </button>

        <p className="entrar-nota">
          Sua conta é criada pelo João. Se você ainda não tem acesso, fale com ele.
        </p>
      </form>
    </main>
  );
}
