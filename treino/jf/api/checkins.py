"""O check-in semanal e a evolução em números.

O aluno preenche, o treinador lê — os dois pela mesma rota, com a permissão
subindo até o aluno dono. Escrever é do aluno e do treinador dele: o João
corrige um peso digitado errado sem precisar pedir.
"""

from __future__ import annotations

from datetime import date, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from jf.auth import aluno_permitido, exigir_acesso, usuario_atual
from jf.banco import obter_sessao
from jf.esquemas import (
    CheckinEmResposta,
    Evolucao,
    NovoCheckin,
    PontoDaSerie,
    SerieDoGrafico,
)
from jf.modelos import Aluno, CheckinSemanal, MedidaCorporal, Usuario

rotas = APIRouter(tags=["check-in"])

# Quantas semanas a média móvel do peso cobre. Quatro é o mínimo que tira o
# ruído de água e sal sem atrasar demais a leitura de uma tendência real.
JANELA_DA_TENDENCIA = 4

SERIES = [
    ("peso_kg", "Peso", "kg"),
    ("horas_de_sono", "Sono", "h/noite"),
    ("qualidade_do_sono", "Qualidade do sono", "1–5"),
    ("disposicao", "Disposição", "1–5"),
    ("recuperacao", "Recuperação", "1–5"),
    ("passos_por_dia", "Passos", "por dia"),
    ("aderencia_dieta", "Aderência à dieta", "%"),
    ("aderencia_treino", "Aderência ao treino", "%"),
]


def checkin_permitido(
    checkin_id: int,
    usuario: Usuario = Depends(usuario_atual),
    sessao: Session = Depends(obter_sessao),
) -> CheckinSemanal:
    checkin = sessao.get(CheckinSemanal, checkin_id)
    if checkin is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Check-in não encontrado.")
    exigir_acesso(usuario, checkin.aluno)
    return checkin


def _aplicar(checkin: CheckinSemanal, dados: NovoCheckin, parcial: bool) -> None:
    campos = dados.model_dump(exclude={"medidas"}, exclude_unset=parcial)
    for campo, valor in campos.items():
        setattr(checkin, campo, valor)

    if dados.medidas is None:
        return

    if checkin.medidas is None:
        checkin.medidas = MedidaCorporal()
    for campo, valor in dados.medidas.model_dump(exclude_unset=parcial).items():
        setattr(checkin.medidas, campo, valor)

    # Medida toda em branco não vira uma linha vazia no banco.
    if checkin.medidas.vazia:
        checkin.medidas = None


@rotas.get("/alunos/{aluno_id}/checkins", response_model=list[CheckinEmResposta])
def listar(
    aluno: Aluno = Depends(aluno_permitido),
    sessao: Session = Depends(obter_sessao),
    semanas: int = 52,
) -> list[CheckinSemanal]:
    limite = date.today() - timedelta(weeks=max(semanas, 1))
    return list(
        sessao.scalars(
            select(CheckinSemanal)
            .where(CheckinSemanal.aluno_id == aluno.id)
            .where(CheckinSemanal.semana >= limite)
            .order_by(CheckinSemanal.semana)
        ).all()
    )


@rotas.post(
    "/alunos/{aluno_id}/checkins",
    response_model=CheckinEmResposta,
    status_code=status.HTTP_201_CREATED,
)
def registrar(
    dados: NovoCheckin,
    aluno: Aluno = Depends(aluno_permitido),
    sessao: Session = Depends(obter_sessao),
) -> CheckinSemanal:
    checkin = CheckinSemanal(aluno_id=aluno.id)
    _aplicar(checkin, dados, parcial=False)
    sessao.add(checkin)

    try:
        sessao.commit()
    except IntegrityError:
        # O índice único de (aluno, semana) é quem decide; conferir antes com um
        # SELECT deixaria uma corrida entre dois envios simultâneos.
        sessao.rollback()
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "Já existe um check-in desta semana. Edite o que já está lá.",
        ) from None

    sessao.refresh(checkin)
    return checkin


@rotas.patch("/checkins/{checkin_id}", response_model=CheckinEmResposta)
def editar(
    dados: NovoCheckin,
    checkin: CheckinSemanal = Depends(checkin_permitido),
    sessao: Session = Depends(obter_sessao),
) -> CheckinSemanal:
    _aplicar(checkin, dados, parcial=True)
    sessao.commit()
    sessao.refresh(checkin)
    return checkin


@rotas.delete("/checkins/{checkin_id}", status_code=status.HTTP_204_NO_CONTENT)
def apagar(
    checkin: CheckinSemanal = Depends(checkin_permitido),
    sessao: Session = Depends(obter_sessao),
) -> None:
    sessao.delete(checkin)
    sessao.commit()


def _media_movel(pontos: list[PontoDaSerie], janela: int) -> list[PontoDaSerie]:
    """Média móvel simples, só a partir do ponto em que a janela está cheia.

    Começar antes disso desenharia uma tendência a partir de duas semanas, que
    é exatamente o ruído que a média existe para tirar.
    """
    if len(pontos) < janela:
        return []
    return [
        PontoDaSerie(
            semana=pontos[fim - 1].semana,
            valor=round(
                sum(p.valor for p in pontos[fim - janela : fim]) / janela, 2
            ),
        )
        for fim in range(janela, len(pontos) + 1)
    ]


@rotas.get("/alunos/{aluno_id}/evolucao", response_model=Evolucao)
def evolucao(
    aluno: Aluno = Depends(aluno_permitido),
    sessao: Session = Depends(obter_sessao),
    semanas: int = 26,
) -> Evolucao:
    """As séries prontas para o gráfico, já sem os buracos.

    Semana sem resposta some da série em vez de virar zero: o aluno que não
    pesou não pesa zero, e uma linha caindo até o eixo seria mentira.
    """
    limite = date.today() - timedelta(weeks=max(semanas, 1))
    checkins = list(
        sessao.scalars(
            select(CheckinSemanal)
            .where(CheckinSemanal.aluno_id == aluno.id)
            .where(CheckinSemanal.semana >= limite)
            .order_by(CheckinSemanal.semana)
        ).all()
    )

    series: list[SerieDoGrafico] = []
    variacao: dict[str, float] = {}

    for chave, rotulo, unidade in SERIES:
        pontos = [
            PontoDaSerie(semana=c.semana, valor=float(getattr(c, chave)))
            for c in checkins
            if getattr(c, chave) is not None
        ]
        if not pontos:
            continue

        series.append(
            SerieDoGrafico(
                chave=chave,
                rotulo=rotulo,
                unidade=unidade,
                pontos=pontos,
                tendencia=(
                    _media_movel(pontos, JANELA_DA_TENDENCIA)
                    if chave == "peso_kg"
                    else []
                ),
            )
        )
        if len(pontos) > 1:
            variacao[chave] = round(pontos[-1].valor - pontos[0].valor, 2)

    return Evolucao(
        aluno_id=aluno.id, semanas=semanas, series=series, variacao=variacao
    )
