"""Importa uma tabela nutricional para o catálogo.

A TACO (NEPA/UNICAMP) é a referência brasileira, e o Open Food Facts cobre o
que vem com rótulo. Nenhuma das duas vem embutida aqui: **o catálogo nasce
vazio de propósito**. Chutar kcal e macro num app que alguém usa para cortar
peso não é aproximação, é dano — então o valor só entra vindo de uma tabela de
verdade, apontada por quem importa.

O que o módulo resolve é o formato: as versões em CSV da TACO que circulam não
combinam nos nomes das colunas, então a leitura casa por apelido em vez de
exigir um cabeçalho exato.
"""

from __future__ import annotations

import csv
import unicodedata
from dataclasses import dataclass
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from jf.modelos import Alimento

# Cada campo e os cabeçalhos que já apareceram apontando para ele.
APELIDOS: dict[str, tuple[str, ...]] = {
    "nome": (
        "nome",
        "alimento",
        "descricao",
        "description",
        "food",
        "name",
        "produto",
        "product_name",
    ),
    "marca": ("marca", "brand", "brands", "fabricante"),
    "codigo_de_barras": ("codigo_de_barras", "ean", "barcode", "code", "gtin"),
    "kcal_100g": ("energia_kcal", "kcal", "energia", "energy_kcal", "calorias", "energia kcal"),
    "proteina_100g": ("proteina", "proteina_g", "protein", "proteins", "proteinas"),
    "carboidrato_100g": (
        "carboidrato",
        "carboidratos",
        "carboidrato_g",
        "carbohydrates",
        "carbohydrate",
        "cho",
    ),
    "gordura_100g": (
        "lipideos",
        "lipidios",
        "lipideos_g",
        "gordura",
        "gorduras",
        "gordura_g",
        "fat",
    ),
    "fibra_100g": ("fibra", "fibra_alimentar", "fibras", "fiber", "fibra_g"),
}

# A TACO marca "Tr" para traço e "*"/"NA" para não analisado. Nenhum dos dois é
# zero: zero é uma afirmação, e "não medido" não afirma nada.
SEM_VALOR = {"", "tr", "traco", "na", "n/a", "*", "-", "nd"}

NUMEROS = ("kcal_100g", "proteina_100g", "carboidrato_100g", "gordura_100g", "fibra_100g")


@dataclass
class Resultado:
    lidas: int = 0
    novos: int = 0
    atualizados: int = 0
    ignoradas: int = 0
    colunas: dict[str, str] | None = None

    def __str__(self) -> str:
        return (
            f"{self.lidas} linha(s) lidas — {self.novos} novo(s), "
            f"{self.atualizados} atualizado(s), {self.ignoradas} sem nome ou sem dado."
        )


def _chave(texto: str) -> str:
    decomposto = unicodedata.normalize("NFKD", texto.strip().lower())
    limpo = "".join(c for c in decomposto if not unicodedata.combining(c))
    return "".join(c if c.isalnum() else "_" for c in limpo).strip("_")


def mapear_colunas(cabecalho: list[str]) -> dict[str, str]:
    """Descobre qual coluna do arquivo é qual campo. Sobra é ignorada."""
    encontrado: dict[str, str] = {}
    for coluna in cabecalho:
        chave = _chave(coluna)
        for campo, apelidos in APELIDOS.items():
            if campo in encontrado:
                continue
            if chave in {_chave(a) for a in apelidos} or chave.startswith(
                tuple(_chave(a) + "_" for a in apelidos)
            ):
                encontrado[campo] = coluna
                break
    return encontrado


def _numero(bruto: str | None) -> float | None:
    if bruto is None:
        return None
    texto = bruto.strip()
    if _chave(texto) in SEM_VALOR:
        return None
    try:
        return float(texto.replace(",", "."))
    except ValueError:
        return None


def importar(sessao: Session, caminho: Path | str, fonte: str = "taco") -> Resultado:
    """Lê o CSV e escreve no catálogo, atualizando o que já estava lá.

    A identidade é (nome, marca, fonte): reimportar a mesma tabela corrigida
    atualiza os valores em vez de criar um segundo "Arroz branco".
    """
    caminho = Path(caminho)
    resultado = Resultado()

    with caminho.open(encoding="utf-8-sig", newline="") as arquivo:
        leitor = csv.DictReader(arquivo)
        colunas = mapear_colunas(list(leitor.fieldnames or []))
        resultado.colunas = colunas

        if "nome" not in colunas:
            raise ValueError(
                "Não encontrei a coluna do nome do alimento. "
                f"Cabeçalhos aceitos: {', '.join(APELIDOS['nome'])}."
            )

        for linha in leitor:
            resultado.lidas += 1
            nome = (linha.get(colunas["nome"]) or "").strip()
            if not nome:
                resultado.ignoradas += 1
                continue

            valores = {
                campo: _numero(linha.get(colunas[campo]))
                for campo in NUMEROS
                if campo in colunas
            }
            # Linha sem nenhum número não acrescenta nada ao catálogo, e entraria
            # como um alimento cujos macros são todos desconhecidos.
            if not any(v is not None for v in valores.values()):
                resultado.ignoradas += 1
                continue

            marca = (linha.get(colunas.get("marca", "")) or "").strip() or None
            codigo = (linha.get(colunas.get("codigo_de_barras", "")) or "").strip() or None

            alimento = sessao.scalars(
                select(Alimento)
                .where(Alimento.nome == nome)
                .where(Alimento.marca.is_(marca) if marca is None else Alimento.marca == marca)
                .where(Alimento.fonte == fonte)
            ).first()

            if alimento is None:
                alimento = Alimento(nome=nome, marca=marca, fonte=fonte)
                sessao.add(alimento)
                resultado.novos += 1
            else:
                resultado.atualizados += 1

            alimento.codigo_de_barras = codigo
            for campo, valor in valores.items():
                setattr(alimento, campo, valor)

    sessao.commit()
    return resultado
