"""Estimativa de 1RM e cálculo de carga.

Módulo puro: recebe números, devolve números, não conhece banco nem HTTP. É o
que permite conferi-lo contra o paper em `testes/teste_forca.py`.

A equação principal é a de Marzagão (2026), *A Weight-Dependent 1RM Prediction
Equation Optimized on 303,494 Near-Failure Sets Across 388 Exercises*,
arXiv:2603.17495v1. A ideia dela é que o fator de conversão entre repetições e
1RM não é constante — ele cresce com a carga. Nas equações clássicas ele é fixo
(30 no Epley, ≈36 no Brzycki), e é aí que elas erram, sobretudo nos exercícios
leves.

As clássicas ficam disponíveis lado a lado de propósito: o João pode comparar, e
comparar é o argumento de por que a proposta é melhor.
"""

from __future__ import annotations

import enum
import math
from dataclasses import dataclass

# ---------------------------------------------------------------- constantes

# Coeficientes publicados. `w` em QUILOS: o paper fixa w₀ = 1 kg e observa que
# em libras o intercepto `a` deslocaria em b × ln(2,205) ≈ 3,61. Trocar a
# unidade sem trocar `A` produz número errado sem quebrar nada.
A = -2.55
B = 4.58
ALFA = 0.85

# Guard do próprio paper, não defesa nossa: sem ele o denominador zera em
# w ≈ 1,74 kg. Na amostra do autor ativa em 0,06% das séries, todas abaixo de 2 kg.
K_MINIMO = 0.5

# Abaixo desta carga a equação proposta deixa de fazer sentido, e o guard do
# paper não cobre isso.
#
# Derivando 1RM = w × (1 + C/k(w)) em w, com C = (r−1)^α e k = a + b·ln(w):
#
#     d(1RM)/dw = 1 + C × (k − b) / k²
#
# que é garantidamente positiva só quando k(w) ≥ b. Abaixo disso a estimativa
# *cai* conforme a carga sobe: 2 kg por 8 reps devolve 18,7 kg de 1RM, e 3 kg
# pelas mesmas 8 reps devolve 9,3 kg. Não é um detalhe numérico — é a equação
# invertendo de sentido, e quebraria a bisseção de `carga_para` junto.
#
# k(w) = b em w = e^((b−a)/b) ≈ 4,74 kg. Cargas assim existem de verdade
# (elevação lateral com halter de 3 kg), então o app não ignora o caso: cai
# para Epley, que é monótona em todo o domínio, e diz que caiu.
CARGA_MINIMA_PROPOSTA = math.exp((B - A) / B)

# Acima disso a precisão de toda equação de 1RM cai — achado consistente na
# literatura revisada pelo paper (Reynolds et al., 2006; Mayhew et al., 2008).
REPS_CONFIAVEIS = 10

# O paper calibrou em séries perto da falha. Série com reserva grande enviesa a
# estimativa para baixo, então ela não entra no acompanhamento de e1RM.
RIR_MAXIMO_CONFIAVEL = 2

REPS_MAXIMAS = 30


class Equacao(str, enum.Enum):
    PROPOSTA = "proposta"
    EPLEY = "epley"
    BRZYCKI = "brzycki"


NOMES = {
    Equacao.PROPOSTA: "Marzagão (2026)",
    Equacao.EPLEY: "Epley (1985)",
    Equacao.BRZYCKI: "Brzycki (1993)",
}


class CargaInvalida(ValueError):
    """Entrada fora do domínio em que qualquer estimativa faria sentido."""


class ForaDoDominio(CargaInvalida):
    """A entrada é legítima, mas não para *esta* equação.

    Separada de `CargaInvalida` porque a resposta é diferente: entrada inválida
    é erro de quem chamou, isto aqui é motivo para trocar de equação.
    """


# ------------------------------------------------------------------ equações


def fator_de_conversao(carga_kg: float) -> float:
    """O `k(w)` do paper: quanto cada repetição extra vale em termos de 1RM.

    Menor significa que cada rep "vale mais". Cresce com a carga, o que é a
    inovação da equação — em 12 kg dá ≈ 8,8; em 100 kg, ≈ 18,5.
    """
    return max(K_MINIMO, A + B * math.log(carga_kg))


def _conferir(carga_kg: float, reps: int) -> None:
    if carga_kg <= 0:
        raise CargaInvalida("A carga precisa ser maior que zero.")
    if reps < 1:
        raise CargaInvalida("A série precisa ter pelo menos uma repetição.")
    if reps > REPS_MAXIMAS:
        raise CargaInvalida(
            f"Acima de {REPS_MAXIMAS} repetições nenhuma equação de 1RM se sustenta."
        )


def estimar_1rm(carga_kg: float, reps: int, equacao: Equacao = Equacao.PROPOSTA) -> float:
    """Estima o 1RM a partir de uma série levada perto da falha.

    Com `reps = 1` toda equação devolve a própria carga, por construção.
    """
    _conferir(carga_kg, reps)

    if reps == 1:
        return carga_kg

    if equacao is Equacao.PROPOSTA:
        if carga_kg < CARGA_MINIMA_PROPOSTA:
            raise ForaDoDominio(
                f"A equação proposta só é monótona a partir de "
                f"{CARGA_MINIMA_PROPOSTA:.1f} kg; abaixo disso ela inverte de "
                f"sentido. Use Epley para cargas leves."
            )
        return carga_kg * (1 + (reps - 1) ** ALFA / fator_de_conversao(carga_kg))

    if equacao is Equacao.EPLEY:
        return carga_kg * (1 + reps / 30)

    # Brzycki zera o denominador em 37 reps; `REPS_MAXIMAS` já barra antes.
    return carga_kg / (1.0278 - 0.0278 * reps)


def carga_para(
    alvo_1rm: float, reps: int, equacao: Equacao = Equacao.PROPOSTA
) -> float:
    """A carga que, levada a `reps` perto da falha, corresponde a `alvo_1rm`.

    É a inversão de `estimar_1rm`. Na equação proposta ela não tem forma
    fechada: `k` depende de `w`, então `w` aparece dos dois lados. Como
    `estimar_1rm` é monótona crescente em `w`, bisseção resolve — e resolve
    igual para as três equações, o que evita manter três inversões diferentes.
    """
    if alvo_1rm <= 0:
        raise CargaInvalida("O 1RM alvo precisa ser maior que zero.")
    _conferir(alvo_1rm, reps)

    if reps == 1:
        return alvo_1rm

    # `estimar_1rm(w, r) >= w` sempre, então a resposta nunca passa do alvo.
    # O piso é onde a equação começa a ser monótona — fora dele a bisseção
    # poderia convergir para a raiz errada em vez de falhar.
    baixo = CARGA_MINIMA_PROPOSTA if equacao is Equacao.PROPOSTA else 1e-4
    alto = alvo_1rm

    if baixo >= alto or estimar_1rm(baixo, reps, equacao) > alvo_1rm:
        raise ForaDoDominio(
            f"Um 1RM de {alvo_1rm:.1f} kg em {reps} repetições cai numa carga "
            f"abaixo do domínio de {NOMES[equacao]}."
        )

    for _ in range(200):
        meio = (baixo + alto) / 2
        if estimar_1rm(meio, reps, equacao) < alvo_1rm:
            baixo = meio
        else:
            alto = meio
    return (baixo + alto) / 2


def arredondar_para_anilha(carga_kg: float, incremento_kg: float) -> float:
    """Arredonda para o que existe na academia.

    Uma sugestão de 63,7 kg é inútil: o rack tem 60 ou 65. O incremento vem do
    exercício (2,5 kg numa barra, 2 kg num rack de halteres, 5 kg numa máquina
    de pino) e o João edita por exercício quando a academia dele é diferente.
    """
    if incremento_kg <= 0:
        raise CargaInvalida("O incremento precisa ser maior que zero.")
    passos = round(carga_kg / incremento_kg)
    # Nunca devolve zero: arredondar 1 kg para baixo num incremento de 2,5
    # sugeriria treinar com a barra vazia.
    return max(passos, 1) * incremento_kg


def percentual_do_1rm(carga_kg: float, um_rm: float) -> float:
    if um_rm <= 0:
        raise CargaInvalida("O 1RM precisa ser maior que zero.")
    return 100 * carga_kg / um_rm


# -------------------------------------------------------------------- volume


def tonelagem(series: int, reps: int, carga_kg: float) -> float:
    """Volume da prescrição, em quilos movidos: séries × reps × carga.

    Responde uma pergunta diferente do 1RM, e as duas não se substituem.
    Tonelagem mede *quanto trabalho* foi feito; e1RM mede *quão forte* a pessoa
    está. Três séries de 15 com carga leve batem em tonelagem uma série pesada
    de 3 e não dizem nada sobre força máxima.
    """
    if series < 0 or reps < 0 or carga_kg < 0:
        raise CargaInvalida("Séries, repetições e carga não podem ser negativos.")
    return series * reps * carga_kg


# ------------------------------------------------------------------ leituras


@dataclass(frozen=True)
class Estimativa:
    """O resultado com a ressalva junto, para a ressalva não se perder."""

    um_rm: float
    equacao: Equacao
    confiavel: bool
    ressalva: str | None

    @property
    def nome_da_equacao(self) -> str:
        return NOMES[self.equacao]


def estimar(
    carga_kg: float,
    reps: int,
    equacao: Equacao = Equacao.PROPOSTA,
    rir: int | None = None,
    tecnica_distorce: bool = False,
) -> Estimativa:
    """`estimar_1rm` com o julgamento sobre o quanto confiar no número.

    Três coisas derrubam a confiança, e o app precisa mostrar qual delas foi:
    repetições demais, reserva demais, e técnica que muda o que "uma série"
    significa — um cluster de 3×3 não é uma série de 9 reps, e tratá-lo como
    tal subestima o 1RM de forma grosseira.
    """
    trocou_de_equacao = False
    try:
        um_rm = estimar_1rm(carga_kg, reps, equacao)
    except ForaDoDominio:
        # Carga leve demais para a proposta. Epley é monótona em todo o
        # domínio, então serve — mas a troca precisa aparecer, nunca ser calada.
        equacao = Equacao.EPLEY
        um_rm = estimar_1rm(carga_kg, reps, equacao)
        trocou_de_equacao = True

    if trocou_de_equacao:
        ressalva = (
            f"Abaixo de {CARGA_MINIMA_PROPOSTA:.1f} kg a equação proposta inverte "
            f"de sentido, então esta estimativa saiu de {NOMES[Equacao.EPLEY]}."
        )
    elif tecnica_distorce:
        ressalva = (
            "A técnica usada muda o que uma série significa; a estimativa não "
            "vale para comparação."
        )
    elif rir is not None and rir > RIR_MAXIMO_CONFIAVEL:
        ressalva = (
            f"Série com {rir} repetições de reserva. A equação foi calibrada perto "
            "da falha, então o 1RM real é maior que este."
        )
    elif reps > REPS_CONFIAVEIS:
        ressalva = (
            f"Acima de {REPS_CONFIAVEIS} repetições a precisão cai em qualquer equação."
        )
    else:
        ressalva = None

    return Estimativa(
        um_rm=um_rm, equacao=equacao, confiavel=ressalva is None, ressalva=ressalva
    )


@dataclass(frozen=True)
class Sugestao:
    reps: int
    carga_kg: float
    carga_arredondada_kg: float
    percentual: float


def tabela_de_cargas(
    um_rm: float,
    incremento_kg: float,
    reps: tuple[int, ...] = (1, 3, 5, 6, 8, 10, 12, 15),
    equacao: Equacao = Equacao.PROPOSTA,
) -> list[Sugestao]:
    """Que carga usar para cada faixa de repetições, dado um 1RM.

    O percentual devolvido é a saída mais útil da tabela: ele *não* é fixo por
    número de reps, como manda a tabela impressa. Dez repetições numa rosca de
    13 kg são 59% do 1RM; num supino de 86 kg, 73%. A mesma tabela não pode
    estar certa para os dois, e é exatamente isso que o `k(w)` corrige.
    """
    sugestoes = []
    for r in reps:
        try:
            carga = carga_para(um_rm, r, equacao)
        except ForaDoDominio:
            # Num exercício muito leve as faixas altas de repetição saem do
            # domínio da proposta. Some a linha em vez de inventar um número.
            continue
        sugestoes.append(
            Sugestao(
                reps=r,
                carga_kg=carga,
                carga_arredondada_kg=arredondar_para_anilha(carga, incremento_kg),
                percentual=percentual_do_1rm(carga, um_rm),
            )
        )
    return sugestoes
