"""Testes de A07-006 · Estatísticas das vendas.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_tres_vendas():
    verificar(ex.resolver([100, 200, 300]), (3, 600, 200.0, 1))


def teste_uma_venda():
    verificar(ex.resolver([50]), (1, 50, 50.0, 0),
              dica="Uma venda sozinha é exatamente a média — não fica acima dela.")


def teste_lista_vazia():
    verificar(ex.resolver([]), (0, 0, 0.0, 0))


def teste_todas_iguais():
    verificar(ex.resolver([10, 10, 10]), (3, 30, 10.0, 0))


def teste_media_com_dizima():
    verificar(ex.resolver([1, 2, 2]), (3, 5, 1.67, 2),
              dica="Compare com a média exata (1.666...), não com o valor arredondado.")
