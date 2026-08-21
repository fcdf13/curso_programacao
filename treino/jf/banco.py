"""Ligação com o banco: engine, sessão e criação das tabelas."""

from __future__ import annotations

from collections.abc import Iterator

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from jf.config import config
from jf.modelos import Base


def _criar_engine(url: str) -> Engine:
    # `check_same_thread` só existe no SQLite; o pool do FastAPI usa threads.
    argumentos = {"check_same_thread": False} if url.startswith("sqlite") else {}
    return create_engine(url, connect_args=argumentos, future=True)


engine = _criar_engine(config.banco_url)
Sessao = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


@event.listens_for(Engine, "connect")
def _ligar_chaves_estrangeiras(conexao, _registro) -> None:
    """O SQLite ignora FOREIGN KEY a menos que a gente peça, conexão por conexão.

    Sem isto, `ondelete="CASCADE"` em `aluno.usuario_id` não faz nada e apagar
    um usuário deixa perfis órfãos apontando para um id que não existe mais.
    """
    if engine.dialect.name != "sqlite":
        return
    cursor = conexao.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def criar_tabelas() -> None:
    Base.metadata.create_all(engine)


def obter_sessao() -> Iterator[Session]:
    """Dependência do FastAPI: uma sessão por requisição, sempre fechada."""
    sessao = Sessao()
    try:
        yield sessao
    finally:
        sessao.close()
