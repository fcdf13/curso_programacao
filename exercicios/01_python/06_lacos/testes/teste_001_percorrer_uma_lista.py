"""Testes de A06-001 · Percorrer uma lista.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_duas_categorias():
    verificar(t.saida_de(ex.resolver, ["Moda", "Casa"]), "Moda\nCasa",
              nome="texto impresso")


def teste_um_item():
    verificar(t.saida_de(ex.resolver, ["Livros"]), "Livros", nome="texto impresso")


def teste_lista_vazia_nao_imprime_nada():
    verificar(t.saida_de(ex.resolver, []), "", nome="texto impresso")
