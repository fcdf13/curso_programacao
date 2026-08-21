"""Confere a configuração antes de o app ir para a internet.

Existe porque as falhas que importam num deploy são silenciosas: o app sobe,
responde, e só semanas depois se descobre que a chave de sessão era a de
desenvolvimento ou que o banco vive num disco que some no próximo restart.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from jf.config import WEB, config

# A chave que o `comecar.sh` e o `compose.yaml` usam. Se ela chegar em
# produção, qualquer pessoa que leia o repositório assina um cookie de sessão
# válido — e entra como quem quiser.
CHAVE_DE_EXEMPLO = "desenvolvimento-local-nao-usar-em-producao"

TAMANHO_MINIMO_DA_CHAVE = 32


@dataclass(frozen=True)
class Achado:
    nivel: str  # "erro" | "aviso" | "ok"
    titulo: str
    detalhe: str

    @property
    def bloqueia(self) -> bool:
        return self.nivel == "erro"


def _chave() -> Achado:
    chave = os.environ.get("JF_CHAVE_SECRETA", "")

    if not chave:
        # Em produção isto é o `impedimento` da própria configuração: uma regra
        # só, num lugar só.
        return Achado(
            "erro" if config.impedimento else "aviso",
            "JF_CHAVE_SECRETA não está definida",
            config.impedimento
            or "Sem chave fixa, cada reinício derruba a sessão de todo mundo, e "
            "com mais de um worker o login simplesmente não funciona. "
            "Gere uma com: python3 -c 'import secrets; print(secrets.token_hex(32))'",
        )

    if chave == CHAVE_DE_EXEMPLO:
        return Achado(
            "erro",
            "JF_CHAVE_SECRETA é a chave de exemplo",
            "Ela está escrita no repositório. Quem lê o código assina um cookie "
            "de sessão válido e entra como qualquer usuário.",
        )

    if len(chave) < TAMANHO_MINIMO_DA_CHAVE:
        return Achado(
            "aviso",
            "JF_CHAVE_SECRETA é curta",
            f"{len(chave)} caracteres. Use pelo menos {TAMANHO_MINIMO_DA_CHAVE}.",
        )

    return Achado("ok", "Chave de sessão", "definida e com tamanho razoável")


def _producao() -> Achado:
    if config.producao:
        return Achado(
            "ok",
            "Modo produção",
            "cookie de sessão só viaja em HTTPS (Secure)",
        )
    return Achado(
        "aviso",
        "JF_PRODUCAO não está ligada",
        "O cookie de sessão sai sem a marca `Secure`, então ele viaja em HTTP "
        "puro. Ligue com JF_PRODUCAO=1 em qualquer servidor que não seja a sua "
        "máquina.",
    )


def _banco() -> list[Achado]:
    url = config.banco_url
    achados: list[Achado] = []

    if not url.startswith("sqlite"):
        return [Achado("ok", "Banco", f"{url.split('://')[0]} — fora do contêiner")]

    caminho = url.replace("sqlite:///", "").replace("sqlite://", "")
    if not caminho:
        return [
            Achado(
                "erro",
                "Banco em memória",
                "`sqlite://` sem arquivo perde tudo ao reiniciar. Aponte "
                "JF_BANCO para um arquivo num disco que persista.",
            )
        ]

    pasta = Path(caminho).parent
    achados.append(Achado("ok", "Banco", f"SQLite em {caminho}"))

    # O caso que morde de verdade: SQLite dentro do contêiner, sem volume. O
    # app sobe, funciona, e o histórico some no primeiro restart.
    if config.producao and not _parece_volume(pasta):
        achados.append(
            Achado(
                "aviso",
                "O arquivo do banco pode não sobreviver ao restart",
                f"{pasta} não parece um volume montado. Em Fly.io ou Render, "
                "monte um disco e aponte JF_BANCO para dentro dele — senão o "
                "histórico do aluno some no próximo deploy.",
            )
        )

    return achados


def _parece_volume(pasta: Path) -> bool:
    """Heurística: o disco montado quase nunca fica na raiz do app."""
    return any(
        str(pasta).startswith(prefixo) for prefixo in ("/dados", "/data", "/mnt", "/var/lib")
    )


def _pwa() -> Achado:
    if not (WEB / "index.html").is_file():
        return Achado(
            "erro",
            "O PWA não está compilado",
            f"{WEB} não tem index.html. Rode `npm run build` em web/ — sem isso "
            "o servidor só responde a /api.",
        )

    if not (WEB / "manifest.webmanifest").is_file():
        return Achado(
            "aviso",
            "Sem manifest",
            "Sem o manifest o app não instala na tela de início.",
        )

    return Achado("ok", "PWA compilado", "index.html e manifest no lugar")


def _dominios() -> Achado:
    dominios = os.environ.get("JF_DOMINIOS", "").strip()
    if dominios:
        return Achado("ok", "Domínios permitidos", dominios)
    return Achado(
        "aviso" if config.producao else "ok",
        "JF_DOMINIOS não está definida",
        "Sem a lista de domínios, o app responde a qualquer Host. Defina "
        "JF_DOMINIOS=treino.seudominio.com.br quando souber o endereço.",
    )


def examinar() -> list[Achado]:
    return [_chave(), _producao(), _dominios(), *_banco(), _pwa()]


def relatorio() -> tuple[str, bool]:
    """Devolve o texto e se algo bloqueia o deploy."""
    marcas = {"ok": "  ok  ", "erro": " ERRO ", "aviso": "aviso "}
    linhas = []
    bloqueia = False

    for achado in examinar():
        linhas.append(f"[{marcas[achado.nivel]}] {achado.titulo}")
        linhas.append(f"          {achado.detalhe}")
        bloqueia = bloqueia or achado.bloqueia

    linhas.append("")
    linhas.append(
        "Há algo que impede subir com segurança."
        if bloqueia
        else "Nada impede subir."
    )
    return "\n".join(linhas), bloqueia
