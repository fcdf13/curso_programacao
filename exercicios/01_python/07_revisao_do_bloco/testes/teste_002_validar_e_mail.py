"""Testes de A07-002 · Validar e-mail.

Arquivo gerado por autoria/construir.py — editar aqui não adianta,
a próxima geração sobrescreve. A resposta vai em respostas/."""

from curso.teste import carregar, verificar  # noqa: F401
from curso import teste as t  # noqa: F401

ex = carregar(__file__)


def teste_email_valido():
    verificar(ex.resolver("ana@loja.com"), True)


def teste_sem_arroba():
    verificar(ex.resolver("analoja.com"), False)


def teste_nada_antes_do_arroba():
    verificar(ex.resolver("@loja.com"), False)


def teste_dominio_sem_ponto():
    verificar(ex.resolver("ana@lojacom"), False)


def teste_com_espaco():
    verificar(ex.resolver("a na@loja.com"), False)


def teste_dois_arrobas():
    verificar(ex.resolver("a@b@loja.com"), False,
              dica="Com dois @, o split devolveria 3 partes — trate isso antes.")


def teste_subdominio():
    verificar(ex.resolver("ana@mail.loja.com.br"), True)
