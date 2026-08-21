"""Os alunos do treinador: listar, cadastrar e editar o perfil."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from jf.auth import (
    aluno_permitido,
    consentimento_em_dia,
    hash_de_senha,
    normalizar_email,
    treinador_atual,
)
from jf.banco import obter_sessao
from jf.esquemas import AlunoEmResposta, EdicaoDoAluno, NovoAluno
from jf.modelos import Aluno, Papel, Usuario

rotas = APIRouter(prefix="/alunos", tags=["alunos"])


def resposta(aluno: Aluno) -> AlunoEmResposta:
    """Junta o perfil com o nome e o email, que moram em `Usuario`."""
    return AlunoEmResposta(
        id=aluno.id,
        nome=aluno.usuario.nome,
        email=aluno.usuario.email,
        nascimento=aluno.nascimento,
        sexo=aluno.sexo,
        altura_cm=aluno.altura_cm,
        objetivo=aluno.objetivo,
        observacoes=aluno.observacoes,
    )


@rotas.get("", response_model=list[AlunoEmResposta])
def listar(
    treinador: Usuario = Depends(treinador_atual),
    sessao: Session = Depends(obter_sessao),
) -> list[AlunoEmResposta]:
    alunos = sessao.scalars(
        select(Aluno)
        .where(Aluno.treinador_id == treinador.id)
        .join(Aluno.usuario)
        .order_by(Usuario.nome)
    ).all()
    return [resposta(aluno) for aluno in alunos]


@rotas.post("", response_model=AlunoEmResposta, status_code=status.HTTP_201_CREATED)
def cadastrar(
    dados: NovoAluno,
    treinador: Usuario = Depends(treinador_atual),
    sessao: Session = Depends(obter_sessao),
) -> AlunoEmResposta:
    usuario = Usuario(
        nome=dados.nome.strip(),
        email=normalizar_email(dados.email),
        senha_hash=hash_de_senha(dados.senha),
        papel=Papel.ALUNO,
    )
    aluno = Aluno(
        usuario=usuario,
        treinador_id=treinador.id,
        nascimento=dados.nascimento,
        sexo=dados.sexo,
        altura_cm=dados.altura_cm,
        objetivo=dados.objetivo,
        observacoes=dados.observacoes,
    )
    sessao.add(aluno)

    try:
        sessao.commit()
    except IntegrityError:
        # O índice único de `usuario.email` é quem decide de verdade; conferir
        # antes com um SELECT deixaria uma corrida entre dois cadastros
        # simultâneos do mesmo email.
        sessao.rollback()
        raise HTTPException(
            status.HTTP_409_CONFLICT, "Já existe uma conta com esse email."
        ) from None

    sessao.refresh(aluno)
    return resposta(aluno)


@rotas.get("/{aluno_id}", response_model=AlunoEmResposta)
def detalhar(aluno: Aluno = Depends(aluno_permitido)) -> AlunoEmResposta:
    return resposta(aluno)


@rotas.patch("/{aluno_id}", response_model=AlunoEmResposta)
def editar(
    dados: EdicaoDoAluno,
    aluno: Aluno = Depends(aluno_permitido),
    _: Usuario = Depends(consentimento_em_dia),
    sessao: Session = Depends(obter_sessao),
) -> AlunoEmResposta:
    # `exclude_unset` para que não mandar um campo signifique "deixa como está",
    # e mandar `null` signifique "apaga".
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(aluno, campo, valor)
    sessao.commit()
    sessao.refresh(aluno)
    return resposta(aluno)
