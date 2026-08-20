"""Catálogo de exercícios.

Lê o bloco META de cada exercício **sem importar o arquivo** — para Python via `ast`,
para SQL via um bloco de comentário JSON. Isso é essencial: o motor precisa listar e
agendar exercícios mesmo quando a sua resposta atual não compila.
"""

from __future__ import annotations

import ast
import json
import re
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

from curso import caminhos

RE_META_SQL = re.compile(r"/\*\s*META\s*\n(.*?)\n\s*\*/", re.DOTALL)
RE_ENUNCIADO_SQL = re.compile(r"/\*\s*ENUNCIADO\s*\n(.*?)\n\s*\*/", re.DOTALL)
RE_ID = re.compile(r"^([A-D])(\d{2})-(\d{3})$")
# Os dois blocos de comentário que abrem todo exercício de SQL: META e ENUNCIADO.
RE_CABECALHO_SQL = re.compile(r"\A\s*(?:/\*.*?\*/\s*)+", re.DOTALL)

NOMES_DOS_BLOCOS = {
    "A": "Python",
    "B": "Pandas",
    "C": "SQL",
    "D": "Ponte Pandas ↔ SQL",
}


@dataclass(frozen=True)
class Exercicio:
    id: str
    titulo: str
    nivel: int
    tempo_min: int
    tags: tuple[str, ...]
    requer: tuple[str, ...]
    dicas: tuple[str, ...]
    enunciado: str
    linguagem: str          # "python" ou "sql"
    caminho: Path           # o arquivo em exercicios/
    modulo: Path            # a pasta do módulo, relativa a exercicios/

    @property
    def bloco(self) -> str:
        return self.id[0]

    @property
    def nome_do_bloco(self) -> str:
        return NOMES_DOS_BLOCOS.get(self.bloco, self.bloco)

    @property
    def nome_do_modulo(self) -> str:
        """O título do módulo, lido do README dele — com acentos e tudo."""
        return _titulo_do_modulo(caminhos.pasta_exercicios() / self.modulo)

    @property
    def caminho_resposta(self) -> Path:
        return caminhos.em_arvore(self.caminho, caminhos.RESPOSTAS)

    @property
    def caminho_solucao(self) -> Path:
        return caminhos.em_arvore(self.caminho, caminhos.SOLUCOES)

    @property
    def caminho_teste(self) -> Path:
        return self.caminho.parent / "testes" / f"teste_{self.caminho.stem[3:]}.py"

    @property
    def estrelas(self) -> str:
        return "●" * self.nivel + "○" * (5 - self.nivel)

    def iniciada(self) -> bool:
        """A resposta já foi criada (você já começou a mexer)?"""
        return self.caminho_resposta.exists()

    def separar(self, texto: str) -> tuple[str, str]:
        """Divide um arquivo de exercício em (cabeçalho, corpo).

        O cabeçalho é o enunciado mais o META — que **não** devem aparecer no
        editor do aluno: o META guarda as três dicas, e a última costuma ser a
        resposta. O corpo é o código de fato, do primeiro import ou `def` em
        diante.
        """
        if self.linguagem == "sql":
            corpo = RE_CABECALHO_SQL.sub("", texto, count=1)
            corte = len(texto) - len(corpo)
            return texto[:corte], corpo.lstrip("\n")

        arvore = ast.parse(texto)
        for no in arvore.body:
            e_docstring = (
                isinstance(no, ast.Expr)
                and isinstance(no.value, ast.Constant)
                and isinstance(no.value.value, str)
            )
            e_meta = isinstance(no, ast.Assign) and any(
                isinstance(alvo, ast.Name) and alvo.id == "META" for alvo in no.targets
            )
            if e_docstring or e_meta:
                continue
            linhas = texto.splitlines(keepends=True)
            primeira = min(
                [no.lineno, *[d.lineno for d in getattr(no, "decorator_list", [])]]
            )
            return "".join(linhas[: primeira - 1]), "".join(linhas[primeira - 1:])
        return texto, ""

    def cabecalho(self) -> str:
        """O cabeçalho canônico, sempre vindo do enunciado original.

        Reconstituir o arquivo com este cabeçalho — e não com o que estava na
        resposta do aluno — impede que um META editado sem querer quebre o
        catálogo ou apague as dicas.
        """
        return self.separar(self.caminho.read_text(encoding="utf-8"))[0]

    def corpo_atual(self) -> str:
        """Só o código que o aluno escreve — o que vai para o editor."""
        origem = self.caminho_resposta if self.caminho_resposta.exists() else self.caminho
        return self.separar(origem.read_text(encoding="utf-8"))[1]

    def montar(self, corpo: str) -> str:
        """Junta o cabeçalho canônico ao corpo, do jeito que o arquivo deve ficar."""
        return self.cabecalho() + corpo.lstrip("\n")

    def codigo_da_solucao(self) -> str:
        """O gabarito sem o enunciado nem o META — só o que interessa ver."""
        return self.separar(
            self.caminho_solucao.read_text(encoding="utf-8")
        )[1].strip()


class ErroDeCatalogo(Exception):
    """META ausente, malformado ou inconsistente."""


@lru_cache(maxsize=128)
def _titulo_do_modulo(pasta: Path) -> str:
    """'# Módulo A5 — Listas' no README vira 'Listas'."""
    leia = pasta / "README.md"
    if leia.exists():
        primeira = leia.read_text(encoding="utf-8").lstrip().splitlines()[0]
        titulo = primeira.lstrip("# ").strip()
        if "—" in titulo:
            return titulo.split("—", 1)[1].strip()
        return titulo
    return re.sub(r"^\d+_", "", pasta.name).replace("_", " ").capitalize()


# --------------------------------------------------------------------------- #
# Leitura dos metadados
# --------------------------------------------------------------------------- #

def _ler_meta_python(texto: str, caminho: Path) -> tuple[dict, str]:
    try:
        arvore = ast.parse(texto)
    except SyntaxError as erro:
        raise ErroDeCatalogo(f"{caminho}: erro de sintaxe na linha {erro.lineno}") from None

    enunciado = ast.get_docstring(arvore) or ""
    for no in arvore.body:
        if isinstance(no, ast.Assign) and any(
            isinstance(alvo, ast.Name) and alvo.id == "META" for alvo in no.targets
        ):
            try:
                return ast.literal_eval(no.value), enunciado
            except ValueError:
                raise ErroDeCatalogo(f"{caminho}: META não é um literal Python") from None
    raise ErroDeCatalogo(f"{caminho}: não encontrei o dicionário META")


def _ler_meta_sql(texto: str, caminho: Path) -> tuple[dict, str]:
    casamento = RE_META_SQL.search(texto)
    if not casamento:
        raise ErroDeCatalogo(f"{caminho}: não encontrei o bloco /* META ... */")
    try:
        meta = json.loads(casamento.group(1))
    except json.JSONDecodeError as erro:
        raise ErroDeCatalogo(f"{caminho}: META não é JSON válido ({erro})") from None

    enunciado = RE_ENUNCIADO_SQL.search(texto)
    return meta, (enunciado.group(1).strip() if enunciado else "")


def _montar(caminho: Path) -> Exercicio:
    texto = caminho.read_text(encoding="utf-8")
    if caminho.suffix == ".py":
        meta, enunciado = _ler_meta_python(texto, caminho)
        linguagem = "python"
    else:
        meta, enunciado = _ler_meta_sql(texto, caminho)
        linguagem = "sql"

    for chave in ("id", "titulo", "nivel"):
        if chave not in meta:
            raise ErroDeCatalogo(f"{caminho}: META sem a chave obrigatória {chave!r}")
    if not RE_ID.match(meta["id"]):
        raise ErroDeCatalogo(
            f"{caminho}: id {meta['id']!r} fora do formato BLOCO+MÓDULO-NÚMERO (ex.: A01-003)"
        )
    if not 1 <= meta["nivel"] <= 5:
        raise ErroDeCatalogo(f"{caminho}: nivel deve ficar entre 1 e 5")

    return Exercicio(
        id=meta["id"],
        titulo=meta["titulo"],
        nivel=int(meta["nivel"]),
        tempo_min=int(meta.get("tempo_min", 5)),
        tags=tuple(meta.get("tags", ())),
        requer=tuple(meta.get("requer", ())),
        dicas=tuple(meta.get("dicas", ())),
        enunciado=enunciado.strip(),
        linguagem=linguagem,
        caminho=caminho,
        modulo=caminhos.relativo(caminho).parent,
    )


# --------------------------------------------------------------------------- #
# Catálogo
# --------------------------------------------------------------------------- #

@lru_cache(maxsize=1)
def catalogo() -> tuple[Exercicio, ...]:
    """Todos os exercícios, em ordem didática (ordem do id)."""
    base = caminhos.pasta_exercicios()
    arquivos = sorted(
        [*base.rglob("ex_*.py"), *base.rglob("ex_*.sql")],
        key=lambda p: str(p),
    )
    exercicios = [_montar(a) for a in arquivos if "testes" not in a.parts]

    vistos: dict[str, Path] = {}
    for ex in exercicios:
        if ex.id in vistos:
            raise ErroDeCatalogo(
                f"id duplicado {ex.id!r}: {vistos[ex.id]} e {ex.caminho}"
            )
        vistos[ex.id] = ex.caminho

    conhecidos = set(vistos)
    for ex in exercicios:
        for pre_requisito in ex.requer:
            if pre_requisito not in conhecidos:
                raise ErroDeCatalogo(
                    f"{ex.id} declara requer={pre_requisito!r}, que não existe"
                )

    return tuple(sorted(exercicios, key=lambda e: e.id))


def recarregar() -> None:
    catalogo.cache_clear()


def por_id(identificador: str) -> Exercicio:
    """Busca por id completo ('A01-003') ou pelo número solto ('3', '003')."""
    alvo = identificador.strip().upper()
    todos = catalogo()

    for ex in todos:
        if ex.id == alvo:
            return ex

    if alvo.isdigit():
        sufixo = f"-{int(alvo):03d}"
        parciais = [ex for ex in todos if ex.id.endswith(sufixo)]
        if len(parciais) == 1:
            return parciais[0]
        if len(parciais) > 1:
            opcoes = ", ".join(ex.id for ex in parciais)
            raise ErroDeCatalogo(
                f"{identificador!r} é ambíguo — vale para {opcoes}. Use o id completo."
            )

    raise ErroDeCatalogo(f"Não existe exercício {identificador!r}.")


def por_modulo() -> dict[Path, list[Exercicio]]:
    agrupado: dict[Path, list[Exercicio]] = {}
    for ex in catalogo():
        agrupado.setdefault(ex.modulo, []).append(ex)
    return agrupado


def buscar(termo: str) -> list[Exercicio]:
    """Procura por id, título, tag ou trecho do enunciado."""
    alvo = termo.lower()
    return [
        ex for ex in catalogo()
        if alvo in ex.id.lower()
        or alvo in ex.titulo.lower()
        or any(alvo in tag.lower() for tag in ex.tags)
        or alvo in ex.enunciado.lower()
    ]
