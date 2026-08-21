"""O catálogo de exercícios e a semeadura."""

from __future__ import annotations

import pytest
from sqlalchemy import select

from jf.dados import semear_exercicios
from jf.modelos import ConvencaoDeCarga, Exercicio, Papel

from .conftest import SENHA


@pytest.fixture
def catalogo(sessao_de_banco):
    semear_exercicios(sessao_de_banco)
    return sessao_de_banco


def teste_semeadura_insere_o_catalogo(catalogo):
    total = len(catalogo.scalars(select(Exercicio)).all())
    assert total > 50


def teste_semear_de_novo_nao_duplica(catalogo):
    antes = len(catalogo.scalars(select(Exercicio)).all())
    inseridos, existiam = semear_exercicios(catalogo)
    assert inseridos == 0
    assert existiam == antes
    assert len(catalogo.scalars(select(Exercicio)).all()) == antes


def teste_semear_de_novo_preserva_edicao_do_treinador(catalogo):
    """O João ajusta o incremento para bater com a academia dele; isso fica."""
    agachamento = catalogo.scalar(
        select(Exercicio).where(Exercicio.nome == "Agachamento livre")
    )
    agachamento.incremento_kg = 5.0
    catalogo.commit()

    semear_exercicios(catalogo)
    catalogo.refresh(agachamento)
    assert agachamento.incremento_kg == 5.0


def teste_halteres_registram_por_unidade(catalogo):
    """A convenção do paper: dois halteres de 25 kg registram 25."""
    supino = catalogo.scalar(
        select(Exercicio).where(Exercicio.nome == "Supino reto com halteres")
    )
    assert supino.convencao_de_carga is ConvencaoDeCarga.POR_HALTER

    barra = catalogo.scalar(
        select(Exercicio).where(Exercicio.nome == "Supino reto com barra")
    )
    assert barra.convencao_de_carga is ConvencaoDeCarga.TOTAL


def teste_todo_incremento_e_positivo(catalogo):
    for exercicio in catalogo.scalars(select(Exercicio)):
        assert exercicio.incremento_kg > 0, exercicio.nome


def teste_aluno_consulta_o_catalogo(cliente, catalogo, criar_usuario, criar_aluno):
    joao = criar_usuario("João Filho", "joao@exemplo.com", Papel.TREINADOR)
    criar_aluno("Filipe", "filipe@exemplo.com", joao)

    sessao = cliente("filipe@exemplo.com")
    peito = sessao.get("/api/exercicios", params={"grupo": "Peito"}).json()
    assert peito and all(item["grupo_muscular"] == "Peito" for item in peito)

    busca = sessao.get("/api/exercicios", params={"busca": "agachamento"}).json()
    assert any("Agachamento" in item["nome"] for item in busca)

    grupos = sessao.get("/api/exercicios/grupos").json()
    assert "Costas" in grupos and grupos == sorted(grupos)


def teste_senha_do_conftest_serve_de_referencia():
    assert len(SENHA) >= 10
