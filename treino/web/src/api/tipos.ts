/** Os formatos que a API devolve. Espelham `jf/esquemas.py`. */

export type Papel = "treinador" | "aluno";

export type Sexo = "masculino" | "feminino" | "outro";

export type ConvencaoDeCarga = "total" | "por_halter" | "peso_corporal";

export interface Usuario {
  id: number;
  nome: string;
  email: string;
  papel: Papel;
}

export interface QuemSouEu {
  usuario: Usuario;
  /** Só vem preenchido quando o papel é aluno. */
  aluno_id: number | null;
}

export interface Aluno {
  id: number;
  nome: string;
  email: string;
  nascimento: string | null;
  sexo: Sexo | null;
  altura_cm: number | null;
  objetivo: string | null;
  observacoes: string | null;
}

export interface NovoAluno {
  nome: string;
  email: string;
  senha: string;
  nascimento?: string | null;
  sexo?: Sexo | null;
  altura_cm?: number | null;
  objetivo?: string | null;
}

export interface Exercicio {
  id: number;
  nome: string;
  grupo_muscular: string;
  equipamento: string;
  composto: boolean;
  convencao_de_carga: ConvencaoDeCarga;
  incremento_kg: number;
}

// ------------------------------------------------------------------- treino

export type EscopoDaTecnica = "execucao" | "intra_serie" | "agrupamento";

export type FaseDaPeriodizacao =
  | "acumulacao"
  | "intensificacao"
  | "pico"
  | "deload"
  | "manutencao";

export type Equacao = "proposta" | "epley" | "brzycki";

export interface Tecnica {
  id: number;
  nome: string;
  escopo: EscopoDaTecnica;
  descricao: string;
  /** Se a técnica quebra a comparabilidade da contagem de repetições. */
  distorce_estimativa: boolean;
}

export interface Prescricao {
  id: number;
  ordem: number;
  bloco: string | null;
  series: number;
  reps_min: number;
  reps_max: number;
  rir_alvo: number | null;
  descanso_s: number | null;
  carga_alvo_kg: number | null;
  percentual_1rm: number | null;
  cadencia: string | null;
  observacao: string | null;
  exercicio: Exercicio;
  agrupamento: Tecnica | null;
  tecnicas: Tecnica[];
  /** Séries × reps × carga. Mede trabalho, não força. */
  tonelagem_prevista: number | null;
  distorce_estimativa: boolean;
}

export interface NovaPrescricao {
  exercicio_id: number;
  ordem?: number;
  bloco?: string | null;
  agrupamento_id?: number | null;
  series: number;
  reps_min: number;
  reps_max: number;
  rir_alvo?: number | null;
  descanso_s?: number | null;
  carga_alvo_kg?: number | null;
  percentual_1rm?: number | null;
  cadencia?: string | null;
  observacao?: string | null;
  tecnica_ids: number[];
}

export interface SessaoModelo {
  id: number;
  nome: string;
  ordem: number;
  dia_da_semana: number | null;
  observacoes: string | null;
  prescricoes: Prescricao[];
  tonelagem_prevista: number;
  prescricoes_sem_carga: number;
}

export interface PeriodizacaoBase {
  nome: string;
  objetivo: string | null;
  fase: FaseDaPeriodizacao;
  inicio: string | null;
  semanas: number;
  equacao: Equacao;
  ativa: boolean;
  observacoes: string | null;
}

export interface PeriodizacaoNaLista extends PeriodizacaoBase {
  id: number;
  aluno_id: number;
}

export interface Periodizacao extends PeriodizacaoNaLista {
  sessoes: SessaoModelo[];
  tonelagem_prevista: number;
}

// -------------------------------------------------------------- calculadora

export interface PedidoDeEstimativa {
  carga_kg: number;
  reps: number;
  rir?: number | null;
  equacao?: Equacao;
  exercicio_id?: number | null;
  tecnica_ids?: number[];
}

export interface SugestaoDeCarga {
  reps: number;
  carga_kg: number;
  carga_arredondada_kg: number;
  percentual: number;
}

export interface RespostaDaCalculadora {
  um_rm: number;
  equacao: Equacao;
  nome_da_equacao: string;
  confiavel: boolean;
  ressalva: string | null;
  incremento_kg: number;
  tabela: SugestaoDeCarga[];
  comparacao: Record<string, number>;
}
