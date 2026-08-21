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
