"""Configuração do app, lida do ambiente com padrões bons para desenvolvimento."""

from __future__ import annotations

import os
import secrets
from dataclasses import dataclass
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class Config:
    banco_url: str
    chave_secreta: str
    producao: bool

    @property
    def cookie_seguro(self) -> bool:
        """Em produção o cookie de sessão só viaja em HTTPS.

        Em desenvolvimento o servidor é http://127.0.0.1, e um cookie `Secure`
        simplesmente não seria enviado — o login pareceria quebrado.
        """
        return self.producao


def carregar() -> Config:
    producao = os.environ.get("JF_PRODUCAO", "").lower() in {"1", "true", "sim"}
    chave = os.environ.get("JF_CHAVE_SECRETA", "")

    if not chave:
        if producao:
            raise RuntimeError(
                "JF_CHAVE_SECRETA não está definida. Em produção ela é obrigatória: "
                "sem chave fixa, toda reinicialização derruba a sessão de todo mundo, "
                "e uma chave sorteada em cada processo quebra o app com mais de um worker."
            )
        # Em desenvolvimento uma chave efêmera serve: derruba a sessão a cada
        # reinício, o que é chato mas não é perigoso.
        chave = secrets.token_hex(32)

    return Config(
        banco_url=os.environ.get("JF_BANCO", f"sqlite:///{RAIZ / 'jf.db'}"),
        chave_secreta=chave,
        producao=producao,
    )


config = carregar()
