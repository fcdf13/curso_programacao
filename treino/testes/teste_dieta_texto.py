"""O leitor do protocolo alimentar escrito à mão.

Os casos vêm do protocolo real que o João passou — inclusive as linhas que ele
escreve fora de qualquer padrão, que precisam voltar em `nao_entendidas` em vez
de virar comida.
"""

from __future__ import annotations

import pytest

from jf.dieta_texto import ler_protocolo

# Recorte fiel do PDF, com a pontuação e o espaçamento como estão lá.
PROTOCOLO = """
Protocolo alimentar

500 calorias total de déficit por dia

Carboidratos substituição
Arroz branco: 200g
Mandioca: 200g
Cuscuz: 225g
Batata Doce: 225g
Batata inglesa: 225g
Macarrão: 225g
Pão francês: 2 unidades

Carboidratos de baixo teor molecular:
Doce leite: 20g
Suco de uva: 200ml
Farinha de arroz: 50g

Proteínas substituição
Carne assada: 190g
Frango: 200g
Ovos: 5 und
Peixe: 250g

Frutas:
maçã: 1 und
Melão: 200g
Morango: 200g

Gorduras:
azeite: 1 colher

1° refeição café
Ovos
Pão francês
(Azeite)
Legumes a gosto

2° refeição almoço
Arroz branco
Frango
Salada a gosto

Suplementos:
Multi vitaminico: dose diária
Homega 3: 2 cps
Ioimbina: 5mg

(Berberina 1 cps)em jejum 500ml de água

Só basta fazer o que é preciso!
"""


@pytest.fixture(scope="module")
def lido():
    return ler_protocolo(PROTOCOLO)


def teste_deficit(lido):
    assert lido.deficit_kcal == 500


def teste_grupos_e_refeicoes(lido):
    assert [g.nome for g in lido.grupos] == [
        "Carboidratos",
        "Carboidratos de baixo teor molecular",
        "Proteínas",
        "Frutas",
        "Gorduras",
    ]
    assert [r.nome for r in lido.refeicoes] == [
        "1ª refeição — Café",
        "2ª refeição — Almoço",
    ]


def teste_equivalencia_guarda_a_quantidade_de_cada_item(lido):
    carboidratos = lido.grupos[0]
    porcoes = {i.descricao: (i.quantidade, i.unidade) for i in carboidratos.itens}
    # As quantidades diferem de propósito — é o que torna a troca equivalente.
    assert porcoes["Arroz branco"] == (200.0, "g")
    assert porcoes["Cuscuz"] == (225.0, "g")
    assert porcoes["Pão francês"] == (2.0, "unidades")


def teste_grupo_de_baixo_teor_molecular_nao_se_mistura_ao_normal(lido):
    """O bug que este teste tranca vale mais que o formato.

    "Carboidratos de baixo teor molecular:" não traz a palavra "substituição",
    e sem reconhecê-lo como cabeçalho os itens caíam no grupo anterior — o app
    diria ao aluno que 20 g de doce de leite substituem 200 g de arroz.
    """
    normais = {i.descricao for i in lido.grupos[0].itens}
    rapidos = {i.descricao for i in lido.grupos[1].itens}

    assert "Doce leite" in rapidos
    assert "Doce leite" not in normais
    assert normais.isdisjoint(rapidos)


def teste_unidade_de_volume(lido):
    suco = next(i for i in lido.grupos[1].itens if i.descricao == "Suco de uva")
    assert (suco.quantidade, suco.unidade) == (200.0, "ml")


def teste_parenteses_marcam_o_opcional(lido):
    cafe = lido.refeicoes[0]
    azeite = next(i for i in cafe.itens if i.descricao == "Azeite")
    assert azeite.opcional


def teste_a_gosto_nao_vira_quantidade_zero(lido):
    cafe = lido.refeicoes[0]
    legumes = next(i for i in cafe.itens if i.descricao == "Legumes")
    assert legumes.a_gosto
    assert legumes.quantidade is None


def teste_item_de_refeicao_sem_quantidade_aponta_para_o_grupo(lido):
    cafe = lido.refeicoes[0]
    ovos = next(i for i in cafe.itens if i.descricao == "Ovos")
    # A quantidade dele mora no grupo Proteínas, não na refeição.
    assert ovos.quantidade is None


def teste_suplemento_com_dose_em_texto(lido):
    """"dose diária" não é número, e jogá-lo fora perderia a instrução."""
    doses = {s.descricao: (s.quantidade, s.unidade, s.detalhe) for s in lido.suplementos}
    assert doses["Multi vitaminico"] == (None, None, "dose diária")
    assert doses["Homega 3"] == (2.0, "cps", None)
    assert doses["Ioimbina"] == (5.0, "mg", None)


def teste_o_que_nao_foi_entendido_volta_em_vez_de_sumir(lido):
    """Silêncio aqui seria pior que erro: o João não veria o que ficou de fora."""
    assert "Protocolo alimentar" in lido.nao_entendidas
    # Parêntese aberto e não fechado é anotação solta, não item de gordura.
    assert "(Berberina 1 cps)em jejum 500ml de água" in lido.nao_entendidas
    # A frase de encerramento não é comida.
    assert "Só basta fazer o que é preciso!" in lido.nao_entendidas

    for secao in lido.grupos + lido.refeicoes:
        for item in secao.itens:
            assert "Berberina" not in item.descricao
            assert "basta fazer" not in item.descricao


# ------------------------------------------------------- casos isolados


@pytest.mark.parametrize(
    "linha,descricao,quantidade,unidade",
    [
        ("Arroz branco: 200g", "Arroz branco", 200.0, "g"),
        ("Arroz branco:200 g", "Arroz branco", 200.0, "g"),
        ("Ovos: 5 und", "Ovos", 5.0, "und"),
        ("Doce leite(20g)", "Doce leite", 20.0, "g"),
        ("Cuscuz: 22,5g", "Cuscuz", 22.5, "g"),
        ("azeite: 1 colher", "Azeite", 1.0, "colher"),  # a inicial é normalizada
    ],
)
def teste_medidas(linha, descricao, quantidade, unidade):
    lido = ler_protocolo(f"Carboidratos substituição\n{linha}")
    item = lido.grupos[0].itens[0]
    assert (item.descricao, item.quantidade, item.unidade) == (
        descricao,
        quantidade,
        unidade,
    )


def teste_cabecalho_sem_item_nao_vira_secao():
    """Uma linha com dois-pontos e nada abaixo é ruído, não um grupo vazio."""
    lido = ler_protocolo("Observações:\n\nCarboidratos substituição\nArroz: 200g")
    assert [g.nome for g in lido.grupos] == ["Carboidratos"]


def teste_texto_vazio():
    lido = ler_protocolo("")
    assert (lido.grupos, lido.refeicoes, lido.suplementos) == ([], [], [])
    assert lido.deficit_kcal is None


def teste_marcadores_de_lista_nao_entram_no_nome():
    lido = ler_protocolo("Frutas:\n● maçã: 1 und\n- Melão: 200g\n— Morango: 200g")
    assert [i.descricao for i in lido.grupos[0].itens] == ["Maçã", "Melão", "Morango"]
