"""Testes de A13-008 · Capturar um erro e relançar um mais claro.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401
import pytest

ex = carregar(__file__)


def teste_texto_valido():
    verificar(ex.resolver("42"), 42)


def teste_texto_invalido_levanta_erro_com_mensagem_clara():
    with pytest.raises(ValueError, match="não é um número válido"):
        ex.resolver("abc")
