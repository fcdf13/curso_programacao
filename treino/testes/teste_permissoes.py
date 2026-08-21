"""O teste que não pode faltar: ninguém enxerga o aluno de outra pessoa.

Estes casos existem porque o erro que eles pegam é silencioso. Uma rota que
esquece de filtrar por dono funciona perfeitamente em todo teste feliz — ela só
falha quando alguém troca o número na URL.
"""

from __future__ import annotations

import pytest

from jf.modelos import Papel

from .conftest import SENHA


@pytest.fixture
def cenario(criar_usuario, criar_aluno):
    """Dois treinadores, um aluno cada."""
    joao = criar_usuario("João Filho", "joao@exemplo.com", Papel.TREINADOR)
    outro = criar_usuario("Outro Treinador", "outro@exemplo.com", Papel.TREINADOR)
    filipe = criar_aluno("Filipe", "filipe@exemplo.com", joao)
    alheio = criar_aluno("Aluno Alheio", "alheio@exemplo.com", outro)
    return {"joao": joao, "outro": outro, "filipe": filipe, "alheio": alheio}


def teste_treinador_ve_o_proprio_aluno(cliente, cenario):
    resposta = cliente("joao@exemplo.com").get(f"/api/alunos/{cenario['filipe'].id}")
    assert resposta.status_code == 200
    assert resposta.json()["nome"] == "Filipe"


def teste_treinador_nao_ve_aluno_de_outro_treinador(cliente, cenario):
    resposta = cliente("joao@exemplo.com").get(f"/api/alunos/{cenario['alheio'].id}")
    # 404 e não 403: um 403 confirmaria que aquele id existe.
    assert resposta.status_code == 404


def teste_listagem_traz_so_os_alunos_do_treinador(cliente, cenario):
    corpo = cliente("joao@exemplo.com").get("/api/alunos").json()
    assert [aluno["nome"] for aluno in corpo] == ["Filipe"]


def teste_aluno_ve_a_si_mesmo(cliente, cenario):
    resposta = cliente("filipe@exemplo.com").get(f"/api/alunos/{cenario['filipe'].id}")
    assert resposta.status_code == 200


def teste_aluno_nao_ve_outro_aluno(cliente, cenario):
    resposta = cliente("filipe@exemplo.com").get(f"/api/alunos/{cenario['alheio'].id}")
    assert resposta.status_code == 404


def teste_aluno_nao_edita_outro_aluno(cliente, cenario):
    resposta = cliente("filipe@exemplo.com").patch(
        f"/api/alunos/{cenario['alheio'].id}", json={"objetivo": "invadido"}
    )
    assert resposta.status_code == 404


def teste_aluno_nao_lista_alunos(cliente, cenario):
    assert cliente("filipe@exemplo.com").get("/api/alunos").status_code == 403


def teste_aluno_nao_cadastra_aluno(cliente, cenario):
    resposta = cliente("filipe@exemplo.com").post(
        "/api/alunos",
        json={"nome": "Intruso", "email": "intruso@exemplo.com", "senha": SENHA},
    )
    assert resposta.status_code == 403


@pytest.mark.parametrize(
    "metodo,caminho",
    [
        ("get", "/api/eu"),
        ("get", "/api/alunos"),
        ("get", "/api/alunos/1"),
        ("patch", "/api/alunos/1"),
        ("post", "/api/alunos"),
        ("get", "/api/exercicios"),
        ("get", "/api/exercicios/grupos"),
    ],
)
def teste_sem_login_nada_responde(cliente, cenario, metodo, caminho):
    # `request` e não `getattr(cliente, metodo)`: o TestClient não aceita `json`
    # nos atalhos de GET.
    resposta = cliente().request(metodo.upper(), caminho, json={})
    assert resposta.status_code == 401


def teste_aluno_de_verdade_nao_vaza_no_404(cliente, cenario):
    """O corpo do 404 é igual para 'não existe' e para 'não é seu'."""
    de_outro = cliente("joao@exemplo.com").get(f"/api/alunos/{cenario['alheio'].id}")
    inexistente = cliente("joao@exemplo.com").get("/api/alunos/999999")
    assert de_outro.json() == inexistente.json()
