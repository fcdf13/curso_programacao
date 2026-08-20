"""Testes de A04-004 · As duas condições.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_atende_aos_dois():
    verificar(ex.resolver(250, True), True)


def teste_nao_e_assinante():
    verificar(ex.resolver(250, False), False)


def teste_valor_baixo():
    verificar(ex.resolver(150, True), False)


def teste_valor_exatamente_no_limite():
    verificar(ex.resolver(200, True), False,
              dica="\"Passa de 200\" exclui o próprio 200.")
