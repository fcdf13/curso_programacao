"""Roda o teste de um exercício e devolve um resultado já mastigado.

O pytest roda em subprocesso: se a sua resposta entrar em laço infinito, estourar a
recursão ou sujar o interpretador, quem morre é o subprocesso — não o CLI.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
import textwrap
from dataclasses import dataclass
from pathlib import Path

from curso import caminhos
from curso.registro import Exercicio

TEMPO_LIMITE_S = 60
RE_LINHA_DE_ERRO = re.compile(r"^E(.*)$")
RE_PREFIXO_EXCECAO = re.compile(r"^(?:\w+\.)*(\w*Erro\w*|\w*Error\w*|AssertionError):\s*")


@dataclass
class Resultado:
    ok: bool
    passaram: int
    falharam: int
    primeira_falha: str          # mensagem didática, pronta para exibir
    nome_da_falha: str           # qual teste falhou
    bruto: str                   # saída completa do pytest, para depuração
    dados: dict | None = None    # a mesma falha estruturada, para a interface web


def corrigir(exercicio: Exercicio, fonte: str | None = None) -> Resultado:
    """Executa o teste do exercício contra a resposta (ou o gabarito)."""
    teste = exercicio.caminho_teste
    if not teste.exists():
        raise FileNotFoundError(f"Exercício {exercicio.id} sem arquivo de teste: {teste}")

    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as arquivo:
        relatorio = Path(arquivo.name)

    ambiente = {
        **os.environ,
        "CURSO_RELATORIO": str(relatorio),
        "CURSO_FONTE": fonte or caminhos.fonte(),
        "CURSO_RAIZ": str(caminhos.raiz()),
        "PYTHONDONTWRITEBYTECODE": "1",
    }
    comando = [sys.executable, "-m", "pytest", str(teste),
               "-q", "--no-header", "-p", "no:cacheprovider", "--tb=long"]

    try:
        processo = subprocess.run(
            comando, cwd=caminhos.raiz(), env=ambiente,
            capture_output=True, text=True, timeout=TEMPO_LIMITE_S,
        )
        saida = processo.stdout + processo.stderr
    except subprocess.TimeoutExpired:
        relatorio.unlink(missing_ok=True)
        return Resultado(
            ok=False, passaram=0, falharam=1,
            primeira_falha=(
                f"Seu código passou de {TEMPO_LIMITE_S} segundos e foi interrompido.\n\n"
                "  Quase sempre é um laço que nunca termina: confira se a condição do\n"
                "  `while` chega a ficar falsa, ou se o contador é de fato incrementado."
            ),
            nome_da_falha="tempo esgotado",
            bruto="",
            dados={"tipo": "tempo_esgotado", "limite_s": TEMPO_LIMITE_S},
        )

    dados = {}
    if relatorio.exists():
        conteudo = relatorio.read_text(encoding="utf-8")
        relatorio.unlink(missing_ok=True)
        if conteudo.strip():
            dados = json.loads(conteudo)

    testes = dados.get("testes", [])
    passaram = sum(1 for t in testes if t["resultado"] == "passed")
    falhas = [t for t in testes if t["resultado"] == "failed"]

    if not testes and processo.returncode != 0:
        return Resultado(False, 0, 1, _erro_de_coleta(saida), "erro ao carregar o teste", saida)

    primeira = falhas[0] if falhas else None
    return Resultado(
        ok=not falhas and passaram > 0,
        passaram=passaram,
        falharam=len(falhas),
        primeira_falha=_extrair_mensagem(primeira["detalhe"]) if primeira else "",
        nome_da_falha=primeira["nome"] if primeira else "",
        bruto=saida,
        dados=primeira.get("dados") if primeira else None,
    )


def _extrair_mensagem(traceback_do_pytest: str) -> str:
    """Isola a mensagem da falha (as linhas 'E ...') e tira o prefixo da exceção.

    O pytest alinha o 'E' com a coluna do código-fonte, então o recuo depois dele
    varia. O dedent tira esse recuo comum e preserva a indentação da mensagem.
    """
    linhas = [
        casamento.group(1)
        for linha in traceback_do_pytest.splitlines()
        if (casamento := RE_LINHA_DE_ERRO.match(linha))
    ]
    if not linhas:
        return traceback_do_pytest.strip() or "O teste falhou, mas sem mensagem."

    linhas = textwrap.dedent("\n".join(linhas)).splitlines()
    linhas[0] = RE_PREFIXO_EXCECAO.sub("", linhas[0])
    while linhas and not linhas[-1].strip():
        linhas.pop()
    return "\n".join(linhas)


def _erro_de_coleta(saida: str) -> str:
    """O teste nem chegou a rodar — normalmente sintaxe ou import quebrado."""
    interessantes = [
        linha for linha in saida.splitlines()
        if linha.strip() and not linha.startswith(("=", "_", "platform", "rootdir", "plugins"))
    ]
    return (
        "O teste não chegou a rodar.\n\n"
        + "\n".join("    " + linha for linha in interessantes[-12:])
    )
