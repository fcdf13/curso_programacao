"""Revisão espaçada — o que faz o curso ser revisão *e* aprendizado ao mesmo tempo.

Variação do SM-2 (o algoritmo do Anki), adaptada para exercícios em vez de flashcards:
a "qualidade" da lembrança vem de quantas tentativas você levou para acertar.

    acertou de primeira   -> 5   (intervalo cresce forte)
    acertou na 2ª         -> 4
    acertou na 3ª         -> 3
    acertou depois disso  -> 2   (volta a aparecer amanhã)
    olhou a solução       -> 1

Sequência típica de quem acerta sempre de primeira:
    1 dia -> 3 dias -> 7 dias -> ~18 dias -> ~45 dias
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta

FACILIDADE_INICIAL = 2.5
FACILIDADE_MINIMA = 1.3
INTERVALO_MAXIMO_DIAS = 180


@dataclass(frozen=True)
class Agendamento:
    facilidade: float
    intervalo_dias: int
    proxima_revisao: date


def qualidade(tentativas: int, acertou: bool, viu_solucao: bool = False) -> int:
    """Traduz o desempenho no exercício para a nota 1-5 do SM-2."""
    if not acertou or viu_solucao:
        return 1
    return {1: 5, 2: 4, 3: 3}.get(tentativas, 2)


def agendar(
    nota: int,
    *,
    facilidade: float = FACILIDADE_INICIAL,
    intervalo_dias: int = 0,
    repeticoes: int = 0,
    hoje: date | None = None,
) -> tuple[Agendamento, int]:
    """Calcula o próximo agendamento. Devolve (agendamento, repeticoes_atualizadas)."""
    hoje = hoje or date.today()
    nota = max(1, min(5, int(nota)))

    if nota < 3:
        # Tropeçou: recomeça a escada, mas guarda a facilidade (penalizada).
        nova_facilidade = max(FACILIDADE_MINIMA, facilidade - 0.20)
        return Agendamento(nova_facilidade, 1, hoje + timedelta(days=1)), 0

    # Fórmula do SM-2 para o ajuste da facilidade.
    ajuste = 0.1 - (5 - nota) * (0.08 + (5 - nota) * 0.02)
    nova_facilidade = max(FACILIDADE_MINIMA, facilidade + ajuste)

    repeticoes += 1
    if repeticoes == 1:
        novo_intervalo = 1
    elif repeticoes == 2:
        novo_intervalo = 3
    else:
        novo_intervalo = round(intervalo_dias * nova_facilidade)

    novo_intervalo = max(1, min(INTERVALO_MAXIMO_DIAS, novo_intervalo))
    return Agendamento(nova_facilidade, novo_intervalo,
                       hoje + timedelta(days=novo_intervalo)), repeticoes
