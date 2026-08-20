"""Testes de A02-009 · Média ponderada.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_peso_dobrado_na_ultima():
    verificar(ex.resolver(10, 1, 8, 1, 6, 2), 7.5)


def teste_peso_dobrado_na_primeira():
    verificar(ex.resolver(10, 2, 5, 1, 5, 1), 7.5)


def teste_pesos_iguais_vira_media_simples():
    verificar(ex.resolver(7, 1, 7, 1, 7, 1), 7.0)


def teste_pesos_que_nao_somam_tres():
    verificar(ex.resolver(10, 5, 0, 5, 10, 10), 7.5,
              dica="Divida pela soma dos pesos, não por 3.")
