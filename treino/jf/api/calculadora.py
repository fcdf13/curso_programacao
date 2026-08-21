"""A calculadora de carga — a ferramenta do João.

Ela não decide nada sozinha. Recebe uma série de referência (o que o aluno
levantou e por quantas repetições), devolve o 1RM estimado e a carga para cada
faixa de repetições, e o João escolhe a equação, vê as outras lado a lado e
decide o que prescrever. O paper entra na conta de 1RM; séries e volume
continuam sendo decisão dele.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from jf.auth import usuario_atual
from jf.banco import obter_sessao
from jf.esquemas import PedidoDeEstimativa, RespostaDaCalculadora, SugestaoDeCarga
from jf.forca import (
    CargaInvalida,
    Equacao,
    NOMES,
    estimar,
    estimar_1rm,
    tabela_de_cargas,
)
from jf.modelos import Exercicio, Tecnica, Usuario

rotas = APIRouter(prefix="/calculadora", tags=["calculadora"])

INCREMENTO_PADRAO = 2.5


@rotas.post("", response_model=RespostaDaCalculadora)
def calcular(
    pedido: PedidoDeEstimativa,
    _: Usuario = Depends(usuario_atual),
    sessao: Session = Depends(obter_sessao),
) -> RespostaDaCalculadora:
    incremento = INCREMENTO_PADRAO
    if pedido.exercicio_id is not None:
        exercicio = sessao.get(Exercicio, pedido.exercicio_id)
        if exercicio is None:
            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_CONTENT, "Exercício desconhecido."
            )
        incremento = exercicio.incremento_kg

    # Basta uma técnica que quebre a contagem de repetições para a leitura
    # deixar de valer: um cluster de 3×3 não é uma série de 9 reps corridas.
    distorce = False
    if pedido.tecnica_ids:
        distorce = bool(
            sessao.scalar(
                select(Tecnica.id)
                .where(Tecnica.id.in_(set(pedido.tecnica_ids)))
                .where(Tecnica.distorce_estimativa.is_(True))
                .limit(1)
            )
        )

    try:
        resultado = estimar(
            pedido.carga_kg,
            pedido.reps,
            pedido.equacao,
            rir=pedido.rir,
            tecnica_distorce=distorce,
        )
    except CargaInvalida as erro:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, str(erro)) from None

    # `estimar` pode ter trocado de equação (carga leve demais para a proposta);
    # a tabela precisa sair da mesma equação do 1RM, senão as duas discordam.
    tabela = tabela_de_cargas(resultado.um_rm, incremento, equacao=resultado.equacao)

    comparacao: dict[str, float] = {}
    for equacao in Equacao:
        try:
            comparacao[NOMES[equacao]] = round(
                estimar_1rm(pedido.carga_kg, pedido.reps, equacao), 1
            )
        except CargaInvalida:
            # Fora do domínio daquela equação: não entra na comparação em vez
            # de entrar com um número que não vale.
            continue

    return RespostaDaCalculadora(
        um_rm=round(resultado.um_rm, 1),
        equacao=resultado.equacao,
        nome_da_equacao=resultado.nome_da_equacao,
        confiavel=resultado.confiavel,
        ressalva=resultado.ressalva,
        incremento_kg=incremento,
        tabela=[
            SugestaoDeCarga(
                reps=s.reps,
                carga_kg=round(s.carga_kg, 1),
                carga_arredondada_kg=s.carga_arredondada_kg,
                percentual=round(s.percentual, 1),
            )
            for s in tabela
        ],
        comparacao=comparacao,
    )
