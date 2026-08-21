"""Migrações de esquema.

`criar_tabelas()` só cria o que falta — serve enquanto o banco é descartável.
A partir do momento em que há histórico de treino de um aluno dentro, mudar
uma coluna precisa de um caminho de ida e volta, e é isso que o Alembic dá.
"""

from __future__ import annotations

from pathlib import Path

from alembic import command
from alembic.config import Config
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory

PASTA = Path(__file__).resolve().parent


def _engine():
    """Importada na hora, não no topo.

    `from jf.banco import engine` no import congelaria a engine, e testes que
    trocam o banco por um SQLite em memória migrariam o arquivo de verdade.
    """
    from jf.banco import engine

    return engine


def _configuracao(conexao=None) -> Config:
    configuracao = Config(str(PASTA / "alembic.ini"))
    configuracao.set_main_option("script_location", str(PASTA))
    if conexao is not None:
        # O `env.py` usa esta conexão em vez de abrir uma nova.
        configuracao.attributes["connection"] = conexao
    return configuracao


def revisao_aplicada() -> str | None:
    """A revisão que está no banco, ou `None` num banco ainda sem carimbo."""
    with _engine().connect() as conexao:
        return MigrationContext.configure(conexao).get_current_revision()


def revisao_mais_recente() -> str | None:
    return ScriptDirectory.from_config(_configuracao()).get_current_head()


def esta_atualizado() -> bool:
    return revisao_aplicada() == revisao_mais_recente()


def aplicar(conexao=None) -> None:
    """Leva o banco até a última revisão.

    Aceita uma conexão pronta para o caso do teste, que roda num banco em
    memória: abrir outra conexão daria um SQLite diferente e vazio.
    """
    if conexao is not None:
        command.upgrade(_configuracao(conexao), "head")
        return
    with _engine().begin() as aberta:
        command.upgrade(_configuracao(aberta), "head")


def carimbar(revisao: str = "head") -> None:
    """Marca o banco como já estando numa revisão, sem rodar nada.

    Para o banco que nasceu de `criar_tabelas()` antes das migrações
    existirem: as tabelas já estão lá, então rodar a primeira migração
    falharia com "table already exists".
    """
    with _engine().begin() as conexao:
        command.stamp(_configuracao(conexao), revisao)
