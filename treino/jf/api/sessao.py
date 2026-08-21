"""Entrar, sair e saber quem está logado."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from jf.auth import (
    abrir_sessao,
    autenticar,
    conferir_senha,
    trocar_senha,
    usuario_atual,
)
from jf.banco import obter_sessao
from jf.esquemas import Credenciais, QuemSouEu, TrocaDeSenha, UsuarioEmResposta
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

    abrir_sessao(request, usuario)
    return _quem_sou_eu(sessao, usuario)


@rotas.post("/sair", status_code=status.HTTP_204_NO_CONTENT)
def sair(request: Request) -> None:
    request.session.clear()


@rotas.post("/eu/senha", status_code=status.HTTP_204_NO_CONTENT)
def mudar_a_propria_senha(
    dados: TrocaDeSenha,
    request: Request,
    usuario: Usuario = Depends(usuario_atual),
    sessao: Session = Depends(obter_sessao),
) -> None:
    """Troca a própria senha e derruba os outros aparelhos.

    Reabre esta sessão no fim: quem trocou a senha continua onde estava, e todo
    o resto cai — inclusive a sessão de quem quer que soubesse a senha antiga,
    que é para isso que a troca serve.
    """
    if not conferir_senha(usuario.senha_hash, dados.senha_atual):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Senha atual incorreta.")

    if dados.senha_nova == dados.senha_atual:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_CONTENT,
            "A senha nova precisa ser diferente da atual.",
        )

    trocar_senha(usuario, dados.senha_nova)
    sessao.commit()
    abrir_sessao(request, usuario)


@rotas.get("/eu", response_model=QuemSouEu)
def eu(
    usuario: Usuario = Depends(usuario_atual),
    sessao: Session = Depends(obter_sessao),
) -> QuemSouEu:
    return _quem_sou_eu(sessao, usuario)
