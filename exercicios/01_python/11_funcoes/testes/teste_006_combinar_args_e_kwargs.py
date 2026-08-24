"""Testes de A11-006 · Combinar *args e **kwargs.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_com_itens_e_opcional():
    verificar(
        ex.resolver("Ana", "Fone", "Capa", desconto=0.1),
        {"cliente": "Ana", "itens": ["Fone", "Capa"], "desconto": 0.1},
    )


def teste_sem_itens_nem_opcionais():
    verificar(ex.resolver("Bruno"), {"cliente": "Bruno", "itens": []})


def teste_multiplos_opcionais():
    verificar(
        ex.resolver("Carla", "Mouse", cor="preto", garantia=True),
        {"cliente": "Carla", "itens": ["Mouse"], "cor": "preto", "garantia": True},
    )
