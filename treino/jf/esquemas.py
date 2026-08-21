"""Os formatos que entram e saem da API.

Nenhum esquema de saída carrega `senha_hash`: os modelos do SQLAlchemy nunca
viram JSON direto, sempre passam por aqui.
"""

from __future__ import annotations

from datetime import date

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator

from jf.auth import TAMANHO_MINIMO_DA_SENHA
from jf.forca import Equacao
from jf.modelos import (
    ConvencaoDeCarga,
    EscopoDaTecnica,
    FaseDaPeriodizacao,
    Papel,
    Sexo,
    TipoDeSerie,
)

_do_orm = ConfigDict(from_attributes=True)


# ------------------------------------------------------------------- sessão


class Credenciais(BaseModel):
    email: EmailStr
    senha: str


class UsuarioEmResposta(BaseModel):
    model_config = _do_orm

    id: int
    nome: str
    email: EmailStr
    papel: Papel


class QuemSouEu(BaseModel):
    usuario: UsuarioEmResposta
    # Preenchido só quando o papel é aluno: é o id que o front usa nas URLs.
    aluno_id: int | None = None


# -------------------------------------------------------------------- aluno


class NovoAluno(BaseModel):
    nome: str = Field(min_length=2, max_length=120)
    email: EmailStr
    senha: str = Field(min_length=TAMANHO_MINIMO_DA_SENHA)
    nascimento: date | None = None
    sexo: Sexo | None = None
    altura_cm: float | None = Field(default=None, gt=50, lt=260)
    objetivo: str | None = Field(default=None, max_length=200)
    observacoes: str | None = None


class EdicaoDoAluno(BaseModel):
    nascimento: date | None = None
    sexo: Sexo | None = None
    altura_cm: float | None = Field(default=None, gt=50, lt=260)
    objetivo: str | None = Field(default=None, max_length=200)
    observacoes: str | None = None


class AlunoEmResposta(BaseModel):
    model_config = _do_orm

    id: int
    nome: str
    email: EmailStr
    nascimento: date | None
    sexo: Sexo | None
    altura_cm: float | None
    objetivo: str | None
    observacoes: str | None


# --------------------------------------------------------------- exercício


class ExercicioEmResposta(BaseModel):
    model_config = _do_orm

    id: int
    nome: str
    grupo_muscular: str
    equipamento: str
    composto: bool
    convencao_de_carga: ConvencaoDeCarga
    incremento_kg: float


# ------------------------------------------------------------------ técnica


class TecnicaEmResposta(BaseModel):
    model_config = _do_orm

    id: int
    nome: str
    escopo: EscopoDaTecnica
    descricao: str
    distorce_estimativa: bool


# --------------------------------------------------------------- prescrição


class PrescricaoBase(BaseModel):
    exercicio_id: int
    ordem: int = 0
    bloco: str | None = Field(default=None, max_length=4)
    agrupamento_id: int | None = None
    series: int = Field(default=3, ge=1, le=20)
    reps_min: int = Field(default=8, ge=1, le=100)
    reps_max: int = Field(default=12, ge=1, le=100)
    rir_alvo: int | None = Field(default=2, ge=0, le=10)
    descanso_s: int | None = Field(default=90, ge=0, le=900)
    carga_alvo_kg: float | None = Field(default=None, gt=0, le=1000)
    percentual_1rm: float | None = Field(default=None, gt=0, le=150)
    cadencia: str | None = Field(default=None, max_length=15)
    observacao: str | None = Field(default=None, max_length=300)
    tecnica_ids: list[int] = Field(default_factory=list)

    @model_validator(mode="after")
    def faixa_coerente(self) -> "PrescricaoBase":
        if self.reps_max < self.reps_min:
            raise ValueError("O máximo de repetições não pode ser menor que o mínimo.")
        return self


class NovaPrescricao(PrescricaoBase):
    pass


class PrescricaoEmResposta(BaseModel):
    model_config = _do_orm

    id: int
    ordem: int
    bloco: str | None
    series: int
    reps_min: int
    reps_max: int
    rir_alvo: int | None
    descanso_s: int | None
    carga_alvo_kg: float | None
    percentual_1rm: float | None
    cadencia: str | None
    observacao: str | None

    exercicio: ExercicioEmResposta
    agrupamento: TecnicaEmResposta | None
    tecnicas: list[TecnicaEmResposta]

    # As séries individuais, quando há progressão de carga entre elas.
    series_detalhadas: list["SerieEmResposta"]
    tem_progressao: bool

    # Repetições × carga somadas nas séries de trabalho. Mede trabalho, não força.
    tonelagem_prevista: float | None
    distorce_estimativa: bool


# ------------------------------------------------------------------- sessão


class SessaoModeloBase(BaseModel):
    nome: str = Field(min_length=1, max_length=120)
    ordem: int = 0
    dia_da_semana: int | None = Field(default=None, ge=0, le=6)
    observacoes: str | None = None


class NovaSessaoModelo(SessaoModeloBase):
    pass


class SessaoModeloEmResposta(SessaoModeloBase):
    model_config = _do_orm

    id: int
    prescricoes: list[PrescricaoEmResposta]
    tonelagem_prevista: float
    # Quantas prescrições ficaram de fora da tonelagem por não terem carga.
    # Sem isto o total engana: some sozinho conforme o João preenche.
    prescricoes_sem_carga: int


# ------------------------------------------------------------ periodização


class PeriodizacaoBase(BaseModel):
    nome: str = Field(min_length=1, max_length=120)
    objetivo: str | None = Field(default=None, max_length=200)
    fase: FaseDaPeriodizacao = FaseDaPeriodizacao.ACUMULACAO
    inicio: date | None = None
    semanas: int = Field(default=4, ge=1, le=52)
    equacao: Equacao = Equacao.PROPOSTA
    ativa: bool = True
    observacoes: str | None = None


class NovaPeriodizacao(PeriodizacaoBase):
    pass


class EdicaoDaPeriodizacao(BaseModel):
    nome: str | None = Field(default=None, min_length=1, max_length=120)
    objetivo: str | None = Field(default=None, max_length=200)
    fase: FaseDaPeriodizacao | None = None
    inicio: date | None = None
    semanas: int | None = Field(default=None, ge=1, le=52)
    equacao: Equacao | None = None
    ativa: bool | None = None
    observacoes: str | None = None


class PeriodizacaoEmResposta(PeriodizacaoBase):
    model_config = _do_orm

    id: int
    aluno_id: int
    sessoes: list[SessaoModeloEmResposta]
    tonelagem_prevista: float


class PeriodizacaoNaLista(PeriodizacaoBase):
    model_config = _do_orm

    id: int
    aluno_id: int


# ------------------------------------------------------------- calculadora


class PedidoDeEstimativa(BaseModel):
    """Uma série de referência: o que o aluno levantou, e por quantas reps."""

    carga_kg: float = Field(gt=0, le=1000)
    reps: int = Field(ge=1, le=30)
    rir: int | None = Field(default=None, ge=0, le=10)
    equacao: Equacao = Equacao.PROPOSTA
    exercicio_id: int | None = None
    # Quando alguma técnica da série muda o que "uma série" significa.
    tecnica_ids: list[int] = Field(default_factory=list)


class SugestaoDeCarga(BaseModel):
    reps: int
    carga_kg: float
    carga_arredondada_kg: float
    percentual: float


class RespostaDaCalculadora(BaseModel):
    um_rm: float
    equacao: Equacao
    nome_da_equacao: str
    confiavel: bool
    ressalva: str | None
    incremento_kg: float
    tabela: list[SugestaoDeCarga]
    # As outras equações no mesmo caso, para o João poder comparar.
    comparacao: dict[str, float]


# ------------------------------------------------------------------- séries


class SerieBase(BaseModel):
    ordem: int = 0
    reps: int | None = Field(default=None, ge=1, le=100)
    carga_kg: float | None = Field(default=None, ge=0, le=1000)
    carga_ate_kg: float | None = Field(default=None, ge=0, le=1000)
    tipo: TipoDeSerie = TipoDeSerie.VALIDA
    rir: int | None = Field(default=None, ge=0, le=10)
    observacao: str | None = Field(default=None, max_length=200)
    tecnica_ids: list[int] = Field(default_factory=list)

    @model_validator(mode="after")
    def rampa_coerente(self) -> "SerieBase":
        if self.carga_ate_kg is None:
            return self
        if self.carga_kg is None:
            raise ValueError("Uma rampa precisa da carga inicial.")
        if self.carga_ate_kg <= self.carga_kg:
            raise ValueError(
                "Na rampa a carga final precisa ser maior que a inicial; "
                "para carga fixa, deixe o segundo campo em branco."
            )
        return self


class NovaSerie(SerieBase):
    pass


class SerieEmResposta(BaseModel):
    model_config = _do_orm

    id: int
    ordem: int
    reps: int | None
    carga_kg: float | None
    carga_ate_kg: float | None
    tipo: TipoDeSerie
    rir: int | None
    observacao: str | None
    tecnicas: list[TecnicaEmResposta]

    em_rampa: bool
    tonelagem: float | None
    # Se esta série pode virar estimativa de 1RM — rampa, aquecimento e técnica
    # que quebra a contagem de repetições ficam de fora.
    serve_para_1rm: bool


class SeriesEmLote(BaseModel):
    """Substitui todas as séries de uma prescrição de uma vez.

    Substituição e não acréscimo: editar a progressão é reescrever a lista, e
    tentar casar item a item com o que já existe convidaria a duplicação.
    """

    series: list[NovaSerie] = Field(max_length=30)


# ------------------------------------------------------ leitura do texto


class TextoDaPrescricao(BaseModel):
    texto: str = Field(max_length=4000)


class LinhaLidaEmResposta(BaseModel):
    texto: str
    entendida: bool
    erro: str | None
    reps: int | None
    carga_kg: float | None
    carga_ate_kg: float | None
    tipo: TipoDeSerie
    observacao: str | None
    # Só as que existem no catálogo; as citadas e não encontradas vêm à parte.
    tecnica_ids: list[int]
    tecnicas: list[str]


class LeituraEmResposta(BaseModel):
    linhas: list[LinhaLidaEmResposta]
    entendidas: int
    nao_entendidas: int


PrescricaoEmResposta.model_rebuild()
