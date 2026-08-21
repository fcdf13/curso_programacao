"""Dados que acompanham o app: o catálogo de exercícios, por enquanto."""

from __future__ import annotations

import csv
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from jf.modelos import ConvencaoDeCarga, Exercicio

PASTA = Path(__file__).resolve().parent


def semear_exercicios(sessao: Session) -> tuple[int, int]:
    """Insere o catálogo, sem tocar no que já existe.

    Devolve `(inseridos, ja_existiam)`. É seguro rodar de novo: o João pode ter
    editado o incremento de carga de um exercício para bater com a academia
    dele, e reexecutar a semeadura não pode desfazer isso.
    """
    existentes = set(sessao.scalars(select(Exercicio.nome)).all())
    inseridos = 0

    with (PASTA / "exercicios.csv").open(encoding="utf-8", newline="") as arquivo:
        for linha in csv.DictReader(arquivo):
            if linha["nome"] in existentes:
                continue
            sessao.add(
                Exercicio(
                    nome=linha["nome"],
                    grupo_muscular=linha["grupo_muscular"],
                    equipamento=linha["equipamento"],
                    composto=linha["composto"] == "1",
                    convencao_de_carga=ConvencaoDeCarga(linha["convencao_de_carga"]),
                    incremento_kg=float(linha["incremento_kg"]),
                )
            )
            inseridos += 1

    sessao.commit()
    return inseridos, len(existentes)
