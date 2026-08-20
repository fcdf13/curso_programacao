"""Testes de A06-015 · FizzBuzz.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_ate_cinco():
    verificar(ex.resolver(5), [1, 2, "Fizz", 4, "Buzz"])


def teste_pega_o_quinze():
    verificar(ex.resolver(15)[-1], "FizzBuzz", nome="último item",
              dica="Se veio 'Fizz', o teste de divisível por 3 está vindo antes.")


def teste_lista_completa():
    verificar(
        ex.resolver(15),
        [1, 2, "Fizz", 4, "Buzz", "Fizz", 7, 8, "Fizz", "Buzz",
         11, "Fizz", 13, 14, "FizzBuzz"],
    )


def teste_numeros_seguem_inteiros():
    verificar(ex.resolver(2), [1, 2],
              dica="Os números que não são Fizz nem Buzz entram como int, não como texto.")


def teste_zero():
    verificar(ex.resolver(0), [])
