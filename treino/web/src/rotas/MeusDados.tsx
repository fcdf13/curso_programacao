/** Meus dados — os direitos do titular em botão.
 *
 *  Cada coisa aqui existe porque a LGPD dá esse direito (art. 18) e porque
 *  atender por email é atender no papel: ver, baixar, revogar o consentimento e
 *  apagar a conta são quatro cliques, não quatro pedidos.
 */

import { useCallback, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { api, ErroDaApi } from "../api/cliente";
import type { EstadoDoConsentimento, Termo } from "../api/tipos";
import { useSessao } from "../sessao";
import "./meusdados.css";
import "./paginas.css";

function paraData(iso: string | null): string {
  if (iso === null) return "";
  return new Date(iso).toLocaleDateString("pt-BR", {
    day: "2-digit",
    month: "long",
    year: "numeric",
  });
}

/** O termo é markdown simples: títulos, ênfase e listas. Uma biblioteca inteira
 *  para isso seria peso de bundle sem retorno.
 *
 *  Agrupa por **bloco**, separado por linha em branco — não por linha. Markdown
 *  quebra um parágrafo em várias linhas no arquivo, e tratar cada linha como um
 *  parágrafo transformava uma frase em três caixas soltas.
 */
function Enfase({ texto }: { texto: string }) {
  // Um passe só, para `**negrito**` ganhar de `*itálico*` — senão o primeiro
  // asterisco do negrito casaria como abertura de itálico.
  const partes = texto.split(/(\*\*[^*]+\*\*|\*[^*]+\*)/g);
  return (
    <>
      {partes.map((parte, indice) => {
        if (parte.startsWith("**") && parte.endsWith("**")) {
          return <strong key={indice}>{parte.slice(2, -2)}</strong>;
        }
        if (parte.startsWith("*") && parte.endsWith("*") && parte.length > 2) {
          return <em key={indice}>{parte.slice(1, -1)}</em>;
        }
        return <span key={indice}>{parte}</span>;
      })}
    </>
  );
}

function Termo({ texto }: { texto: string }) {
  const blocos = texto
    .split(/\n\s*\n/)
    .map((bloco) => bloco.trim())
    .filter((bloco) => bloco !== "" && bloco !== "---");

  return (
    <div className="termo">
      {blocos.map((bloco, indice) => {
        const linhas = bloco.split("\n").map((linha) => linha.trim());

        if (linhas[0]!.startsWith("## ")) {
          return <h3 key={indice}>{linhas[0]!.slice(3)}</h3>;
        }
        if (linhas[0]!.startsWith("# ")) {
          return <h2 key={indice}>{linhas[0]!.slice(2)}</h2>;
        }

        if (linhas.every((linha) => linha.startsWith("- "))) {
          return (
            <ul key={indice}>
              {linhas.map((linha, item) => (
                <li key={item}>
                  <Enfase texto={linha.slice(2)} />
                </li>
              ))}
            </ul>
          );
        }

        // O último bloco do termo é a nota de versão, em itálico do começo ao
        // fim — e é o único que se lê como rodapé.
        const inteiro = linhas.join(" ");
        if (inteiro.startsWith("*") && inteiro.endsWith("*") && !inteiro.startsWith("**")) {
          return (
            <p key={indice} className="termo-nota">
              {inteiro.slice(1, -1)}
            </p>
          );
        }

        return (
          <p key={indice}>
            <Enfase texto={inteiro} />
          </p>
        );
      })}
    </div>
  );
}

export function MeusDados() {
  const { eu, sair, recarregar } = useSessao();
  const navegar = useNavigate();

  const [termo, definirTermo] = useState<Termo | null>(null);
  const [estado, definirEstado] = useState<EstadoDoConsentimento | null>(null);
  const [lendoTermo, definirLendoTermo] = useState(false);
  const [erro, definirErro] = useState<string | null>(null);
  const [aviso, definirAviso] = useState<string | null>(null);
  const [ocupado, definirOcupado] = useState(false);

  const [apagando, definirApagando] = useState(false);
  const [confirmacao, definirConfirmacao] = useState("");

  const [senhaAtual, definirSenhaAtual] = useState("");
  const [senhaNova, definirSenhaNova] = useState("");
  const [repetida, definirRepetida] = useState("");

  const carregar = useCallback(async () => {
    definirEstado(await api.consentimento());
  }, []);

  useEffect(() => {
    api.termo().then(definirTermo).catch(() => undefined);
    carregar().catch((falha) =>
      definirErro(falha instanceof ErroDaApi ? falha.message : "Não foi possível carregar."),
    );
  }, [carregar]);

  const ehAluno = eu?.usuario.papel === "aluno";

  async function comErro(acao: () => Promise<void>) {
    definirErro(null);
    definirAviso(null);
    definirOcupado(true);
    try {
      await acao();
    } catch (falha) {
      definirErro(falha instanceof ErroDaApi ? falha.message : "Não foi possível concluir.");
    } finally {
      definirOcupado(false);
    }
  }

  const aceitar = () =>
    comErro(async () => {
      definirEstado(await api.consentir());
      definirLendoTermo(false);
      definirAviso("Consentimento registrado.");
    });

  const revogar = () =>
    comErro(async () => {
      definirEstado(await api.revogarConsentimento());
      definirAviso(
        "Consentimento revogado. O app não aceita mais peso, sono nem medidas — " +
          "o que já estava guardado continua onde está.",
      );
    });

  const baixar = () =>
    comErro(async () => {
      const dados = await api.meusDados();
      // Gerado e baixado no navegador: o arquivo com o histórico de saúde não
      // precisa passar por mais lugar nenhum.
      const url = URL.createObjectURL(
        new Blob([JSON.stringify(dados, null, 2)], { type: "application/json" }),
      );
      const link = document.createElement("a");
      link.href = url;
      link.download = `jf-treino-${new Date().toISOString().slice(0, 10)}.json`;
      link.click();
      URL.revokeObjectURL(url);
      definirAviso("Arquivo baixado.");
    });

  const trocarSenha = () =>
    comErro(async () => {
      await api.trocarMinhaSenha(senhaAtual, senhaNova);
      definirSenhaAtual("");
      definirSenhaNova("");
      definirRepetida("");
      // `/api/eu` volta com `senha_provisoria: false` e o aviso do topo some.
      await recarregar();
      definirAviso(
        "Senha trocada. As sessões abertas em outros aparelhos foram encerradas.",
      );
    });

  const apagar = () =>
    comErro(async () => {
      await api.apagarMinhaConta(confirmacao);
      await sair();
      navegar("/entrar", { replace: true });
    });

  return (
    <main className="conteudo pilha">
      <div className="titulo-da-pagina">
        <div>
          <p className="rotulo">Privacidade</p>
          <h1>Meus dados</h1>
        </div>
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

      {ehAluno && estado !== null && (
        <section className="painel pilha">
          <div>
            <h2 className="rotulo">Consentimento</h2>
            {estado.consentido ? (
              <p className="dica" style={{ marginTop: 6 }}>
                Você aceitou o termo em <strong>{paraData(estado.aceito_em)}</strong>.
              </p>
            ) : estado.precisa_reaceitar ? (
              <p className="dica" style={{ marginTop: 6 }}>
                O termo mudou desde a última vez que você aceitou. O sim anterior
                não vale para o texto novo — leia e decida de novo.
              </p>
            ) : (
              <p className="dica" style={{ marginTop: 6 }}>
                Você ainda não aceitou. Sem isso o app não registra peso, sono nem
                medidas — mas o seu treino continua visível.
              </p>
            )}
          </div>

          <div className="acoes">
            <button
              type="button"
              className="botao secundario"
              onClick={() => definirLendoTermo((aberto) => !aberto)}
              aria-expanded={lendoTermo}
            >
              {lendoTermo ? "Fechar o termo" : "Ler o termo"}
            </button>

            {estado.consentido ? (
              <button
                type="button"
                className="botao secundario"
                onClick={revogar}
                disabled={ocupado}
              >
                Revogar consentimento
              </button>
            ) : (
              <button type="button" className="botao" onClick={aceitar} disabled={ocupado}>
                Aceitar o termo
              </button>
            )}
          </div>

          {lendoTermo && termo !== null && <Termo texto={termo.texto} />}
        </section>
      )}

      <section className="painel pilha">
        <div>
          <h2 className="rotulo">Trocar a senha</h2>
          {eu?.usuario.senha_provisoria === true ? (
            <p className="dica" style={{ marginTop: 6 }}>
              <strong>Esta senha foi definida por outra pessoa.</strong> Enquanto
              você não trocá-la, quem a escolheu consegue entrar na sua conta.
            </p>
          ) : (
            <p className="dica" style={{ marginTop: 6 }}>
              Trocar a senha encerra as sessões abertas em outros aparelhos —
              esta continua valendo.
            </p>
          )}
        </div>

        <label className="campo">
          <span>Senha atual</span>
          <input
            type="password"
            autoComplete="current-password"
            value={senhaAtual}
            onChange={(evento) => definirSenhaAtual(evento.target.value)}
          />
        </label>
        <label className="campo">
          <span>Senha nova (mínimo de 10 caracteres)</span>
          <input
            type="password"
            autoComplete="new-password"
            value={senhaNova}
            onChange={(evento) => definirSenhaNova(evento.target.value)}
          />
        </label>
        <label className="campo">
          <span>Repita a senha nova</span>
          <input
            type="password"
            autoComplete="new-password"
            value={repetida}
            onChange={(evento) => definirRepetida(evento.target.value)}
          />
          {repetida !== "" && repetida !== senhaNova && (
            <span className="dica">As duas não batem.</span>
          )}
        </label>

        <div className="acoes">
          <button
            type="button"
            className="botao"
            onClick={trocarSenha}
            disabled={
              ocupado ||
              senhaAtual === "" ||
              senhaNova.length < 10 ||
              senhaNova !== repetida
            }
          >
            Trocar a senha
          </button>
        </div>
      </section>

      <section className="painel pilha">
        <div>
          <h2 className="rotulo">Baixar uma cópia</h2>
          <p className="dica" style={{ marginTop: 6 }}>
            Tudo que o app guarda sobre você, num arquivo JSON que qualquer
            planilha ou programa consegue ler. A senha não vai junto — ela é a
            sua credencial, não um dado sobre você.
          </p>
        </div>
        <div className="acoes">
          <button type="button" className="botao secundario" onClick={baixar} disabled={ocupado}>
            Baixar meus dados
          </button>
        </div>
      </section>

      <section className="painel pilha perigo">
        <div>
          <h2 className="rotulo">Apagar a conta</h2>
          <p className="dica" style={{ marginTop: 6 }}>
            Apaga a sua conta e <strong>tudo</strong> que está nela: check-ins,
            medidas, treinos e histórico. É imediato e <strong>não tem
            volta</strong> — não existe lixeira nem prazo de recuperação.
          </p>
          <p className="dica">
            Se você quer só parar de mandar dado novo, revogue o consentimento
            acima: isso preserva o que já está guardado.
          </p>
        </div>

        {!apagando ? (
          <div className="acoes">
            <button
              type="button"
              className="botao secundario"
              onClick={() => definirApagando(true)}
            >
              Quero apagar a minha conta
            </button>
          </div>
        ) : (
          <div className="pilha">
            <label className="campo">
              <span>
                Para confirmar, digite <strong>{eu?.usuario.email}</strong>
              </span>
              <input
                value={confirmacao}
                onChange={(evento) => definirConfirmacao(evento.target.value)}
                autoCapitalize="none"
                autoComplete="off"
                placeholder={eu?.usuario.email}
              />
            </label>
            <div className="acoes">
              <button
                type="button"
                className="botao perigoso"
                onClick={apagar}
                disabled={ocupado || confirmacao.trim().toLowerCase() !== eu?.usuario.email}
              >
                Apagar tudo, definitivamente
              </button>
              <button
                type="button"
                className="botao secundario"
                onClick={() => {
                  definirApagando(false);
                  definirConfirmacao("");
                }}
              >
                Cancelar
              </button>
            </div>
          </div>
        )}
      </section>
    </main>
  );
}
