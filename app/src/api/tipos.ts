/** Espelho dos modelos Pydantic de `curso/api.py`.
 *
 *  Mantenha os dois lados em sincronia: quando um modelo mudar lá, mude aqui —
 *  é o único lugar do front que sabe o formato do backend.
 */

export type Estado = "novo" | "em_andamento" | "resolvido";
export type Linguagem = "python" | "sql";

export interface Resumo {
  id: string;
  titulo: string;
  nivel: number;
  tempo_min: number;
  tags: string[];
  bloco: string;
  nome_do_bloco: string;
  modulo: string;
  nome_do_modulo: string;
  linguagem: Linguagem;
  estado: Estado;
  tentativas: number;
  proxima_revisao: string;
  dias_ate_revisao: number | null;
  vencida: boolean;
}

export interface Detalhe extends Resumo {
  enunciado: string;
  teoria: string;
  codigo: string;
  requer: string[];
  dicas_liberadas: string[];
  total_de_dicas: number;
  ja_tentou: boolean;
}

export interface Ficha {
  estado: Estado;
  tentativas: number;
  tentativas_ate_acertar: number;
  revisoes: number;
  intervalo_dias: number;
  proxima_revisao: string;
}

/** Uma tabela serializada, possivelmente truncada — `total` é o tamanho real. */
export interface Tabela {
  colunas: string[];
  linhas: (string | number | boolean | null)[][];
  total: number;
}

export interface CelulaDivergente {
  linha: number;
  coluna: string;
  esperado: string | number | boolean | null;
  obtido: string | number | boolean | null;
}

/** A falha em forma estruturada. `tipo` diz qual das formas abaixo veio preenchida. */
export interface DadosDaFalha {
  tipo:
    | "sem_retorno"
    | "valor_escalar"
    | "tamanho_da_lista"
    | "item_da_lista"
    | "conjunto"
    | "chaves_do_dicionario"
    | "valor_do_dicionario"
    | "tipo_errado"
    | "esperava_dataframe"
    | "esperava_series"
    | "colunas_diferentes"
    | "ordem_das_colunas"
    | "numero_de_linhas"
    | "indice_diferente"
    | "valores_diferentes"
    | "tipo_da_coluna"
    | "tempo_esgotado"
    | "solucao_lenta";
  esperado?: Tabela | unknown;
  obtido?: Tabela | unknown;
  celulas?: CelulaDivergente[];
  faltando?: unknown[];
  sobrando?: unknown[];
  coluna?: string;
  chave?: unknown;
  posicao?: number;
  tipo_esperado?: string;
  tipo_obtido?: string;
  indice_esperado?: unknown[];
  indice_obtido?: unknown[];
  comparado_sem_ordem?: boolean;
  limite_s?: number;
  segundos?: number;
  limite?: number;
}

export interface ResultadoDaCorrecao {
  ok: boolean;
  passaram: number;
  falharam: number;
  mensagem: string;
  nome_da_falha: string;
  dados: DadosDaFalha | null;
  ficha: Ficha;
}

export interface Dica {
  numero: number;
  total: number;
  texto: string;
}

export interface Solucao {
  codigo: string;
  linguagem: Linguagem;
}

export interface ModuloNoPainel {
  bloco: string;
  nome_do_bloco: string;
  modulo: string;
  nome_do_modulo: string;
  total: number;
  feitos: number;
}

export interface DiaDaPrevisao {
  data: string;
  quantidade: number;
}

export interface PainelDeProgresso {
  total: number;
  feitos: number;
  sequencia: number;
  vencidas: number;
  agendados: number;
  modulos: ModuloNoPainel[];
  previsao: DiaDaPrevisao[];
  dias_praticados: string[];
}

export interface PlanoDoDia {
  novos: Resumo[];
  revisoes: Resumo[];
  sequencia: number;
}

/** Uma tabela de verdade, e não outra forma qualquer de `esperado`/`obtido`. */
export function ehTabela(valor: unknown): valor is Tabela {
  return (
    typeof valor === "object" &&
    valor !== null &&
    Array.isArray((valor as Tabela).colunas) &&
    Array.isArray((valor as Tabela).linhas)
  );
}
