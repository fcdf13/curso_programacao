"""Lê o protocolo alimentar escrito à mão.

O PDF do João tem formato regular o bastante para ser entendido:

    Carboidratos substituição
    Arroz branco: 200g
    Mandioca: 200g
    Pão francês: 2 unidades

    1° refeição café
    Ovos
    Pão francês
    (Azeite)
    Legumes a gosto

Obrigá-lo a recadastrar isso campo por campo seria trocar um formato que ele já
usa por um que dá mais trabalho — e o protocolo do Filipe tem quase quarenta
linhas.

Módulo puro: recebe texto, devolve dados. Não conhece banco nem HTTP.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field

# "Carboidratos substituição", "Proteínas substituição:", "Frutas:"
_CABECALHO_DE_GRUPO = re.compile(
    r"^(?P<nome>[^:]{3,60}?)\s*(?:substitui[çc][ãa]o)\s*:?\s*$", re.IGNORECASE
)

# "1° refeição café", "2º refeição almoço", "5° refeição ceia", "Refeição 3"
_CABECALHO_DE_REFEICAO = re.compile(
    r"^(?:(?P<numero>\d+)\s*[°ºª]?\s*)?refei[çc][ãa]o\s*(?P<nome>.*?)\s*:?\s*$",
    re.IGNORECASE,
)

# "Arroz branco: 200g", "Ovos:5 und", "Multi vitamínico: dose diária"
# O que vem depois dos dois-pontos nem sempre é número: em suplemento é texto
# livre ("dose diária"), e jogá-lo fora perderia a instrução inteira.
_ITEM = re.compile(r"^(?P<descricao>[^:]+?)\s*(?::\s*(?P<resto>.*))?$")

# "200g", "2 unidades", "5 und", "1 colher" — o começo do que vem depois.
_MEDIDA = re.compile(
    r"^(?P<quantidade>\d+(?:[.,]\d+)?)\s*(?P<unidade>[^\d\s][^\d]*?)?\s*$"
)

# "Doce leite(20g)": quantidade entre parênteses, sem dois-pontos.
_MEDIDA_ENTRE_PARENTESES = re.compile(
    r"^(?P<descricao>.+?)\s*\(\s*(?P<quantidade>\d+(?:[.,]\d+)?)\s*(?P<unidade>[^)\d]*?)\s*\)\s*$"
)

_SUPLEMENTOS = re.compile(r"^suplementos?\s*:?\s*$", re.IGNORECASE)

# Frase, não item: o protocolo do João fecha com "Só basta fazer o que é
# preciso!", que sem isto viraria um alimento da última refeição.
_FRASE = re.compile(r"[!?]\s*$")

_A_GOSTO = re.compile(r"\s*[àa]\s*gosto\s*$", re.IGNORECASE)


@dataclass
class ItemLido:
    descricao: str
    quantidade: float | None = None
    unidade: str | None = None
    # O que veio depois dos dois-pontos e não era número: "dose diária",
    # "tomar em jejum ao acordar".
    detalhe: str | None = None
    a_gosto: bool = False
    opcional: bool = False


@dataclass
class SecaoLida:
    tipo: str  # "grupo" | "refeicao" | "suplementos"
    nome: str
    itens: list[ItemLido] = field(default_factory=list)


@dataclass
class ProtocoloLido:
    grupos: list[SecaoLida] = field(default_factory=list)
    refeicoes: list[SecaoLida] = field(default_factory=list)
    suplementos: list[ItemLido] = field(default_factory=list)
    deficit_kcal: int | None = None
    nao_entendidas: list[str] = field(default_factory=list)


def _sem_acento(texto: str) -> str:
    decomposto = unicodedata.normalize("NFKD", texto.lower())
    return "".join(c for c in decomposto if not unicodedata.combining(c))


def _limpar(linha: str) -> str:
    """Tira marcador de lista e espaço. O PDF usa ●, - e — sem critério fixo."""
    return linha.strip().lstrip("●•-–—*+ \t").strip()


def _numero(texto: str) -> float:
    return float(texto.replace(",", "."))


def _maiuscula(texto: str) -> str:
    """Só a primeira letra. `.capitalize()` estragaria "Batata Doce"."""
    return texto[:1].upper() + texto[1:]


def _ler_item(linha: str) -> ItemLido | None:
    bruto = _limpar(linha)
    if not bruto or _FRASE.search(bruto):
        return None

    # "(Azeite)" e "(Berberina/500)": o parêntese é como o João marca o que é
    # opcional dentro da refeição. Parêntese aberto e não fechado é outra coisa
    # — uma anotação solta — e não vira item.
    opcional = bruto.startswith("(")
    if opcional:
        if not bruto.endswith(")"):
            return None
        bruto = bruto[1:-1].strip()

    a_gosto = bool(_A_GOSTO.search(bruto))
    if a_gosto:
        bruto = _A_GOSTO.sub("", bruto).strip()

    entre_parenteses = _MEDIDA_ENTRE_PARENTESES.match(bruto)
    if entre_parenteses:
        return ItemLido(
            descricao=_maiuscula(entre_parenteses["descricao"].strip(" .:-")),
            quantidade=_numero(entre_parenteses["quantidade"]),
            unidade=(entre_parenteses["unidade"] or "").strip() or None,
            a_gosto=a_gosto,
            opcional=opcional,
        )

    casou = _ITEM.match(bruto)
    if casou is None or not casou["descricao"].strip():
        return None

    quantidade = unidade = detalhe = None
    resto = (casou["resto"] or "").strip()
    if resto:
        medida = _MEDIDA.match(resto)
        if medida:
            quantidade = _numero(medida["quantidade"])
            unidade = (medida["unidade"] or "").strip(" .:-") or None
        else:
            detalhe = resto

    return ItemLido(
        descricao=_maiuscula(casou["descricao"].strip(" .:-")),
        quantidade=quantidade,
        unidade=unidade,
        detalhe=detalhe,
        a_gosto=a_gosto,
        opcional=opcional,
    )


def _deficit(linha: str) -> int | None:
    """"500 calorias total de déficit por dia" → 500."""
    if "deficit" not in _sem_acento(linha):
        return None
    numero = re.search(r"(\d{2,5})", linha)
    return int(numero.group(1)) if numero else None


def _cabecalho(linha: str) -> SecaoLida | None:
    limpa = _limpar(linha)
    if not limpa:
        return None

    if _SUPLEMENTOS.match(limpa):
        return SecaoLida(tipo="suplementos", nome="Suplementos")

    grupo = _CABECALHO_DE_GRUPO.match(limpa)
    if grupo:
        return SecaoLida(tipo="grupo", nome=_maiuscula(grupo["nome"].strip()))

    refeicao = _CABECALHO_DE_REFEICAO.match(limpa)
    if refeicao:
        numero = refeicao["numero"]
        nome = _maiuscula(refeicao["nome"].strip())
        rotulo = f"{numero}ª refeição" if numero else "Refeição"
        return SecaoLida(tipo="refeicao", nome=f"{rotulo} — {nome}" if nome else rotulo)

    # Linha que termina em dois-pontos sem nada depois é cabeçalho: "Frutas:",
    # "Gorduras:", "Carboidratos de baixo teor molecular:". Com algo depois —
    # "Multi vitamínico: dose diária" — é item, e o teste dos dois-pontos é o
    # que separa os dois casos sem precisar de uma lista fechada de nomes.
    if limpa.endswith(":") and len(limpa) <= 60:
        nome = limpa.rstrip(":").strip()
        if nome:
            return SecaoLida(tipo="grupo", nome=_maiuscula(nome))

    return None


def ler_protocolo(texto: str) -> ProtocoloLido:
    """Lê o protocolo inteiro e devolve o que entendeu — e o que não entendeu.

    Linha solta antes de qualquer cabeçalho volta em `nao_entendidas` em vez de
    ser jogada fora: a tela mostra o que ficou de fora para o João conferir.
    """
    lido = ProtocoloLido()
    atual: SecaoLida | None = None

    for linha in texto.splitlines():
        limpa = _limpar(linha)
        if not limpa or set(limpa) <= {"-", "—", "–", "_", "="}:
            continue

        deficit = _deficit(limpa)
        if deficit is not None:
            lido.deficit_kcal = deficit
            continue

        cabecalho = _cabecalho(limpa)
        if cabecalho is not None:
            atual = cabecalho
            if cabecalho.tipo == "grupo":
                lido.grupos.append(cabecalho)
            elif cabecalho.tipo == "refeicao":
                lido.refeicoes.append(cabecalho)
            continue

        item = _ler_item(limpa)
        if item is None:
            lido.nao_entendidas.append(linha.strip())
            continue

        if atual is None:
            lido.nao_entendidas.append(linha.strip())
        elif atual.tipo == "suplementos":
            lido.suplementos.append(item)
        else:
            atual.itens.append(item)

    # Cabeçalho sem nenhum item é ruído, não seção.
    lido.grupos = [g for g in lido.grupos if g.itens]
    lido.refeicoes = [r for r in lido.refeicoes if r.itens]
    return lido
