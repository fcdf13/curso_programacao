"""Sobe a interface web local.

Dois modos:

    curso web          serve o React já compilado e a API na mesma porta
    curso web --dev    só a API; o front roda em `npm run dev`, com proxy do Vite
"""

from __future__ import annotations

import threading
import webbrowser
from pathlib import Path

from curso import caminhos, painel

PORTA_PADRAO = 8765
ENDERECO = "127.0.0.1"          # local e só local: nada exposto na rede


def pasta_do_front() -> Path:
    return caminhos.raiz() / "app" / "dist"


def _abrir_navegador(url: str) -> None:
    threading.Timer(1.0, lambda: webbrowser.open(url)).start()


def subir(porta: int = PORTA_PADRAO, dev: bool = False, abrir: bool = True) -> None:
    import uvicorn

    from curso.api import criar_app

    dist = pasta_do_front()
    if dev:
        app = criar_app(None)
        painel.console.print(
            f"\n  [bold]API[/] em http://{ENDERECO}:{porta}\n"
            f"  [dim]agora rode o front:[/] cd app && npm run dev\n"
        )
    elif dist.exists():
        app = criar_app(dist)
        url = f"http://{ENDERECO}:{porta}"
        painel.console.print(f"\n  [bold]Curso Aurora[/] em {url}\n")
        if abrir:
            _abrir_navegador(url)
    else:
        painel.erro(
            "O front ainda não foi compilado.\n\n"
            "    cd app && npm install && npm run build\n\n"
            "  Ou rode em modo de desenvolvimento:  curso web --dev"
        )
        return

    uvicorn.run(app, host=ENDERECO, port=porta, log_level="warning")
