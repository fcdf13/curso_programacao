"""Senha, sessão e quem-pode-ver-o-quê.

O modelo de permissão do app inteiro cabe em duas frases: o treinador enxerga
os alunos vinculados a ele; o aluno enxerga apenas a si mesmo. Toda rota que
recebe um `aluno_id` na URL passa por `aluno_permitido`, e nenhuma consulta
monta filtro de dono por conta própria — é assim que se evita o buraco clássico
de `/api/alunos/7/...` responder para quem não é o 7 nem o treinador do 7.
"""

from __future__ import annotations

import time
from collections import defaultdict

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError
from fastapi import Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from jf.banco import obter_sessao
from jf.modelos import Aluno, Papel, Usuario

_hasher = PasswordHasher()

TAMANHO_MINIMO_DA_SENHA = 10

# Hash descartável de uma senha qualquer. Serve para gastar o mesmo tempo de
# CPU quando o email não existe — sem isso, "email não cadastrado" responde em
# microssegundos e "senha errada" em ~50 ms, e a diferença revela quem tem conta.
_HASH_FALSO = _hasher.hash("nao-existe-nenhum-usuario-com-esta-senha")


def normalizar_email(email: str) -> str:
    return email.strip().lower()


def hash_de_senha(senha: str) -> str:
    if len(senha) < TAMANHO_MINIMO_DA_SENHA:
        raise ValueError(
            f"A senha precisa de pelo menos {TAMANHO_MINIMO_DA_SENHA} caracteres."
        )
    return _hasher.hash(senha)


def conferir_senha(senha_hash: str, senha: str) -> bool:
    try:
        return _hasher.verify(senha_hash, senha)
    except (VerifyMismatchError, VerificationError):
        return False


# ---------------------------------------------------------------- tentativas

_JANELA_SEGUNDOS = 300
_MAXIMO_DE_TENTATIVAS = 10
_tentativas: dict[str, list[float]] = defaultdict(list)


def _tentativas_demais(chave: str) -> bool:
    """Freio simples de força bruta no login.

    O estado vive na memória deste processo, então ele *não* protege um deploy
    com vários workers nem sobrevive a um reinício. Segura o roteiro ingênuo
    que tenta mil senhas seguidas; não substitui um limite no proxy ou uma
    contagem compartilhada, que é o que a fase 5 precisa colocar no lugar.
    """
    agora = time.monotonic()
    recentes = [t for t in _tentativas[chave] if agora - t < _JANELA_SEGUNDOS]
    _tentativas[chave] = recentes
    return len(recentes) >= _MAXIMO_DE_TENTATIVAS


def _registrar_tentativa(chave: str) -> None:
    _tentativas[chave].append(time.monotonic())


def _limpar_tentativas(chave: str) -> None:
    _tentativas.pop(chave, None)


def autenticar(sessao: Session, email: str, senha: str) -> Usuario | None:
    """Devolve o usuário se o par email/senha confere, senão `None`."""
    email = normalizar_email(email)

    if _tentativas_demais(email):
        raise HTTPException(
            status.HTTP_429_TOO_MANY_REQUESTS,
            "Tentativas demais. Espere alguns minutos antes de tentar de novo.",
        )

    usuario = sessao.scalar(select(Usuario).where(Usuario.email == email))

    if usuario is None or not usuario.ativo:
        # Confere contra o hash falso mesmo assim, para o tempo de resposta não
        # denunciar se o email existe.
        conferir_senha(_HASH_FALSO, senha)
        _registrar_tentativa(email)
        return None

    if not conferir_senha(usuario.senha_hash, senha):
        _registrar_tentativa(email)
        return None

    _limpar_tentativas(email)
    return usuario


# ---------------------------------------------------------------- dependências


def usuario_atual(
    request: Request, sessao: Session = Depends(obter_sessao)
) -> Usuario:
    """Quem está logado, ou 401."""
    usuario_id = request.session.get("usuario_id")
    if usuario_id is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Faça login para continuar.")

    usuario = sessao.get(Usuario, usuario_id)
    if usuario is None or not usuario.ativo:
        # A conta sumiu ou foi desativada depois que o cookie foi emitido.
        request.session.clear()
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Sessão expirada.")

    return usuario


def treinador_atual(usuario: Usuario = Depends(usuario_atual)) -> Usuario:
    if usuario.papel is not Papel.TREINADOR:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Só o treinador pode fazer isso.")
    return usuario


def pode_ver(usuario: Usuario, aluno: Aluno) -> bool:
    """A regra inteira do app, num lugar só.

    Tudo que pende de um aluno — periodização, treino, prescrição, check-in —
    resolve a permissão subindo até o aluno e chamando isto aqui. Ter a regra
    escrita duas vezes é como as duas cópias divergem.
    """
    if usuario.papel is Papel.TREINADOR:
        return aluno.treinador_id == usuario.id
    return aluno.usuario_id == usuario.id


def exigir_acesso(usuario: Usuario, aluno: Aluno | None) -> Aluno:
    """`pode_ver` na forma de guarda, com o 404 que não vaza existência."""
    if aluno is None or not pode_ver(usuario, aluno):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Aluno não encontrado.")
    return aluno


def consentimento_em_dia(usuario: Usuario = Depends(usuario_atual)) -> Usuario:
    """Barra a gravação de dado de saúde sem consentimento em vigor.

    É isto que torna o consentimento real em vez de decorativo: sem ele o app
    não *aceita* o dado, em vez de aceitar e depois pedir desculpa. O treinador
    passa direto — ele é o controlador, não o titular, e a base legal do
    tratamento dele é o contrato com o aluno.

    Só a escrita passa por aqui. Ler o que já está guardado é um direito do
    titular (art. 18, II), não um tratamento novo que precise de permissão.
    """
    if usuario.papel is Papel.TREINADOR:
        return usuario

    if usuario.consentimento_ativo is None:
        raise HTTPException(
            status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS,
            "Aceite o termo de uso dos dados antes de registrar peso, sono ou "
            "medidas. Você encontra o termo em Meus dados.",
        )
    return usuario


def aluno_permitido(
    aluno_id: int,
    usuario: Usuario = Depends(usuario_atual),
    sessao: Session = Depends(obter_sessao),
) -> Aluno:
    """O aluno de `aluno_id`, se quem pediu tem direito de vê-lo.

    Responde 404 — e não 403 — quando o aluno existe mas é de outro treinador:
    um 403 confirmaria que aquele id existe, o que já é informação sobre a base
    de alunos de outra pessoa.
    """
    return exigir_acesso(usuario, sessao.get(Aluno, aluno_id))
