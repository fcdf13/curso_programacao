"""Configuração do app, lida do ambiente com padrões bons para desenvolvimento.

Carregar a configuração **nunca levanta exceção**. Um problema fatal — chave de
sessão faltando em produção — vira um campo no objeto, e quem recusa subir é o
servidor. Se `import jf.config` explodisse, o `jf doutor` não conseguiria nem
rodar para explicar o que está errado, que é justamente quando ele é preciso.
"""

from __future__ import annotations

import os
import secrets
from dataclasses import dataclass
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

# O PWA compilado. Fica aqui, e não em `jf.servidor`, para o diagnóstico poder
# conferi-lo sem importar o servidor — que constrói o app no import e, com a
# configuração quebrada, é exatamente o que não sobe.
WEB = RAIZ / "web" / "dist"


@dataclass(frozen=True)
class Config:
    banco_url: str
    chave_secreta: str
    producao: bool
    # Preenchido quando a configuração não serve para subir. O texto vai para o
    # `jf doutor` e para o erro do servidor.
    impedimento: str | None = None

    @property
    def cookie_seguro(self) -> bool:
        """Em produção o cookie de sessão só viaja em HTTPS.

        Em desenvolvimento o servidor é http://127.0.0.1, e um cookie `Secure`
        simplesmente não seria enviado — o login pareceria quebrado.
        """
        return self.producao

    def exigir_que_sirva(self) -> None:
        if self.impedimento is not None:
            raise RuntimeError(self.impedimento)


def carregar() -> Config:
    producao = os.environ.get("JF_PRODUCAO", "").lower() in {"1", "true", "sim"}
    chave = os.environ.get("JF_CHAVE_SECRETA", "")
    impedimento = None

    if not chave:
        if producao:
            impedimento = (
                "JF_CHAVE_SECRETA não está definida. Em produção ela é "
                "obrigatória: sem chave fixa, toda reinicialização derruba a "
                "sessão de todo mundo, e uma chave sorteada em cada processo "
                "quebra o app com mais de um worker. Gere uma com: "
                "python3 -c 'import secrets; print(secrets.token_hex(32))'"
            )
        # Em desenvolvimento uma chave efêmera serve: derruba a sessão a cada
        # reinício, o que é chato mas não é perigoso.
        chave = secrets.token_hex(32)

    return Config(
        banco_url=os.environ.get("JF_BANCO", f"sqlite:///{RAIZ / 'jf.db'}"),
        chave_secreta=chave,
        producao=producao,
        impedimento=impedimento,
    )


config = carregar()
