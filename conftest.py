"""Configuração do pytest para o curso inteiro.

Duas coisas acontecem aqui:

1. A opção `--solucoes` faz a suíte carregar o gabarito em vez das suas respostas.
   É o portão de qualidade do repositório: `pytest --solucoes` prova que todo
   exercício tem uma solução oficial que passa no próprio teste.

2. Quando a variável CURSO_RELATORIO aponta para um arquivo, o resultado de cada
   teste é gravado ali em JSON — é assim que `curso check` mostra uma falha
   legível em vez do traceback cru do pytest.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

_resultados: list[dict] = []


def pytest_addoption(parser):
    parser.addoption(
        "--solucoes",
        action="store_true",
        default=False,
        help="Roda os testes contra solucoes/ em vez de respostas/.",
    )


def pytest_configure(config):
    if config.getoption("--solucoes"):
        os.environ["CURSO_FONTE"] = "solucoes"


def pytest_runtest_logreport(report):
    if report.when == "call" or (report.when in ("setup", "teardown") and report.failed):
        _resultados.append({
            "id": report.nodeid,
            "nome": report.nodeid.rsplit("::", 1)[-1],
            "resultado": report.outcome,
            "duracao": round(report.duration, 3),
            "detalhe": report.longreprtext if report.failed else "",
        })


def pytest_sessionfinish(session, exitstatus):
    destino = os.environ.get("CURSO_RELATORIO")
    if not destino:
        return
    Path(destino).write_text(
        json.dumps({"saida": int(exitstatus), "testes": _resultados},
                   ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
