"""Linha de comando: preparar o banco, criar o treinador, subir o servidor.

    jf preparar                    cria as tabelas e semeia os catálogos
    jf treinador "João Filho" joao@exemplo.com
    jf demonstracao                banco de brinquedo, com treino dentro
    jf servir
"""

from __future__ import annotations

import argparse
import getpass
import sys

from sqlalchemy import select

from jf.auth import TAMANHO_MINIMO_DA_SENHA, hash_de_senha, normalizar_email
from jf.banco import Sessao, criar_tabelas
from jf.dados import semear_tudo
from jf.modelos import Papel, Usuario


def preparar(_: argparse.Namespace) -> int:
    criar_tabelas()
    print("Tabelas prontas.")
    with Sessao() as sessao:
        for nome, inseridos, existiam in semear_tudo(sessao):
            print(f"  {nome}: {inseridos} novos, {existiam} já estavam lá.")
    return 0


def criar_treinador(argumentos: argparse.Namespace) -> int:
    criar_tabelas()
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


def demonstracao(_: argparse.Namespace) -> int:
    from jf.dados.demonstracao import DemonstracaoRecusada, montar

    criar_tabelas()
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


def servir(argumentos: argparse.Namespace) -> int:
    from jf.servidor import servir as subir

    criar_tabelas()
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

    servidor = comandos.add_parser("servir", help="sobe a API e o app")
    servidor.add_argument("--host", default="127.0.0.1")
    servidor.add_argument("--porta", type=int, default=8770)
    servidor.set_defaults(funcao=servir)

    argumentos = analisador.parse_args(argv)
    return argumentos.funcao(argumentos)


if __name__ == "__main__":
    raise SystemExit(main())
