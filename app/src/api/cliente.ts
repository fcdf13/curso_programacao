/** Todas as chamadas ao backend, num lugar só. */

import type {
  Detalhe,
  Dica,
  PainelDeProgresso,
  PlanoDoDia,
  ResultadoDaCorrecao,
  Resumo,
  Solucao,
} from "./tipos";

export class ErroDaApi extends Error {
  constructor(public status: number, mensagem: string) {
    super(mensagem);
  }
}

async function pedir<T>(caminho: string, opcoes: RequestInit = {}): Promise<T> {
  const resposta = await fetch(`/api${caminho}`, {
    headers: { "Content-Type": "application/json" },
    ...opcoes,
  });
  if (!resposta.ok) {
    // O FastAPI devolve {"detail": "..."} nos erros; se não vier, fica o status.
    const corpo = await resposta.json().catch(() => null);
    throw new ErroDaApi(
      resposta.status,
      corpo?.detail ?? `Erro ${resposta.status} em ${caminho}`,
    );
  }
  return resposta.json() as Promise<T>;
}

const comCorpo = (metodo: string, dados: unknown): RequestInit => ({
  method: metodo,
  body: JSON.stringify(dados),
});

export const api = {
  listar: (filtros: { busca?: string; bloco?: string } = {}) => {
    const parametros = new URLSearchParams();
    if (filtros.busca) parametros.set("busca", filtros.busca);
    if (filtros.bloco) parametros.set("bloco", filtros.bloco);
    const consulta = parametros.toString();
    return pedir<Resumo[]>(`/exercicios${consulta ? `?${consulta}` : ""}`);
  },

  hoje: (quantidade = 5) => pedir<PlanoDoDia>(`/hoje?quantidade=${quantidade}`),

  detalhar: (id: string) => pedir<Detalhe>(`/exercicios/${id}`),

  salvar: (id: string, codigo: string) =>
    pedir<{ codigo: string }>(`/exercicios/${id}/resposta`, comCorpo("PUT", { codigo })),

  corrigir: (id: string, codigo: string) =>
    pedir<ResultadoDaCorrecao>(`/exercicios/${id}/check`, comCorpo("POST", { codigo })),

  dica: (id: string) => pedir<Dica>(`/exercicios/${id}/dica`, { method: "POST" }),

  solucao: (id: string, forcar = false) =>
    pedir<Solucao>(`/exercicios/${id}/solucao${forcar ? "?forcar=true" : ""}`),

  revisao: () => pedir<Resumo[]>("/revisao"),

  prepararRevisao: (id: string) =>
    pedir<{ codigo: string }>(`/revisao/${id}/preparar`, { method: "POST" }),

  progresso: () => pedir<PainelDeProgresso>("/progresso"),
};
