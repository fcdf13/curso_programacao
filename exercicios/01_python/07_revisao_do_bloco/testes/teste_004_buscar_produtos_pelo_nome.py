"""Testes de A07-004 · Buscar produtos pelo nome.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_encontra_dois():
    verificar(ex.resolver(["Fone Aurora", "Capa Slim", "Fone Pro"], "fone"),
              ["Fone Aurora", "Fone Pro"])


def teste_termo_em_maiusculas():
    verificar(ex.resolver(["Fone Aurora"], "FONE"), ["Fone Aurora"],
              dica="Passe os dois lados para minúsculas antes de comparar.")


def teste_nao_encontra():
    verificar(ex.resolver(["Capa Slim"], "fone"), [])


def teste_lista_vazia():
    verificar(ex.resolver([], "fone"), [])


def teste_termo_vazio_acha_tudo():
    verificar(ex.resolver(["Capa Slim"], ""), ["Capa Slim"])


def teste_preserva_a_grafia_original():
    verificar(ex.resolver(["FONE AURORA"], "fone"), ["FONE AURORA"],
              dica="Devolva o nome como ele chegou, não em minúsculas.")
