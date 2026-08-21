"""Um banco novo em memória por teste, e clientes já autenticados."""

from __future__ import annotations

import os

# Precisa vir antes de importar `jf.*`: `jf.config` lê o ambiente no import, e
# `jf.banco` cria a engine a partir dele.
os.environ.setdefault("JF_BANCO", "sqlite://")
os.environ.setdefault("JF_CHAVE_SECRETA", "chave-de-teste-nao-usar-em-producao")

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import StaticPool, create_engine  # noqa: E402
from sqlalchemy.orm import sessionmaker  # noqa: E402

from jf import banco  # noqa: E402
from jf.auth import hash_de_senha  # noqa: E402
from jf.modelos import Aluno, Base, Papel, Usuario  # noqa: E402
from jf.servidor import criar_app  # noqa: E402

SENHA = "senha-de-teste-123"


@pytest.fixture
def sessao_de_banco(monkeypatch):
    """SQLite em memória, compartilhado entre as conexões do teste.

    `StaticPool` mantém uma conexão só; sem isso cada checkout do pool abriria
    um banco em memória diferente e vazio.
    """
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    fabrica = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

    monkeypatch.setattr(banco, "engine", engine)
    monkeypatch.setattr(banco, "Sessao", fabrica)

    def obter_sessao():
        sessao = fabrica()
        try:
            yield sessao
        finally:
            sessao.close()

    monkeypatch.setattr(banco, "obter_sessao", obter_sessao)

    with fabrica() as sessao:
        yield sessao


@pytest.fixture
def app(sessao_de_banco):
    from jf.banco import obter_sessao as original

    aplicacao = criar_app()
    # As rotas capturaram a função original em `Depends(obter_sessao)` no import;
    # o override do FastAPI é o que redireciona para o banco do teste.
    aplicacao.dependency_overrides[original] = lambda: sessao_de_banco
    return aplicacao


@pytest.fixture
def criar_usuario(sessao_de_banco):
    def criar(nome: str, email: str, papel: Papel) -> Usuario:
        usuario = Usuario(
            nome=nome, email=email, senha_hash=hash_de_senha(SENHA), papel=papel
        )
        sessao_de_banco.add(usuario)
        sessao_de_banco.commit()
        return usuario

    return criar


@pytest.fixture
def criar_aluno(sessao_de_banco, criar_usuario):
    def criar(nome: str, email: str, treinador: Usuario) -> Aluno:
        usuario = criar_usuario(nome, email, Papel.ALUNO)
        aluno = Aluno(usuario_id=usuario.id, treinador_id=treinador.id)
        sessao_de_banco.add(aluno)
        sessao_de_banco.commit()
        return aluno

    return criar


@pytest.fixture
def cliente(app):
    """Um cliente por chamada, para cada um ter seu próprio cookie de sessão."""

    def abrir(email: str | None = None, senha: str = SENHA) -> TestClient:
        cliente = TestClient(app)
        if email is not None:
            resposta = cliente.post("/api/entrar", json={"email": email, "senha": senha})
            assert resposta.status_code == 200, resposta.text
        return cliente

    return abrir
