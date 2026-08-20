import { useEffect, useState } from "react";
import { NavLink, Route, Routes } from "react-router-dom";

import { api } from "./api/cliente";
import { Catalogo } from "./rotas/Catalogo";
import { Hoje } from "./rotas/Hoje";
import { Painel } from "./rotas/Painel";
import { Resolver } from "./rotas/Resolver";
import { Revisao } from "./rotas/Revisao";
import "./rotas/paginas.css";

const classeDoLink = ({ isActive }: { isActive: boolean }) => (isActive ? "ativo" : "");

export function App() {
  const [vencidas, setVencidas] = useState(0);

  // O contador de revisões vive no topo, então é recarregado a cada navegação
  // que possa tê-lo mudado — barato, e evita um número desatualizado à vista.
  useEffect(() => {
    const atualizar = () =>
      api
        .revisao()
        .then((fila) => setVencidas(fila.length))
        .catch(() => setVencidas(0));
    atualizar();
    const relogio = window.setInterval(atualizar, 60_000);
    return () => window.clearInterval(relogio);
  }, []);

  return (
    <div className="app">
      <header className="topo">
        <NavLink to="/" className="marca">
          Curso <span>Aurora</span>
        </NavLink>
        <nav>
          <NavLink to="/" className={classeDoLink} end>
            Hoje
          </NavLink>
          <NavLink to="/revisao" className={classeDoLink}>
            Revisão
            {vencidas > 0 && <span className="selo-vencidas">{vencidas}</span>}
          </NavLink>
          <NavLink to="/catalogo" className={classeDoLink}>
            Catálogo
          </NavLink>
          <NavLink to="/progresso" className={classeDoLink}>
            Progresso
          </NavLink>
        </nav>
      </header>

      <div className="conteudo">
        <Routes>
          <Route path="/" element={<Hoje />} />
          <Route path="/exercicio/:id" element={<Resolver />} />
          <Route path="/revisao" element={<Revisao />} />
          <Route path="/catalogo" element={<Catalogo />} />
          <Route path="/progresso" element={<Painel />} />
          <Route
            path="*"
            element={<div className="pagina">Página não encontrada.</div>}
          />
        </Routes>
      </div>
    </div>
  );
}
