"""Testes de A01-002 · Três linhas na tela.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_imprime_as_tres_linhas():
    verificar(
        t.saida_de(ex.resolver),
        "Loja Aurora\nCatálogo 2026\nBem-vindo!",
        nome="texto impresso",
    )
