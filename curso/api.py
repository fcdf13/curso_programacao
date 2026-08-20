"""API HTTP do curso — uma casca fina sobre o motor.

Nenhuma regra de negócio mora aqui. Catálogo, correção, agendamento de revisão e
progresso continuam em `registro`, `executor`, `srs` e `progresso`; esta camada só
traduz para JSON. É o que garante que o app e o CLI nunca discordem.

O progresso é lido do disco a cada requisição e salvo na hora, sem cópia viva em
memória — assim o `curso check` no terminal e o app aberto no navegador podem
conviver sem um sobrescrever o outro.
"""

from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path
from typing import Any, Literal

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from curso import caminhos, executor, registro
from curso import progresso as prog
from curso.registro import ErroDeCatalogo, Exercicio

DIAS_DE_PREVISAO = 30
DIAS_NO_MAPA = 182


# --------------------------------------------------------------------------- #
# Modelos
# --------------------------------------------------------------------------- #

class Resumo(BaseModel):
    id: str
    titulo: str
    nivel: int
    tempo_min: int
    tags: list[str]
    bloco: str
    nome_do_bloco: str
    modulo: str
    nome_do_modulo: str
    linguagem: str
    estado: str
    tentativas: int
    proxima_revisao: str = ""
    dias_ate_revisao: int | None = None
    vencida: bool = False


class Detalhe(Resumo):
    enunciado: str
    teoria: str
    codigo: str
    requer: list[str]
    dicas_liberadas: list[str]
    total_de_dicas: int
    ja_tentou: bool


class FichaResumida(BaseModel):
    estado: str
    tentativas: int
    tentativas_ate_acertar: int
    revisoes: int
    intervalo_dias: int
    proxima_revisao: str


class ResultadoDaCorrecao(BaseModel):
    ok: bool
    passaram: int
    falharam: int
    mensagem: str
    nome_da_falha: str
    dados: dict[str, Any] | None = None
    ficha: FichaResumida


class Codigo(BaseModel):
    codigo: str


class Dica(BaseModel):
    numero: int
    total: int
    texto: str


class Solucao(BaseModel):
    codigo: str
    linguagem: str


class ModuloNoPainel(BaseModel):
    bloco: str
    nome_do_bloco: str
    modulo: str
    nome_do_modulo: str
    total: int
    feitos: int


class DiaDaPrevisao(BaseModel):
    data: str
    quantidade: int


class PainelDeProgresso(BaseModel):
    total: int
    feitos: int
    sequencia: int
    vencidas: int
    agendados: int
    modulos: list[ModuloNoPainel]
    previsao: list[DiaDaPrevisao]
    dias_praticados: list[str]


class PlanoDoDia(BaseModel):
    novos: list[Resumo]
    revisoes: list[Resumo]
    sequencia: int


# --------------------------------------------------------------------------- #
# Conversões
# --------------------------------------------------------------------------- #

def _resumo(ex: Exercicio, ficha: prog.Ficha | None, hoje: date) -> Resumo:
    ficha = ficha or prog.Ficha(id=ex.id)
    return Resumo(
        id=ex.id, titulo=ex.titulo, nivel=ex.nivel, tempo_min=ex.tempo_min,
        tags=list(ex.tags), bloco=ex.bloco, nome_do_bloco=ex.nome_do_bloco,
        modulo=str(ex.modulo), nome_do_modulo=ex.nome_do_modulo,
        linguagem=ex.linguagem, estado=ficha.estado, tentativas=ficha.tentativas,
        proxima_revisao=ficha.proxima_revisao,
        dias_ate_revisao=ficha.dias_ate_revisao(hoje),
        vencida=ficha.vencida(hoje),
    )


def _teoria_do_modulo(ex: Exercicio) -> str:
    leia = caminhos.pasta_exercicios() / ex.modulo / "README.md"
    return leia.read_text(encoding="utf-8") if leia.exists() else ""


def _gravar(ex: Exercicio, corpo: str) -> None:
    """Grava a resposta reconstituindo o cabeçalho canônico.

    O editor manda só o corpo; o enunciado e o META voltam do arquivo original.
    Assim o arquivo em `respostas/` continua sendo um exercício completo — o CLI
    e o pytest leem os dois do mesmo jeito.
    """
    ex.caminho_resposta.parent.mkdir(parents=True, exist_ok=True)
    ex.caminho_resposta.write_text(ex.montar(corpo), encoding="utf-8")


def _achar(identificador: str) -> Exercicio:
    try:
        return registro.por_id(identificador)
    except ErroDeCatalogo as erro:
        raise HTTPException(status_code=404, detail=str(erro)) from None


def _ficha_resumida(ficha: prog.Ficha) -> FichaResumida:
    return FichaResumida(
        estado=ficha.estado, tentativas=ficha.tentativas,
        tentativas_ate_acertar=ficha.tentativas_ate_acertar,
        revisoes=ficha.revisoes, intervalo_dias=ficha.intervalo_dias,
        proxima_revisao=ficha.proxima_revisao,
    )


# --------------------------------------------------------------------------- #
# Rotas
# --------------------------------------------------------------------------- #

def criar_app(pasta_do_front: Path | None = None) -> FastAPI:
    app = FastAPI(title="Curso Loja Aurora", docs_url="/api/docs", redoc_url=None)

    @app.get("/api/exercicios", response_model=list[Resumo])
    def listar(busca: str = "", bloco: str = "") -> list[Resumo]:
        hoje = date.today()
        p = prog.Progresso.carregar()
        achados = registro.buscar(busca) if busca else list(registro.catalogo())
        if bloco:
            achados = [ex for ex in achados if ex.bloco == bloco.upper()]
        return [_resumo(ex, p.fichas.get(ex.id), hoje) for ex in achados]

    @app.get("/api/hoje", response_model=PlanoDoDia)
    def hoje(quantidade: int = 5) -> PlanoDoDia:
        agora = date.today()
        p = prog.Progresso.carregar()
        por_id = {ex.id: ex for ex in registro.catalogo()}

        revisoes = [
            _resumo(por_id[f.id], f, agora) for f in p.vencidas(agora) if f.id in por_id
        ]
        resolvidos = p.resolvidos()
        novos = [
            _resumo(ex, p.fichas.get(ex.id), agora)
            for ex in registro.catalogo() if ex.id not in resolvidos
        ][:quantidade]
        return PlanoDoDia(novos=novos, revisoes=revisoes,
                          sequencia=p.sequencia_de_dias(agora))

    @app.get("/api/exercicios/{identificador}", response_model=Detalhe)
    def detalhar(identificador: str) -> Detalhe:
        ex = _achar(identificador)
        p = prog.Progresso.carregar()
        ficha = p.fichas.get(ex.id) or prog.Ficha(id=ex.id)
        base = _resumo(ex, ficha, date.today())
        return Detalhe(
            **base.model_dump(),
            enunciado=ex.enunciado,
            teoria=_teoria_do_modulo(ex),
            codigo=ex.corpo_atual(),
            requer=list(ex.requer),
            dicas_liberadas=list(ex.dicas[:ficha.dicas_vistas]),
            total_de_dicas=len(ex.dicas),
            ja_tentou=ficha.tentativas > 0 or ficha.estado == prog.RESOLVIDO,
        )

    @app.put("/api/exercicios/{identificador}/resposta", response_model=Codigo)
    def salvar(identificador: str, corpo: Codigo) -> Codigo:
        _gravar(_achar(identificador), corpo.codigo)
        return corpo

    @app.post("/api/exercicios/{identificador}/check",
              response_model=ResultadoDaCorrecao)
    def corrigir(identificador: str, corpo: Codigo | None = None) -> ResultadoDaCorrecao:
        ex = _achar(identificador)
        if corpo is not None:
            salvar(identificador, corpo)
        elif not ex.caminho_resposta.exists():
            _gravar(ex, ex.corpo_atual())

        resultado = executor.corrigir(ex, fonte=caminhos.RESPOSTAS)
        p = prog.Progresso.carregar()
        ficha = p.registrar_tentativa(ex.id, resultado.ok)
        p.salvar()

        return ResultadoDaCorrecao(
            ok=resultado.ok, passaram=resultado.passaram, falharam=resultado.falharam,
            mensagem=resultado.primeira_falha, nome_da_falha=resultado.nome_da_falha,
            dados=resultado.dados, ficha=_ficha_resumida(ficha),
        )

    @app.post("/api/exercicios/{identificador}/dica", response_model=Dica)
    def dica(identificador: str) -> Dica:
        ex = _achar(identificador)
        if not ex.dicas:
            raise HTTPException(404, "Este exercício não tem dicas.")
        p = prog.Progresso.carregar()
        if p.ficha(ex.id).dicas_vistas >= len(ex.dicas):
            raise HTTPException(
                409, f"As {len(ex.dicas)} dicas já foram liberadas."
            )
        numero = p.registrar_dica(ex.id)
        p.salvar()
        return Dica(numero=numero, total=len(ex.dicas), texto=ex.dicas[numero - 1])

    @app.get("/api/exercicios/{identificador}/solucao", response_model=Solucao)
    def solucao(identificador: str, forcar: bool = False) -> Solucao:
        ex = _achar(identificador)
        if not ex.caminho_solucao.exists():
            raise HTTPException(404, "O gabarito deste exercício está faltando.")

        p = prog.Progresso.carregar()
        ficha = p.ficha(ex.id)
        if ficha.estado != prog.RESOLVIDO and ficha.tentativas < 1 and not forcar:
            raise HTTPException(
                409, "Tente pelo menos uma vez antes de olhar a solução."
            )
        if ficha.estado != prog.RESOLVIDO:
            p.registrar_solucao_vista(ex.id)
            p.salvar()
        return Solucao(codigo=ex.codigo_da_solucao(), linguagem=ex.linguagem)

    @app.get("/api/revisao", response_model=list[Resumo])
    def revisao() -> list[Resumo]:
        agora = date.today()
        p = prog.Progresso.carregar()
        por_id = {ex.id: ex for ex in registro.catalogo()}
        return [
            _resumo(por_id[f.id], f, agora) for f in p.vencidas(agora) if f.id in por_id
        ]

    @app.post("/api/revisao/{identificador}/preparar", response_model=Codigo)
    def preparar(identificador: str) -> Codigo:
        """Arquiva a resposta anterior e devolve o esqueleto, para resolver do zero."""
        ex = _achar(identificador)
        p = prog.Progresso.carregar()
        p.preparar_revisao(ex.id)
        p.salvar()
        return Codigo(codigo=ex.corpo_atual())

    @app.get("/api/progresso", response_model=PainelDeProgresso)
    def painel() -> PainelDeProgresso:
        agora = date.today()
        p = prog.Progresso.carregar()
        resolvidos = p.resolvidos()
        exercicios = registro.catalogo()

        modulos: dict[str, ModuloNoPainel] = {}
        for ex in exercicios:
            chave = str(ex.modulo)
            entrada = modulos.get(chave)
            if entrada is None:
                entrada = ModuloNoPainel(
                    bloco=ex.bloco, nome_do_bloco=ex.nome_do_bloco,
                    modulo=chave, nome_do_modulo=ex.nome_do_modulo,
                    total=0, feitos=0,
                )
                modulos[chave] = entrada
            entrada.total += 1
            if ex.id in resolvidos:
                entrada.feitos += 1

        agendadas: dict[str, int] = {}
        for ficha in p.fichas.values():
            if ficha.estado != prog.RESOLVIDO or not ficha.proxima_revisao:
                continue
            dia = max(date.fromisoformat(ficha.proxima_revisao), agora)
            if (dia - agora).days < DIAS_DE_PREVISAO:
                agendadas[dia.isoformat()] = agendadas.get(dia.isoformat(), 0) + 1

        previsao = [
            DiaDaPrevisao(
                data=(agora + timedelta(days=n)).isoformat(),
                quantidade=agendadas.get((agora + timedelta(days=n)).isoformat(), 0),
            )
            for n in range(DIAS_DE_PREVISAO)
        ]

        limite = (agora - timedelta(days=DIAS_NO_MAPA)).isoformat()
        return PainelDeProgresso(
            total=len(exercicios),
            feitos=len(resolvidos & {ex.id for ex in exercicios}),
            sequencia=p.sequencia_de_dias(agora),
            vencidas=len(p.vencidas(agora)),
            agendados=sum(1 for f in p.fichas.values()
                          if f.estado == prog.RESOLVIDO and not f.vencida(agora)),
            modulos=list(modulos.values()),
            previsao=previsao,
            dias_praticados=[d for d in p.dias_praticados if d >= limite],
        )

    _servir_o_front(app, pasta_do_front)
    return app


def _servir_o_front(app: FastAPI, pasta: Path | None) -> None:
    """Entrega o React já compilado, com fallback de rota para o roteador do front."""
    if pasta is None or not (pasta / "index.html").exists():
        return

    indice = pasta / "index.html"
    if (pasta / "assets").is_dir():
        app.mount("/assets", StaticFiles(directory=pasta / "assets"), name="assets")

    @app.get("/{caminho:path}", include_in_schema=False)
    def spa(caminho: str):
        # As rotas de /api já foram registradas antes desta, então vencem no
        # casamento; qualquer outro caminho é rota do React e volta como index.html.
        if caminho.startswith("api/"):
            raise HTTPException(404, "Rota de API inexistente.")
        arquivo = pasta / caminho
        if caminho and arquivo.is_file():
            return FileResponse(arquivo)
        return FileResponse(indice)
