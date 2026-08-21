"""Entrar, sair e saber quem está logado."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from jf.auth import autenticar, usuario_atual
from jf.banco import obter_sessao
from jf.esquemas import Credenciais, QuemSouEu, UsuarioEmResposta
from jf.modelos import Aluno, Papel, Usuario

rotas = APIRouter(tags=["sessão"])


def _quem_sou_eu(sessao: Session, usuario: Usuario) -> QuemSouEu:
    aluno_id = None
    if usuario.papel is Papel.ALUNO:
        aluno_id = sessao.scalar(
            select(Aluno.id).where(Aluno.usuario_id == usuario.id)
        )
    return QuemSouEu(
        usuario=UsuarioEmResposta.model_validate(usuario), aluno_id=aluno_id
    )


@rotas.post("/entrar", response_model=QuemSouEu)
def entrar(
    credenciais: Credenciais,
    request: Request,
    sessao: Session = Depends(obter_sessao),
) -> QuemSouEu:
    usuario = autenticar(sessao, credenciais.email, credenciais.senha)
    if usuario is None:
        # Mensagem única de propósito: dizer "esse email não existe" entrega
        # quem é cliente do João para quem só tem uma lista de emails.
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, "Email ou senha incorretos."
        )

    # Troca o identificador da sessão ao autenticar, para que um cookie plantado
    # antes do login não continue valendo depois dele (fixação de sessão).
    request.session.clear()
    request.session["usuario_id"] = usuario.id

    return _quem_sou_eu(sessao, usuario)


@rotas.post("/sair", status_code=status.HTTP_204_NO_CONTENT)
def sair(request: Request) -> None:
    request.session.clear()


@rotas.get("/eu", response_model=QuemSouEu)
def eu(
    usuario: Usuario = Depends(usuario_atual),
    sessao: Session = Depends(obter_sessao),
) -> QuemSouEu:
    return _quem_sou_eu(sessao, usuario)
