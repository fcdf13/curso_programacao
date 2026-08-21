"""Periodização, treinos e prescrições — séries × repetições × carga.

A permissão de tudo aqui sobe até o aluno dono e passa por `auth.exigir_acesso`.
Ler é permitido aos dois lados; escrever, só ao treinador.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from jf.auth import aluno_permitido, exigir_acesso, treinador_atual, usuario_atual
from jf.banco import obter_sessao
from jf.esquemas import (
    EdicaoDaPeriodizacao,
    NovaPeriodizacao,
    NovaPrescricao,
    NovaSessaoModelo,
    PeriodizacaoEmResposta,
    PeriodizacaoNaLista,
    PrescricaoEmResposta,
    SessaoModeloEmResposta,
    TecnicaEmResposta,
)
from jf.modelos import (
    Aluno,
    EscopoDaTecnica,
    Periodizacao,
    Prescricao,
    SessaoModelo,
    Tecnica,
    Usuario,
)

rotas = APIRouter(tags=["treino"])


# ----------------------------------------------------------- técnicas


@rotas.get("/tecnicas", response_model=list[TecnicaEmResposta])
def listar_tecnicas(
    escopo: EscopoDaTecnica | None = None,
    _: Usuario = Depends(usuario_atual),
    sessao: Session = Depends(obter_sessao),
) -> list[Tecnica]:
    consulta = select(Tecnica).where(Tecnica.ativo.is_(True))
    if escopo is not None:
        consulta = consulta.where(Tecnica.escopo == escopo)
    return list(sessao.scalars(consulta.order_by(Tecnica.escopo, Tecnica.nome)).all())


# ------------------------------------------------------- resolver e permitir


def periodizacao_permitida(
    periodizacao_id: int,
    usuario: Usuario = Depends(usuario_atual),
    sessao: Session = Depends(obter_sessao),
) -> Periodizacao:
    periodizacao = sessao.get(Periodizacao, periodizacao_id)
    if periodizacao is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Periodização não encontrada.")
    exigir_acesso(usuario, periodizacao.aluno)
    return periodizacao


def sessao_permitida(
    sessao_id: int,
    usuario: Usuario = Depends(usuario_atual),
    sessao: Session = Depends(obter_sessao),
) -> SessaoModelo:
    treino = sessao.get(SessaoModelo, sessao_id)
    if treino is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Treino não encontrado.")
    exigir_acesso(usuario, treino.periodizacao.aluno)
    return treino


def prescricao_permitida(
    prescricao_id: int,
    usuario: Usuario = Depends(usuario_atual),
    sessao: Session = Depends(obter_sessao),
) -> Prescricao:
    prescricao = sessao.get(Prescricao, prescricao_id)
    if prescricao is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Prescrição não encontrada.")
    exigir_acesso(usuario, prescricao.sessao.periodizacao.aluno)
    return prescricao


# ------------------------------------------------------------ periodização


@rotas.get("/alunos/{aluno_id}/periodizacoes", response_model=list[PeriodizacaoNaLista])
def listar_periodizacoes(
    aluno: Aluno = Depends(aluno_permitido),
    sessao: Session = Depends(obter_sessao),
) -> list[Periodizacao]:
    return list(
        sessao.scalars(
            select(Periodizacao)
            .where(Periodizacao.aluno_id == aluno.id)
            .order_by(Periodizacao.criada_em.desc())
        ).all()
    )


@rotas.post(
    "/alunos/{aluno_id}/periodizacoes",
    response_model=PeriodizacaoEmResposta,
    status_code=status.HTTP_201_CREATED,
)
def criar_periodizacao(
    dados: NovaPeriodizacao,
    aluno: Aluno = Depends(aluno_permitido),
    _: Usuario = Depends(treinador_atual),
    sessao: Session = Depends(obter_sessao),
) -> Periodizacao:
    periodizacao = Periodizacao(
        aluno_id=aluno.id, **dados.model_dump(exclude={"equacao"}), equacao=dados.equacao.value
    )
    sessao.add(periodizacao)
    sessao.commit()
    sessao.refresh(periodizacao)
    return periodizacao


@rotas.get("/periodizacoes/{periodizacao_id}", response_model=PeriodizacaoEmResposta)
def detalhar_periodizacao(
    periodizacao: Periodizacao = Depends(periodizacao_permitida),
) -> Periodizacao:
    return periodizacao


@rotas.patch("/periodizacoes/{periodizacao_id}", response_model=PeriodizacaoEmResposta)
def editar_periodizacao(
    dados: EdicaoDaPeriodizacao,
    periodizacao: Periodizacao = Depends(periodizacao_permitida),
    _: Usuario = Depends(treinador_atual),
    sessao: Session = Depends(obter_sessao),
) -> Periodizacao:
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(periodizacao, campo, valor.value if campo == "equacao" else valor)
    sessao.commit()
    sessao.refresh(periodizacao)
    return periodizacao


@rotas.delete(
    "/periodizacoes/{periodizacao_id}", status_code=status.HTTP_204_NO_CONTENT
)
def apagar_periodizacao(
    periodizacao: Periodizacao = Depends(periodizacao_permitida),
    _: Usuario = Depends(treinador_atual),
    sessao: Session = Depends(obter_sessao),
) -> None:
    sessao.delete(periodizacao)
    sessao.commit()


# ------------------------------------------------------------------ treinos


@rotas.post(
    "/periodizacoes/{periodizacao_id}/sessoes",
    response_model=SessaoModeloEmResposta,
    status_code=status.HTTP_201_CREATED,
)
def criar_sessao(
    dados: NovaSessaoModelo,
    periodizacao: Periodizacao = Depends(periodizacao_permitida),
    _: Usuario = Depends(treinador_atual),
    sessao: Session = Depends(obter_sessao),
) -> SessaoModelo:
    treino = SessaoModelo(periodizacao_id=periodizacao.id, **dados.model_dump())
    sessao.add(treino)
    sessao.commit()
    sessao.refresh(treino)
    return treino


@rotas.get("/sessoes/{sessao_id}", response_model=SessaoModeloEmResposta)
def detalhar_sessao(treino: SessaoModelo = Depends(sessao_permitida)) -> SessaoModelo:
    return treino


@rotas.delete("/sessoes/{sessao_id}", status_code=status.HTTP_204_NO_CONTENT)
def apagar_sessao(
    treino: SessaoModelo = Depends(sessao_permitida),
    _: Usuario = Depends(treinador_atual),
    sessao: Session = Depends(obter_sessao),
) -> None:
    sessao.delete(treino)
    sessao.commit()


# -------------------------------------------------------------- prescrições


def _conferir_tecnicas(
    sessao: Session, tecnica_ids: list[int], agrupamento_id: int | None
) -> tuple[list[Tecnica], Tecnica | None]:
    """Garante que cada técnica está no campo do seu escopo.

    Bi-set não é uma técnica de execução: ele liga exercícios, então vive em
    `agrupamento`. Aceitar os dois no mesmo campo tornaria impossível saber, a
    partir do dado, se uma prescrição é um bloco ou um exercício solto.
    """
    tecnicas: list[Tecnica] = []
    if tecnica_ids:
        tecnicas = list(
            sessao.scalars(select(Tecnica).where(Tecnica.id.in_(set(tecnica_ids)))).all()
        )
        if len(tecnicas) != len(set(tecnica_ids)):
            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_CONTENT, "Técnica desconhecida."
            )
        for tecnica in tecnicas:
            if tecnica.escopo is EscopoDaTecnica.AGRUPAMENTO:
                raise HTTPException(
                    status.HTTP_422_UNPROCESSABLE_CONTENT,
                    f"{tecnica.nome} liga exercícios diferentes; informe-a como "
                    "agrupamento do bloco, não como técnica do exercício.",
                )

    agrupamento = None
    if agrupamento_id is not None:
        agrupamento = sessao.get(Tecnica, agrupamento_id)
        if agrupamento is None:
            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_CONTENT, "Agrupamento desconhecido."
            )
        if agrupamento.escopo is not EscopoDaTecnica.AGRUPAMENTO:
            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_CONTENT,
                f"{agrupamento.nome} age dentro de um exercício só; ela não serve "
                "como agrupamento de bloco.",
            )

    return tecnicas, agrupamento


def _aplicar(prescricao: Prescricao, dados: NovaPrescricao, tecnicas: list[Tecnica]) -> None:
    for campo, valor in dados.model_dump(exclude={"tecnica_ids"}).items():
        setattr(prescricao, campo, valor)
    prescricao.tecnicas = tecnicas


@rotas.post(
    "/sessoes/{sessao_id}/prescricoes",
    response_model=PrescricaoEmResposta,
    status_code=status.HTTP_201_CREATED,
)
def criar_prescricao(
    dados: NovaPrescricao,
    treino: SessaoModelo = Depends(sessao_permitida),
    _: Usuario = Depends(treinador_atual),
    sessao: Session = Depends(obter_sessao),
) -> Prescricao:
    tecnicas, agrupamento = _conferir_tecnicas(
        sessao, dados.tecnica_ids, dados.agrupamento_id
    )
    if agrupamento is not None and dados.bloco is None:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_CONTENT,
            f"{agrupamento.nome} liga exercícios, então precisa de um bloco "
            "para dizer com quais.",
        )

    prescricao = Prescricao(sessao_modelo_id=treino.id)
    _aplicar(prescricao, dados, tecnicas)
    sessao.add(prescricao)
    sessao.commit()
    sessao.refresh(prescricao)
    return prescricao


@rotas.put("/prescricoes/{prescricao_id}", response_model=PrescricaoEmResposta)
def editar_prescricao(
    dados: NovaPrescricao,
    prescricao: Prescricao = Depends(prescricao_permitida),
    _: Usuario = Depends(treinador_atual),
    sessao: Session = Depends(obter_sessao),
) -> Prescricao:
    tecnicas, _agrupamento = _conferir_tecnicas(
        sessao, dados.tecnica_ids, dados.agrupamento_id
    )
    _aplicar(prescricao, dados, tecnicas)
    sessao.commit()
    sessao.refresh(prescricao)
    return prescricao


@rotas.delete("/prescricoes/{prescricao_id}", status_code=status.HTTP_204_NO_CONTENT)
def apagar_prescricao(
    prescricao: Prescricao = Depends(prescricao_permitida),
    _: Usuario = Depends(treinador_atual),
    sessao: Session = Depends(obter_sessao),
) -> None:
    sessao.delete(prescricao)
    sessao.commit()
