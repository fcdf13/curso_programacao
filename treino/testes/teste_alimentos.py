"""O catálogo nutricional: nasce vazio e só recebe tabela com procedência."""

from __future__ import annotations

import pytest

from jf.alimentos import importar, mapear_colunas
from jf.modelos import Alimento, Papel

TACO = """id,descricao,energia_kcal,proteina_g,carboidrato_g,lipideos_g,fibra_alimentar_g
1,"Arroz, tipo 1, cozido",128,2.5,28.1,0.2,1.6
2,"Feijao, carioca, cozido",76,4.8,13.6,0.5,8.5
3,"Ovo, de galinha, inteiro, cozido",146,13.3,0.6,9.5,NA
"""


def escrever(tmp_path, conteudo, nome="taco.csv"):
    caminho = tmp_path / nome
    caminho.write_text(conteudo, encoding="utf-8")
    return caminho


def teste_importa_a_taco(sessao_de_banco, tmp_path):
    resultado = importar(sessao_de_banco, escrever(tmp_path, TACO))

    assert (resultado.lidas, resultado.novos, resultado.ignoradas) == (3, 3, 0)
    arroz = sessao_de_banco.query(Alimento).filter_by(nome="Arroz, tipo 1, cozido").one()
    assert (arroz.kcal_100g, arroz.proteina_100g, arroz.fibra_100g) == (128.0, 2.5, 1.6)


def teste_nao_medido_nao_vira_zero(sessao_de_banco, tmp_path):
    """A TACO escreve "NA" e "Tr"; virar 0 seria afirmar o que ninguém mediu."""
    importar(sessao_de_banco, escrever(tmp_path, TACO))
    ovo = sessao_de_banco.query(Alimento).filter(Alimento.nome.like("Ovo%")).one()
    assert ovo.fibra_100g is None

    traco = "alimento,kcal,proteina,carboidrato,gordura,fibra\nÓleo,884,Tr,Tr,100,*\n"
    importar(sessao_de_banco, escrever(tmp_path, traco, "traco.csv"))
    oleo = sessao_de_banco.query(Alimento).filter_by(nome="Óleo").one()
    assert (oleo.proteina_100g, oleo.fibra_100g) == (None, None)
    assert oleo.gordura_100g == 100.0


def teste_reimportar_atualiza_em_vez_de_duplicar(sessao_de_banco, tmp_path):
    importar(sessao_de_banco, escrever(tmp_path, TACO))
    corrigido = TACO.replace("128,2.5", "130,2.6")
    resultado = importar(sessao_de_banco, escrever(tmp_path, corrigido, "taco2.csv"))

    assert (resultado.novos, resultado.atualizados) == (0, 3)
    assert sessao_de_banco.query(Alimento).count() == 3
    arroz = sessao_de_banco.query(Alimento).filter_by(nome="Arroz, tipo 1, cozido").one()
    assert arroz.kcal_100g == 130.0


def teste_cabecalho_com_acento_e_unidade_entre_parenteses():
    """As versões em CSV da TACO que circulam não combinam nos nomes."""
    assert mapear_colunas(["Descrição", "Energia (kcal)", "Proteína (g)"]) == {
        "nome": "Descrição",
        "kcal_100g": "Energia (kcal)",
        "proteina_100g": "Proteína (g)",
    }


def teste_cabecalho_do_open_food_facts():
    colunas = mapear_colunas(
        [
            "code",
            "product_name",
            "brands",
            "energy-kcal_100g",
            "proteins_100g",
            "carbohydrates_100g",
            "fat_100g",
            "fiber_100g",
        ]
    )
    assert colunas == {
        "codigo_de_barras": "code",
        "nome": "product_name",
        "marca": "brands",
        "kcal_100g": "energy-kcal_100g",
        "proteina_100g": "proteins_100g",
        "carboidrato_100g": "carbohydrates_100g",
        "gordura_100g": "fat_100g",
        "fibra_100g": "fiber_100g",
    }


def teste_marca_separa_dois_produtos_de_mesmo_nome(sessao_de_banco, tmp_path):
    conteudo = (
        "product_name,brands,energy-kcal_100g\n"
        "Whey Protein,Growth,380\n"
        "Whey Protein,Max Titanium,400\n"
    )
    resultado = importar(sessao_de_banco, escrever(tmp_path, conteudo), fonte="off")
    assert resultado.novos == 2
    assert sessao_de_banco.query(Alimento).filter_by(nome="Whey Protein").count() == 2


def teste_sem_coluna_de_nome_o_comando_avisa(sessao_de_banco, tmp_path):
    with pytest.raises(ValueError, match="nome do alimento"):
        importar(sessao_de_banco, escrever(tmp_path, "kcal,proteina\n100,10\n"))


def teste_linha_sem_numero_nenhum_e_ignorada(sessao_de_banco, tmp_path):
    conteudo = "alimento,kcal\nArroz,128\nSó um título,\n"
    resultado = importar(sessao_de_banco, escrever(tmp_path, conteudo))
    assert (resultado.novos, resultado.ignoradas) == (1, 1)


def teste_a_busca_encontra_o_que_foi_importado(cliente, criar_usuario, sessao_de_banco, tmp_path):
    criar_usuario("João Filho", "joao@exemplo.com", Papel.TREINADOR)
    importar(sessao_de_banco, escrever(tmp_path, TACO))

    sessao = cliente("joao@exemplo.com")
    achados = sessao.get("/api/alimentos", params={"busca": "arroz"}).json()
    assert [a["nome"] for a in achados] == ["Arroz, tipo 1, cozido"]
    assert achados[0]["kcal_100g"] == 128.0

    # Uma letra só devolveria meio catálogo a cada tecla.
    assert sessao.get("/api/alimentos", params={"busca": "a"}).json() == []


def teste_o_catalogo_nasce_vazio(cliente, criar_usuario):
    """Nenhum valor nutricional embutido: o que não foi medido não é chutado."""
    criar_usuario("João Filho", "joao@exemplo.com", Papel.TREINADOR)
    assert cliente("joao@exemplo.com").get(
        "/api/alimentos", params={"busca": "arroz"}
    ).json() == []


def teste_busca_exige_login(cliente):
    assert cliente().get("/api/alimentos", params={"busca": "arroz"}).status_code == 401
