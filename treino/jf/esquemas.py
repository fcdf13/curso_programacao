"""Os formatos que entram e saem da API.

Nenhum esquema de saída carrega `senha_hash`: os modelos do SQLAlchemy nunca
viram JSON direto, sempre passam por aqui.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta

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


class TrocaDeSenha(BaseModel):
    """A senha atual é pedida mesmo com a sessão aberta.

    Quem senta no celular destravado de outra pessoa não deve conseguir mudar a
    senha dela — sem isso, uma sessão emprestada vira uma conta tomada.
    """

    senha_atual: str
    senha_nova: str = Field(min_length=TAMANHO_MINIMO_DA_SENHA, max_length=200)


class SenhaDefinidaPeloTreinador(BaseModel):
    senha: str = Field(min_length=TAMANHO_MINIMO_DA_SENHA, max_length=200)


class UsuarioEmResposta(BaseModel):
    model_config = _do_orm

    id: int
    nome: str
    email: EmailStr
    papel: Papel
    # Enquanto for `True`, outra pessoa sabe esta senha — foi ela quem a
    # definiu. A tela usa isto para pedir a troca.
    senha_provisoria: bool


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
    observacoes: str | None = Field(default=None, max_length=2000)


class EdicaoDoAluno(BaseModel):
    nascimento: date | None = None
    sexo: Sexo | None = None
    altura_cm: float | None = Field(default=None, gt=50, lt=260)
    objetivo: str | None = Field(default=None, max_length=200)
    observacoes: str | None = Field(default=None, max_length=2000)


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
    observacoes: str | None = Field(default=None, max_length=2000)


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
    observacoes: str | None = Field(default=None, max_length=2000)


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
    observacoes: str | None = Field(default=None, max_length=2000)


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


# ------------------------------------------------------------------ check-in


def _segunda(dia: date) -> date:
    """A segunda-feira da semana de `dia`.

    Toda semana é identificada pela segunda: assim o aluno que preenche no
    domingo e o que preenche na terça caem na mesma linha do gráfico.
    """
    return dia - timedelta(days=dia.weekday())


class MedidasBase(BaseModel):
    cintura_cm: float | None = Field(default=None, gt=20, lt=250)
    quadril_cm: float | None = Field(default=None, gt=20, lt=250)
    torax_cm: float | None = Field(default=None, gt=20, lt=250)
    braco_cm: float | None = Field(default=None, gt=10, lt=100)
    coxa_cm: float | None = Field(default=None, gt=10, lt=150)
    panturrilha_cm: float | None = Field(default=None, gt=10, lt=100)


class MedidasEmResposta(MedidasBase):
    model_config = _do_orm


class CheckinBase(BaseModel):
    semana: date | None = None

    peso_kg: float | None = Field(default=None, gt=20, lt=400)
    horas_de_sono: float | None = Field(default=None, ge=0, le=16)
    passos_por_dia: int | None = Field(default=None, ge=0, le=100_000)

    # 1 a 5, sempre com 5 = melhor.
    qualidade_do_sono: int | None = Field(default=None, ge=1, le=5)
    disposicao: int | None = Field(default=None, ge=1, le=5)
    recuperacao: int | None = Field(default=None, ge=1, le=5)

    aderencia_dieta: int | None = Field(default=None, ge=0, le=100)
    aderencia_treino: int | None = Field(default=None, ge=0, le=100)

    # Texto livre precisa de teto: `Text` no banco aceita megabytes, e um
    # campo sem limite é armazenamento ilimitado a pedido de quem manda o POST.
    observacoes: str | None = Field(default=None, max_length=2000)
    medidas: MedidasBase | None = None

    @model_validator(mode="after")
    def normalizar_semana(self) -> "CheckinBase":
        # Sem `object.__setattr__` porque o modelo não é frozen; a semana
        # sempre vira a segunda-feira correspondente, mesmo se vier outro dia.
        self.semana = _segunda(self.semana or date.today())
        return self


class NovoCheckin(CheckinBase):
    pass


class CheckinEmResposta(BaseModel):
    model_config = _do_orm

    id: int
    aluno_id: int
    semana: date
    peso_kg: float | None
    horas_de_sono: float | None
    passos_por_dia: int | None
    qualidade_do_sono: int | None
    disposicao: int | None
    recuperacao: int | None
    aderencia_dieta: int | None
    aderencia_treino: int | None
    observacoes: str | None
    medidas: MedidasEmResposta | None


# ------------------------------------------------------------------ evolução


class PontoDaSerie(BaseModel):
    semana: date
    valor: float


class SerieDoGrafico(BaseModel):
    chave: str
    rotulo: str
    unidade: str
    pontos: list[PontoDaSerie]
    # Média móvel de 4 semanas do peso: a tendência é o dado, o ponto é ruído.
    tendencia: list[PontoDaSerie] = Field(default_factory=list)


class Evolucao(BaseModel):
    aluno_id: int
    semanas: int
    series: list[SerieDoGrafico]
    # O que mudou entre o primeiro e o último check-in, por série.
    variacao: dict[str, float]


# --------------------------------------------------------------- privacidade


class TermoEmResposta(BaseModel):
    versao: str
    texto: str


class EstadoDoConsentimento(BaseModel):
    versao_atual: str
    consentido: bool
    aceito_em: datetime | None = None
    # `True` quando a pessoa aceitou uma versão anterior e o texto mudou — é
    # uma conversa diferente de "nunca aceitou".
    precisa_reaceitar: bool = False


class MeusDados(BaseModel):
    exportado_em: datetime
    conta: dict
    consentimentos: list[dict]
    # Só quem é aluno tem histórico de treino e check-in.
    aluno: dict | None = None


# ---------------------------------------------------------------- dieta


class ItemDeSubstituicaoBase(BaseModel):
    descricao: str = Field(max_length=120)
    quantidade: float | None = Field(default=None, gt=0, le=10000)
    unidade: str | None = Field(default=None, max_length=20)


class ItemDeSubstituicaoEmResposta(ItemDeSubstituicaoBase):
    model_config = _do_orm

    id: int
    # "Cuscuz 225 g", já montado — a mesma regra em toda tela que mostrar isto.
    porcao: str


class GrupoBase(BaseModel):
    nome: str = Field(max_length=80)
    observacao: str | None = Field(default=None, max_length=200)
    itens: list[ItemDeSubstituicaoBase] = Field(default_factory=list)


class GrupoEmResposta(BaseModel):
    model_config = _do_orm

    id: int
    nome: str
    ordem: int
    observacao: str | None
    itens: list[ItemDeSubstituicaoEmResposta]


class ItemDaRefeicaoBase(BaseModel):
    descricao: str | None = Field(default=None, max_length=120)
    # Pelo **nome** do grupo, não por id: quem monta o protocolo inteiro numa
    # tacada só ainda não tem os ids dos grupos que está criando junto.
    grupo: str | None = Field(default=None, max_length=80)
    quantidade: float | None = Field(default=None, gt=0, le=10000)
    unidade: str | None = Field(default=None, max_length=20)
    a_gosto: bool = False
    opcional: bool = False
    observacao: str | None = Field(default=None, max_length=200)

    @model_validator(mode="after")
    def tem_o_que_mostrar(self) -> "ItemDaRefeicaoBase":
        if not (self.descricao or "").strip() and not (self.grupo or "").strip():
            raise ValueError("O item precisa de uma descrição ou de um grupo.")
        return self


class ItemDaRefeicaoEmResposta(BaseModel):
    model_config = _do_orm

    id: int
    descricao: str | None
    quantidade: float | None
    unidade: str | None
    a_gosto: bool
    opcional: bool
    observacao: str | None
    # O grupo vem só como id: a lista completa de substituições já veio no
    # protocolo, e repeti-la em cada item multiplicaria o mesmo dado por dez.
    grupo_id: int | None


class RefeicaoBase(BaseModel):
    nome: str = Field(max_length=80)
    horario: str | None = Field(default=None, max_length=20)
    observacoes: str | None = Field(default=None, max_length=2000)
    itens: list[ItemDaRefeicaoBase] = Field(default_factory=list)


class RefeicaoEmResposta(BaseModel):
    model_config = _do_orm

    id: int
    nome: str
    ordem: int
    horario: str | None
    observacoes: str | None
    itens: list[ItemDaRefeicaoEmResposta]


class SuplementoBase(BaseModel):
    nome: str = Field(max_length=80)
    dose: str | None = Field(default=None, max_length=80)
    momento: str | None = Field(default=None, max_length=80)
    observacao: str | None = Field(default=None, max_length=200)


class SuplementoEmResposta(SuplementoBase):
    model_config = _do_orm

    id: int
    ordem: int


class ProtocoloBase(BaseModel):
    nome: str = Field(default="Protocolo alimentar", max_length=120)
    kcal_alvo: int | None = Field(default=None, ge=0, le=20000)
    deficit_kcal: int | None = Field(default=None, ge=0, le=5000)
    proteina_g: int | None = Field(default=None, ge=0, le=2000)
    carboidrato_g: int | None = Field(default=None, ge=0, le=2000)
    gordura_g: int | None = Field(default=None, ge=0, le=2000)
    observacoes: str | None = Field(default=None, max_length=4000)
    ativo: bool = True

    grupos: list[GrupoBase] = Field(default_factory=list)
    refeicoes: list[RefeicaoBase] = Field(default_factory=list)
    suplementos: list[SuplementoBase] = Field(default_factory=list)


class NovoProtocolo(ProtocoloBase):
    pass


class ProtocoloEmResposta(BaseModel):
    model_config = _do_orm

    id: int
    aluno_id: int
    nome: str
    kcal_alvo: int | None
    deficit_kcal: int | None
    proteina_g: int | None
    carboidrato_g: int | None
    gordura_g: int | None
    observacoes: str | None
    ativo: bool
    criado_em: datetime

    grupos: list[GrupoEmResposta]
    refeicoes: list[RefeicaoEmResposta]
    suplementos: list[SuplementoEmResposta]


class ProtocoloNaLista(BaseModel):
    model_config = _do_orm

    id: int
    nome: str
    ativo: bool
    criado_em: datetime
    kcal_alvo: int | None
    deficit_kcal: int | None


class AlimentoEmResposta(BaseModel):
    model_config = _do_orm

    id: int
    nome: str
    marca: str | None
    fonte: str
    # Sempre por 100 g, e `None` quando a tabela não mediu — não zero: zero é
    # uma afirmação, "não medido" não é.
    kcal_100g: float | None
    proteina_100g: float | None
    carboidrato_100g: float | None
    gordura_100g: float | None
    fibra_100g: float | None


# ------------------------------------------------- leitura do protocolo


class TextoDoProtocolo(BaseModel):
    texto: str = Field(max_length=20000)
    nome: str = Field(default="Protocolo alimentar", max_length=120)


class ProtocoloLidoEmResposta(BaseModel):
    """O rascunho pronto para editar, e o que ficou de fora.

    `nao_entendidas` não é detalhe de erro: é o que a tela mostra ao João para
    ele conferir. Uma linha perdida em silêncio é pior que uma linha recusada.
    """

    protocolo: ProtocoloBase
    nao_entendidas: list[str]


# ------------------------------------------------------------- aderência


class MarcacaoDaRefeicao(BaseModel):
    dia: date = Field(default_factory=date.today)
    seguiu: bool = True
    observacao: str | None = Field(default=None, max_length=200)


class AderenciaEmResposta(BaseModel):
    model_config = _do_orm

    id: int
    refeicao_id: int
    dia: date
    seguiu: bool
    observacao: str | None


# -------------------------------------------------------- treino executado


class AberturaDeTreino(BaseModel):
    sessao_id: int
    dia: date = Field(default_factory=date.today)


class SerieExecutada(BaseModel):
    """Uma série como o celular a manda.

    `chave_local` é gerada no aparelho e é o que torna o envio repetível: sem
    ela, reenviar a fila depois de uma conexão instável duplicaria as séries, e
    o volume da semana passaria a mentir.
    """

    chave_local: str = Field(min_length=8, max_length=64)
    ordem: int = 0
    exercicio_id: int
    prescricao_id: int | None = None
    serie_id: int | None = None
    reps: int | None = Field(default=None, ge=1, le=200)
    carga_kg: float | None = Field(default=None, ge=0, le=1000)
    rir: int | None = Field(default=None, ge=0, le=10)
    tipo: TipoDeSerie = TipoDeSerie.VALIDA
    observacao: str | None = Field(default=None, max_length=200)


class SeriesExecutadas(BaseModel):
    """O que o aparelho tem para esta sessão.

    Só acrescenta e atualiza; **nunca apaga** o que não veio na lista. Um
    celular com visão parcial — ficou offline no meio do treino — apagaria
    séries registradas de outro lugar se a ausência valesse como remoção.
    """

    series: list[SerieExecutada] = Field(default_factory=list, max_length=200)


class SerieExecutadaEmResposta(BaseModel):
    model_config = _do_orm

    id: int
    chave_local: str
    ordem: int
    exercicio_id: int
    prescricao_id: int | None
    serie_id: int | None
    reps: int | None
    carga_kg: float | None
    rir: int | None
    tipo: TipoDeSerie
    observacao: str | None
    tonelagem: float | None
    # A técnica vem da prescrição, não da mão do aluno no meio do treino.
    distorce_estimativa: bool


class TreinoRealizadoEmResposta(BaseModel):
    model_config = _do_orm

    id: int
    aluno_id: int
    sessao_id: int | None
    nome: str
    dia: date
    iniciada_em: datetime
    encerrada_em: datetime | None
    encerrada: bool
    observacoes: str | None
    tonelagem: float
    series: list[SerieExecutadaEmResposta]


class TreinoNaLista(BaseModel):
    model_config = _do_orm

    id: int
    sessao_id: int | None
    nome: str
    dia: date
    encerrada: bool
    tonelagem: float


class EncerramentoDoTreino(BaseModel):
    observacoes: str | None = Field(default=None, max_length=2000)
