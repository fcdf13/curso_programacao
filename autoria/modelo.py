"""O formato em que um exercício é declarado, e como ele vira arquivos."""

from __future__ import annotations

import re
import textwrap
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

from curso import caminhos

# id do módulo -> pasta dentro de exercicios/
MODULOS: dict[str, str] = {
    "A01": "01_python/01_primeiros_passos",
    "A02": "01_python/02_numeros_e_operadores",
    "A03": "01_python/03_strings",
    "A04": "01_python/04_condicionais",
    "A05": "01_python/05_listas",
    "A06": "01_python/06_lacos",
    "A07": "01_python/07_revisao_do_bloco",
    "A08": "01_python/08_dicionarios_e_conjuntos",
    "A09": "01_python/09_complexidade_e_big_o",
    "A10": "01_python/10_tuplas_e_desempacotamento",
    "B01": "02_pandas/01_series_e_dataframe",
    "B05": "02_pandas/05_filtros",
    "C01": "03_sql/01_select",
    "C05": "03_sql/05_agregacao",
}


@dataclass
class Exercicio:
    id: str
    titulo: str
    nivel: int
    enunciado: str
    dicas: list[str]
    testes: str
    solucao: str = ""              # corpo da função (Python) ou query inteira (SQL)
    esqueleto: str = "    ..."     # corpo inicial que o aluno recebe
    assinatura: str = "def resolver():"
    preambulo: str = ""            # imports/constantes acima da função
    preambulo_do_teste: str = ""   # imports extras no topo do arquivo de teste
    tempo_min: int = 5
    tags: list[str] = field(default_factory=list)
    requer: list[str] = field(default_factory=list)
    linguagem: str = "python"
    nota_da_solucao: str = ""      # o "porquê" do gabarito, em uma ou duas frases

    @property
    def numero(self) -> str:
        return self.id.split("-")[1]

    @property
    def slug(self) -> str:
        return f"{self.numero}_{_apelidar(self.titulo)}"

    @property
    def pasta(self) -> Path:
        chave = self.id.split("-")[0]
        if chave not in MODULOS:
            raise KeyError(f"Módulo {chave} não está registrado em MODULOS")
        return caminhos.pasta_exercicios() / MODULOS[chave]

    @property
    def extensao(self) -> str:
        return ".py" if self.linguagem == "python" else ".sql"


@dataclass
class Modulo:
    """Um módulo: o texto de teoria que abre e os exercícios que vêm depois."""
    id: str
    titulo: str
    resumo: str
    teoria: str
    exercicios: list[Exercicio]


# --------------------------------------------------------------------------- #
# Materialização
# --------------------------------------------------------------------------- #

def _apelidar(texto: str) -> str:
    sem_acento = "".join(
        c for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )
    limpo = re.sub(r"[^a-z0-9]+", "_", sem_acento.lower()).strip("_")
    return "_".join(limpo.split("_")[:5])


def _bloco_meta(ex: Exercicio) -> str:
    def lista(itens: list[str]) -> str:
        return "[" + ", ".join(_texto_python(i) for i in itens) + "]"

    linhas = [
        "META = {",
        f'    "id": "{ex.id}",',
        f'    "titulo": {_texto_python(ex.titulo)},',
        f'    "nivel": {ex.nivel},',
        f'    "tempo_min": {ex.tempo_min},',
        f'    "tags": {lista(ex.tags)},',
    ]
    if ex.requer:
        linhas.append(f'    "requer": {lista(ex.requer)},')
    if ex.dicas:
        linhas.append('    "dicas": [')
        for dica in ex.dicas:
            linhas.append(f"        {_texto_python(dica)},")
        linhas.append("    ],")
    linhas.append("}")
    return "\n".join(linhas)


def _texto_python(s: str) -> str:
    """repr com aspas duplas quando possível — combina com o resto do código."""
    if '"' not in s and "\\" not in s:
        return f'"{s}"'
    return repr(s)


def _limpar(bloco: str) -> str:
    return textwrap.dedent(bloco).strip("\n")


def _corpo_de_funcao(bloco: str, comentario: str = "") -> str:
    """Normaliza o corpo: tira a indentação da fonte e recoloca os 4 espaços."""
    texto = _limpar(bloco)
    if comentario:
        texto = f"# {comentario}\n{texto}"
    return "\n".join(
        ("    " + linha) if linha.strip() else "" for linha in texto.splitlines()
    )


def _arquivo_python(ex: Exercicio, corpo: str) -> str:
    partes = [f'"""\n{_limpar(ex.enunciado)}\n"""', ""]
    partes += [_bloco_meta(ex), "", ""]
    if ex.preambulo:
        partes += [_limpar(ex.preambulo), "", ""]
    partes += [ex.assinatura, corpo.rstrip(), ""]
    return "\n".join(partes)


def _arquivo_sql(ex: Exercicio, corpo: str, comentario: str = "") -> str:
    import json

    meta = {
        "id": ex.id, "titulo": ex.titulo, "nivel": ex.nivel,
        "tempo_min": ex.tempo_min, "tags": ex.tags,
    }
    if ex.requer:
        meta["requer"] = ex.requer
    if ex.dicas:
        meta["dicas"] = ex.dicas

    consulta = _limpar(corpo).rstrip()
    if comentario:
        consulta = f"-- {comentario}\n{consulta}"
    return (
        "/* META\n" + json.dumps(meta, ensure_ascii=False, indent=2) + "\n*/\n"
        "/* ENUNCIADO\n" + _limpar(ex.enunciado) + "\n*/\n\n"
        + consulta + "\n"
    )


def _arquivo_de_teste(ex: Exercicio) -> str:
    carregador = "carregar" if ex.linguagem == "python" else "carregar_sql"
    return (
        f'"""Testes de {ex.id} · {ex.titulo}.\n\n'
        f"Arquivo gerado por autoria/construir.py — editar aqui não adianta,\n"
        f'a próxima geração sobrescreve. A resposta vai em respostas/."""\n\n'
        f"from curso.teste import {carregador}, verificar  # noqa: F401\n"
        f"from curso import teste as t  # noqa: F401\n"
        + (_limpar(ex.preambulo_do_teste) + "\n" if ex.preambulo_do_teste else "")
        + f"\nex = {carregador}(__file__)\n\n\n"
        + _limpar(ex.testes) + "\n"
    )


def materializar(ex: Exercicio) -> list[Path]:
    """Escreve enunciado, teste e gabarito. Devolve os caminhos criados."""
    pasta = ex.pasta
    (pasta / "testes").mkdir(parents=True, exist_ok=True)

    destino_solucao = caminhos.raiz() / caminhos.SOLUCOES / ex.pasta.relative_to(
        caminhos.pasta_exercicios()
    )
    destino_solucao.mkdir(parents=True, exist_ok=True)

    enunciado_arq = pasta / f"ex_{ex.slug}{ex.extensao}"
    teste_arq = pasta / "testes" / f"teste_{ex.slug}.py"
    solucao_arq = destino_solucao / f"ex_{ex.slug}{ex.extensao}"

    if ex.linguagem == "python":
        enunciado_arq.write_text(
            _arquivo_python(ex, _corpo_de_funcao(ex.esqueleto)), encoding="utf-8"
        )
        solucao_arq.write_text(
            _arquivo_python(ex, _corpo_de_funcao(ex.solucao, ex.nota_da_solucao)),
            encoding="utf-8",
        )
    else:
        enunciado_arq.write_text(_arquivo_sql(ex, ex.esqueleto), encoding="utf-8")
        solucao_arq.write_text(
            _arquivo_sql(ex, ex.solucao, ex.nota_da_solucao), encoding="utf-8"
        )

    teste_arq.write_text(_arquivo_de_teste(ex), encoding="utf-8")
    return [enunciado_arq, teste_arq, solucao_arq]


def materializar_modulo(modulo: Modulo) -> list[Path]:
    criados: list[Path] = []
    for ex in modulo.exercicios:
        criados += materializar(ex)

    if modulo.exercicios:
        pasta = modulo.exercicios[0].pasta
        leia = pasta / "README.md"
        niveis = sorted({ex.nivel for ex in modulo.exercicios})
        indice = "\n".join(
            f"| `{ex.id}` | {ex.titulo} | {'●' * ex.nivel}{'○' * (5 - ex.nivel)} |"
            for ex in modulo.exercicios
        )
        leia.write_text(
            f"# {modulo.titulo}\n\n"
            f"> {modulo.resumo}\n\n"
            f"{_limpar(modulo.teoria)}\n\n"
            f"## Exercícios deste módulo\n\n"
            f"{len(modulo.exercicios)} exercícios, "
            f"nível {niveis[0]} a {niveis[-1]}.\n\n"
            f"| id | título | nível |\n|---|---|---|\n{indice}\n\n"
            f"Comece com `curso proximo`.\n",
            encoding="utf-8",
        )
        criados.append(leia)
    return criados
