"""A força do aluno ao longo do tempo, a partir do que ele levantou.

O e1RM é o que fecha o ciclo da calculadora: sem saber o que o aluno fez de
verdade, a carga sugerida sai de um número que o João digitou de memória. Com as
séries registradas, ela sai do treino da semana passada.

Módulo puro: recebe registros, devolve pontos. Não conhece banco nem HTTP — o
que permite testá-lo contra números escritos à mão, que é como se confere uma
conta.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from jf.forca import Equacao, estimar

# Quantas repetições ainda dizem alguma coisa sobre força máxima. Acima disso a
# série mede resistência, e a estimativa vira uma extrapolação longa demais para
# entrar num gráfico de evolução sem enganar.
REPS_MAXIMAS_PARA_E1RM = 15


@dataclass(frozen=True)
class Registro:
    """Uma série executada, no mínimo que a conta precisa."""

    dia: date
    reps: int
    carga_kg: float
    rir: int | None = None
    distorce: bool = False


@dataclass(frozen=True)
class PontoDeForca:
    dia: date
    e1rm: float
    # De qual série saiu — o gráfico mostra "86 kg (8 × 70)" em vez de um número
    # solto, e assim dá para conferir se a estimativa faz sentido.
    reps: int
    carga_kg: float
    confiavel: bool
    ressalva: str | None


def _serve(registro: Registro) -> bool:
    if registro.distorce:
        return False
    if registro.reps < 1 or registro.reps > REPS_MAXIMAS_PARA_E1RM:
        return False
    return registro.carga_kg > 0


def melhor_do_dia(
    registros: list[Registro], equacao: Equacao = Equacao.PROPOSTA
) -> list[PontoDeForca]:
    """Um ponto por dia: a **melhor** estimativa daquele treino.

    A melhor, e não a média, porque a pergunta é "quanto ele consegue" — e a
    série mais fraca do dia não responde isso. Somar as séries seria medir
    volume, que é outro gráfico.
    """
    por_dia: dict[date, PontoDeForca] = {}

    for registro in registros:
        if not _serve(registro):
            continue

        estimativa = estimar(
            registro.carga_kg,
            registro.reps,
            equacao=equacao,
            rir=registro.rir,
            tecnica_distorce=registro.distorce,
        )
        ponto = PontoDeForca(
            dia=registro.dia,
            e1rm=round(estimativa.um_rm, 1),
            reps=registro.reps,
            carga_kg=registro.carga_kg,
            confiavel=estimativa.confiavel,
            ressalva=estimativa.ressalva,
        )

        atual = por_dia.get(registro.dia)
        # Estimativa confiável ganha de estimativa alta: um número tirado de uma
        # série com 5 de reserva não pode virar o recorde do dia.
        if atual is None or _melhor(ponto, atual):
            por_dia[registro.dia] = ponto

    return [por_dia[dia] for dia in sorted(por_dia)]


def _melhor(novo: PontoDeForca, atual: PontoDeForca) -> bool:
    if novo.confiavel != atual.confiavel:
        return novo.confiavel
    return novo.e1rm > atual.e1rm


def variacao(pontos: list[PontoDeForca]) -> float | None:
    """Quanto mudou entre o primeiro e o último ponto, em kg."""
    if len(pontos) < 2:
        return None
    return round(pontos[-1].e1rm - pontos[0].e1rm, 1)


def atual(pontos: list[PontoDeForca]) -> PontoDeForca | None:
    return pontos[-1] if pontos else None
