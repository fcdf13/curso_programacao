import { Navigate, Route, Routes, useLocation } from "react-router-dom";
import type { ReactElement } from "react";

import { AvisoDeSenha } from "./componentes/AvisoDeSenha";
import { Cabecalho } from "./componentes/Cabecalho";
import { Alunos } from "./rotas/Alunos";
import { Calculadora } from "./rotas/Calculadora";
import { Catalogo } from "./rotas/Catalogo";
import { Checkin } from "./rotas/Checkin";
import { Dieta } from "./rotas/Dieta";
import { Entrar } from "./rotas/Entrar";
import { FichaDoAluno } from "./rotas/FichaDoAluno";
import { Inicio } from "./rotas/Inicio";
import { MeusDados } from "./rotas/MeusDados";
import { Periodizacao } from "./rotas/Periodizacao";
import { Treinar } from "./rotas/Treinar";
import { ProtocoloAlimentar } from "./rotas/ProtocoloAlimentar";
import { useSessao } from "./sessao";
import type { Papel } from "./api/tipos";

/** Exige login — e, quando `papel` é passado, exige também aquele papel.
 *
 *  Isto é conveniência de navegação, não segurança: quem decide é o servidor.
 *  Esconder um botão no front não protege nada; `jf/auth.py` é que protege.
 */
function Protegido({ children, papel }: { children: ReactElement; papel?: Papel }) {
  const { eu, carregando } = useSessao();
  const local = useLocation();

  // Enquanto /api/eu não respondeu não dá para saber se há sessão; redirecionar
  // aqui expulsaria quem está logado a cada recarga da página.
  if (carregando) return null;

  if (eu === null) {
    return <Navigate to="/entrar" state={{ de: local.pathname }} replace />;
  }

  if (papel !== undefined && eu.usuario.papel !== papel) {
    return <Navigate to="/" replace />;
  }

  return children;
}

/** A raiz manda cada papel para a sua tela. */
function Raiz() {
  const { eu, carregando } = useSessao();
  if (carregando) return null;
  if (eu === null) return <Navigate to="/entrar" replace />;
  return <Navigate to={eu.usuario.papel === "treinador" ? "/alunos" : "/inicio"} replace />;
}

export function App() {
  return (
    <>
      <Cabecalho />
      <AvisoDeSenha />
      <Routes>
        <Route path="/entrar" element={<Entrar />} />
        <Route path="/" element={<Raiz />} />

        <Route
          path="/alunos"
          element={
            <Protegido papel="treinador">
              <Alunos />
            </Protegido>
          }
        />
        <Route
          path="/alunos/:id"
          element={
            <Protegido>
              <FichaDoAluno />
            </Protegido>
          }
        />
        <Route
          path="/alunos/:id/dieta"
          element={
            <Protegido papel="treinador">
              <ProtocoloAlimentar />
            </Protegido>
          }
        />
        <Route
          path="/inicio"
          element={
            <Protegido papel="aluno">
              <Inicio />
            </Protegido>
          }
        />
        <Route
          path="/checkin"
          element={
            <Protegido papel="aluno">
              <Checkin />
            </Protegido>
          }
        />
        <Route
          path="/dieta"
          element={
            <Protegido papel="aluno">
              <Dieta />
            </Protegido>
          }
        />
        <Route
          path="/treinar/:id"
          element={
            <Protegido papel="aluno">
              <Treinar />
            </Protegido>
          }
        />
        <Route
          path="/periodizacoes/:id"
          element={
            <Protegido>
              <Periodizacao />
            </Protegido>
          }
        />
        <Route
          path="/calculadora"
          element={
            <Protegido papel="treinador">
              <Calculadora />
            </Protegido>
          }
        />
        <Route
          path="/meus-dados"
          element={
            <Protegido>
              <MeusDados />
            </Protegido>
          }
        />
        <Route
          path="/exercicios"
          element={
            <Protegido>
              <Catalogo />
            </Protegido>
          }
        />

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </>
  );
}
