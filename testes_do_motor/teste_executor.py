"""O caminho completo de `curso check`: rodar o teste e traduzir o resultado.

Cada teste aqui dispara um pytest em subprocesso, então este arquivo é o mais
lento do repositório — e o mais importante, porque cobre o que o aluno vê.
"""

import pytest

from curso import caminhos, executor, registro


@pytest.fixture(scope="module")
def exercicio():
    return registro.por_id("A02-002")   # "Par ou ímpar": pequeno e sem dependências


def teste_gabarito_passa(exercicio):
    resultado = executor.corrigir(exercicio, fonte=caminhos.SOLUCOES)
    assert resultado.ok
    assert resultado.passaram == 4
    assert resultado.falharam == 0
    assert resultado.primeira_falha == ""


def teste_esqueleto_vazio_reprova_falando_de_return(exercicio):
    resultado = executor.corrigir(exercicio, fonte=caminhos.EXERCICIOS)
    assert not resultado.ok
    assert resultado.falharam > 0
    assert "return" in resultado.primeira_falha
    assert "assert" not in resultado.primeira_falha, "nada de jargão de pytest"


@pytest.fixture
def resposta_provisoria(exercicio):
    """Escreve uma resposta de verdade em respostas/ e a remove no fim.

    O pytest roda em subprocesso e resolve os caminhos sozinho, então não adianta
    monkeypatch: a resposta precisa existir mesmo no disco.
    """
    alvo = exercicio.caminho_resposta
    tinha_antes = alvo.exists()
    guardado = alvo.read_text(encoding="utf-8") if tinha_antes else None
    alvo.parent.mkdir(parents=True, exist_ok=True)

    def escrever(codigo: str):
        alvo.write_text(codigo, encoding="utf-8")
        return alvo

    yield escrever

    if tinha_antes:
        alvo.write_text(guardado, encoding="utf-8")
    else:
        alvo.unlink(missing_ok=True)


def teste_resposta_errada_mostra_os_dois_valores(exercicio, resposta_provisoria):
    # Troca par por ímpar: passa em alguns casos e falha em outros.
    resposta_provisoria("def resolver(numero):\n    return numero % 2 == 1\n")

    resultado = executor.corrigir(exercicio, fonte=caminhos.RESPOSTAS)
    assert not resultado.ok
    assert resultado.falharam >= 1
    assert "esperado" in resultado.primeira_falha
    assert "obtido" in resultado.primeira_falha
    assert resultado.nome_da_falha.startswith("teste_")


def teste_erro_de_sintaxe_vira_mensagem_e_nao_traceback(exercicio, resposta_provisoria):
    resposta_provisoria("def resolver(numero)\n    return True\n")

    resultado = executor.corrigir(exercicio, fonte=caminhos.RESPOSTAS)
    assert not resultado.ok
    assert "erro de sintaxe" in resultado.primeira_falha
    assert "linha 1" in resultado.primeira_falha


def teste_laco_infinito_e_interrompido(exercicio, resposta_provisoria, monkeypatch):
    monkeypatch.setattr(executor, "TEMPO_LIMITE_S", 3)
    resposta_provisoria("def resolver(numero):\n    while True:\n        pass\n")

    resultado = executor.corrigir(exercicio, fonte=caminhos.RESPOSTAS)
    assert not resultado.ok
    assert "laço que nunca termina" in resultado.primeira_falha


def teste_mensagem_perde_o_prefixo_da_excecao():
    bruto = (
        "    def teste_x():\n"
        ">       verificar(1, 2)\n"
        "E       curso.comparar.ErroDidatico: O resultado não bate.\n"
        "E       \n"
        "E           esperado: 2\n"
    )
    limpa = executor._extrair_mensagem(bruto)
    assert limpa.startswith("O resultado não bate.")
    assert "ErroDidatico" not in limpa
    assert "esperado: 2" in limpa


def teste_sem_linhas_de_erro_devolve_o_bruto():
    assert executor._extrair_mensagem("qualquer coisa") == "qualquer coisa"


def teste_exercicio_sem_teste_reclama(monkeypatch, tmp_path):
    ex = registro.por_id("A02-002")
    monkeypatch.setattr(
        type(ex), "caminho_teste", property(lambda self: tmp_path / "nao_existe.py")
    )
    with pytest.raises(FileNotFoundError, match="sem arquivo de teste"):
        executor.corrigir(ex)
