/** Os formatos que a API devolve. Espelham `jf/esquemas.py`. */

export type Papel = "treinador" | "aluno";

export type Sexo = "masculino" | "feminino" | "outro";

export type ConvencaoDeCarga = "total" | "por_halter" | "peso_corporal";

export interface Usuario {
  id: number;
  nome: string;
  email: string;
  papel: Papel;
  /** A senha foi definida por outra pessoa — o treinador cadastrou ou
   *  redefiniu. Enquanto for `true`, ele consegue entrar como este usuário. */
  senha_provisoria: boolean;
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
  /** As séries individuais, quando há progressão de carga entre elas. */
  series_detalhadas: Serie[];
  tem_progressao: boolean;
  /** Reps × carga somadas nas séries de trabalho. Mede trabalho, não força. */
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

// -------------------------------------------------------- séries da prescrição

export type TipoDeSerie = "aquecimento" | "up_set" | "valida" | "back_off";

export interface Serie {
  id: number;
  ordem: number;
  /** Nulo no up set puro, que sobe a carga sem contagem fixa de repetições. */
  reps: number | null;
  carga_kg: number | null;
  /** Quando preenchida, a série é uma rampa: "12x50 a 92kg". */
  carga_ate_kg: number | null;
  tipo: TipoDeSerie;
  rir: number | null;
  observacao: string | null;
  tecnicas: Tecnica[];
  em_rampa: boolean;
  tonelagem: number | null;
  serve_para_1rm: boolean;
}

export interface NovaSerie {
  ordem?: number;
  reps?: number | null;
  carga_kg?: number | null;
  carga_ate_kg?: number | null;
  tipo?: TipoDeSerie;
  rir?: number | null;
  observacao?: string | null;
  tecnica_ids?: number[];
}

export interface LinhaLida {
  texto: string;
  entendida: boolean;
  erro: string | null;
  reps: number | null;
  carga_kg: number | null;
  carga_ate_kg: number | null;
  tipo: TipoDeSerie;
  observacao: string | null;
  tecnica_ids: number[];
  tecnicas: string[];
}

export interface Leitura {
  linhas: LinhaLida[];
  entendidas: number;
  nao_entendidas: number;
}

// ------------------------------------------------------------------ check-in

export interface Medidas {
  cintura_cm: number | null;
  quadril_cm: number | null;
  torax_cm: number | null;
  braco_cm: number | null;
  coxa_cm: number | null;
  panturrilha_cm: number | null;
}

export interface Checkin {
  id: number;
  aluno_id: number;
  /** A segunda-feira da semana, sempre — o servidor normaliza. */
  semana: string;
  peso_kg: number | null;
  horas_de_sono: number | null;
  passos_por_dia: number | null;
  /** 1 a 5, com 5 sempre sendo o melhor. */
  qualidade_do_sono: number | null;
  disposicao: number | null;
  recuperacao: number | null;
  aderencia_dieta: number | null;
  aderencia_treino: number | null;
  observacoes: string | null;
  medidas: Medidas | null;
}

export type NovoCheckin = Partial<Omit<Checkin, "id" | "aluno_id" | "medidas">> & {
  medidas?: Partial<Medidas> | null;
};

export interface PontoDaSerie {
  semana: string;
  valor: number;
}

export interface SerieDoGrafico {
  chave: string;
  rotulo: string;
  unidade: string;
  pontos: PontoDaSerie[];
  tendencia: PontoDaSerie[];
}

export interface Evolucao {
  aluno_id: number;
  semanas: number;
  series: SerieDoGrafico[];
  variacao: Record<string, number>;
}

// ---------------------------------------------------------------- privacidade

export interface Termo {
  /** Hash do próprio texto: editar o termo muda a versão sozinho. */
  versao: string;
  texto: string;
}

export interface EstadoDoConsentimento {
  versao_atual: string;
  consentido: boolean;
  aceito_em: string | null;
  /** Aceitou uma versão anterior e o texto mudou — diferente de nunca aceitar. */
  precisa_reaceitar: boolean;
}

export interface MeusDados {
  exportado_em: string;
  conta: Record<string, unknown>;
  consentimentos: Record<string, unknown>[];
  aluno: Record<string, unknown> | null;
}

// --------------------------------------------------------------------- dieta

export interface ItemDeSubstituicao {
  id: number;
  descricao: string;
  quantidade: number | null;
  unidade: string | null;
  /** "Cuscuz 225 g", montado no servidor — a mesma regra em toda tela. */
  porcao: string;
}

export interface GrupoDeSubstituicao {
  id: number;
  nome: string;
  ordem: number;
  observacao: string | null;
  itens: ItemDeSubstituicao[];
}

export interface ItemDaRefeicao {
  id: number;
  descricao: string | null;
  quantidade: number | null;
  unidade: string | null;
  a_gosto: boolean;
  opcional: boolean;
  observacao: string | null;
  /** Onde estão as substituições deste alimento; a lista já veio no protocolo. */
  grupo_id: number | null;
}

export interface Refeicao {
  id: number;
  nome: string;
  ordem: number;
  horario: string | null;
  observacoes: string | null;
  itens: ItemDaRefeicao[];
}

export interface Suplemento {
  id: number;
  ordem: number;
  nome: string;
  dose: string | null;
  momento: string | null;
  observacao: string | null;
}

export interface Protocolo {
  id: number;
  aluno_id: number;
  nome: string;
  kcal_alvo: number | null;
  deficit_kcal: number | null;
  proteina_g: number | null;
  carboidrato_g: number | null;
  gordura_g: number | null;
  observacoes: string | null;
  ativo: boolean;
  criado_em: string;
  grupos: GrupoDeSubstituicao[];
  refeicoes: Refeicao[];
  suplementos: Suplemento[];
}

export interface ProtocoloNaLista {
  id: number;
  nome: string;
  ativo: boolean;
  criado_em: string;
  kcal_alvo: number | null;
  deficit_kcal: number | null;
}

/** O que vai para o servidor. Sem ids: o protocolo é gravado inteiro, e os
 *  itens não têm identidade própria — o João reescreve a lista, não a linha 3. */
export interface ItemDeSubstituicaoNovo {
  descricao: string;
  quantidade: number | null;
  unidade: string | null;
}

export interface GrupoNovo {
  nome: string;
  observacao?: string | null;
  itens: ItemDeSubstituicaoNovo[];
}

export interface ItemDaRefeicaoNovo {
  descricao: string | null;
  /** Pelo nome: quem grava tudo de uma vez ainda não tem os ids dos grupos. */
  grupo?: string | null;
  quantidade: number | null;
  unidade: string | null;
  a_gosto: boolean;
  opcional: boolean;
  observacao?: string | null;
}

export interface RefeicaoNova {
  nome: string;
  horario?: string | null;
  observacoes?: string | null;
  itens: ItemDaRefeicaoNovo[];
}

export interface SuplementoNovo {
  nome: string;
  dose: string | null;
  momento: string | null;
  observacao?: string | null;
}

export interface ProtocoloNovo {
  nome: string;
  kcal_alvo: number | null;
  deficit_kcal: number | null;
  proteina_g: number | null;
  carboidrato_g: number | null;
  gordura_g: number | null;
  observacoes: string | null;
  ativo: boolean;
  grupos: GrupoNovo[];
  refeicoes: RefeicaoNova[];
  suplementos: SuplementoNovo[];
}

export interface ProtocoloLido {
  protocolo: ProtocoloNovo;
  /** O que o leitor não entendeu, para conferir antes de salvar. */
  nao_entendidas: string[];
}

export interface Aderencia {
  id: number;
  refeicao_id: number;
  dia: string;
  seguiu: boolean;
  observacao: string | null;
}

export interface Alimento {
  id: number;
  nome: string;
  marca: string | null;
  fonte: string;
  /** Por 100 g. `null` é "não medido", que não é zero. */
  kcal_100g: number | null;
  proteina_100g: number | null;
  carboidrato_100g: number | null;
  gordura_100g: number | null;
  fibra_100g: number | null;
}
