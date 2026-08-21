"""Lê a prescrição escrita à mão e devolve séries.

O João já escreve os treinos assim, num bloco de texto:

    Up set de 40 a 100kg
    10x100kg
    12x100kg cluster set

Obrigá-lo a preencher quatro campos por série seria trocar um formato que
funciona por um que dá mais trabalho. Então o app lê o formato dele.

Módulo puro: recebe texto e a lista de nomes de técnicas conhecidas, devolve
dados. Não conhece banco nem HTTP, e é testado linha a linha.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field

from jf.modelos import TipoDeSerie

# 12x50 a 92kg · 10x100kg · 8 x 109 · 12×22,5kg
#   grupo 1: repetições   2: carga inicial   3: carga final (rampa)   4: resto
_SERIE = re.compile(
    r"""^
    (?P<reps>\d{1,3})\s*[x×]\s*
    (?P<carga>\d+(?:[.,]\d+)?)
    (?:\s*(?:a|até|-|–|—|até)\s*(?P<ate>\d+(?:[.,]\d+)?))?
    \s*(?:kg|quilos?)?
    (?P<resto>.*)$
    """,
    re.IGNORECASE | re.VERBOSE,
)

# Up set de 40 a 100kg · Aquecimento 20 a 60kg · Up set 40-100
_RAMPA = re.compile(
    r"""^
    (?P<rotulo>up\s*-?\s*set|aquecimento|aquec\.?|back\s*-?\s*off|drop)\s*
    (?:de\s+)?
    (?P<carga>\d+(?:[.,]\d+)?)
    \s*(?:a|até|-|–|—)\s*
    (?P<ate>\d+(?:[.,]\d+)?)
    \s*(?:kg|quilos?)?
    (?P<resto>.*)$
    """,
    re.IGNORECASE | re.VERBOSE,
)

# Um rótulo de tipo grudado numa série normal: "10x100kg back off".
_ROTULOS = {
    "up set": TipoDeSerie.UP_SET,
    "upset": TipoDeSerie.UP_SET,
    "aquecimento": TipoDeSerie.AQUECIMENTO,
    "aquec": TipoDeSerie.AQUECIMENTO,
    "back off": TipoDeSerie.BACK_OFF,
    "backoff": TipoDeSerie.BACK_OFF,
    "drop": TipoDeSerie.BACK_OFF,
}


@dataclass
class LinhaLida:
    """Uma linha do texto, entendida ou não."""

    texto: str
    reps: int | None = None
    carga_kg: float | None = None
    carga_ate_kg: float | None = None
    tipo: TipoDeSerie = TipoDeSerie.VALIDA
    tecnicas: list[str] = field(default_factory=list)
    observacao: str | None = None
    erro: str | None = None

    @property
    def entendida(self) -> bool:
        return self.erro is None


def _sem_acento(texto: str) -> str:
    decomposto = unicodedata.normalize("NFKD", texto.lower())
    return "".join(c for c in decomposto if not unicodedata.combining(c))


def _numero(texto: str) -> float:
    """Aceita 22.5 e 22,5 — o João escreve com vírgula."""
    return float(texto.replace(",", "."))


def _achar_tipo(resto: str) -> tuple[TipoDeSerie | None, str]:
    """Tira um rótulo de tipo do resto da linha, se houver."""
    limpo = _sem_acento(resto).strip(" .·-–—")
    for rotulo, tipo in _ROTULOS.items():
        if limpo.startswith(rotulo):
            return tipo, resto.strip()[len(rotulo) :].strip(" .·-–—")
    return None, resto.strip(" .·-–—")


def _achar_tecnicas(resto: str, conhecidas: list[str]) -> tuple[list[str], str | None]:
    """Casa o resto da linha com o catálogo de técnicas.

    Procura da mais longa para a mais curta: sem isso "Cluster set" seria
    encontrado como "set" caso o catálogo tivesse as duas.
    """
    achadas: list[str] = []
    sobra = resto

    for nome in sorted(conhecidas, key=len, reverse=True):
        alvo = _sem_acento(nome)
        posicao = _sem_acento(sobra).find(alvo)
        if posicao >= 0:
            achadas.append(nome)
            sobra = (sobra[:posicao] + sobra[posicao + len(nome) :]).strip(" .,·-–—")

    sobra = sobra.strip(" .,·-–—")
    return achadas, sobra or None


def ler_linha(texto: str, tecnicas_conhecidas: list[str] | None = None) -> LinhaLida:
    """Entende uma linha só. Devolve o erro em vez de levantar exceção."""
    conhecidas = tecnicas_conhecidas or []
    linha = texto.strip().strip("•-–— \t")

    if not linha:
        return LinhaLida(texto=texto, erro="Linha vazia.")

    rampa = _RAMPA.match(linha)
    if rampa:
        rotulo = _sem_acento(rampa["rotulo"]).replace("-", " ").replace("  ", " ").strip()
        tipo = _ROTULOS.get(rotulo.replace(" ", ""), None) or _ROTULOS.get(
            rotulo, TipoDeSerie.UP_SET
        )
        achadas, sobra = _achar_tecnicas(rampa["resto"].strip(), conhecidas)
        return LinhaLida(
            texto=texto,
            reps=None,
            carga_kg=_numero(rampa["carga"]),
            carga_ate_kg=_numero(rampa["ate"]),
            tipo=tipo,
            tecnicas=achadas,
            observacao=sobra,
        )

    serie = _SERIE.match(linha)
    if serie:
        tipo, resto = _achar_tipo(serie["resto"])
        achadas, sobra = _achar_tecnicas(resto, conhecidas)
        return LinhaLida(
            texto=texto,
            reps=int(serie["reps"]),
            carga_kg=_numero(serie["carga"]),
            carga_ate_kg=_numero(serie["ate"]) if serie["ate"] else None,
            tipo=tipo or TipoDeSerie.VALIDA,
            tecnicas=achadas,
            observacao=sobra,
        )

    return LinhaLida(
        texto=texto,
        erro=(
            "Não entendi. Escreva no formato 12x50kg, 12x50 a 92kg ou "
            "Up set de 40 a 100kg."
        ),
    )


def ler(texto: str, tecnicas_conhecidas: list[str] | None = None) -> list[LinhaLida]:
    """Lê um bloco inteiro, uma linha por série.

    Devolve também as linhas que não entendeu, com o motivo — a tela mostra
    quais foram, em vez de descartá-las em silêncio.
    """
    return [
        ler_linha(linha, tecnicas_conhecidas)
        for linha in texto.splitlines()
        if linha.strip()
    ]
