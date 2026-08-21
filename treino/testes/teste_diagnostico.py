"""O `jf doutor` — o que ele precisa pegar antes do app ir para a internet."""

from __future__ import annotations

import importlib

import pytest

from jf import config as modulo_de_config


def recarregar(monkeypatch, **ambiente):
    """Recarrega a configuração com um ambiente novo.

    `jf.config.config` é lido no import, então mexer só em `os.environ` não
    muda nada — o módulo precisa ser reconstruído.
    """
    for chave in ("JF_CHAVE_SECRETA", "JF_PRODUCAO", "JF_BANCO"):
        monkeypatch.delenv(chave, raising=False)
    for chave, valor in ambiente.items():
        monkeypatch.setenv(chave, valor)

    importlib.reload(modulo_de_config)
    diagnostico = importlib.reload(importlib.import_module("jf.diagnostico"))
    return diagnostico


def teste_producao_sem_chave_bloqueia(monkeypatch):
    diagnostico = recarregar(monkeypatch, JF_PRODUCAO="1")
    _, bloqueia = diagnostico.relatorio()
    assert bloqueia


def teste_a_chave_de_exemplo_bloqueia(monkeypatch):
    """Ela está escrita no repositório: quem lê o código assina um cookie."""
    diagnostico = recarregar(
        monkeypatch,
        JF_PRODUCAO="1",
        JF_CHAVE_SECRETA=modulo_de_config.__dict__.get("_", "")
        or "desenvolvimento-local-nao-usar-em-producao",
    )
    texto, bloqueia = diagnostico.relatorio()
    assert bloqueia
    assert "exemplo" in texto


def teste_desenvolvimento_sem_chave_e_so_aviso(monkeypatch):
    """Na máquina de quem desenvolve, chave efêmera é chata, não perigosa."""
    diagnostico = recarregar(monkeypatch)
    _, bloqueia = diagnostico.relatorio()
    assert not bloqueia


def teste_banco_em_memoria_bloqueia(monkeypatch):
    diagnostico = recarregar(
        monkeypatch,
        JF_PRODUCAO="1",
        JF_CHAVE_SECRETA="a" * 64,
        JF_BANCO="sqlite://",
    )
    texto, bloqueia = diagnostico.relatorio()
    assert bloqueia
    assert "memória" in texto


def teste_sqlite_fora_de_volume_avisa(monkeypatch):
    """O erro que só aparece no primeiro restart, com o histórico já dentro."""
    diagnostico = recarregar(
        monkeypatch,
        JF_PRODUCAO="1",
        JF_CHAVE_SECRETA="a" * 64,
        JF_BANCO="sqlite:////app/jf.db",
    )
    texto, bloqueia = diagnostico.relatorio()
    assert not bloqueia  # é aviso, não impedimento
    assert "restart" in texto


def teste_producao_bem_configurada_passa(monkeypatch):
    diagnostico = recarregar(
        monkeypatch,
        JF_PRODUCAO="1",
        JF_CHAVE_SECRETA="a" * 64,
        JF_BANCO="sqlite:////dados/jf.db",
    )
    texto, bloqueia = diagnostico.relatorio()
    assert not bloqueia
    assert "Nada impede subir" in texto


def teste_carregar_nunca_levanta(monkeypatch):
    """A configuração quebrada vira um campo, não uma exceção de import.

    Se `import jf.config` explodisse, o próprio `jf doutor` não rodaria — e ele
    é justamente a ferramenta para explicar o que está errado.
    """
    monkeypatch.setenv("JF_PRODUCAO", "1")
    monkeypatch.delenv("JF_CHAVE_SECRETA", raising=False)

    configuracao = modulo_de_config.carregar()
    assert configuracao.impedimento is not None
    with pytest.raises(RuntimeError):
        configuracao.exigir_que_sirva()


def teste_config_boa_nao_impede(monkeypatch):
    monkeypatch.setenv("JF_PRODUCAO", "1")
    monkeypatch.setenv("JF_CHAVE_SECRETA", "a" * 64)
    configuracao = modulo_de_config.carregar()
    assert configuracao.impedimento is None
    assert configuracao.cookie_seguro
    configuracao.exigir_que_sirva()


# ------------------------------------------------------------------ migrações


def teste_o_esquema_do_codigo_bate_com_as_migracoes(sessao_de_banco):
    """Modelo alterado sem migração nova é o erro que só aparece no deploy.

    O `autogenerate` compara os modelos com o banco migrado; se sobrar
    diferença, é porque alguém mexeu numa tabela e esqueceu a revisão.
    """
    from alembic.autogenerate import compare_metadata
    from alembic.migration import MigrationContext

    from jf.banco import engine
    from jf.migracoes import aplicar
    from jf.modelos import Base

    # `sessao_de_banco` já trocou a engine por um SQLite em memória vazio,
    # mas ele vem com as tabelas criadas por `create_all`; começamos limpos.
    Base.metadata.drop_all(engine)

    with engine.begin() as conexao:
        aplicar(conexao)
        contexto = MigrationContext.configure(conexao)
        diferencas = compare_metadata(contexto, Base.metadata)

    assert diferencas == [], (
        "O esquema do código não bate com as migrações. Gere uma revisão nova."
    )
