"""Testes de A13-010 · Desafio: processar um pedido com parcelas.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401
import pytest

ex = carregar(__file__)


def teste_calculo_correto():
    verificar(ex.resolver(300.0, 2, 3), "3x de R$ 200.00")


def teste_parcelas_zero():
    verificar(ex.resolver(300.0, 2, 0), "Erro: número de parcelas inválido")


def teste_preco_invalido():
    verificar(ex.resolver(None, 2, 3), "Erro: preço inválido")


def teste_quantidade_invalida_levanta_erro():
    with pytest.raises(ValueError):
        ex.resolver(300.0, 0, 3)


def teste_conta_todas_as_tentativas_exceto_a_barrada_pelo_raise():
    anterior = ex.tentativas_de_processamento
    ex.resolver(300.0, 2, 3)
    ex.resolver(300.0, 2, 0)
    ex.resolver(None, 2, 3)
    verificar(ex.tentativas_de_processamento, anterior + 3, nome="tentativas_de_processamento")
