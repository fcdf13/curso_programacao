"""As tabelas do app.

Fase 0 traz só o que sustenta o login e o vínculo treinador–aluno: `Usuario`,
`Aluno` e o catálogo de `Exercicio`. Check-in, treino e dieta entram nas fases
seguintes, cada um com suas tabelas.
"""

from __future__ import annotations

import enum
from datetime import date, datetime, timezone

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


def agora() -> datetime:
    """Instante atual em UTC, sempre com fuso.

    `datetime.utcnow()` devolve um datetime ingênuo, que compara errado com
    qualquer datetime com fuso. Todo carimbo de tempo do app passa por aqui.
    """
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    pass


class Papel(str, enum.Enum):
    TREINADOR = "treinador"
    ALUNO = "aluno"


class Sexo(str, enum.Enum):
    MASCULINO = "masculino"
    FEMININO = "feminino"
    OUTRO = "outro"


class ConvencaoDeCarga(str, enum.Enum):
    """Como a carga de um exercício é registrada.

    Não é preciosismo: a estimativa de 1RM da fase 3 recebe a carga como número
    puro, então registrar 25 quando são dois halteres de 25 kg — que é a
    convenção do paper e da maioria dos apps — precisa estar combinado de
    antemão, ou a conta erra sem dar nenhum sinal.
    """

    TOTAL = "total"                  # barra com anilhas (incluindo a barra), máquina, polia
    POR_HALTER = "por_halter"        # o peso de UM halter, mesmo em exercício bilateral
    PESO_CORPORAL = "peso_corporal"  # barra fixa, paralelas: a carga é só o que se adiciona


class Usuario(Base):
    """Quem faz login. O papel decide o que a pessoa enxerga."""

    __tablename__ = "usuario"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(120))
    # Guardado sempre em minúsculas — ver `jf.auth.normalizar_email`.
    email: Mapped[str] = mapped_column(String(254), unique=True, index=True)
    senha_hash: Mapped[str] = mapped_column(String(255))
    papel: Mapped[Papel] = mapped_column(Enum(Papel, native_enum=False))
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=agora)

    perfil: Mapped["Aluno | None"] = relationship(
        back_populates="usuario",
        foreign_keys="Aluno.usuario_id",
        uselist=False,
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Usuario {self.id} {self.email} {self.papel.value}>"


class Aluno(Base):
    """O perfil de quem treina, e o vínculo com o treinador responsável."""

    __tablename__ = "aluno"

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuario.id", ondelete="CASCADE"), unique=True, index=True
    )
    treinador_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"), index=True)

    nascimento: Mapped[date | None] = mapped_column(Date, default=None)
    sexo: Mapped[Sexo | None] = mapped_column(Enum(Sexo, native_enum=False), default=None)
    altura_cm: Mapped[float | None] = mapped_column(Float, default=None)
    objetivo: Mapped[str | None] = mapped_column(String(200), default=None)
    observacoes: Mapped[str | None] = mapped_column(Text, default=None)
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=agora)

    usuario: Mapped[Usuario] = relationship(
        back_populates="perfil", foreign_keys=[usuario_id]
    )
    treinador: Mapped[Usuario] = relationship(foreign_keys=[treinador_id])

    def __repr__(self) -> str:
        return f"<Aluno {self.id} usuario={self.usuario_id}>"


class Exercicio(Base):
    """Catálogo compartilhado. O João pode acrescentar, mas não parte do zero."""

    __tablename__ = "exercicio"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    grupo_muscular: Mapped[str] = mapped_column(String(40), index=True)
    equipamento: Mapped[str] = mapped_column(String(40))
    composto: Mapped[bool] = mapped_column(Boolean, default=False)
    convencao_de_carga: Mapped[ConvencaoDeCarga] = mapped_column(
        Enum(ConvencaoDeCarga, native_enum=False), default=ConvencaoDeCarga.TOTAL
    )
    # Menor salto de carga possível naquele equipamento: 2,5 kg numa barra
    # (anilha de 1,25 de cada lado), 2 kg num rack de halteres, 5 kg numa
    # máquina de pino. É o que a fase 3 usa para arredondar a carga sugerida.
    incremento_kg: Mapped[float] = mapped_column(Float, default=2.5)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)

    def __repr__(self) -> str:
        return f"<Exercicio {self.id} {self.nome}>"


# ============================================================ treino prescrito


class EscopoDaTecnica(str, enum.Enum):
    """Onde a técnica age. Não é taxonomia decorativa: os três escopos entram
    na prescrição em lugares diferentes e afetam o cálculo de forma diferente.
    """

    # Como cada repetição é feita: dead stop, cadência lenta, isometria.
    # Não muda o que "uma série de 8" significa.
    EXECUCAO = "execucao"

    # Muda o que uma série é: cluster, rest-pause, drop-set. Uma série de
    # "9 reps" em cluster 3×3 não é comparável a 9 reps corridas.
    INTRA_SERIE = "intra_serie"

    # Liga exercícios diferentes: bi-set, tri-set, super-série, circuito.
    # Vive no bloco, não no exercício isolado.
    AGRUPAMENTO = "agrupamento"


class FaseDaPeriodizacao(str, enum.Enum):
    ACUMULACAO = "acumulacao"
    INTENSIFICACAO = "intensificacao"
    PICO = "pico"
    DELOAD = "deload"
    MANUTENCAO = "manutencao"


class Tecnica(Base):
    """Catálogo de técnicas. O João acrescenta as dele."""

    __tablename__ = "tecnica"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(60), unique=True, index=True)
    escopo: Mapped[EscopoDaTecnica] = mapped_column(
        Enum(EscopoDaTecnica, native_enum=False), index=True
    )
    descricao: Mapped[str] = mapped_column(String(300))

    # Se a técnica quebra a comparabilidade da contagem de repetições, a série
    # não serve para estimar 1RM. Um cluster 3×3 lido como "9 reps corridas"
    # subestimaria a força de forma grosseira — e em silêncio.
    distorce_estimativa: Mapped[bool] = mapped_column(Boolean, default=False)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)

    def __repr__(self) -> str:
        return f"<Tecnica {self.nome} ({self.escopo.value})>"


prescricao_tecnica = Table(
    "prescricao_tecnica",
    Base.metadata,
    Column(
        "prescricao_id",
        ForeignKey("prescricao.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column("tecnica_id", ForeignKey("tecnica.id"), primary_key=True),
)


class Periodizacao(Base):
    """Um mesociclo do aluno. É aqui que o João controla a calculadora."""

    __tablename__ = "periodizacao"

    id: Mapped[int] = mapped_column(primary_key=True)
    aluno_id: Mapped[int] = mapped_column(
        ForeignKey("aluno.id", ondelete="CASCADE"), index=True
    )
    nome: Mapped[str] = mapped_column(String(120))
    objetivo: Mapped[str | None] = mapped_column(String(200), default=None)
    fase: Mapped[FaseDaPeriodizacao] = mapped_column(
        Enum(FaseDaPeriodizacao, native_enum=False),
        default=FaseDaPeriodizacao.ACUMULACAO,
    )
    inicio: Mapped[date | None] = mapped_column(Date, default=None)
    semanas: Mapped[int] = mapped_column(Integer, default=4)

    # Qual equação a calculadora usa neste bloco. O João escolhe, e pode
    # comparar: é o argumento de por que a proposta é melhor que a tabela dele.
    equacao: Mapped[str] = mapped_column(String(20), default="proposta")

    ativa: Mapped[bool] = mapped_column(Boolean, default=True)
    observacoes: Mapped[str | None] = mapped_column(Text, default=None)
    criada_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=agora)

    aluno: Mapped[Aluno] = relationship()
    sessoes: Mapped[list["SessaoModelo"]] = relationship(
        back_populates="periodizacao",
        cascade="all, delete-orphan",
        order_by="SessaoModelo.ordem",
    )

    @property
    def tonelagem_prevista(self) -> float:
        """Volume de uma passagem por todos os treinos do bloco."""
        return sum(sessao.tonelagem_prevista for sessao in self.sessoes)


class SessaoModelo(Base):
    """Um treino da periodização: "Treino A — peito e tríceps"."""

    __tablename__ = "sessao_modelo"

    id: Mapped[int] = mapped_column(primary_key=True)
    periodizacao_id: Mapped[int] = mapped_column(
        ForeignKey("periodizacao.id", ondelete="CASCADE"), index=True
    )
    nome: Mapped[str] = mapped_column(String(120))
    ordem: Mapped[int] = mapped_column(Integer, default=0)
    # 0 = segunda … 6 = domingo. Nulo quando o treino não tem dia fixo.
    dia_da_semana: Mapped[int | None] = mapped_column(Integer, default=None)
    observacoes: Mapped[str | None] = mapped_column(Text, default=None)

    periodizacao: Mapped[Periodizacao] = relationship(back_populates="sessoes")
    prescricoes: Mapped[list["Prescricao"]] = relationship(
        back_populates="sessao",
        cascade="all, delete-orphan",
        order_by="Prescricao.ordem",
    )

    @property
    def tonelagem_prevista(self) -> float:
        """Soma o que tem carga definida; prescrição sem carga entra como zero.

        Somar só o que existe é melhor que devolver `None` para o treino
        inteiro por causa de um exercício sem carga — mas a tela precisa dizer
        quantos ficaram de fora, senão o número engana.
        """
        return sum(
            p.tonelagem_prevista or 0.0 for p in self.prescricoes
        )

    @property
    def prescricoes_sem_carga(self) -> int:
        return sum(1 for p in self.prescricoes if p.carga_alvo_kg is None)


class Prescricao(Base):
    """Um exercício prescrito: séries × repetições × carga, com as técnicas."""

    __tablename__ = "prescricao"

    id: Mapped[int] = mapped_column(primary_key=True)
    sessao_modelo_id: Mapped[int] = mapped_column(
        ForeignKey("sessao_modelo.id", ondelete="CASCADE"), index=True
    )
    exercicio_id: Mapped[int] = mapped_column(ForeignKey("exercicio.id"), index=True)
    ordem: Mapped[int] = mapped_column(Integer, default=0)

    # Exercícios com o mesmo `bloco` são executados juntos — é assim que um
    # bi-set vira dois registros ligados em vez de um campo de texto.
    bloco: Mapped[str | None] = mapped_column(String(4), default=None)
    agrupamento_id: Mapped[int | None] = mapped_column(
        ForeignKey("tecnica.id"), default=None
    )

    series: Mapped[int] = mapped_column(Integer, default=3)
    reps_min: Mapped[int] = mapped_column(Integer, default=8)
    reps_max: Mapped[int] = mapped_column(Integer, default=12)
    rir_alvo: Mapped[int | None] = mapped_column(Integer, default=2)
    descanso_s: Mapped[int | None] = mapped_column(Integer, default=90)

    # A carga vem de um dos dois: o João digita os quilos, ou dá o percentual e
    # a calculadora resolve a partir do e1RM do aluno. `carga_alvo_kg` é sempre
    # o valor final — inclusive quando saiu do percentual — para que a tela do
    # aluno não dependa de recalcular nada na academia.
    carga_alvo_kg: Mapped[float | None] = mapped_column(Float, default=None)
    percentual_1rm: Mapped[float | None] = mapped_column(Float, default=None)

    # Cadência em quatro tempos: excêntrica-pausa-concêntrica-pausa ("3-1-1-0").
    cadencia: Mapped[str | None] = mapped_column(String(15), default=None)
    observacao: Mapped[str | None] = mapped_column(String(300), default=None)

    sessao: Mapped[SessaoModelo] = relationship(back_populates="prescricoes")
    exercicio: Mapped[Exercicio] = relationship()
    series_detalhadas: Mapped[list["SerieDaPrescricao"]] = relationship(
        back_populates="prescricao",
        cascade="all, delete-orphan",
        order_by="SerieDaPrescricao.ordem",
    )
    agrupamento: Mapped[Tecnica | None] = relationship(foreign_keys=[agrupamento_id])
    tecnicas: Mapped[list[Tecnica]] = relationship(
        secondary=prescricao_tecnica, order_by="Tecnica.nome"
    )

    @property
    def reps_medio(self) -> float:
        return (self.reps_min + self.reps_max) / 2

    @property
    def tem_progressao(self) -> bool:
        """Se as séries de trabalho diferem entre si em repetições ou carga."""
        distintas = {
            (serie.reps, serie.carga_kg, serie.carga_ate_kg)
            for serie in self.series_detalhadas
            if serie.tipo.conta_no_volume
        }
        return len(distintas) > 1

    @property
    def tonelagem_prevista(self) -> float | None:
        """Repetições × carga somadas sobre as séries de trabalho.

        Mede trabalho, não força — e as duas não se substituem. Três séries de
        15 leves batem em tonelagem uma série pesada de 3 e não dizem nada
        sobre o quanto o aluno levanta.

        Aquecimento e up set ficam de fora: eles sobem até a carga de trabalho,
        e somá-los inflaria o volume sem o aluno ter treinado mais.
        """
        if self.series_detalhadas:
            parcelas = [s.tonelagem for s in self.series_detalhadas if s.tonelagem]
            return sum(parcelas) if parcelas else None

        # Sem séries detalhadas vale o resumo: todas as séries iguais.
        if self.carga_alvo_kg is None:
            return None
        return self.series * self.reps_medio * self.carga_alvo_kg

    @property
    def distorce_estimativa(self) -> bool:
        """Se alguma técnica invalida a leitura de 1RM — do exercício ou de
        qualquer uma das séries."""
        if any(tecnica.distorce_estimativa for tecnica in self.tecnicas):
            return True
        return any(
            tecnica.distorce_estimativa
            for serie in self.series_detalhadas
            for tecnica in serie.tecnicas
        )

    def __repr__(self) -> str:
        return f"<Prescricao {self.id} ex={self.exercicio_id} {self.series}x{self.reps_min}-{self.reps_max}>"


class TipoDeSerie(str, enum.Enum):
    """O papel da série dentro do exercício.

    Separa o que é trabalho do que é preparação. Aquecimento e up set sobem até
    a carga de trabalho e não são volume — contá-los na tonelagem inflaria o
    número sem que o aluno tenha treinado mais.
    """

    AQUECIMENTO = "aquecimento"
    UP_SET = "up_set"        # rampa até a carga de trabalho
    VALIDA = "valida"        # série de trabalho
    BACK_OFF = "back_off"    # série mais leve depois da pesada

    @property
    def conta_no_volume(self) -> bool:
        return self in {TipoDeSerie.VALIDA, TipoDeSerie.BACK_OFF}


serie_tecnica = Table(
    "serie_tecnica",
    Base.metadata,
    Column(
        "serie_id",
        ForeignKey("serie_da_prescricao.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column("tecnica_id", ForeignKey("tecnica.id"), primary_key=True),
)


class SerieDaPrescricao(Base):
    """Uma série, com reps e carga próprias.

    Existe porque a progressão dentro do exercício é a regra, não a exceção:
    `12x20kg / 10x30kg / 8x40kg` não cabe num único "3 × 8–12 @ 30 kg". E a
    técnica costuma ser de uma série só — no `10x100kg / 12x100kg cluster set`,
    só a segunda é cluster.
    """

    __tablename__ = "serie_da_prescricao"

    id: Mapped[int] = mapped_column(primary_key=True)
    prescricao_id: Mapped[int] = mapped_column(
        ForeignKey("prescricao.id", ondelete="CASCADE"), index=True
    )
    ordem: Mapped[int] = mapped_column(Integer, default=0)

    # Nulo no up set puro ("Up set de 40 a 100kg"), que sobe a carga sem
    # contagem fixa de repetições.
    reps: Mapped[int | None] = mapped_column(Integer, default=None)

    carga_kg: Mapped[float | None] = mapped_column(Float, default=None)
    # Quando preenchida, a série é uma rampa: "12x50 a 92kg" vai de 50 a 92.
    carga_ate_kg: Mapped[float | None] = mapped_column(Float, default=None)

    tipo: Mapped[TipoDeSerie] = mapped_column(
        Enum(TipoDeSerie, native_enum=False), default=TipoDeSerie.VALIDA
    )
    rir: Mapped[int | None] = mapped_column(Integer, default=None)
    observacao: Mapped[str | None] = mapped_column(String(200), default=None)

    prescricao: Mapped["Prescricao"] = relationship(back_populates="series_detalhadas")
    tecnicas: Mapped[list[Tecnica]] = relationship(
        secondary=serie_tecnica, order_by="Tecnica.nome"
    )

    @property
    def em_rampa(self) -> bool:
        return self.carga_ate_kg is not None

    @property
    def carga_media_kg(self) -> float | None:
        """A carga que representa a série para efeito de volume.

        Numa rampa é o ponto médio: aproximação, mas melhor do que contar só a
        inicial (subestima) ou só a final (superestima).
        """
        if self.carga_kg is None:
            return None
        if self.carga_ate_kg is None:
            return self.carga_kg
        return (self.carga_kg + self.carga_ate_kg) / 2

    @property
    def tonelagem(self) -> float | None:
        if not self.tipo.conta_no_volume:
            return None
        carga = self.carga_media_kg
        if carga is None or self.reps is None:
            return None
        return self.reps * carga

    @property
    def serve_para_1rm(self) -> bool:
        """Se esta série pode virar estimativa de 1RM.

        Rampa não serve — a carga não é um número só. Aquecimento e up set não
        servem porque não vão perto da falha. Técnica que quebra a contagem de
        repetições também invalida.
        """
        if self.em_rampa or self.reps is None or self.carga_kg is None:
            return False
        if not self.tipo.conta_no_volume:
            return False
        return not any(tecnica.distorce_estimativa for tecnica in self.tecnicas)

    def __repr__(self) -> str:
        return f"<Serie {self.ordem} {self.reps}x{self.carga_kg}>"


# ============================================================ a semana do aluno


class CheckinSemanal(Base):
    """Como foi a semana, pela mão do aluno.

    A semana é identificada pela segunda-feira (`semana`), com índice único por
    aluno: sem isso, dois envios no mesmo domingo virariam dois check-ins da
    mesma semana e o gráfico ganharia um degrau falso.
    """

    __tablename__ = "checkin_semanal"
    __table_args__ = (
        UniqueConstraint("aluno_id", "semana", name="um_checkin_por_semana"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    aluno_id: Mapped[int] = mapped_column(
        ForeignKey("aluno.id", ondelete="CASCADE"), index=True
    )
    semana: Mapped[date] = mapped_column(Date, index=True)

    peso_kg: Mapped[float | None] = mapped_column(Float, default=None)
    horas_de_sono: Mapped[float | None] = mapped_column(Float, default=None)
    passos_por_dia: Mapped[int | None] = mapped_column(Integer, default=None)

    # Escalas de 1 a 5, todas na mesma direção: 5 é sempre o melhor. Ter
    # "qualidade do sono 5 = ótimo" ao lado de "fadiga 5 = péssimo" faria o
    # aluno responder no piloto automático e errar.
    qualidade_do_sono: Mapped[int | None] = mapped_column(Integer, default=None)
    disposicao: Mapped[int | None] = mapped_column(Integer, default=None)
    recuperacao: Mapped[int | None] = mapped_column(Integer, default=None)

    aderencia_dieta: Mapped[int | None] = mapped_column(Integer, default=None)
    aderencia_treino: Mapped[int | None] = mapped_column(Integer, default=None)

    observacoes: Mapped[str | None] = mapped_column(Text, default=None)
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=agora)

    aluno: Mapped[Aluno] = relationship()
    medidas: Mapped["MedidaCorporal | None"] = relationship(
        back_populates="checkin", cascade="all, delete-orphan", uselist=False
    )

    def __repr__(self) -> str:
        return f"<Checkin {self.aluno_id} {self.semana}>"


class MedidaCorporal(Base):
    """Fita métrica. Opcional — muita gente mede uma vez por mês, não toda semana."""

    __tablename__ = "medida_corporal"

    id: Mapped[int] = mapped_column(primary_key=True)
    checkin_id: Mapped[int] = mapped_column(
        ForeignKey("checkin_semanal.id", ondelete="CASCADE"), unique=True, index=True
    )

    cintura_cm: Mapped[float | None] = mapped_column(Float, default=None)
    quadril_cm: Mapped[float | None] = mapped_column(Float, default=None)
    torax_cm: Mapped[float | None] = mapped_column(Float, default=None)
    braco_cm: Mapped[float | None] = mapped_column(Float, default=None)
    coxa_cm: Mapped[float | None] = mapped_column(Float, default=None)
    panturrilha_cm: Mapped[float | None] = mapped_column(Float, default=None)

    checkin: Mapped[CheckinSemanal] = relationship(back_populates="medidas")

    @property
    def vazia(self) -> bool:
        return all(
            getattr(self, campo) is None
            for campo in (
                "cintura_cm", "quadril_cm", "torax_cm",
                "braco_cm", "coxa_cm", "panturrilha_cm",
            )
        )
