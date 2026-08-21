/** A tela do João: quem são os alunos e o formulário para cadastrar mais um. */

import { useEffect, useState } from "react";
import type { FormEvent } from "react";
import { Link } from "react-router-dom";

import { api, ErroDaApi } from "../api/cliente";
import type { Aluno, AlunoComAlertas, Sexo } from "../api/tipos";
import "./paginas.css";

const SENHA_MINIMA = 10;

/** Junta o perfil com os alertas dele, na ordem de quem precisa de atenção
 *  primeiro. Sem os alertas (ainda carregando, ou a chamada falhou), cai para
 *  a ordem alfabética que a API de alunos já devolve. */
function ordenarPorAlerta(
  alunos: Aluno[],
  alertas: AlunoComAlertas[] | null,
): { aluno: Aluno; alertas: AlunoComAlertas["alertas"] }[] {
  if (alertas === null) {
    return alunos.map((aluno) => ({ aluno, alertas: [] }));
  }

  const porId = new Map(alunos.map((aluno) => [aluno.id, aluno]));
  const ordenados = alertas
    .map((item) => {
      const aluno = porId.get(item.aluno_id);
      return aluno === undefined ? null : { aluno, alertas: item.alertas };
    })
    .filter(
      (item): item is { aluno: Aluno; alertas: AlunoComAlertas["alertas"] } =>
        item !== null,
    );

  // Um aluno cadastrado depois da última busca de alertas ainda não aparece
  // na lista deles; entra no fim em vez de sumir da tela.
  const vistos = new Set(ordenados.map((item) => item.aluno.id));
  for (const aluno of alunos) {
    if (!vistos.has(aluno.id)) ordenados.push({ aluno, alertas: [] });
  }
  return ordenados;
}

function SinalDeAlerta({ alertas }: { alertas: AlunoComAlertas["alertas"] }) {
  const grave = alertas.some((a) => a.gravidade >= 3);
  const dica = alertas.map((a) => a.mensagem).join(" ");
  return (
    <span
      className={`sinal-de-alerta ${grave ? "grave" : "atencao"}`}
      title={dica}
      aria-label={dica}
    >
      {alertas.length}
    </span>
  );
}


const VAZIO = {
  nome: "",
  email: "",
  senha: "",
  nascimento: "",
  sexo: "" as Sexo | "",
  altura_cm: "",
  objetivo: "",
};

export function Alunos() {
  const [alunos, definirAlunos] = useState<Aluno[] | null>(null);
  const [alertas, definirAlertas] = useState<AlunoComAlertas[] | null>(null);
  const [erro, definirErro] = useState<string | null>(null);

  const [abrirFormulario, definirAbrirFormulario] = useState(false);
  const [formulario, definirFormulario] = useState(VAZIO);
  const [erroDoFormulario, definirErroDoFormulario] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);
  const [recemCadastrado, definirRecemCadastrado] = useState<string | null>(null);

  useEffect(() => {
    api
      .listarAlunos()
      .then(definirAlunos)
      .catch((falha) =>
        definirErro(
          falha instanceof ErroDaApi ? falha.message : "Não foi possível carregar.",
        ),
      );
    // Silenciosa: sem os alertas a lista ainda funciona, só volta a ordenar
    // por nome — um extra que falhou não pode travar a tela principal.
    api.alertasDosAlunos().then(definirAlertas).catch(() => undefined);
  }, []);

  function alterar(campo: keyof typeof VAZIO, valor: string) {
    definirFormulario((atual) => ({ ...atual, [campo]: valor }));
  }

  async function cadastrar(evento: FormEvent) {
    evento.preventDefault();
    definirErroDoFormulario(null);
    definirEnviando(true);
    try {
      const criado = await api.cadastrarAluno({
        nome: formulario.nome,
        email: formulario.email,
        senha: formulario.senha,
        // Campos opcionais vão como null quando em branco: string vazia não
        // passa na validação de data nem de número.
        nascimento: formulario.nascimento || null,
        sexo: formulario.sexo || null,
        altura_cm: formulario.altura_cm ? Number(formulario.altura_cm) : null,
        objetivo: formulario.objetivo || null,
      });
      definirAlunos((atual) =>
        [...(atual ?? []), criado].sort((a, b) => a.nome.localeCompare(b.nome, "pt-BR")),
      );
      definirFormulario(VAZIO);
      definirAbrirFormulario(false);
      definirRecemCadastrado(criado.nome);
    } catch (falha) {
      definirErroDoFormulario(
        falha instanceof ErroDaApi ? falha.message : "Não foi possível cadastrar.",
      );
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <main className="conteudo pilha">
      <div className="titulo-da-pagina">
        <div>
          <p className="rotulo">Seus alunos</p>
          <h1>Alunos</h1>
        </div>
        <button
          type="button"
          className={abrirFormulario ? "botao secundario" : "botao"}
          onClick={() => {
            definirAbrirFormulario((aberto) => !aberto);
            definirRecemCadastrado(null);
          }}
        >
          {abrirFormulario ? "Cancelar" : "Cadastrar aluno"}
        </button>
      </div>

      {recemCadastrado !== null && (
        <p className="aviso certo" role="status">
          {recemCadastrado} foi cadastrado. Passe o email e a senha para ele entrar.
        </p>
      )}

      {abrirFormulario && (
        <form className="painel pilha" onSubmit={cadastrar}>
          {erroDoFormulario !== null && (
            <p className="aviso erro" role="alert">
              {erroDoFormulario}
            </p>
          )}

          <label className="campo">
            <span>Nome</span>
            <input
              value={formulario.nome}
              onChange={(evento) => alterar("nome", evento.target.value)}
              required
              minLength={2}
            />
          </label>

          <div className="linha-de-campos">
            <label className="campo">
              <span>Email</span>
              <input
                type="email"
                value={formulario.email}
                onChange={(evento) => alterar("email", evento.target.value)}
                autoCapitalize="none"
                required
              />
            </label>
            <label className="campo">
              <span>Senha provisória</span>
              <input
                type="text"
                value={formulario.senha}
                onChange={(evento) => alterar("senha", evento.target.value)}
                minLength={SENHA_MINIMA}
                required
              />
            </label>
          </div>

          <div className="linha-de-campos">
            <label className="campo">
              <span>Nascimento</span>
              <input
                type="date"
                value={formulario.nascimento}
                onChange={(evento) => alterar("nascimento", evento.target.value)}
              />
            </label>
            <label className="campo">
              <span>Sexo</span>
              <select
                value={formulario.sexo}
                onChange={(evento) => alterar("sexo", evento.target.value)}
              >
                <option value="">—</option>
                <option value="masculino">Masculino</option>
                <option value="feminino">Feminino</option>
                <option value="outro">Outro</option>
              </select>
            </label>
            <label className="campo">
              <span>Altura (cm)</span>
              <input
                type="number"
                inputMode="numeric"
                min={51}
                max={259}
                value={formulario.altura_cm}
                onChange={(evento) => alterar("altura_cm", evento.target.value)}
              />
            </label>
          </div>

          <label className="campo">
            <span>Objetivo</span>
            <input
              value={formulario.objetivo}
              onChange={(evento) => alterar("objetivo", evento.target.value)}
              placeholder="Corte com 500 kcal de déficit"
              maxLength={200}
            />
          </label>

          <p className="dica">
            A senha aparece em texto de propósito: você precisa copiá-la para passar ao
            aluno. Peça que ele troque assim que entrar.
          </p>

          <button type="submit" className="botao" disabled={enviando}>
            {enviando ? "Cadastrando…" : "Cadastrar"}
          </button>
        </form>
      )}

      {erro !== null && (
        <p className="aviso erro" role="alert">
          {erro}
        </p>
      )}

      {alunos === null && erro === null && <p className="carregando">Carregando…</p>}

      {alunos !== null && alunos.length === 0 && (
        <div className="vazio">
          <p>
            <strong>Nenhum aluno ainda.</strong>
          </p>
          <p>Cadastre o primeiro e ele já consegue entrar no app.</p>
        </div>
      )}

      {alunos !== null && alunos.length > 0 && (
        <ul className="lista-de-alunos">
          {ordenarPorAlerta(alunos, alertas).map(({ aluno, alertas: doAluno }) => {
            const grave = doAluno.some((item) => item.gravidade >= 3);
            const atencao = doAluno.some((item) => item.gravidade === 2);
            return (
            <li key={aluno.id}>
              <Link
                to={`/alunos/${aluno.id}`}
                className={grave ? "grave" : atencao ? "atencao" : undefined}
              >
                <div className="aluno-linha">
                  <span className="aluno-nome">{aluno.nome}</span>
                  {doAluno.length > 0 && <SinalDeAlerta alertas={doAluno} />}
                </div>
                <span className="aluno-objetivo">
                  {doAluno[0]?.mensagem ?? aluno.objetivo ?? "sem objetivo definido"}
                </span>
              </Link>
            </li>
            );
          })}
        </ul>
      )}
    </main>
  );
}
