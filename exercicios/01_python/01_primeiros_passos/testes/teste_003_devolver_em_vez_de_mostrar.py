"""Testes de A01-003 · Devolver em vez de mostrar.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_devolve_a_saudacao():
    verificar(ex.resolver(), "Olá, Aurora!")


def teste_nao_imprime_nada():
    verificar(t.saida_de(ex.resolver), "", nome="texto impresso",
              dica="Este exercício é sobre return. Tire o print.")
