"""Linha de comando: preparar o banco, criar o treinador, subir o servidor.

    jf preparar                    migra o banco e semeia os catálogos
    jf treinador "João Filho" joao@exemplo.com
    jf demonstracao                banco de brinquedo, com treino dentro
    jf importar-alimentos taco.csv tabela nutricional para o catálogo
    jf doutor                      confere a configuração antes de subir
    jf backup arquivo.db           cópia consistente do banco, sem parar o app
    jf servir
"""

from __future__ import annotations

import argparse
import getpass
import sys

from sqlalchemy import select

from jf.auth import TAMANHO_MINIMO_DA_SENHA, hash_de_senha, normalizar_email
from jf.banco import Sessao
from jf.dados import semear_tudo
from jf.modelos import Papel, Usuario


def preparar(_: argparse.Namespace) -> int:
    """Leva o banco até a última revisão e semeia os catálogos.

    Idempotente de propósito: é isto que o contêiner roda a cada início, então
    precisa ser seguro rodar num banco já em dia.
    """
    from jf.migracoes import aplicar, esta_atualizado, revisao_aplicada

    ja_existia = _tem_tabelas()
    if ja_existia and revisao_aplicada() is None:
        # Banco criado por `criar_tabelas()` antes das migrações existirem: as
        # tabelas já estão lá, então rodar a primeira migração daria
        # "table already exists".
        from jf.migracoes import carimbar

        print("Banco anterior às migrações; carimbando como atualizado.")
        carimbar()

    if esta_atualizado():
        print("Banco já está na última revisão.")
    else:
        aplicar()
        print("Migrações aplicadas.")

    with Sessao() as sessao:
        for nome, inseridos, existiam in semear_tudo(sessao):
            print(f"  {nome}: {inseridos} novos, {existiam} já estavam lá.")
    return 0


def _tem_tabelas() -> bool:
    from sqlalchemy import inspect

    from jf.banco import engine

    nomes = set(inspect(engine).get_table_names())
    return bool(nomes - {"alembic_version"})


def criar_treinador(argumentos: argparse.Namespace) -> int:
    preparar(argumentos)
    email = normalizar_email(argumentos.email)

    with Sessao() as sessao:
        if sessao.scalar(select(Usuario).where(Usuario.email == email)):
            print(f"Já existe uma conta com o email {email}.", file=sys.stderr)
            return 1

        senha = argumentos.senha or getpass.getpass("Senha: ")
        if len(senha) < TAMANHO_MINIMO_DA_SENHA:
            print(
                f"A senha precisa de pelo menos {TAMANHO_MINIMO_DA_SENHA} caracteres.",
                file=sys.stderr,
            )
            return 1
        if not argumentos.senha and senha != getpass.getpass("Repita a senha: "):
            print("As senhas não conferem.", file=sys.stderr)
            return 1

        sessao.add(
            Usuario(
                nome=argumentos.nome.strip(),
                email=email,
                senha_hash=hash_de_senha(senha),
                papel=Papel.TREINADOR,
            )
        )
        sessao.commit()

    print(f"Treinador {argumentos.nome} criado. Entre em /entrar com {email}.")
    return 0


def demonstracao(argumentos: argparse.Namespace) -> int:
    from jf.dados.demonstracao import DemonstracaoRecusada, montar

    preparar(argumentos)
    with Sessao() as sessao:
        try:
            contas = montar(sessao)
        except DemonstracaoRecusada as motivo:
            print(motivo, file=sys.stderr)
            return 1

    print("Demonstração pronta. Entre com:")
    print(f"  treinador  {contas['treinador']}")
    print(f"  aluno      {contas['aluno']}")
    print("\nAgora rode `jf servir`.")
    return 0


def importar_alimentos(argumentos: argparse.Namespace) -> int:
    """Carrega uma tabela nutricional (TACO, Open Food Facts) no catálogo.

    O arquivo vem de fora porque o valor nutricional precisa ter procedência:
    o app não embute uma tabela própria e não estima o que não foi medido.
    """
    from jf.alimentos import importar

    with Sessao() as sessao:
        try:
            resultado = importar(sessao, argumentos.arquivo, fonte=argumentos.fonte)
        except FileNotFoundError:
            print(f"Não encontrei {argumentos.arquivo!r}.", file=sys.stderr)
            return 1
        except ValueError as erro:
            print(str(erro), file=sys.stderr)
            return 1

    print(resultado)
    campos = ", ".join(sorted(resultado.colunas or {}))
    print(f"Colunas aproveitadas: {campos or 'nenhuma'}.")
    return 0


def doutor(_: argparse.Namespace) -> int:
    from jf.diagnostico import relatorio

    texto, bloqueia = relatorio()
    print(texto)
    return 1 if bloqueia else 0


def backup(argumentos: argparse.Namespace) -> int:
    """Cópia consistente do banco, com o app rodando.

    Usa a API de backup do próprio SQLite em vez de `cp`: copiar o arquivo
    enquanto há escrita em andamento produz um banco corrompido que só se
    descobre na hora de restaurar.
    """
    import sqlite3
    from pathlib import Path

    from jf.config import config

    if not config.banco_url.startswith("sqlite"):
        print(
            "Este comando é do SQLite. Em Postgres, use `pg_dump`.",
            file=sys.stderr,
        )
        return 1

    origem = config.banco_url.replace("sqlite:///", "").replace("sqlite://", "")
    if not origem or not Path(origem).is_file():
        print(f"Não encontrei o banco em {origem!r}.", file=sys.stderr)
        return 1

    destino = Path(argumentos.destino)
    destino.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(origem) as de, sqlite3.connect(destino) as para:
        de.backup(para)

    print(f"{destino} — {destino.stat().st_size / 1024:.0f} kB")
    return 0


def servir(argumentos: argparse.Namespace) -> int:
    from jf.servidor import servir as subir

    print(f"JF Treino em http://{argumentos.host}:{argumentos.porta}")
    subir(argumentos.host, argumentos.porta)
    return 0


def main(argv: list[str] | None = None) -> int:
    analisador = argparse.ArgumentParser(prog="jf", description=__doc__)
    comandos = analisador.add_subparsers(dest="comando", required=True)

    comandos.add_parser("preparar", help="cria as tabelas e semeia o catálogo").set_defaults(
        funcao=preparar
    )

    treinador = comandos.add_parser("treinador", help="cria uma conta de treinador")
    treinador.add_argument("nome")
    treinador.add_argument("email")
    treinador.add_argument(
        "--senha",
        help="informe para uso não interativo; sem isto a senha é pedida sem eco",
    )
    treinador.set_defaults(funcao=criar_treinador)

    comandos.add_parser(
        "demonstracao", help="cria um banco de brinquedo com um treino dentro"
    ).set_defaults(funcao=demonstracao)

    alimentos = comandos.add_parser(
        "importar-alimentos", help="carrega uma tabela nutricional no catálogo"
    )
    alimentos.add_argument("arquivo", help="CSV da TACO ou do Open Food Facts")
    alimentos.add_argument(
        "--fonte", default="taco", help="de onde veio a tabela (padrão: taco)"
    )
    alimentos.set_defaults(funcao=importar_alimentos)

    comandos.add_parser(
        "doutor", help="confere a configuração antes de subir"
    ).set_defaults(funcao=doutor)

    copia = comandos.add_parser("backup", help="cópia consistente do banco")
    copia.add_argument("destino")
    copia.set_defaults(funcao=backup)

    servidor = comandos.add_parser("servir", help="sobe a API e o app")
    servidor.add_argument("--host", default="127.0.0.1")
    servidor.add_argument("--porta", type=int, default=8770)
    servidor.set_defaults(funcao=servir)

    argumentos = analisador.parse_args(argv)
    return argumentos.funcao(argumentos)


if __name__ == "__main__":
    raise SystemExit(main())
