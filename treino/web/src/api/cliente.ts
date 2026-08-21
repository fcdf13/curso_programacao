/** Todas as chamadas ao backend, num lugar só. */

import type {
  Aderencia,
  Alimento,
  Aluno,
  AlunoComAlertas,
  CargaSugerida,
  Checkin,
  Evolucao,
  Exercicio,
  EscopoDaTecnica,
  EstadoDoConsentimento,
  Leitura,
  MeusDados,
  NovaPrescricao,
  NovaSerie,
  NovoAluno,
  NovoCheckin,
  PedidoDeEstimativa,
  Periodizacao,
  PeriodizacaoBase,
  PeriodizacaoNaLista,
  ForcaDoExercicio,
  Prescricao,
  Protocolo,
  ProtocoloLido,
  ProtocoloNaLista,
  ProtocoloNovo,
  QuemSouEu,
  RespostaDaCalculadora,
  SessaoModelo,
  SerieParaEnviar,
  Tecnica,
  Termo,
  TreinoNaLista,
  TreinoRealizado,
} from "./tipos";

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

  // ------------------------------------------------------------- treino

  tecnicas: (escopo?: EscopoDaTecnica) =>
    pedir<Tecnica[]>(`/tecnicas${escopo ? `?escopo=${escopo}` : ""}`),

  listarPeriodizacoes: (alunoId: number) =>
    pedir<PeriodizacaoNaLista[]>(`/alunos/${alunoId}/periodizacoes`),

  criarPeriodizacao: (alunoId: number, dados: Partial<PeriodizacaoBase>) =>
    pedir<Periodizacao>(`/alunos/${alunoId}/periodizacoes`, comCorpo("POST", dados)),

  verPeriodizacao: (id: number) => pedir<Periodizacao>(`/periodizacoes/${id}`),

  editarPeriodizacao: (id: number, dados: Partial<PeriodizacaoBase>) =>
    pedir<Periodizacao>(`/periodizacoes/${id}`, comCorpo("PATCH", dados)),

  apagarPeriodizacao: (id: number) =>
    pedir<void>(`/periodizacoes/${id}`, { method: "DELETE" }),

  criarSessao: (periodizacaoId: number, dados: { nome: string; ordem?: number; dia_da_semana?: number | null }) =>
    pedir<SessaoModelo>(`/periodizacoes/${periodizacaoId}/sessoes`, comCorpo("POST", dados)),

  verSessao: (id: number) => pedir<SessaoModelo>(`/sessoes/${id}`),

  apagarSessao: (id: number) => pedir<void>(`/sessoes/${id}`, { method: "DELETE" }),

  criarPrescricao: (sessaoId: number, dados: NovaPrescricao) =>
    pedir<Prescricao>(`/sessoes/${sessaoId}/prescricoes`, comCorpo("POST", dados)),

  editarPrescricao: (id: number, dados: NovaPrescricao) =>
    pedir<Prescricao>(`/prescricoes/${id}`, comCorpo("PUT", dados)),

  apagarPrescricao: (id: number) =>
    pedir<void>(`/prescricoes/${id}`, { method: "DELETE" }),

  /** Reescreve a progressão inteira: substitui, não acrescenta. */
  definirSeries: (prescricaoId: number, series: NovaSerie[]) =>
    pedir<Prescricao>(`/prescricoes/${prescricaoId}/series`, comCorpo("PUT", { series })),

  /** Lê o texto escrito à mão sem gravar nada — a tela mostra antes de salvar. */
  lerTexto: (texto: string) =>
    pedir<Leitura>("/prescricoes/ler-texto", comCorpo("POST", { texto })),

  // --------------------------------------------------------- check-in

  listarCheckins: (alunoId: number, semanas = 52) =>
    pedir<Checkin[]>(`/alunos/${alunoId}/checkins?semanas=${semanas}`),

  registrarCheckin: (alunoId: number, dados: NovoCheckin) =>
    pedir<Checkin>(`/alunos/${alunoId}/checkins`, comCorpo("POST", dados)),

  editarCheckin: (id: number, dados: NovoCheckin) =>
    pedir<Checkin>(`/checkins/${id}`, comCorpo("PATCH", dados)),

  evolucao: (alunoId: number, semanas = 26) =>
    pedir<Evolucao>(`/alunos/${alunoId}/evolucao?semanas=${semanas}`),

  // --------------------------------------------------- treino executado

  /** Idempotente: chamar de novo devolve o treino já aberto, não cria outro. */
  abrirTreino: (alunoId: number, sessaoId: number, dia?: string) =>
    pedir<TreinoRealizado>(
      `/alunos/${alunoId}/treinos-realizados`,
      comCorpo("POST", dia === undefined ? { sessao_id: sessaoId } : { sessao_id: sessaoId, dia }),
    ),

  listarTreinosFeitos: (alunoId: number, semanas = 12) =>
    pedir<TreinoNaLista[]>(`/alunos/${alunoId}/treinos-realizados?semanas=${semanas}`),

  verTreinoFeito: (id: number) => pedir<TreinoRealizado>(`/treinos-realizados/${id}`),

  /** Manda a fila do aparelho. Só acrescenta e atualiza — nunca apaga. */
  sincronizarSeries: (treinoId: number, series: SerieParaEnviar[]) =>
    pedir<TreinoRealizado>(`/treinos-realizados/${treinoId}/series`, comCorpo("PUT", { series })),

  apagarSerieFeita: (treinoId: number, chaveLocal: string) =>
    pedir<void>(`/treinos-realizados/${treinoId}/series/${encodeURIComponent(chaveLocal)}`, {
      method: "DELETE",
    }),

  encerrarTreino: (treinoId: number, observacoes: string | null) =>
    pedir<TreinoRealizado>(
      `/treinos-realizados/${treinoId}/encerrar`,
      comCorpo("POST", { observacoes }),
    ),

  reabrirTreino: (treinoId: number) =>
    pedir<TreinoRealizado>(`/treinos-realizados/${treinoId}/reabrir`, { method: "POST" }),

  /** A evolução do 1RM estimado, a partir do que o aluno levantou. */
  forcaDoAluno: (alunoId: number, semanas = 26) =>
    pedir<ForcaDoExercicio[]>(`/alunos/${alunoId}/forca?semanas=${semanas}`),

  forcaNoExercicio: (alunoId: number, exercicioId: number, semanas = 26) =>
    pedir<ForcaDoExercicio>(
      `/alunos/${alunoId}/forca/${exercicioId}?semanas=${semanas}`,
    ),

  /** O ciclo fechando: a carga que sai do e1RM para as prescrições com %1RM. */
  cargasSugeridas: (sessaoId: number) =>
    pedir<CargaSugerida[]>(`/sessoes/${sessaoId}/cargas-sugeridas`),

  /** Os alunos do treinador, ordenados por quem precisa de atenção primeiro. */
  alertasDosAlunos: () => pedir<AlunoComAlertas[]>("/alunos/alertas"),

  // ------------------------------------------------------------- senha

  /** Derruba as sessões abertas em outros aparelhos; esta continua valendo. */
  trocarMinhaSenha: (senhaAtual: string, senhaNova: string) =>
    pedir<void>("/eu/senha", comCorpo("POST", { senha_atual: senhaAtual, senha_nova: senhaNova })),

  /** O caminho de recuperação: sem provedor de email, quem redefine é o João. */
  redefinirSenhaDoAluno: (alunoId: number, senha: string) =>
    pedir<void>(`/alunos/${alunoId}/senha`, comCorpo("POST", { senha })),

  // ------------------------------------------------------- privacidade

  /** Público: dá para ler antes de aceitar, e antes de ter conta. */
  termo: () => pedir<Termo>("/termo"),

  consentimento: () => pedir<EstadoDoConsentimento>("/eu/consentimento"),

  consentir: () =>
    pedir<EstadoDoConsentimento>("/eu/consentimento", { method: "POST" }),

  revogarConsentimento: () =>
    pedir<EstadoDoConsentimento>("/eu/consentimento", { method: "DELETE" }),

  meusDados: () => pedir<MeusDados>("/eu/dados"),

  apagarMinhaConta: (confirmacao: string) =>
    pedir<void>(`/eu?confirmacao=${encodeURIComponent(confirmacao)}`, {
      method: "DELETE",
    }),

  // -------------------------------------------------------------- dieta

  /** O protocolo em vigor. 404 quando o aluno ainda não tem nenhum. */
  protocoloDoAluno: (alunoId: number) => pedir<Protocolo>(`/alunos/${alunoId}/protocolo`),

  listarProtocolos: (alunoId: number) =>
    pedir<ProtocoloNaLista[]>(`/alunos/${alunoId}/protocolos`),

  verProtocolo: (id: number) => pedir<Protocolo>(`/protocolos/${id}`),

  criarProtocolo: (alunoId: number, dados: ProtocoloNovo) =>
    pedir<Protocolo>(`/alunos/${alunoId}/protocolos`, comCorpo("POST", dados)),

  /** Substitui o conteúdo inteiro: o que sai da tela sai do banco. */
  editarProtocolo: (id: number, dados: ProtocoloNovo) =>
    pedir<Protocolo>(`/protocolos/${id}`, comCorpo("PUT", dados)),

  apagarProtocolo: (id: number) => pedir<void>(`/protocolos/${id}`, { method: "DELETE" }),

  /** Lê o protocolo escrito à mão sem gravar — a tela mostra antes de salvar. */
  lerProtocolo: (texto: string) =>
    pedir<ProtocoloLido>("/protocolos/ler-texto", comCorpo("POST", { texto })),

  listarAderencia: (alunoId: number, dias = 30) =>
    pedir<Aderencia[]>(`/alunos/${alunoId}/aderencia?dias=${dias}`),

  marcarRefeicao: (refeicaoId: number, dados: { dia?: string; seguiu: boolean }) =>
    pedir<Aderencia>(`/refeicoes/${refeicaoId}/aderencia`, comCorpo("PUT", dados)),

  /** O catálogo nasce vazio: lista vazia aqui é resposta, não falha. */
  buscarAlimentos: (busca: string) =>
    pedir<Alimento[]>(`/alimentos?busca=${encodeURIComponent(busca)}`),

  // -------------------------------------------------------- calculadora

  calcular: (pedido: PedidoDeEstimativa) =>
    pedir<RespostaDaCalculadora>("/calculadora", comCorpo("POST", pedido)),
};
