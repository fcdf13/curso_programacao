"""A demonstração é o caminho completo rodando: leitor, gravação e permissão.

Ela existe para o app abrir com algo dentro, mas presta um segundo serviço:
o treino e o protocolo saem escritos no formato do João e passam pelos mesmos
leitores que a tela usa. Quebrar um leitor quebra este teste.
"""

from __future__ import annotations

import pytest

from jf.dados.demonstracao import ALUNO, DemonstracaoRecusada, montar
from jf.modelos import ProtocoloAlimentar


@pytest.fixture
def montada(sessao_de_banco):
    contas = montar(sessao_de_banco)
    return contas


def teste_monta_as_duas_contas(montada):
    assert ALUNO[1] in montada["aluno"]


def teste_nao_monta_duas_vezes(montada, sessao_de_banco):
    """Rodar de novo num banco com conta apagaria o que já está lá."""
    with pytest.raises(DemonstracaoRecusada):
        montar(sessao_de_banco)


def teste_recusa_em_producao(monkeypatch, sessao_de_banco):
    """Ela cria contas com senha conhecida e escrita neste repositório."""
    import dataclasses

    from jf.dados import demonstracao
    from jf.config import config

    monkeypatch.setattr(
        demonstracao, "config", dataclasses.replace(config, producao=True)
    )
    with pytest.raises(DemonstracaoRecusada, match="JF_PRODUCAO"):
        montar(sessao_de_banco)


def teste_o_protocolo_do_joao_atravessa_o_leitor(montada, sessao_de_banco):
    protocolo = sessao_de_banco.query(ProtocoloAlimentar).one()

    assert protocolo.deficit_kcal == 500
    assert [g.nome for g in protocolo.grupos] == [
        "Carboidratos",
        "Carboidratos de baixo teor molecular",
        "Proteínas",
        "Frutas",
        "Fibras",
        "Gorduras",
    ]
    assert len(protocolo.refeicoes) == 5
    assert len(protocolo.suplementos) == 3

    carboidratos = protocolo.grupos[0]
    assert carboidratos.itens[0].porcao == "Arroz branco 200 g"
    assert carboidratos.itens[-1].porcao == "Pão francês 2 unidades"

    # O açúcar rápido não se mistura ao carboidrato normal: 20 g de doce de
    # leite não substituem 200 g de arroz.
    rapidos = {i.descricao for i in protocolo.grupos[1].itens}
    assert rapidos == {"Doce leite", "Suco de uva", "Farinha de arroz"}


def teste_a_refeicao_encontra_o_grupo_do_alimento(montada, sessao_de_banco):
    protocolo = sessao_de_banco.query(ProtocoloAlimentar).one()
    cafe = protocolo.refeicoes[0]

    ovos = next(i for i in cafe.itens if i.descricao == "Ovos")
    assert ovos.grupo is not None and ovos.grupo.nome == "Proteínas"

    legumes = next(i for i in cafe.itens if i.descricao == "Legumes")
    assert legumes.a_gosto and legumes.grupo is None

    azeite = next(i for i in cafe.itens if i.descricao == "Azeite")
    assert azeite.opcional
