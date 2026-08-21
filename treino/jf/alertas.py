"""Os sinais que merecem a atenção do João primeiro.

Ele acompanha vários alunos, e a tela de "Alunos" em ordem alfabética esconde
quem precisa de atenção atrás de quem está indo bem. Aqui a régua é simples de
propósito — cada sinal é uma regra que dá para explicar numa frase — porque um
alerta que ninguém entende por que disparou é um alerta que se aprende a
ignorar.

Módulo puro: recebe o que já foi calculado (check-ins, tendência de peso, força
por exercício), devolve os alertas. Buscar o dado é trabalho da API.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

# Quantos dias sem check-in acendem o sinal. Uma semana perdida é normal
# (viagem, imprevisto); duas seguidas já é o tipo de silêncio que o João
# precisa saber que existe.
DIAS_SEM_CHECKIN = 10

HORAS_DE_SONO_BAIXAS = 6.0

# Pontos percentuais de queda na aderência entre um check-in e o anterior.
QUEDA_DE_ADERENCIA_PP = 15

# kg de subida na média móvel do peso, comparando o início e o fim da janela
# recente, para contar como "subindo" — não qualquer oscilação de água e sal.
SUBIDA_DE_PESO_KG = 0.5


@dataclass(frozen=True)
class Alerta:
    tipo: str
    # 3 = grave, 2 = atenção, 1 = a acompanhar. Decide a ordem dos cartões.
    gravidade: int
    mensagem: str


def sem_checkin(ultimo: date | None, hoje: date, limite_dias: int = DIAS_SEM_CHECKIN) -> Alerta | None:
    if ultimo is None:
        return Alerta("sem_checkin", 3, "Nunca fez check-in.")
    dias = (hoje - ultimo).days
    if dias < limite_dias:
        return None
    semanas = dias // 7
    return Alerta(
        "sem_checkin",
        3 if dias >= limite_dias * 2 else 2,
        f"Sem check-in há {semanas} semana(s)." if semanas >= 2 else f"Sem check-in há {dias} dias.",
    )


def sono_baixo(horas: float | None, minimo: float = HORAS_DE_SONO_BAIXAS) -> Alerta | None:
    if horas is None or horas >= minimo:
        return None
    return Alerta("sono_baixo", 2, f"Dormindo {horas:g} h no último check-in.")


def peso_subindo_no_corte(
    em_corte: bool, tendencia_kg: list[float], limite_kg: float = SUBIDA_DE_PESO_KG
) -> Alerta | None:
    """A tendência (média móvel), não o peso cru: ruído de água e sal não é sinal.

    Só dispara em déficit ativo — peso subindo é o resultado esperado fora de
    corte, e alertar sobre ele seria confundir o João à toa.
    """
    if not em_corte or len(tendencia_kg) < 2:
        return None
    subida = tendencia_kg[-1] - tendencia_kg[0]
    if subida < limite_kg:
        return None
    return Alerta(
        "peso_subindo",
        2,
        f"Peso subindo {subida:.1f} kg na tendência recente, em fase de déficit.",
    )


def forca_caindo(exercicio: str, e1rm_kg: list[float]) -> Alerta | None:
    """Duas quedas seguidas no mesmo exercício — um treino ruim não é sinal.

    A régua pede três pontos para não confundir "um dia fraco" com queda: se o
    segundo ponto já é menor que o primeiro, ainda pode ser variação do dia.
    """
    if len(e1rm_kg) < 3:
        return None
    ultimos = e1rm_kg[-3:]
    if not (ultimos[0] > ultimos[1] > ultimos[2]):
        return None
    queda = ultimos[0] - ultimos[2]
    return Alerta(
        "forca_caindo",
        2,
        f"{exercicio}: e1RM caindo há dois registros seguidos ({queda:.1f} kg).",
    )


def aderencia_caindo(
    atual: int | None, anterior: int | None, queda_minima: int = QUEDA_DE_ADERENCIA_PP
) -> Alerta | None:
    if atual is None or anterior is None:
        return None
    queda = anterior - atual
    if queda < queda_minima:
        return None
    return Alerta(
        "aderencia_caindo", 1, f"Aderência à dieta caiu {queda} pontos percentuais."
    )


def avaliar(
    *,
    hoje: date,
    ultimo_checkin: date | None,
    horas_de_sono: float | None,
    em_corte: bool,
    tendencia_de_peso_kg: list[float],
    forca_por_exercicio: dict[str, list[float]],
    aderencia_dieta_atual: int | None,
    aderencia_dieta_anterior: int | None,
) -> list[Alerta]:
    """Todos os sinais de um aluno, do mais grave para o mais leve."""
    candidatos = [
        sem_checkin(ultimo_checkin, hoje),
        sono_baixo(horas_de_sono),
        peso_subindo_no_corte(em_corte, tendencia_de_peso_kg),
        aderencia_caindo(aderencia_dieta_atual, aderencia_dieta_anterior),
        *(
            forca_caindo(exercicio, pontos)
            for exercicio, pontos in forca_por_exercicio.items()
        ),
    ]
    achados = [a for a in candidatos if a is not None]
    return sorted(achados, key=lambda a: (-a.gravidade, a.tipo))


def pontuacao(alertas: list[Alerta]) -> int:
    """Soma as gravidades — é a chave de ordenação dos cartões na lista."""
    return sum(a.gravidade for a in alertas)
