"""Testes de A12-012 · Desafio: catálogo por categoria.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_duas_categorias():
    verificar(
        ex.resolver(
            ["Fone", "Sofá", "Caneca", "Mesa"],
            ["Eletrônicos", "Casa", "Casa", "Casa"],
            [150.0, 800.0, 15.0, 300.0],
            50.0,
        ),
        {"Eletrônicos": ["Fone"], "Casa": ["Sofá", "Mesa"]},
    )


def teste_categoria_fica_com_lista_vazia_se_nada_passa():
    verificar(
        ex.resolver(["Caneca"], ["Casa"], [15.0], 50.0),
        {"Casa": []},
    )


def teste_entrada_vazia():
    verificar(ex.resolver([], [], [], 50.0), {})
