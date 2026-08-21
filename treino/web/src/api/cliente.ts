/** Todas as chamadas ao backend, num lugar só. */

import type { Aluno, Exercicio, NovoAluno, QuemSouEu } from "./tipos";

export class ErroDaApi extends Error {
  constructor(
    public status: number,
    mensagem: string,
  ) {
    super(mensagem);
  }

  get naoAutenticado(): boolean {
    return this.status === 401;
  }
}

/** Achata o 422 do FastAPI, que vem como lista de erros por campo. */
function mensagemDoErro(corpo: unknown, status: number, caminho: string): string {
  const detalhe = (corpo as { detail?: unknown } | null)?.detail;

  if (typeof detalhe === "string") return detalhe;

  if (Array.isArray(detalhe)) {
    const partes = detalhe
      .map((item) => (item as { msg?: string }).msg)
      .filter((msg): msg is string => Boolean(msg));
    if (partes.length > 0) return partes.join("; ");
  }

  return `Erro ${status} em ${caminho}`;
}

async function pedir<T>(caminho: string, opcoes: RequestInit = {}): Promise<T> {
  const resposta = await fetch(`/api${caminho}`, {
    headers: { "Content-Type": "application/json" },
    // O cookie de sessão é httpOnly e mora na mesma origem.
    credentials: "same-origin",
    ...opcoes,
  });

  if (!resposta.ok) {
    const corpo = await resposta.json().catch(() => null);
    throw new ErroDaApi(resposta.status, mensagemDoErro(corpo, resposta.status, caminho));
  }

  if (resposta.status === 204) return undefined as T;
  return (await resposta.json()) as T;
}

const comCorpo = (metodo: string, dados: unknown): RequestInit => ({
  method: metodo,
  body: JSON.stringify(dados),
});

export const api = {
  entrar: (email: string, senha: string) =>
    pedir<QuemSouEu>("/entrar", comCorpo("POST", { email, senha })),

  sair: () => pedir<void>("/sair", { method: "POST" }),

  eu: () => pedir<QuemSouEu>("/eu"),

  listarAlunos: () => pedir<Aluno[]>("/alunos"),

  cadastrarAluno: (dados: NovoAluno) =>
    pedir<Aluno>("/alunos", comCorpo("POST", dados)),

  verAluno: (id: number) => pedir<Aluno>(`/alunos/${id}`),

  editarAluno: (id: number, dados: Partial<Aluno>) =>
    pedir<Aluno>(`/alunos/${id}`, comCorpo("PATCH", dados)),

  listarExercicios: (filtros: { busca?: string; grupo?: string } = {}) => {
    const parametros = new URLSearchParams();
    if (filtros.busca) parametros.set("busca", filtros.busca);
    if (filtros.grupo) parametros.set("grupo", filtros.grupo);
    const consulta = parametros.toString();
    return pedir<Exercicio[]>(`/exercicios${consulta ? `?${consulta}` : ""}`);
  },

  gruposMusculares: () => pedir<string[]>("/exercicios/grupos"),
};
