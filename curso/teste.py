"""Ferramentas usadas *dentro* dos arquivos de teste de cada exercício.

Um teste típico do curso tem três linhas de cerimônia e o resto é conteúdo:

    from curso.teste import carregar, verificar

    ex = carregar(__file__)

    def teste_soma_de_dois_numeros():
        verificar(ex.resolver(2, 3), 5)

`carregar` resolve sozinho de qual árvore ler (`respostas/` no dia a dia,
`solucoes/` quando o pytest roda com `--solucoes`).
"""

from __future__ import annotations

import importlib.util
import io
import re
import sys
import time
from contextlib import contextmanager, redirect_stdout
from functools import lru_cache
from pathlib import Path
from types import ModuleType
from typing import Any, Callable, Iterator

from curso import caminhos
from curso.comparar import ErroDidatico, verificar  # noqa: F401  (re-exportado)

__all__ = ["carregar", "carregar_sql", "verificar", "ErroDidatico",
           "consultar", "banco", "tabela", "saida_de", "chamar",
           "verificar_tempo", "cronometrar"]

RE_SQL_VAZIO = re.compile(r"^\s*(--[^\n]*\n|/\*.*?\*/|\s)*$", re.DOTALL)


# --------------------------------------------------------------------------- #
# Localizar o arquivo do exercício a partir do arquivo de teste
# --------------------------------------------------------------------------- #

def _arquivo_do_exercicio(arquivo_teste: str | Path) -> Path:
    """`.../testes/teste_003_slug.py` -> `.../ex_003_slug.py` (ou .sql)."""
    teste = Path(arquivo_teste).resolve()
    if teste.parent.name != "testes" or not teste.name.startswith("teste_"):
        raise RuntimeError(
            f"{teste} não parece um teste de exercício "
            "(esperava .../<modulo>/testes/teste_NNN_slug.py)"
        )
    modulo = teste.parent.parent
    slug = teste.stem[len("teste_"):]
    for extensao in (".py", ".sql"):
        alvo = modulo / f"ex_{slug}{extensao}"
        if alvo.exists():
            return alvo
    raise RuntimeError(f"Não achei o exercício ex_{slug}.py|.sql em {modulo}")


def _versao_a_usar(arquivo_exercicio: Path) -> Path:
    """Aplica CURSO_FONTE, com queda para o esqueleto quando não há resposta."""
    escolhida = caminhos.em_arvore(arquivo_exercicio, caminhos.fonte())
    if escolhida.exists():
        return escolhida
    if caminhos.fonte() == caminhos.SOLUCOES:
        raise ErroDidatico(
            f"Falta o gabarito de {arquivo_exercicio.name} em solucoes/.\n"
            "Todo exercício precisa de solução oficial que passe no próprio teste."
        )
    return arquivo_exercicio  # ainda não começou: usa o esqueleto


# --------------------------------------------------------------------------- #
# Exercícios de Python
# --------------------------------------------------------------------------- #

class _ExercicioQuebrado:
    """Substitui o módulo quando o arquivo do aluno não carrega.

    O `carregar(__file__)` roda na importação do teste. Se ele levantasse a
    exceção ali, o pytest registraria um erro de *coleta* — que aborta a suíte
    inteira e não diz qual exercício está errado. Adiando a exceção para o
    primeiro uso, o problema vira a falha daquele teste, com a mensagem certa.
    """

    def __init__(self, erro: ErroDidatico):
        self._erro = erro

    def __getattr__(self, nome: str):
        raise self._erro


def carregar(arquivo_teste: str | Path) -> ModuleType:
    """Importa o exercício correspondente a este arquivo de teste."""
    try:
        alvo = _versao_a_usar(_arquivo_do_exercicio(arquivo_teste))
    except ErroDidatico as erro:
        return _ExercicioQuebrado(erro)

    nome = "exercicio_" + re.sub(r"\W", "_", str(alvo.relative_to(caminhos.raiz())))

    especificacao = importlib.util.spec_from_file_location(nome, alvo)
    if especificacao is None or especificacao.loader is None:
        raise RuntimeError(f"Não consegui carregar {alvo}")
    modulo = importlib.util.module_from_spec(especificacao)
    sys.modules[nome] = modulo

    try:
        especificacao.loader.exec_module(modulo)
    except SyntaxError as erro:
        return _ExercicioQuebrado(ErroDidatico(
            f"Seu arquivo tem um erro de sintaxe e nem chegou a rodar.\n\n"
            f"    arquivo: {alvo.name}\n"
            f"    linha {erro.lineno}: {(erro.text or '').strip()}\n"
            f"    {erro.msg}\n\n"
            "  Sintaxe é o Python não entendendo o que você escreveu — costuma ser\n"
            "  parêntese/aspas sem fechar, dois-pontos faltando ou indentação torta."
        ))
    except Exception as erro:
        return _ExercicioQuebrado(ErroDidatico(
            f"Seu arquivo levantou {type(erro).__name__} ao ser carregado: {erro}\n\n"
            "  Isso acontece com código solto fora de qualquer função.\n"
            "  Deixe só definições no arquivo; o cálculo vai dentro de resolver()."
        ))
    return modulo


def chamar(funcao: Callable, *args: Any, **kwargs: Any) -> Any:
    """Chama a função do aluno traduzindo os erros mais comuns."""
    try:
        return funcao(*args, **kwargs)
    except ErroDidatico:
        raise
    except TypeError as erro:
        if "positional argument" in str(erro) or "argument" in str(erro):
            raise ErroDidatico(
                f"A assinatura da sua função não bate com a que o exercício pede.\n\n"
                f"    {erro}\n\n"
                "  Não mude o nome nem a quantidade de parâmetros de resolver()."
            ) from None
        raise
    except NotImplementedError:
        raise ErroDidatico("A função ainda está por escrever.") from None


def saida_de(funcao: Callable, *args: Any, **kwargs: Any) -> str:
    """Captura o que a função imprime com print(), já sem espaços nas pontas."""
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        chamar(funcao, *args, **kwargs)
    return buffer.getvalue().strip()


# --------------------------------------------------------------------------- #
# Exercícios de SQL
# --------------------------------------------------------------------------- #

class ConsultaDoAluno(str):
    """A query escrita pelo aluno, sabendo de que arquivo veio.

    É uma str comum para todos os efeitos; o caminho serve só para a mensagem
    de erro quando o arquivo ainda está vazio.
    """

    origem: Path

    def __new__(cls, texto: str, origem: Path):
        consulta = super().__new__(cls, texto)
        consulta.origem = origem
        return consulta


def carregar_sql(arquivo_teste: str | Path) -> ConsultaDoAluno:
    """Devolve o texto da query escrita pelo aluno, sem os blocos de comentário."""
    alvo = _versao_a_usar(_arquivo_do_exercicio(arquivo_teste))
    texto = alvo.read_text(encoding="utf-8")
    corpo = re.sub(r"/\*.*?\*/", "", texto, flags=re.DOTALL)
    return ConsultaDoAluno(corpo, alvo)


@lru_cache(maxsize=1)
def banco():
    """Conexão só-leitura com dados/loja.duckdb."""
    import duckdb

    arquivo = caminhos.banco_path()
    if not arquivo.exists():
        raise ErroDidatico(
            "O banco de dados ainda não existe.\n\n"
            "    rode:  curso setup"
        )
    return duckdb.connect(str(arquivo), read_only=True)


def consultar(sql: str):
    """Roda a query no DuckDB e devolve um DataFrame, com erro traduzido."""
    import duckdb

    if RE_SQL_VAZIO.match(sql):
        onde = getattr(sql, "origem", None)
        raise ErroDidatico(
            "O arquivo ainda não tem nenhuma query."
            + (f"\n\n    escreva o SELECT em: {onde}" if onde else "")
        )
    try:
        return banco().sql(sql).df()
    except duckdb.Error as erro:
        raise ErroDidatico(_traduzir_erro_sql(erro)) from None


def _traduzir_erro_sql(erro: Exception) -> str:
    bruto = str(erro).strip()
    cabecalho = f"O banco recusou sua query.\n\n    {bruto.splitlines()[0]}"
    pistas = {
        "Referenced column": "\n\n  Coluna que não existe: confira o nome com `DESCRIBE <tabela>;`.",
        "Table with name": "\n\n  Tabela que não existe: as tabelas são clientes, produtos,\n  pedidos, itens_pedido, pagamentos, eventos_web e estoque_diario.",
        "syntax error": "\n\n  Erro de sintaxe: vírgula sobrando antes do FROM, aspas ou\n  parêntese sem fechar são os suspeitos de sempre.",
        "must appear in the GROUP BY": "\n\n  Toda coluna do SELECT que não está dentro de uma função de\n  agregação precisa aparecer também no GROUP BY.",
    }
    for marca, pista in pistas.items():
        if marca.lower() in bruto.lower():
            return cabecalho + pista
    return cabecalho


@contextmanager
def cronometrar() -> Iterator[dict]:
    """Mede quanto tempo o bloco `with` levou.

        with cronometrar() as t:
            resultado = ex.resolver(entrada_grande)
        verificar_tempo(t["segundos"], limite=1.0)

    Separado em duas chamadas (medir, depois verificar) para o teste poder
    conferir o resultado antes de reclamar da velocidade — errado e lento não
    deveria mostrar só a mensagem de lento.
    """
    info: dict = {}
    inicio = time.perf_counter()
    try:
        yield info
    finally:
        info["segundos"] = time.perf_counter() - inicio


def verificar_tempo(segundos: float, limite: float, dica: str = "") -> None:
    """Erro didático quando a solução é correta, mas lenta demais.

    Existe para os exercícios do módulo de complexidade: a entrada é grande de
    propósito, para que uma solução O(n²) estoure o limite enquanto uma O(n)
    passe com folga. O limite é generoso (a diferença real costuma ser de
    10x-100x), então isto não deveria pegar quem já resolveu com a técnica certa.
    """
    if segundos > limite:
        texto = (
            f"Sua solução dá o resultado certo, mas é lenta demais: levou "
            f"{segundos:.2f}s para uma entrada onde o limite é {limite:.2f}s.\n\n"
            "  Isso quase sempre quer dizer uma complexidade maior do que a\n"
            "  necessária — o suspeito de sempre é uma busca linear (`x in lista`)\n"
            "  rodando dentro de um laço, onde um dict ou set resolveria em O(1)."
        )
        if dica:
            texto += f"\n\n  Dica: {dica}"
        raise ErroDidatico(texto, {
            "tipo": "solucao_lenta", "segundos": round(segundos, 3), "limite": limite,
        })


def tabela(nome: str):
    """Lê uma tabela do dataset como DataFrame — para exercícios de Pandas."""
    import pandas as pd

    arquivo = caminhos.pasta_brutos() / f"{nome}.csv"
    if not arquivo.exists():
        raise ErroDidatico(
            f"Não encontrei dados/brutos/{nome}.csv.\n\n    rode:  curso setup"
        )
    return pd.read_csv(arquivo)
