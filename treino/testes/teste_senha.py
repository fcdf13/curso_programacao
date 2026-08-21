"""Trocar a senha, redefinir a de um aluno, e o que isso derruba.

A parte que importa não é a troca em si: é que trocar a senha **derruba as
sessões abertas em outros aparelhos**. Sem isso, quem trocou a senha porque
desconfiava de alguém continuaria com esse alguém dentro da conta.
"""

from __future__ import annotations

import pytest

from jf.modelos import Papel

from .conftest import SENHA

NOVA = "uma-senha-nova-bem-comprida"


@pytest.fixture
def joao(criar_usuario):
    return criar_usuario("João Filho", "joao@exemplo.com", Papel.TREINADOR)


@pytest.fixture
def filipe(criar_aluno, joao):
    return criar_aluno("Filipe", "filipe@exemplo.com", joao)


# ------------------------------------------------------- trocar a própria


def teste_trocar_a_propria_senha(cliente, joao):
    sessao = cliente("joao@exemplo.com")
    resposta = sessao.post(
        "/api/eu/senha", json={"senha_atual": SENHA, "senha_nova": NOVA}
    )
    assert resposta.status_code == 204

    # A senha nova entra; a antiga não.
    assert cliente("joao@exemplo.com", senha=NOVA).get("/api/eu").status_code == 200
    assert (
        cliente().post("/api/entrar", json={"email": "joao@exemplo.com", "senha": SENHA})
    ).status_code == 401


def teste_quem_trocou_continua_dentro(cliente, joao):
    """Trocar a senha não pode expulsar quem trocou: seria um castigo esquisito."""
    sessao = cliente("joao@exemplo.com")
    sessao.post("/api/eu/senha", json={"senha_atual": SENHA, "senha_nova": NOVA})
    assert sessao.get("/api/eu").status_code == 200


def teste_a_troca_derruba_os_outros_aparelhos(cliente, joao):
    celular = cliente("joao@exemplo.com")
    computador = cliente("joao@exemplo.com")
    assert celular.get("/api/eu").status_code == 200

    computador.post("/api/eu/senha", json={"senha_atual": SENHA, "senha_nova": NOVA})

    # É este o ponto: o cookie do celular continua assinado e válido, mas é
    # anterior à troca — e por isso não vale mais.
    caiu = celular.get("/api/eu")
    assert caiu.status_code == 401
    assert "senha" in caiu.json()["detail"].lower()


def teste_a_senha_atual_e_exigida(cliente, joao):
    """Sessão emprestada não pode virar conta tomada."""
    sessao = cliente("joao@exemplo.com")
    resposta = sessao.post(
        "/api/eu/senha", json={"senha_atual": "chute-que-nao-e-a-senha", "senha_nova": NOVA}
    )
    assert resposta.status_code == 403
    # E a senha continua sendo a antiga.
    assert cliente("joao@exemplo.com").get("/api/eu").status_code == 200


def teste_senha_nova_igual_a_atual_e_recusada(cliente, joao):
    resposta = cliente("joao@exemplo.com").post(
        "/api/eu/senha", json={"senha_atual": SENHA, "senha_nova": SENHA}
    )
    assert resposta.status_code == 422


def teste_senha_curta_e_recusada(cliente, joao):
    resposta = cliente("joao@exemplo.com").post(
        "/api/eu/senha", json={"senha_atual": SENHA, "senha_nova": "curta"}
    )
    assert resposta.status_code == 422


def teste_sem_login_nao_troca_senha(cliente, joao):
    resposta = cliente().post(
        "/api/eu/senha", json={"senha_atual": SENHA, "senha_nova": NOVA}
    )
    assert resposta.status_code == 401


# ------------------------------------------------------ provisória


def teste_aluno_cadastrado_nasce_com_senha_provisoria(cliente, joao):
    treinador = cliente("joao@exemplo.com")
    treinador.post(
        "/api/alunos",
        json={"nome": "Novato", "email": "novato@exemplo.com", "senha": SENHA},
    )

    eu = cliente("novato@exemplo.com").get("/api/eu").json()
    # Quem escolheu a senha foi o treinador; o app diz isso em vez de deixar a
    # porta aberta em silêncio.
    assert eu["usuario"]["senha_provisoria"] is True


def teste_trocar_a_senha_tira_a_marca_de_provisoria(cliente, joao):
    treinador = cliente("joao@exemplo.com")
    treinador.post(
        "/api/alunos",
        json={"nome": "Novato", "email": "novato@exemplo.com", "senha": SENHA},
    )

    aluno = cliente("novato@exemplo.com")
    aluno.post("/api/eu/senha", json={"senha_atual": SENHA, "senha_nova": NOVA})
    assert aluno.get("/api/eu").json()["usuario"]["senha_provisoria"] is False


def teste_o_treinador_nao_nasce_provisorio(cliente, joao):
    assert cliente("joao@exemplo.com").get("/api/eu").json()["usuario"][
        "senha_provisoria"
    ] is False


# ------------------------------------------------ redefinir a de um aluno


def teste_treinador_redefine_a_senha_do_aluno(cliente, joao, filipe):
    """Não há "esqueci minha senha": sem provedor de email, quem redefine é ele."""
    resposta = cliente("joao@exemplo.com").post(
        f"/api/alunos/{filipe.id}/senha", json={"senha": NOVA}
    )
    assert resposta.status_code == 204

    assert cliente("filipe@exemplo.com", senha=NOVA).get("/api/eu").json()["usuario"][
        "senha_provisoria"
    ] is True


def teste_redefinir_derruba_a_sessao_do_aluno(cliente, joao, filipe):
    aluno = cliente("filipe@exemplo.com")
    assert aluno.get("/api/eu").status_code == 200

    cliente("joao@exemplo.com").post(f"/api/alunos/{filipe.id}/senha", json={"senha": NOVA})
    assert aluno.get("/api/eu").status_code == 401


def teste_aluno_nao_redefine_a_propria_senha_por_essa_rota(cliente, filipe):
    """Essa rota pula a conferência da senha atual — é só do treinador."""
    resposta = cliente("filipe@exemplo.com").post(
        f"/api/alunos/{filipe.id}/senha", json={"senha": NOVA}
    )
    assert resposta.status_code == 403


def teste_treinador_nao_redefine_senha_de_aluno_alheio(
    cliente, criar_usuario, criar_aluno, filipe
):
    outro = criar_usuario("Outro", "outro@exemplo.com", Papel.TREINADOR)
    criar_aluno("Alheio", "alheio@exemplo.com", outro)

    resposta = cliente("outro@exemplo.com").post(
        f"/api/alunos/{filipe.id}/senha", json={"senha": NOVA}
    )
    # 404 e não 403: quem não pode ver também não fica sabendo que existe.
    assert resposta.status_code == 404
