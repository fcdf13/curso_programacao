"""O catálogo precisa ler os metadados de arquivos que podem estar quebrados."""

import pytest

from curso import registro
from curso.registro import ErroDeCatalogo


def teste_catalogo_nao_esta_vazio():
    assert len(registro.catalogo()) >= 90


def teste_ids_sao_unicos_e_estao_em_ordem():
    ids = [ex.id for ex in registro.catalogo()]
    assert len(ids) == len(set(ids))
    assert ids == sorted(ids)


def teste_todo_exercicio_tem_teste_e_gabarito():
    faltando = [
        ex.id for ex in registro.catalogo()
        if not ex.caminho_teste.exists() or not ex.caminho_solucao.exists()
    ]
    assert faltando == []


def teste_todo_exercicio_tem_enunciado_e_dicas():
    sem_enunciado = [ex.id for ex in registro.catalogo() if len(ex.enunciado) < 40]
    sem_dicas = [ex.id for ex in registro.catalogo() if not ex.dicas]
    assert sem_enunciado == []
    assert sem_dicas == []


def teste_pre_requisito_sempre_vem_antes():
    for ex in registro.catalogo():
        for pre in ex.requer:
            assert pre < ex.id, f"{ex.id} depende de {pre}, que vem depois"


def teste_meta_e_lido_sem_importar_o_arquivo(tmp_path, monkeypatch):
    """O ponto principal: um arquivo com código quebrado ainda precisa ser catalogado."""
    quebrado = tmp_path / "ex_001_teste.py"
    quebrado.write_text(
        '"""Enunciado de mentirinha."""\n\n'
        'META = {"id": "A01-001", "titulo": "Teste", "nivel": 1}\n\n'
        "def resolver():\n"
        "    return 1 / 0    # explodiria se fosse importado\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(registro.caminhos, "pasta_exercicios", lambda: tmp_path)
    ex = registro._montar(quebrado)
    assert ex.id == "A01-001"
    assert ex.enunciado == "Enunciado de mentirinha."


def teste_arquivo_sem_meta_acusa():
    with pytest.raises(ErroDeCatalogo, match="META"):
        registro._ler_meta_python('"""oi"""\n', __import__("pathlib").Path("x.py"))


def teste_busca_por_id_completo_e_por_numero():
    assert registro.por_id("A01-001").titulo == "Olá, Aurora"
    assert registro.por_id("a01-001").id == "A01-001"
    with pytest.raises(ErroDeCatalogo, match="ambíguo"):
        registro.por_id("001")


def teste_id_inexistente_reclama():
    with pytest.raises(ErroDeCatalogo, match="Não existe"):
        registro.por_id("Z99-999")


def teste_busca_por_tema():
    achados = registro.buscar("fizzbuzz")
    assert [ex.id for ex in achados] == ["A06-015"]
    assert len(registro.buscar("lista")) > 5


def teste_nomes_amigaveis():
    ex = registro.por_id("A06-015")
    assert ex.bloco == "A"
    assert ex.nome_do_bloco == "Python"
    assert ex.nome_do_modulo == "Laços"
    assert ex.estrelas == "●●●○○"


def teste_gabarito_mostra_so_o_codigo():
    codigo = registro.por_id("A02-002").codigo_da_solucao()
    assert codigo.startswith("def resolver(")
    assert "META" not in codigo
    assert "Exemplos:" not in codigo, "o enunciado não precisa aparecer de novo"


def teste_gabarito_de_sql_perde_os_comentarios_de_bloco():
    codigo = registro.por_id("C01-001").codigo_da_solucao()
    assert codigo.upper().startswith("--") or codigo.upper().startswith("SELECT")
    assert "META" not in codigo
    assert "ENUNCIADO" not in codigo
