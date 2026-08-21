"""A aplicação: a API sob `/api` e o PWA compilado em todo o resto."""

from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, FastAPI, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from jf.api import alunos, calculadora, exercicios, sessao, treinos
from jf.config import RAIZ, config

WEB = RAIZ / "web" / "dist"

DURACAO_DA_SESSAO = 60 * 60 * 24 * 30  # 30 dias


def criar_app() -> FastAPI:
    app = FastAPI(title="JF Treino", version="0.1.0")

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

    uvicorn.run(app, host=host, port=porta)
