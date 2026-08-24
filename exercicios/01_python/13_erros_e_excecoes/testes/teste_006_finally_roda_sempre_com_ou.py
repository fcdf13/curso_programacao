"""Testes de A13-006 · finally: roda sempre, com ou sem erro.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_conta_as_duas_tentativas():
    verificar(ex.resolver(10, 2), 5.0)
    verificar(ex.resolver(10, 0), None)
    verificar(ex.tentativas, 2, nome="tentativas")


def teste_conta_mesmo_so_com_sucesso():
    anterior = ex.tentativas
    ex.resolver(4, 2)
    verificar(ex.tentativas, anterior + 1, nome="tentativas")
