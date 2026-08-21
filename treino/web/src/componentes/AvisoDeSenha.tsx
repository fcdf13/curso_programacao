/** "Outra pessoa sabe a sua senha" é um aviso que precisa aparecer em toda tela.
 *
 *  Enquanto a senha for provisória — foi o João quem a definiu, cadastrando ou
 *  redefinindo — ele consegue entrar como o aluno. Dizer isso uma vez só, numa
 *  tela que o aluno talvez não abra, seria o mesmo que não dizer. Some sozinho
 *  quando ele troca.
 */

import { Link, useLocation } from "react-router-dom";

import { useSessao } from "../sessao";
import "./avisodesenha.css";

export function AvisoDeSenha() {
  const { eu } = useSessao();
  const local = useLocation();

  if (eu === null || !eu.usuario.senha_provisoria) return null;
  // Na própria tela de troca o aviso viraria eco: a mesma frase já está lá.
  if (local.pathname === "/meus-dados") return null;

  return (
    <div className="aviso-de-senha" role="status">
      <span>
        Sua senha foi definida por outra pessoa, que consegue entrar na sua
        conta enquanto ela valer.
      </span>
      <Link to="/meus-dados">Trocar agora</Link>
    </div>
  );
}
