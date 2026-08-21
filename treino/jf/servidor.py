"""A aplicação: a API sob `/api` e o PWA compilado em todo o resto."""

from __future__ import annotations

from pathlib import Path

import os

from fastapi import APIRouter, FastAPI, HTTPException, Request, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from jf.api import (
    alunos,
    calculadora,
    checkins,
    dieta,
    exercicios,
    privacidade,
    sessao,
    treinos,
)
from jf.config import WEB, config

DURACAO_DA_SESSAO = 60 * 60 * 24 * 30  # 30 dias

# Tudo vem da própria origem, menos as fontes do Google. `unsafe-inline` em
# `style-src` cobre os poucos `style={{...}}` do React; em `script-src` ele não
# aparece, que é onde importaria.
CSP = "; ".join(
    [
        "default-src 'self'",
        "script-src 'self'",
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
        "font-src 'self' https://fonts.gstatic.com",
        "img-src 'self' data:",
        "connect-src 'self'",
        "base-uri 'self'",
        "form-action 'self'",
        # O app não deve ser embutido em iframe nenhum: é o que impede
        # clickjacking sobre a tela de login.
        "frame-ancestors 'none'",
    ]
)


def criar_app() -> FastAPI:
    # Configuração que não serve para produção derruba aqui, não no import:
    # assim `jf doutor` ainda consegue rodar e explicar o problema.
    config.exigir_que_sirva()

    app = FastAPI(
        title="JF Treino",
        version="0.1.0",
        # `/docs` e `/openapi.json` expõem a superfície inteira da API para
        # quem passar pela URL. Num app privado de um treinador, isso não tem
        # por que estar aberto na internet.
        docs_url=None if config.producao else "/docs",
        redoc_url=None,
        openapi_url=None if config.producao else "/openapi.json",
    )

    @app.middleware("http")
    async def cabecalhos_de_seguranca(request: Request, seguir):
        resposta = await seguir(request)
        resposta.headers["Content-Security-Policy"] = CSP
        resposta.headers["X-Content-Type-Options"] = "nosniff"
        resposta.headers["Referrer-Policy"] = "same-origin"
        # O app lida com dado de saúde; nada dele deve ir para buscador.
        resposta.headers["X-Robots-Tag"] = "noindex, nofollow"
        if config.producao:
            resposta.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains"
            )
        return resposta

    # Em produção, só responde para os domínios declarados: sem isso, um Host
    # forjado envenena link absoluto e cache. `JF_DOMINIOS` aceita lista
    # separada por vírgula.
    dominios = [d.strip() for d in os.environ.get("JF_DOMINIOS", "").split(",") if d.strip()]
    if dominios:
        app.add_middleware(TrustedHostMiddleware, allowed_hosts=dominios)

    app.add_middleware(
        SessionMiddleware,
        secret_key=config.chave_secreta,
        session_cookie="jf_sessao",
        max_age=DURACAO_DA_SESSAO,
        https_only=config.cookie_seguro,
        # `Lax` já barra o cookie em POST vindo de outro site, que é o vetor de
        # CSRF que interessa aqui. `Strict` derrubaria o aluno ao abrir o app por
        # um link do WhatsApp, que é justamente como ele vai chegar.
        same_site="lax",
    )

    api = APIRouter(prefix="/api")

    @api.get("/saude")
    def saude() -> dict[str, str]:
        return {"estado": "ok"}

    api.include_router(sessao.rotas)
    api.include_router(alunos.rotas)
    api.include_router(exercicios.rotas)
    api.include_router(treinos.rotas)
    api.include_router(checkins.rotas)
    api.include_router(dieta.rotas)
    api.include_router(privacidade.rotas)
    api.include_router(calculadora.rotas)
    # Depois de todas as rotas: o que se registra num router após a inclusão
    # não entra no app.
    app.include_router(api)

    _servir_o_app(app)
    return app


def _servir_o_app(app: FastAPI) -> None:
    """Entrega o PWA compilado, se ele existir.

    Sem `web/dist` o servidor continua subindo — em desenvolvimento o Vite serve
    o front na porta dele e só a API vem daqui.
    """
    if not WEB.is_dir():
        return

    app.mount("/assets", StaticFiles(directory=WEB / "assets"), name="assets")

    @app.get("/{caminho:path}", include_in_schema=False)
    def spa(caminho: str) -> FileResponse:
        # Arquivo real na raiz do build (manifest.webmanifest, ícones, sw.js).
        arquivo = (WEB / caminho).resolve()
        if caminho and arquivo.is_file() and arquivo.is_relative_to(WEB):
            return FileResponse(arquivo)

        # Qualquer outra rota é do react-router — menos `/api`, que já foi
        # tratada acima e precisa devolver 404 de verdade em vez de HTML.
        if caminho.startswith("api/"):
            raise HTTPException(status.HTTP_404_NOT_FOUND)

        return FileResponse(WEB / "index.html")


app = criar_app()


def servir(host: str = "127.0.0.1", porta: int = 8770) -> None:
    import uvicorn

    from jf.backup import agendar

    # Fica no `servir`, e não no `criar_app`: os testes criam o app dezenas de
    # vezes, e uma thread de backup por app seria um enxame copiando banco de
    # teste. Quem serve de verdade passa por aqui uma vez só.
    agendar()

    uvicorn.run(
        app,
        host=host,
        port=porta,
        # Atrás do proxy do Fly ou do Render, sem isto o app enxerga o IP do
        # proxy e acha que a conexão é HTTP — o que quebra qualquer decisão
        # baseada em esquema.
        proxy_headers=config.producao,
        forwarded_allow_ips="*" if config.producao else None,
    )
