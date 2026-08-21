"""Ambiente do Alembic.

A URL do banco vem de `jf.config`, nunca do `alembic.ini`: com a URL escrita
nos dois lugares, migrar o banco errado é questão de tempo.
"""

from __future__ import annotations

from alembic import context
from sqlalchemy import engine_from_config, pool

from jf.config import config as configuracao_do_app
from jf.modelos import Base

configuracao = context.config
if configuracao.attributes.get("connection") is None:
    configuracao.set_main_option("sqlalchemy.url", configuracao_do_app.banco_url)

# O `autogenerate` compara o banco com isto.
target_metadata = Base.metadata


def migrar_offline() -> None:
    """Gera o SQL sem conectar — útil para revisar antes de aplicar."""
    context.configure(
        url=configuracao_do_app.banco_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def migrar_online() -> None:
    conexao_existente = configuracao.attributes.get("connection")

    if conexao_existente is not None:
        _rodar(conexao_existente)
        return

    engine = engine_from_config(
        configuracao.get_section(configuracao.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with engine.connect() as conexao:
        _rodar(conexao)


def _rodar(conexao) -> None:
    context.configure(
        connection=conexao,
        target_metadata=target_metadata,
        # O SQLite não sabe ALTER TABLE de verdade; o modo batch recria a
        # tabela por baixo. Sem isso, qualquer alteração de coluna falha.
        render_as_batch=True,
    )
    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    migrar_offline()
else:
    migrar_online()
