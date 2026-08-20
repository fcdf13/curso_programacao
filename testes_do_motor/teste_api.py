"""A API HTTP: cada rota, e o ciclo de estudo inteiro passando por ela.

Estes testes escrevem em `respostas/` e em `.curso/progresso.json` de verdade —
não há como testar a integração com o motor sem isso. A fixture `estado_limpo`
guarda e restaura os dois.
"""

from __future__ import annotations

import json
import shutil

import pytest
from fastapi.testclient import TestClient

from curso import caminhos, registro
from curso import progresso as prog
from curso.api import criar_app

PYTHON = "A02-002"      # "Par ou ímpar"
PANDAS = "B05-001"      # "Produtos ativos e caros"

# O editor manda só o corpo do exercício; o cabeçalho (enunciado + META) fica no
# servidor e é recolocado na hora de gravar.
CERTO_PYTHON = "def resolver(numero: int) -> bool:\n    return numero % 2 == 0\n"
ERRADO_PYTHON = "def resolver(numero: int) -> bool:\n    return numero % 2 == 1\n"


@pytest.fixture
def cliente(tmp_path):
    """Client da API com o progresso apontado para um arquivo descartável."""
    arquivo = tmp_path / "progresso.json"
    original = prog.Progresso.carregar

    @classmethod
    def carregar_do_tmp(cls, alvo=None):
        return original.__func__(cls, alvo or arquivo)

    prog.Progresso.carregar = carregar_do_tmp
    try:
        with TestClient(criar_app(None)) as c:
            yield c
    finally:
        prog.Progresso.carregar = original


@pytest.fixture(autouse=True)
def respostas_intactas():
    """Devolve `respostas/` ao estado anterior — os testes escrevem lá de verdade."""
    pasta = caminhos.raiz() / caminhos.RESPOSTAS
    guardado = pasta.exists() and any(pasta.iterdir())
    copia = None
    if guardado:
        copia = pasta.parent / "_respostas_do_teste"
        shutil.copytree(pasta, copia, dirs_exist_ok=True)
    yield
    for identificador in (PYTHON, PANDAS):
        registro.por_id(identificador).caminho_resposta.unlink(missing_ok=True)
    if copia is not None:
        shutil.copytree(copia, pasta, dirs_exist_ok=True)
        shutil.rmtree(copia)


# --------------------------------------------------------------------- catálogo --

def teste_lista_o_catalogo_inteiro(cliente):
    corpo = cliente.get("/api/exercicios").json()
    assert len(corpo) >= 90
    assert [e["id"] for e in corpo] == sorted(e["id"] for e in corpo)
    primeiro = corpo[0]
    assert primeiro["nome_do_bloco"] == "Python"
    assert primeiro["estado"] == prog.NOVO


def teste_filtra_por_bloco_e_por_busca(cliente):
    so_sql = cliente.get("/api/exercicios", params={"bloco": "C"}).json()
    assert so_sql and all(e["bloco"] == "C" for e in so_sql)

    achados = cliente.get("/api/exercicios", params={"busca": "fizzbuzz"}).json()
    assert [e["id"] for e in achados] == ["A06-015"]


def teste_detalhe_traz_enunciado_teoria_e_esqueleto(cliente):
    corpo = cliente.get(f"/api/exercicios/{PYTHON}").json()
    assert corpo["titulo"] == "Par ou ímpar"
    assert "resto da divisão" in corpo["enunciado"]
    assert corpo["teoria"].startswith("# Módulo A2")
    assert corpo["codigo"].startswith("def resolver(numero: int) -> bool:")
    assert "META" not in corpo["codigo"], "as dicas não podem vazar para o editor"
    assert "Exemplos:" not in corpo["codigo"], "o enunciado já está renderizado ao lado"
    assert corpo["dicas_liberadas"] == [], "dica nenhuma vem de graça"
    assert corpo["total_de_dicas"] == 3
    assert corpo["ja_tentou"] is False


def teste_exercicio_inexistente_da_404(cliente):
    assert cliente.get("/api/exercicios/Z99-999").status_code == 404


# ---------------------------------------------------------------------- escrita --

def teste_salva_e_recupera_a_resposta(cliente):
    cliente.put(f"/api/exercicios/{PYTHON}/resposta", json={"codigo": CERTO_PYTHON})
    assert cliente.get(f"/api/exercicios/{PYTHON}").json()["codigo"] == CERTO_PYTHON


# --------------------------------------------------------------------- correção --

def teste_resposta_certa_passa_e_agenda_revisao(cliente):
    corpo = cliente.post(f"/api/exercicios/{PYTHON}/check",
                         json={"codigo": CERTO_PYTHON}).json()
    assert corpo["ok"] is True
    assert corpo["passaram"] == 4 and corpo["falharam"] == 0
    assert corpo["dados"] is None
    assert corpo["ficha"]["estado"] == prog.RESOLVIDO
    assert corpo["ficha"]["proxima_revisao"], "acertar precisa agendar a revisão"


def teste_resposta_errada_devolve_falha_estruturada(cliente):
    corpo = cliente.post(f"/api/exercicios/{PYTHON}/check",
                         json={"codigo": ERRADO_PYTHON}).json()
    assert corpo["ok"] is False
    assert corpo["falharam"] >= 1
    assert corpo["ficha"]["estado"] == prog.EM_ANDAMENTO

    dados = corpo["dados"]
    assert dados["tipo"] == "valor_escalar"
    assert dados["esperado"] is True and dados["obtido"] is False


def teste_falha_de_dataframe_vem_como_tabela(cliente):
    """O payload que existe para a interface desenhar esperado × obtido."""
    esqueleto = registro.por_id(PANDAS).corpo_atual()
    sem_filtro_de_ativo = esqueleto.replace(
        "    ...", '    return produtos[produtos["preco"] >= preco_minimo]'
    )
    corpo = cliente.post(f"/api/exercicios/{PANDAS}/check",
                         json={"codigo": sem_filtro_de_ativo}).json()

    dados = corpo["dados"]
    assert dados["tipo"] == "numero_de_linhas"
    assert dados["esperado"]["colunas"] == ["nome", "preco", "ativo"]
    assert dados["esperado"]["total"] == 1
    assert dados["obtido"]["total"] == 2
    assert dados["obtido"]["linhas"][1][0] == "Notebook"
    json.dumps(dados)          # precisa continuar serializável


def teste_corrigir_sem_corpo_usa_o_que_esta_salvo(cliente):
    cliente.put(f"/api/exercicios/{PYTHON}/resposta", json={"codigo": CERTO_PYTHON})
    assert cliente.post(f"/api/exercicios/{PYTHON}/check").json()["ok"] is True


# ------------------------------------------------------------- dicas e gabarito --

def teste_dicas_saem_uma_de_cada_vez(cliente):
    vistas = [cliente.post(f"/api/exercicios/{PYTHON}/dica").json() for _ in range(3)]
    assert [d["numero"] for d in vistas] == [1, 2, 3]
    assert all(d["total"] == 3 for d in vistas)
    assert "%" in vistas[0]["texto"]
    assert cliente.post(f"/api/exercicios/{PYTHON}/dica").status_code == 409

    liberadas = cliente.get(f"/api/exercicios/{PYTHON}").json()["dicas_liberadas"]
    assert len(liberadas) == 3


def teste_gabarito_exige_uma_tentativa_antes(cliente):
    assert cliente.get(f"/api/exercicios/{PYTHON}/solucao").status_code == 409

    forcado = cliente.get(f"/api/exercicios/{PYTHON}/solucao",
                          params={"forcar": True})
    assert forcado.status_code == 200
    assert forcado.json()["codigo"].startswith("def resolver(")
    assert "META" not in forcado.json()["codigo"]


def teste_gabarito_liberado_depois_de_tentar(cliente):
    cliente.post(f"/api/exercicios/{PYTHON}/check", json={"codigo": ERRADO_PYTHON})
    assert cliente.get(f"/api/exercicios/{PYTHON}/solucao").status_code == 200


# ---------------------------------------------------------- revisão e progresso --

def teste_plano_do_dia(cliente):
    corpo = cliente.get("/api/hoje", params={"quantidade": 3}).json()
    assert len(corpo["novos"]) == 3
    assert corpo["revisoes"] == []

    cliente.post(f"/api/exercicios/{PYTHON}/check", json={"codigo": CERTO_PYTHON})
    depois = cliente.get("/api/hoje").json()
    assert PYTHON not in [e["id"] for e in depois["novos"]], "resolvido sai da fila"
    assert depois["sequencia"] == 1


def teste_revisao_arquiva_a_resposta_e_devolve_o_esqueleto(cliente, tmp_path):
    cliente.post(f"/api/exercicios/{PYTHON}/check", json={"codigo": CERTO_PYTHON})

    # Adianta o relógio no arquivo de progresso para a revisão vencer.
    arquivo = prog.Progresso.carregar().arquivo
    estado = json.loads(arquivo.read_text(encoding="utf-8"))
    estado["exercicios"][PYTHON]["proxima_revisao"] = "2020-01-01"
    arquivo.write_text(json.dumps(estado), encoding="utf-8")

    fila = cliente.get("/api/revisao").json()
    assert [e["id"] for e in fila] == [PYTHON]
    assert fila[0]["vencida"] is True

    devolvido = cliente.post(f"/api/revisao/{PYTHON}/preparar").json()["codigo"]
    assert devolvido.rstrip().endswith("..."), "a revisão devolve o esqueleto em branco"
    assert "numero % 2 == 0" not in devolvido


def teste_painel_de_progresso(cliente):
    antes = cliente.get("/api/progresso").json()
    assert antes["total"] >= 90
    assert antes["feitos"] == 0
    assert len(antes["previsao"]) == 30
    assert any(m["nome_do_modulo"] == "Laços" for m in antes["modulos"])

    cliente.post(f"/api/exercicios/{PYTHON}/check", json={"codigo": CERTO_PYTHON})
    depois = cliente.get("/api/progresso").json()
    assert depois["feitos"] == 1
    assert depois["agendados"] == 1
    assert sum(d["quantidade"] for d in depois["previsao"]) == 1
    assert len(depois["dias_praticados"]) == 1

    modulo = next(m for m in depois["modulos"]
                  if m["nome_do_modulo"] == "Números e operadores")
    assert (modulo["feitos"], modulo["total"]) == (1, 10)


def teste_o_editor_nunca_recebe_o_meta(cliente):
    """A regressão que motivou separar cabeçalho de corpo.

    O META guarda as três dicas do exercício, e a última costuma ser a resposta.
    Mandar o arquivo inteiro para o editor entregaria o gabarito de graça.
    """
    for identificador in ("A06-015", PANDAS, "C01-001"):
        codigo = cliente.get(f"/api/exercicios/{identificador}").json()["codigo"]
        assert "META" not in codigo
        assert "dicas" not in codigo
        assert "ENUNCIADO" not in codigo


def teste_salvar_reconstitui_o_arquivo_completo(cliente):
    """O arquivo em respostas/ continua válido para o CLI e para o pytest."""
    cliente.put(f"/api/exercicios/{PYTHON}/resposta", json={"codigo": CERTO_PYTHON})

    gravado = registro.por_id(PYTHON).caminho_resposta.read_text(encoding="utf-8")
    assert gravado.startswith('"""'), "o enunciado volta ao topo do arquivo"
    assert '"id": "A02-002"' in gravado, "o META volta junto"
    assert gravado.endswith(CERTO_PYTHON)
