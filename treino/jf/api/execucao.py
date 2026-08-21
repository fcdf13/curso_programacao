"""O treino como ele aconteceu — o modo academia.

O aluno abre o treino no celular, faz a série e registra carga, repetições e
RIR. É o dado que faltava para a calculadora sair de tela isolada: sem saber o
que ele levantou de verdade, não há e1RM, e sem e1RM a carga sugerida é chute.

Subsolo de academia não tem sinal, então o celular guarda a fila e manda quando
der. Tudo aqui é pensado para isso: a abertura do treino é idempotente, e a
sincronização das séries é um **upsert por chave gerada no aparelho**, nunca um
"substitua tudo por isto".
"""

from __future__ import annotations

from datetime import date, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from jf.auth import (
    aluno_permitido,
    consentimento_em_dia,
    exigir_acesso,
    usuario_atual,
)
from jf.banco import obter_sessao
from jf.esquemas import (
    AberturaDeTreino,
    EncerramentoDoTreino,
    SeriesExecutadas,
    TreinoNaLista,
    TreinoRealizadoEmResposta,
)
from jf.modelos import (
    Aluno,
    Exercicio,
    Prescricao,
    SerieDaPrescricao,
    SerieRealizada,
    SessaoModelo,
    SessaoRealizada,
    Usuario,
    agora,
)

rotas = APIRouter(tags=["treino executado"])


def treino_permitido(
    treino_id: int,
    usuario: Usuario = Depends(usuario_atual),
    sessao: Session = Depends(obter_sessao),
) -> SessaoRealizada:
    treino = sessao.get(SessaoRealizada, treino_id)
    if treino is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Treino não encontrado.")
    exigir_acesso(usuario, treino.aluno)
    return treino


@rotas.post(
    "/alunos/{aluno_id}/treinos-realizados",
    response_model=TreinoRealizadoEmResposta,
    status_code=status.HTTP_201_CREATED,
)
def abrir(
    dados: AberturaDeTreino,
    aluno: Aluno = Depends(aluno_permitido),
    _: Usuario = Depends(consentimento_em_dia),
    sessao: Session = Depends(obter_sessao),
) -> SessaoRealizada:
    """Abre o treino de hoje — ou devolve o que já estava aberto.

    Idempotente porque o celular vai chamar isto de novo: perdeu o sinal,
    recarregou a tela, voltou no dia seguinte para terminar. Criar um segundo
    treino a cada tentativa partiria o registro em dois.
    """
    if dados.dia > date.today():
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_CONTENT,
            "Não dá para registrar um treino de um dia que ainda não chegou.",
        )

    modelo = sessao.get(SessaoModelo, dados.sessao_id)
    if modelo is None or modelo.periodizacao.aluno_id != aluno.id:
        # 404 e não 403: o treino de outro aluno não existe, para quem pergunta.
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Treino não encontrado.")

    existente = sessao.scalars(
        select(SessaoRealizada)
        .where(SessaoRealizada.aluno_id == aluno.id)
        .where(SessaoRealizada.sessao_id == modelo.id)
        .where(SessaoRealizada.dia == dados.dia)
    ).first()
    if existente is not None:
        return existente

    # O nome vem copiado: quando o João reorganizar a periodização, o histórico
    # do aluno continua legível em vez de virar "treino apagado".
    treino = SessaoRealizada(
        aluno_id=aluno.id, sessao_id=modelo.id, nome=modelo.nome, dia=dados.dia
    )
    sessao.add(treino)
    sessao.commit()
    sessao.refresh(treino)
    return treino


@rotas.get(
    "/alunos/{aluno_id}/treinos-realizados", response_model=list[TreinoNaLista]
)
def listar(
    aluno: Aluno = Depends(aluno_permitido),
    sessao: Session = Depends(obter_sessao),
    semanas: int = 12,
) -> list[SessaoRealizada]:
    limite = date.today() - timedelta(weeks=max(semanas, 1))
    return list(
        sessao.scalars(
            select(SessaoRealizada)
            .where(SessaoRealizada.aluno_id == aluno.id)
            .where(SessaoRealizada.dia >= limite)
            .order_by(SessaoRealizada.dia.desc(), SessaoRealizada.id.desc())
        ).all()
    )


@rotas.get(
    "/treinos-realizados/{treino_id}", response_model=TreinoRealizadoEmResposta
)
def detalhar(
    treino: SessaoRealizada = Depends(treino_permitido),
) -> SessaoRealizada:
    return treino


@rotas.put(
    "/treinos-realizados/{treino_id}/series",
    response_model=TreinoRealizadoEmResposta,
)
def sincronizar(
    dados: SeriesExecutadas,
    treino: SessaoRealizada = Depends(treino_permitido),
    _: Usuario = Depends(consentimento_em_dia),
    sessao: Session = Depends(obter_sessao),
) -> SessaoRealizada:
    """Recebe a fila do celular e devolve o estado do servidor.

    Acrescenta o que é novo e atualiza o que mudou, casando pela `chave_local`.
    Mandar a mesma fila dez vezes dá o mesmo resultado que mandar uma — que é o
    requisito de quem sincroniza com sinal ruim.

    **Não apaga** o que não veio: um aparelho com visão parcial do treino
    limparia o que foi registrado de outro lugar. Apagar é uma chamada própria.
    """
    if treino.encerrada:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "Este treino já foi encerrado. Reabra antes de registrar mais séries.",
        )

    por_chave = {serie.chave_local: serie for serie in treino.series}
    exercicios = set()

    for entrada in dados.series:
        exercicios.add(entrada.exercicio_id)

    if exercicios:
        conhecidos = set(
            sessao.scalars(
                select(Exercicio.id).where(Exercicio.id.in_(exercicios))
            ).all()
        )
        faltando = exercicios - conhecidos
        if faltando:
            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_CONTENT, "Exercício desconhecido."
            )

    for entrada in dados.series:
        _conferir_procedencia(sessao, treino, entrada)

        serie = por_chave.get(entrada.chave_local)
        if serie is None:
            serie = SerieRealizada(
                sessao_realizada_id=treino.id, chave_local=entrada.chave_local
            )
            treino.series.append(serie)
            por_chave[entrada.chave_local] = serie

        for campo, valor in entrada.model_dump(exclude={"chave_local"}).items():
            setattr(serie, campo, valor)

    sessao.commit()
    sessao.refresh(treino)
    return treino


def _conferir_procedencia(
    sessao: Session, treino: SessaoRealizada, entrada
) -> None:
    """A prescrição citada precisa ser mesmo deste treino.

    Sem isto, um aluno poderia pendurar a própria série na prescrição de outro
    — e o histórico de quem não treinou ganharia carga que ele não levantou.
    """
    if entrada.prescricao_id is not None:
        prescricao = sessao.get(Prescricao, entrada.prescricao_id)
        if prescricao is None or prescricao.sessao_modelo_id != treino.sessao_id:
            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_CONTENT,
                "Essa prescrição não é deste treino.",
            )

    if entrada.serie_id is not None:
        prescrita = sessao.get(SerieDaPrescricao, entrada.serie_id)
        if prescrita is None or prescrita.prescricao_id != entrada.prescricao_id:
            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_CONTENT,
                "Essa série não é dessa prescrição.",
            )


@rotas.delete(
    "/treinos-realizados/{treino_id}/series/{chave_local}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def apagar_serie(
    chave_local: str,
    treino: SessaoRealizada = Depends(treino_permitido),
    _: Usuario = Depends(consentimento_em_dia),
    sessao: Session = Depends(obter_sessao),
) -> None:
    """Apagar é explícito. A sincronização nunca apaga por omissão."""
    for serie in treino.series:
        if serie.chave_local == chave_local:
            sessao.delete(serie)
            sessao.commit()
            return
    raise HTTPException(status.HTTP_404_NOT_FOUND, "Série não encontrada.")


@rotas.post(
    "/treinos-realizados/{treino_id}/encerrar",
    response_model=TreinoRealizadoEmResposta,
)
def encerrar(
    dados: EncerramentoDoTreino,
    treino: SessaoRealizada = Depends(treino_permitido),
    _: Usuario = Depends(consentimento_em_dia),
    sessao: Session = Depends(obter_sessao),
) -> SessaoRealizada:
    treino.encerrada_em = treino.encerrada_em or agora()
    if dados.observacoes is not None:
        treino.observacoes = dados.observacoes
    sessao.commit()
    sessao.refresh(treino)
    return treino


@rotas.post(
    "/treinos-realizados/{treino_id}/reabrir",
    response_model=TreinoRealizadoEmResposta,
)
def reabrir(
    treino: SessaoRealizada = Depends(treino_permitido),
    _: Usuario = Depends(consentimento_em_dia),
    sessao: Session = Depends(obter_sessao),
) -> SessaoRealizada:
    """Encerrou sem querer, ou lembrou de uma série depois. Acontece."""
    treino.encerrada_em = None
    sessao.commit()
    sessao.refresh(treino)
    return treino


@rotas.delete(
    "/treinos-realizados/{treino_id}", status_code=status.HTTP_204_NO_CONTENT
)
def apagar(
    treino: SessaoRealizada = Depends(treino_permitido),
    _: Usuario = Depends(consentimento_em_dia),
    sessao: Session = Depends(obter_sessao),
) -> None:
    sessao.delete(treino)
    sessao.commit()
