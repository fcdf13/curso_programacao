"""Testes de A03-005 · Tirar os espaços das pontas.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_espacos_dos_dois_lados():
    verificar(ex.resolver("  Ana Souza  "), "Ana Souza")


def teste_sem_espacos():
    verificar(ex.resolver("Ana"), "Ana")


def teste_so_espacos():
    verificar(ex.resolver("   "), "")


def teste_preserva_espaco_do_meio():
    verificar(ex.resolver(" a  b "), "a  b",
              dica="strip só mexe nas pontas — o miolo fica intacto.")
