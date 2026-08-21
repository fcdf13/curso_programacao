"""Cópia do banco, feita sozinha.

O histórico de treino de um atleta não tem como ser recriado: se o arquivo se
perder, não existe "refazer" — as cargas de seis meses atrás simplesmente não
estão em lugar nenhum. Um `jf backup` que depende de alguém lembrar de rodar é
um backup que não existe.

Não há cron dentro do contêiner, então quem agenda é o próprio processo do
servidor. Uma thread que dorme e copia é modesta o bastante para não ter como
falhar de forma interessante — e uma falha dela **nunca** derruba o app: um
backup que não saiu é ruim, o app fora do ar por causa disso é pior.
"""

from __future__ import annotations

import logging
import os
import sqlite3
import threading
from datetime import datetime, timedelta, timezone
from pathlib import Path

from jf.config import config

registro = logging.getLogger("jf.backup")

# Nome ordenável e sem ambiguidade de fuso: comparar por nome é comparar por
# data, que é o que a retenção precisa.
FORMATO = "jf-%Y-%m-%dT%H%M%SZ.db"
PADRAO = "jf-*.db"

HORAS_PADRAO = 24
MANTER_PADRAO = 14


def caminho_do_banco() -> Path | None:
    """O arquivo SQLite, ou `None` quando o banco não é SQLite."""
    url = config.banco_url
    if not url.startswith("sqlite"):
        return None
    caminho = url.replace("sqlite:///", "").replace("sqlite://", "")
    return Path(caminho) if caminho else None


def copiar(destino: Path) -> Path:
    """Cópia consistente, com o app escrevendo.

    Usa a API de backup do próprio SQLite: `cp` durante uma escrita produz um
    arquivo que parece bom e só se revela corrompido na hora de restaurar —
    que é a pior hora possível para descobrir.

    Escreve num nome temporário e renomeia no fim. Rename é atômico dentro do
    mesmo sistema de arquivos, então um processo morto no meio da cópia deixa
    lixo reconhecível em vez de um backup pela metade com cara de bom.
    """
    origem = caminho_do_banco()
    if origem is None:
        raise ValueError("Este backup é do SQLite. Em Postgres, use `pg_dump`.")
    if not origem.is_file():
        raise FileNotFoundError(f"Não encontrei o banco em {origem}.")

    destino.parent.mkdir(parents=True, exist_ok=True)
    parcial = destino.with_suffix(destino.suffix + ".parcial")

    try:
        with sqlite3.connect(origem) as de, sqlite3.connect(parcial) as para:
            de.backup(para)
        parcial.replace(destino)
    except BaseException:
        parcial.unlink(missing_ok=True)
        raise

    return destino


def copias(pasta: Path) -> list[Path]:
    """Da mais antiga para a mais nova."""
    return sorted(pasta.glob(PADRAO))


def podar(pasta: Path, manter: int) -> list[Path]:
    """Apaga as cópias mais antigas, devolvendo o que saiu.

    Sem isto o disco enche e o app para de escrever — um backup que derruba o
    banco que ele protege.
    """
    existentes = copias(pasta)
    if manter <= 0 or len(existentes) <= manter:
        return []

    apagadas = existentes[: len(existentes) - manter]
    for velha in apagadas:
        velha.unlink(missing_ok=True)
    return apagadas


def rodar(pasta: Path, manter: int = MANTER_PADRAO) -> Path:
    """Uma cópia datada dentro da pasta, mais a poda."""
    destino = pasta / datetime.now(timezone.utc).strftime(FORMATO)
    copiar(destino)
    podar(pasta, manter)
    return destino


def idade(pasta: Path) -> timedelta | None:
    """Há quanto tempo saiu a cópia mais recente. `None` se não há nenhuma."""
    existentes = copias(pasta)
    if not existentes:
        return None
    quando = datetime.fromtimestamp(existentes[-1].stat().st_mtime, timezone.utc)
    return datetime.now(timezone.utc) - quando


# ------------------------------------------------------------- agendamento


def _inteiro(nome: str, padrao: int) -> int:
    try:
        valor = int(os.environ.get(nome, ""))
    except ValueError:
        return padrao
    return valor if valor > 0 else padrao


def pasta_configurada() -> Path | None:
    destino = os.environ.get("JF_BACKUP_PASTA", "").strip()
    return Path(destino) if destino else None


def intervalo() -> timedelta:
    return timedelta(hours=_inteiro("JF_BACKUP_HORAS", HORAS_PADRAO))


def quantas_manter() -> int:
    return _inteiro("JF_BACKUP_MANTER", MANTER_PADRAO)


def agendar(parar: threading.Event | None = None) -> threading.Thread | None:
    """Liga o backup periódico, se `JF_BACKUP_PASTA` estiver definida.

    Copia na hora quando a última cópia já passou do intervalo — um contêiner
    que reinicia todo dia, de outra forma, nunca chegaria a completar um ciclo
    e nunca faria backup nenhum.
    """
    pasta = pasta_configurada()
    if pasta is None:
        return None

    if caminho_do_banco() is None:
        registro.warning(
            "JF_BACKUP_PASTA está definida, mas o banco não é SQLite. "
            "Use as ferramentas do seu banco (pg_dump) — nada será copiado."
        )
        return None

    espera = intervalo()
    manter = quantas_manter()
    fim = parar or threading.Event()

    def laco() -> None:
        while not fim.is_set():
            desde = idade(pasta)
            if desde is None or desde >= espera:
                try:
                    feito = rodar(pasta, manter)
                    registro.info("Backup em %s", feito)
                except Exception:
                    # Nunca derruba o servidor: um backup que falhou é ruim, o
                    # app fora do ar por causa dele é pior. Fica no log, e o
                    # `jf doutor` mostra a idade da última cópia.
                    registro.exception("O backup automático falhou")
                desde = timedelta(0)

            # Acorda quando faltar pouco para a próxima, não a cada hora cheia.
            fim.wait(max((espera - desde).total_seconds(), 60))

    thread = threading.Thread(target=laco, name="jf-backup", daemon=True)
    thread.start()
    return thread
