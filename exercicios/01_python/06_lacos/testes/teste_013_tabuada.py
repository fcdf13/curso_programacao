"""Testes de A06-013 · Tabuada.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_tabuada_de_dois():
    verificar(ex.resolver(2), [1, 2, 2, 4])


def teste_tabuada_de_tres():
    verificar(ex.resolver(3), [1, 2, 3, 2, 4, 6, 3, 6, 9])


def teste_tabuada_de_um():
    verificar(ex.resolver(1), [1])


def teste_quantidade_de_resultados():
    verificar(len(ex.resolver(4)), 16, nome="tamanho do resultado",
              dica="São n × n produtos no total.")
