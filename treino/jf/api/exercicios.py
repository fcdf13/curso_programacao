"""O catálogo de exercícios, compartilhado por todo mundo."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from jf.auth import usuario_atual
from jf.banco import obter_sessao
from jf.esquemas import ExercicioEmResposta
from jf.modelos import Exercicio, Usuario

rotas = APIRouter(prefix="/exercicios", tags=["exercícios"])


@rotas.get("", response_model=list[ExercicioEmResposta])
def listar(
    busca: str | None = None,
    grupo: str | None = None,
    _: Usuario = Depends(usuario_atual),
    sessao: Session = Depends(obter_sessao),
) -> list[Exercicio]:
    consulta = select(Exercicio).where(Exercicio.ativo.is_(True))
    if busca:
        consulta = consulta.where(Exercicio.nome.icontains(busca.strip()))
    if grupo:
        consulta = consulta.where(Exercicio.grupo_muscular == grupo)
    consulta = consulta.order_by(Exercicio.grupo_muscular, Exercicio.nome)
    return list(sessao.scalars(consulta).all())


@rotas.get("/grupos", response_model=list[str])
def grupos(
    _: Usuario = Depends(usuario_atual),
    sessao: Session = Depends(obter_sessao),
) -> list[str]:
    consulta = (
        select(Exercicio.grupo_muscular)
        .where(Exercicio.ativo.is_(True))
        .distinct()
        .order_by(Exercicio.grupo_muscular)
    )
    return list(sessao.scalars(consulta).all())
