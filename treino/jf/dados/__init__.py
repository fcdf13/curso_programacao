"""Dados que acompanham o app: o catálogo de exercícios e o de técnicas."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Callable, Iterable

from sqlalchemy import select
from sqlalchemy.orm import Session

from jf.modelos import Base, ConvencaoDeCarga, EscopoDaTecnica, Exercicio, Tecnica

PASTA = Path(__file__).resolve().parent


def _semear(
    sessao: Session,
    arquivo: str,
    modelo: type[Base],
    construir: Callable[[dict[str, str]], Base],
) -> tuple[int, int]:
    """Insere as linhas do CSV que ainda não existem, pelo nome.

    Nunca sobrescreve: o João pode ter ajustado o incremento de um exercício
    para bater com a academia dele, e reexecutar a semeadura não pode desfazer
    isso. Devolve `(inseridos, ja_existiam)`.
    """
    existentes = set(sessao.scalars(select(modelo.nome)).all())  # type: ignore[attr-defined]
    inseridos = 0

    with (PASTA / arquivo).open(encoding="utf-8", newline="") as entrada:
        for linha in csv.DictReader(entrada):
            if linha["nome"] in existentes:
                continue
            sessao.add(construir(linha))
            inseridos += 1

    sessao.commit()
    return inseridos, len(existentes)


def semear_exercicios(sessao: Session) -> tuple[int, int]:
    return _semear(
        sessao,
        "exercicios.csv",
        Exercicio,
        lambda linha: Exercicio(
            nome=linha["nome"],
            grupo_muscular=linha["grupo_muscular"],
            equipamento=linha["equipamento"],
            composto=linha["composto"] == "1",
            convencao_de_carga=ConvencaoDeCarga(linha["convencao_de_carga"]),
            incremento_kg=float(linha["incremento_kg"]),
        ),
    )


def semear_tecnicas(sessao: Session) -> tuple[int, int]:
    return _semear(
        sessao,
        "tecnicas.csv",
        Tecnica,
        lambda linha: Tecnica(
            nome=linha["nome"],
            escopo=EscopoDaTecnica(linha["escopo"]),
            descricao=linha["descricao"],
            distorce_estimativa=linha["distorce_estimativa"] == "1",
        ),
    )


def semear_tudo(sessao: Session) -> Iterable[tuple[str, int, int]]:
    yield ("exercícios", *semear_exercicios(sessao))
    yield ("técnicas", *semear_tecnicas(sessao))
