"""O backup do banco, e a prova de que a cópia serve para restaurar.

Um backup que ninguém tenta restaurar é um arquivo, não um backup. O teste
central aqui abre a cópia e confere que os dados estão lá — e o de corrupção
confere que ela é consistente mesmo com escrita acontecendo durante a cópia,
que é a diferença entre a API do SQLite e um `cp`.
"""

from __future__ import annotations

import sqlite3
import threading
from datetime import timedelta

import pytest

from jf import backup


@pytest.fixture
def banco(tmp_path, monkeypatch):
    """Um SQLite de verdade em disco — backup não se testa em memória."""
    import dataclasses

    from jf import config as modulo
    from jf.config import config

    arquivo = tmp_path / "jf.db"
    con = sqlite3.connect(arquivo)
    con.executescript(
        "CREATE TABLE checkin (id INTEGER PRIMARY KEY, peso REAL);"
        "INSERT INTO checkin (peso) VALUES (86.4), (85.9), (85.1);"
    )
    con.commit()
    con.close()

    falso = dataclasses.replace(config, banco_url=f"sqlite:///{arquivo}")
    monkeypatch.setattr(modulo, "config", falso)
    monkeypatch.setattr(backup, "config", falso)
    return arquivo


def linhas(arquivo):
    con = sqlite3.connect(arquivo)
    try:
        return [tuple(linha) for linha in con.execute("SELECT id, peso FROM checkin")]
    finally:
        con.close()


# ----------------------------------------------------------------- copiar


def teste_a_copia_pode_ser_restaurada(banco, tmp_path):
    """O ponto do backup: abrir a cópia e achar o dado lá dentro."""
    destino = backup.copiar(tmp_path / "guardado" / "copia.db")

    assert destino.is_file()
    assert linhas(destino) == linhas(banco)
    assert linhas(destino)[0] == (1, 86.4)


def teste_copia_com_escrita_acontecendo(banco, tmp_path):
    """É isto que `cp` não garante: cópia consistente com o app escrevendo.

    Um `cp` no meio de uma transação produz um arquivo que parece bom e só se
    revela corrompido na hora de restaurar — a pior hora possível.
    """
    parar = threading.Event()

    def escrevendo():
        con = sqlite3.connect(banco)
        while not parar.is_set():
            con.execute("INSERT INTO checkin (peso) VALUES (84.0)")
            con.commit()
        con.close()

    escritor = threading.Thread(target=escrevendo, daemon=True)
    escritor.start()
    try:
        destino = backup.copiar(tmp_path / "copia.db")
    finally:
        parar.set()
        escritor.join(timeout=5)

    con = sqlite3.connect(destino)
    try:
        assert con.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
        # E o dado original continua lá, não só um arquivo íntegro e vazio.
        assert con.execute("SELECT COUNT(*) FROM checkin").fetchone()[0] >= 3
    finally:
        con.close()


def teste_nao_deixa_arquivo_pela_metade(banco, tmp_path, monkeypatch):
    """Cópia interrompida não pode virar um backup com cara de bom.

    Simula o disco enchendo no meio: `sqlite3.Connection` é um tipo em C e não
    aceita `setattr`, então o dublê entra no lugar do `connect`.
    """

    class ConexaoQueFalha:
        def __enter__(self):
            return self

        def __exit__(self, *_):
            return False

        def backup(self, *_):
            raise OSError("disco cheio")

    monkeypatch.setattr(
        backup.sqlite3, "connect", lambda *a, **k: ConexaoQueFalha(), raising=True
    )

    destino = tmp_path / "copia.db"
    with pytest.raises(OSError, match="disco cheio"):
        backup.copiar(destino)

    # Nem o arquivo final, nem o temporário: o que sobra é nada.
    assert not destino.exists()
    assert list(tmp_path.glob("*.parcial")) == []


def teste_postgres_e_recusado(banco, monkeypatch, tmp_path):
    import dataclasses

    from jf.config import config

    monkeypatch.setattr(
        backup,
        "config",
        dataclasses.replace(config, banco_url="postgresql+psycopg://x/y"),
    )
    with pytest.raises(ValueError, match="pg_dump"):
        backup.copiar(tmp_path / "copia.db")


# ------------------------------------------------------------------ poda


def teste_rodar_cria_copia_datada(banco, tmp_path):
    pasta = tmp_path / "backups"
    feito = backup.rodar(pasta)

    assert feito.parent == pasta
    assert feito.name.startswith("jf-") and feito.name.endswith("Z.db")
    assert backup.copias(pasta) == [feito]


def teste_a_poda_guarda_as_mais_novas(banco, tmp_path):
    """Sem poda o disco enche — um backup que derruba o banco que ele protege."""
    pasta = tmp_path / "backups"
    pasta.mkdir()
    for dia in range(1, 6):
        (pasta / f"jf-2026-08-0{dia}T120000Z.db").write_bytes(b"x")

    apagadas = backup.podar(pasta, manter=2)

    assert [p.name for p in apagadas] == [
        "jf-2026-08-01T120000Z.db",
        "jf-2026-08-02T120000Z.db",
        "jf-2026-08-03T120000Z.db",
    ]
    assert [p.name for p in backup.copias(pasta)] == [
        "jf-2026-08-04T120000Z.db",
        "jf-2026-08-05T120000Z.db",
    ]


def teste_poda_nao_toca_em_arquivo_alheio(banco, tmp_path):
    pasta = tmp_path / "backups"
    pasta.mkdir()
    (pasta / "jf-2026-08-01T120000Z.db").write_bytes(b"x")
    (pasta / "nao-e-backup.db").write_bytes(b"x")
    (pasta / "anotacoes.txt").write_bytes(b"x")

    backup.podar(pasta, manter=0)

    restantes = sorted(p.name for p in pasta.iterdir())
    # `manter=0` desliga a poda; e o que não segue o padrão nunca é candidato.
    assert restantes == ["anotacoes.txt", "jf-2026-08-01T120000Z.db", "nao-e-backup.db"]


def teste_idade_da_ultima_copia(banco, tmp_path):
    pasta = tmp_path / "backups"
    assert backup.idade(pasta) is None

    backup.rodar(pasta)
    desde = backup.idade(pasta)
    assert desde is not None and desde < timedelta(minutes=1)


# ----------------------------------------------------------- agendamento


def teste_sem_pasta_configurada_nao_agenda(banco, monkeypatch):
    monkeypatch.delenv("JF_BACKUP_PASTA", raising=False)
    assert backup.agendar() is None


def teste_agendar_copia_na_hora(banco, tmp_path, monkeypatch):
    """Um contêiner que reinicia todo dia nunca completaria um ciclo."""
    pasta = tmp_path / "backups"
    monkeypatch.setenv("JF_BACKUP_PASTA", str(pasta))

    parar = threading.Event()
    thread = backup.agendar(parar)
    assert thread is not None
    try:
        for _ in range(100):
            if backup.copias(pasta):
                break
            threading.Event().wait(0.05)
    finally:
        parar.set()
        thread.join(timeout=5)

    copias = backup.copias(pasta)
    assert len(copias) == 1
    assert linhas(copias[0]) == linhas(banco)


def teste_falha_no_backup_nao_derruba_o_laco(banco, tmp_path, monkeypatch, caplog):
    """Backup que falhou é ruim; o app fora do ar por causa dele é pior."""
    monkeypatch.setenv("JF_BACKUP_PASTA", str(tmp_path / "backups"))
    monkeypatch.setattr(
        backup, "rodar", lambda *a, **k: (_ for _ in ()).throw(OSError("disco cheio"))
    )

    parar = threading.Event()
    thread = backup.agendar(parar)
    assert thread is not None
    try:
        for _ in range(100):
            if "disco cheio" in caplog.text:
                break
            threading.Event().wait(0.05)
        assert thread.is_alive()
    finally:
        parar.set()
        thread.join(timeout=5)

    assert "disco cheio" in caplog.text


def teste_postgres_nao_agenda(banco, tmp_path, monkeypatch):
    import dataclasses

    from jf.config import config

    monkeypatch.setenv("JF_BACKUP_PASTA", str(tmp_path / "backups"))
    monkeypatch.setattr(
        backup,
        "config",
        dataclasses.replace(config, banco_url="postgresql+psycopg://x/y"),
    )
    assert backup.agendar() is None


# ------------------------------------------------------------- diagnóstico


def teste_o_doutor_avisa_quando_nao_ha_backup(banco, monkeypatch):
    import dataclasses

    from jf import diagnostico
    from jf.config import config

    monkeypatch.delenv("JF_BACKUP_PASTA", raising=False)
    monkeypatch.setattr(
        diagnostico, "config", dataclasses.replace(config, producao=True)
    )

    achado = diagnostico._backup()
    assert achado.nivel == "aviso"
    assert "JF_BACKUP_PASTA" in achado.detalhe


def teste_o_doutor_avisa_quando_a_copia_esta_velha(banco, tmp_path, monkeypatch):
    """Cópia velha é pior que nenhuma: passa a impressão de que há backup."""
    from jf import diagnostico

    pasta = tmp_path / "backups"
    pasta.mkdir()
    velha = pasta / "jf-2026-01-01T120000Z.db"
    velha.write_bytes(b"x")
    import os

    antigo = 1735732800  # 2025-01-01
    os.utime(velha, (antigo, antigo))

    monkeypatch.setenv("JF_BACKUP_PASTA", str(pasta))
    achado = diagnostico._backup()
    assert achado.nivel == "aviso"
    assert "dobro do intervalo" in achado.detalhe


def teste_o_doutor_fica_contente_com_backup_recente(banco, tmp_path, monkeypatch):
    from jf import diagnostico

    pasta = tmp_path / "backups"
    monkeypatch.setenv("JF_BACKUP_PASTA", str(pasta))
    backup.rodar(pasta)

    achado = diagnostico._backup()
    assert achado.nivel == "ok"
    assert "1 cópia(s)" in achado.detalhe
