"""Login, logout e o cadastro de aluno feito pelo treinador."""

from __future__ import annotations

import pytest

from jf.auth import TAMANHO_MINIMO_DA_SENHA, hash_de_senha, normalizar_email
from jf.modelos import Papel

from .conftest import SENHA


@pytest.fixture
def joao(criar_usuario):
    return criar_usuario("João Filho", "joao@exemplo.com", Papel.TREINADOR)


def teste_entrar_e_saber_quem_sou(cliente, joao):
    sessao = cliente("joao@exemplo.com")
    corpo = sessao.get("/api/eu").json()
    assert corpo["usuario"]["papel"] == "treinador"
    assert corpo["aluno_id"] is None


def teste_senha_errada_nao_entra(cliente, joao):
    resposta = cliente().post(
        "/api/entrar", json={"email": "joao@exemplo.com", "senha": "errada-mesmo-123"}
    )
    assert resposta.status_code == 401


def teste_email_desconhecido_da_a_mesma_resposta_que_senha_errada(cliente, joao):
    anonimo = cliente()
    inexistente = anonimo.post(
        "/api/entrar", json={"email": "ninguem@exemplo.com", "senha": SENHA}
    )
    errada = anonimo.post(
        "/api/entrar", json={"email": "joao@exemplo.com", "senha": "errada-mesmo-123"}
    )
    # Respostas distintas revelariam quais emails têm conta.
    assert inexistente.status_code == errada.status_code == 401
    assert inexistente.json() == errada.json()


def teste_email_nao_diferencia_maiuscula(cliente, joao):
    resposta = cliente().post(
        "/api/entrar", json={"email": "JOAO@Exemplo.COM", "senha": SENHA}
    )
    assert resposta.status_code == 200


def teste_sair_derruba_a_sessao(cliente, joao):
    sessao = cliente("joao@exemplo.com")
    assert sessao.post("/api/sair").status_code == 204
    assert sessao.get("/api/eu").status_code == 401


def teste_treinador_cadastra_aluno_que_entra_em_seguida(cliente, joao):
    treinador = cliente("joao@exemplo.com")
    criado = treinador.post(
        "/api/alunos",
        json={
            "nome": "Filipe",
            "email": "Filipe@Exemplo.com",
            "senha": SENHA,
            "altura_cm": 178,
            "objetivo": "Corte com 500 kcal de déficit",
        },
    )
    assert criado.status_code == 201, criado.text
    assert criado.json()["email"] == "filipe@exemplo.com"

    aluno = cliente("filipe@exemplo.com")
    corpo = aluno.get("/api/eu").json()
    assert corpo["usuario"]["papel"] == "aluno"
    assert corpo["aluno_id"] == criado.json()["id"]


def teste_email_repetido_da_conflito(cliente, joao):
    treinador = cliente("joao@exemplo.com")
    dados = {"nome": "Filipe", "email": "filipe@exemplo.com", "senha": SENHA}
    assert treinador.post("/api/alunos", json=dados).status_code == 201
    assert treinador.post("/api/alunos", json=dados).status_code == 409


def teste_senha_curta_e_recusada_no_cadastro(cliente, joao):
    resposta = cliente("joao@exemplo.com").post(
        "/api/alunos",
        json={"nome": "Curto", "email": "curto@exemplo.com", "senha": "12345"},
    )
    assert resposta.status_code == 422


def teste_hash_nunca_vira_a_propria_senha():
    assert hash_de_senha(SENHA) != SENHA
    # Dois hashes da mesma senha diferem: o argon2 sorteia o sal.
    assert hash_de_senha(SENHA) != hash_de_senha(SENHA)


def teste_senha_curta_e_recusada_na_funcao():
    with pytest.raises(ValueError):
        hash_de_senha("a" * (TAMANHO_MINIMO_DA_SENHA - 1))


def teste_normalizar_email():
    assert normalizar_email("  Joao@Exemplo.COM ") == "joao@exemplo.com"


def teste_conta_desativada_nao_entra(cliente, joao, sessao_de_banco):
    joao.ativo = False
    sessao_de_banco.commit()
    resposta = cliente().post(
        "/api/entrar", json={"email": "joao@exemplo.com", "senha": SENHA}
    )
    assert resposta.status_code == 401


def teste_desativar_derruba_sessao_ja_aberta(cliente, joao, sessao_de_banco):
    sessao = cliente("joao@exemplo.com")
    assert sessao.get("/api/eu").status_code == 200

    joao.ativo = False
    sessao_de_banco.commit()

    # O cookie continua válido e assinado, mas a conta não vale mais.
    assert sessao.get("/api/eu").status_code == 401
