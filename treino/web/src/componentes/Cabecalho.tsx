/** A barra fixa do topo: marca, navegação por papel e o botão de sair. */

import { NavLink, useNavigate } from "react-router-dom";

import { useSessao } from "../sessao";
import { Marca } from "./Marca";
import "./cabecalho.css";

export function Cabecalho() {
  const { eu, sair } = useSessao();
  const navegar = useNavigate();

  if (eu === null) return null;

  const ehTreinador = eu.usuario.papel === "treinador";

  async function terminar() {
    await sair();
    navegar("/entrar", { replace: true });
  }

  return (
    <header className="cabecalho">
      <div className="cabecalho-interno">
        <NavLink to="/" className="cabecalho-marca">
          <Marca />
          <span className="marca-texto">JF Treino</span>
        </NavLink>

        <nav className="cabecalho-nav">
          {ehTreinador ? (
            <NavLink to="/alunos">Alunos</NavLink>
          ) : (
            <NavLink to="/inicio">Início</NavLink>
          )}
          <NavLink to="/exercicios">Exercícios</NavLink>
        </nav>

        <div className="cabecalho-conta">
          <span className="cabecalho-nome" title={eu.usuario.email}>
            {eu.usuario.nome}
          </span>
          <button type="button" className="botao discreto" onClick={terminar}>
            Sair
          </button>
        </div>
      </div>
    </header>
  );
}
