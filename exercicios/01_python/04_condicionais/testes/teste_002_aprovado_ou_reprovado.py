"""Testes de A04-002 · Aprovado ou reprovado.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_acima_da_media():
    verificar(ex.resolver(10), "aprovado")


def teste_na_nota_de_corte():
    verificar(ex.resolver(7), "aprovado",
              dica="7 exato aprova: a comparação é >=, não >.")


def teste_logo_abaixo_do_corte():
    verificar(ex.resolver(6.9), "reprovado")


def teste_zero():
    verificar(ex.resolver(0), "reprovado")
