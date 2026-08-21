"""As tabelas do app.

Fase 0 traz só o que sustenta o login e o vínculo treinador–aluno: `Usuario`,
`Aluno` e o catálogo de `Exercicio`. Check-in, treino e dieta entram nas fases
seguintes, cada um com suas tabelas.
"""

from __future__ import annotations

import enum
from datetime import date, datetime, timezone

from sqlalchemy import Boolean, Date, DateTime, Enum, Float, ForeignKey, String, Text
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
