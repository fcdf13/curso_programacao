"""Testes de A03-014 · Iniciais do nome.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_tres_nomes():
    verificar(ex.resolver("ana souza lima"), "A.S.L")


def teste_dois_nomes():
    verificar(ex.resolver("Carlos Oliveira"), "C.O")


def teste_um_nome_so():
    verificar(ex.resolver("aurora"), "A")


def teste_espacos_sobrando():
    verificar(ex.resolver("  maria  clara  "), "M.C",
              dica="split() sem argumento já lida com os espaços extras.")
