"""As mensagens de erro são o produto: cada modo de falha precisa dizer o que houve."""

import pandas as pd
import pytest

from curso.comparar import ErroDidatico, verificar


def mensagem_de(chamada) -> str:
    with pytest.raises(ErroDidatico) as capturado:
        chamada()
    return str(capturado.value)


# ------------------------------------------------------------------ escalares --

def teste_valores_iguais_nao_reclamam():
    verificar(5, 5)
    verificar("a", "a")
    verificar(0.1 + 0.2, 0.3)


def teste_none_avisa_sobre_o_return():
    texto = mensagem_de(lambda: verificar(None, 5))
    assert "return" in texto
    assert "..." in texto


def teste_tipo_trocado_aparece_na_mensagem():
    texto = mensagem_de(lambda: verificar("4", 4))
    assert "int" in texto and "str" in texto
    assert "int(...)" in texto


def teste_float_respeita_a_tolerancia():
    verificar(1 / 3, 0.3333333333333333)
    with pytest.raises(ErroDidatico):
        verificar(0.33, 1 / 3, tolerancia=1e-9)


def teste_nan_e_igual_a_nan():
    verificar(float("nan"), float("nan"))


def teste_booleano_nao_se_confunde_com_inteiro():
    with pytest.raises(ErroDidatico):
        verificar(1, True)


# -------------------------------------------------------------------- listas --

def teste_tamanho_diferente_diz_quantos():
    texto = mensagem_de(lambda: verificar([1, 2], [1, 2, 3]))
    assert "3 itens" in texto and "2 itens" in texto


def teste_diferenca_aponta_a_posicao():
    texto = mensagem_de(lambda: verificar([1, 9, 3], [1, 2, 3]))
    assert "posição 1" in texto


def teste_ignorar_ordem_em_lista():
    verificar([3, 1, 2], [1, 2, 3], ignorar_ordem=True)


def teste_conjunto_lista_o_que_falta_e_o_que_sobra():
    texto = mensagem_de(lambda: verificar({1, 2, 9}, {1, 2, 3}))
    assert "faltam" in texto and "[3]" in texto
    assert "a mais" in texto and "[9]" in texto


def teste_dicionario_separa_chave_de_valor():
    texto = mensagem_de(lambda: verificar({"a": 1}, {"a": 1, "b": 2}))
    assert "chaves" in texto and "'b'" in texto

    texto = mensagem_de(lambda: verificar({"a": 9}, {"a": 1}))
    assert "valor difere" in texto and "'a'" in texto


# ------------------------------------------------------------------- pandas --

def teste_dataframes_iguais_passam():
    df = pd.DataFrame({"a": [1, 2], "b": ["x", "y"]})
    verificar(df.copy(), df)


def teste_coluna_faltando():
    texto = mensagem_de(lambda: verificar(
        pd.DataFrame({"a": [1]}), pd.DataFrame({"a": [1], "b": [2]})
    ))
    assert "colunas que faltam" in texto and "'b'" in texto


def teste_colunas_fora_de_ordem_tem_mensagem_propria():
    texto = mensagem_de(lambda: verificar(
        pd.DataFrame({"b": [2], "a": [1]}), pd.DataFrame({"a": [1], "b": [2]})
    ))
    assert "fora de ordem" in texto
    assert "colunas que faltam" not in texto


def teste_linhas_faltando_sugerem_o_filtro():
    texto = mensagem_de(lambda: verificar(
        pd.DataFrame({"a": [1]}), pd.DataFrame({"a": [1, 2]})
    ))
    assert "Faltam 1 linha" in texto
    assert "Filtro apertado" in texto


def teste_linhas_sobrando_sugerem_o_merge():
    texto = mensagem_de(lambda: verificar(
        pd.DataFrame({"a": [1, 2, 3]}), pd.DataFrame({"a": [1, 2]})
    ))
    assert "Sobram 1 linha" in texto
    assert "duplicatas" in texto


def teste_celula_diferente_aponta_linha_e_coluna():
    texto = mensagem_de(lambda: verificar(
        pd.DataFrame({"a": [1, 99]}), pd.DataFrame({"a": [1, 2]})
    ))
    assert "linha 1" in texto and "'a'" in texto


def teste_series_no_lugar_de_dataframe_explica_os_colchetes():
    texto = mensagem_de(lambda: verificar(
        pd.Series([1, 2], name="a"), pd.DataFrame({"a": [1, 2]})
    ))
    assert "colchetes duplos" in texto


def teste_dataframe_de_uma_coluna_no_lugar_de_series():
    texto = mensagem_de(lambda: verificar(
        pd.DataFrame({"a": [1]}), pd.Series([1], name="a")
    ))
    assert "colchetes simples" in texto


def teste_ignorar_ordem_em_dataframe():
    esperado = pd.DataFrame({"a": [1, 2], "b": ["x", "y"]})
    embaralhado = esperado.iloc[::-1]
    verificar(embaralhado, esperado, ignorar_ordem=True)
    with pytest.raises(ErroDidatico):
        verificar(embaralhado, esperado, ignorar_ordem=False)


def teste_indice_bagunçado_e_ignorado_por_padrao():
    esperado = pd.DataFrame({"a": [1, 2]})
    filtrado = pd.DataFrame({"a": [1, 2]}, index=[7, 9])
    verificar(filtrado, esperado)
    texto = mensagem_de(lambda: verificar(filtrado, esperado, ignorar_indice=False))
    assert "reset_index" in texto


def teste_dtype_so_e_cobrado_quando_pedido():
    obtido = pd.DataFrame({"a": [1.0, 2.0]})
    esperado = pd.DataFrame({"a": [1, 2]})
    verificar(obtido, esperado)
    texto = mensagem_de(
        lambda: verificar(obtido, esperado, checar_tipo_coluna=True)
    )
    assert "tipo da coluna" in texto and "astype" in texto


def teste_dica_do_exercicio_entra_na_mensagem():
    texto = mensagem_de(lambda: verificar(1, 2, dica="confira o arredondamento"))
    assert "confira o arredondamento" in texto
