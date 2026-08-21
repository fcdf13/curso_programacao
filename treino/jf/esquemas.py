"""Os formatos que entram e saem da API.

Nenhum esquema de saída carrega `senha_hash`: os modelos do SQLAlchemy nunca
viram JSON direto, sempre passam por aqui.
"""

from __future__ import annotations

from datetime import date

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from jf.auth import TAMANHO_MINIMO_DA_SENHA
from jf.modelos import ConvencaoDeCarga, Papel, Sexo

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
