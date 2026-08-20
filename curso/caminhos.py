"""Localização das pastas do curso.

Três árvores paralelas guardam o mesmo exercício em papéis diferentes:

    exercicios/  o enunciado + o esqueleto da função (versionado, nunca editado por você)
    respostas/   a sua resolução (é aqui que você escreve)
    solucoes/    o gabarito comentado (só olhe depois de tentar)

`fonte()` decide de qual delas os testes carregam o código, o que permite rodar
a mesma suíte contra as suas respostas ou contra o gabarito (`pytest --solucoes`).
"""

from __future__ import annotations

import os
from pathlib import Path

EXERCICIOS = "exercicios"
RESPOSTAS = "respostas"
SOLUCOES = "solucoes"


def raiz() -> Path:
    """Pasta raiz do curso (a que contém `exercicios/`)."""
    if env := os.environ.get("CURSO_RAIZ"):
        return Path(env).resolve()

    # O pacote `curso` mora em <raiz>/curso quando instalado com `pip install -e .`
    candidato = Path(__file__).resolve().parent.parent
    if (candidato / EXERCICIOS).is_dir():
        return candidato

    # Instalação não-editável: procura subindo a partir do diretório atual.
    for pasta in [Path.cwd(), *Path.cwd().parents]:
        if (pasta / EXERCICIOS).is_dir() and (pasta / "curso").is_dir():
            return pasta

    raise RuntimeError(
        "Não encontrei a raiz do curso (a pasta que contém `exercicios/`).\n"
        "Rode os comandos de dentro do repositório, ou defina CURSO_RAIZ."
    )


def fonte() -> str:
    """De qual árvore os testes devem carregar o código: 'respostas' ou 'solucoes'."""
    escolha = os.environ.get("CURSO_FONTE", RESPOSTAS)
    if escolha not in (RESPOSTAS, SOLUCOES, EXERCICIOS):
        raise ValueError(f"CURSO_FONTE inválido: {escolha!r}")
    return escolha


def pasta_exercicios() -> Path:
    return raiz() / EXERCICIOS


def pasta_dados() -> Path:
    return raiz() / "dados"


def pasta_brutos() -> Path:
    return pasta_dados() / "brutos"


def banco_path() -> Path:
    return pasta_dados() / "loja.duckdb"


def pasta_estado() -> Path:
    """`.curso/` — progresso, histórico de respostas e arquivos temporários."""
    p = raiz() / ".curso"
    p.mkdir(exist_ok=True)
    return p


def relativo(caminho: Path) -> Path:
    """Caminho de um arquivo de exercício relativo a `exercicios/`."""
    return Path(caminho).resolve().relative_to(pasta_exercicios())


def em_arvore(caminho_exercicio: Path, arvore: str) -> Path:
    """Mesmo arquivo, na árvore `exercicios/`, `respostas/` ou `solucoes/`."""
    return raiz() / arvore / relativo(caminho_exercicio)
