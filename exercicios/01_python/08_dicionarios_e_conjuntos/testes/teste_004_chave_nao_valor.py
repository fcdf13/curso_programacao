"""Testes de A08-004 · Chave, não valor.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_e_uma_chave():
    verificar(ex.resolver({"SP": 15.0, "RJ": 15.0}, "SP"), True)


def teste_e_um_valor_nao_uma_chave():
    verificar(ex.resolver({"SP": 15.0, "RJ": 15.0}, 15.0), False,
              dica="in testa as chaves. 15.0 é um valor, não uma chave.")


def teste_nao_existe():
    verificar(ex.resolver({"SP": 15.0, "RJ": 15.0}, "AM"), False)
