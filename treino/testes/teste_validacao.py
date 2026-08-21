"""As mensagens de erro que o aluno lê.

O padrão do Pydantic é "Input should be less than 400", em inglês e com o nome
cru do campo. Quem lê é alguém no vestiário tentando registrar o peso: ver isso
é o mesmo que não ver nada. Os testes de concordância existem porque "Os horas
de sono precisa ser 16" faz a pessoa reler para entender.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from jf import esquemas
from jf.modelos import Papel
from jf.validacao import nome_do_campo, traduzir


def mensagens(modelo, **dados) -> list[str]:
    with pytest.raises(ValidationError) as capturado:
        modelo(**dados)
    return [traduzir(erro) for erro in capturado.value.errors()]


def primeira(modelo, **dados) -> str:
    return mensagens(modelo, **dados)[0]


# ------------------------------------------------------------ concordância


@pytest.mark.parametrize(
    "campo,esperado",
    [
        ("peso_kg", "o peso"),
        ("horas_de_sono", "as horas de sono"),
        ("passos_por_dia", "os passos por dia"),
        ("qualidade_do_sono", "a qualidade do sono"),
        ("altura_cm", "a altura"),
        ("descanso_s", "o descanso"),
        ("series", "as séries"),
        ("reps", "as repetições"),
        ("nome", "o nome"),
        ("observacoes", "as observações"),
    ],
)
def teste_o_campo_vem_com_artigo_certo(campo, esperado):
    assert nome_do_campo(campo).com_artigo == esperado


def teste_o_verbo_concorda_com_o_campo():
    assert primeira(esquemas.NovoCheckin, horas_de_sono=30) == (
        "As horas de sono precisam ser no máximo 16."
    )
    assert primeira(esquemas.NovoCheckin, peso_kg=900) == (
        "O peso precisa ser menor que 400."
    )
    assert primeira(esquemas.NovoCheckin, passos_por_dia=-5) == (
        "Os passos por dia precisam ser pelo menos 0."
    )


def teste_gender_sai_da_terminacao_quando_nao_ha_apelido():
    # "qualidade" é feminino pela terminação, sem entrada na tabela de nomes.
    assert nome_do_campo("qualidade_do_sono").artigo == "a"
    assert nome_do_campo("objetivo").artigo == "o"


def teste_o_acento_que_o_nome_do_campo_nao_tem(monkeypatch):
    assert "disposição" in primeira(esquemas.NovoCheckin, disposicao=9)
    assert "recuperação" in primeira(esquemas.NovoCheckin, recuperacao=0)


# ------------------------------------------------------------- por tipo


def teste_campo_faltando():
    assert primeira(esquemas.NovaPrescricao) == "Falta preencher o exercício."


def teste_numero_fora_da_faixa():
    assert primeira(esquemas.NovaPrescricao, exercicio_id=1, series=50) == (
        "As séries precisam ser no máximo 20."
    )
    assert primeira(esquemas.NovaPrescricao, exercicio_id=1, carga_alvo_kg=0) == (
        "A carga alvo precisa ser maior que 0."
    )


def teste_texto_no_lugar_de_numero():
    """No imperativo, a frase serve ao singular e ao plural sem tropeçar."""
    assert primeira(esquemas.NovoCheckin, peso_kg="muito") == (
        "Escreva o peso como número."
    )
    assert primeira(esquemas.NovaSerie, reps="oito") == (
        "Escreva as repetições como número."
    )


def teste_texto_longo_demais():
    assert primeira(esquemas.ProtocoloBase, nome="x" * 200) == (
        "O nome passa de 120 caracteres."
    )


def teste_senha_curta():
    assert primeira(
        esquemas.TrocaDeSenha, senha_atual="a", senha_nova="curta"
    ) == "A senha nova precisa de pelo menos 10 caracteres."


def teste_data_invalida():
    assert primeira(esquemas.NovoCheckin, semana="ontem") == (
        "A semana precisa ser uma data válida."
    )


def teste_opcao_que_nao_existe():
    """O "or" do Pydantic não pode ficar em inglês no meio da frase."""
    frase = primeira(
        esquemas.NovoAluno, nome="Ana", email="a@b.com", senha="x" * 10, sexo="nenhum"
    )
    assert frase == (
        "O sexo não aceita esse valor. Use 'masculino', 'feminino' ou 'outro'."
    )
    assert " or " not in frase


def teste_email_invalido():
    assert primeira(
        esquemas.NovoAluno, nome="Ana", email="nao-e-email", senha="x" * 10
    ) == "Esse email não parece um email."


def teste_a_validacao_escrita_a_mao_passa_inteira():
    """Essas já nascem em português; traduzir por cima só as estragaria."""
    assert primeira(
        esquemas.NovaPrescricao, exercicio_id=1, reps_min=12, reps_max=8
    ) == "O máximo de repetições não pode ser menor que o mínimo."

    assert primeira(esquemas.ItemDaRefeicaoBase) == (
        "O item precisa de uma descrição ou de um grupo."
    )


def teste_nenhuma_mensagem_sai_em_ingles():
    """Uma varredura por resíduo, para o que não tem teste próprio."""
    suspeitas = ("Input should", "String should", "Value error", "valid", " or ", "field")
    casos = [
        (esquemas.NovoCheckin, {"peso_kg": 900}),
        (esquemas.NovoCheckin, {"peso_kg": "x"}),
        (esquemas.NovoCheckin, {"semana": "ontem"}),
        (esquemas.NovoCheckin, {"observacoes": "x" * 5000}),
        (esquemas.NovoAluno, {"nome": "A", "email": "a@b.com", "senha": "curta"}),
        (esquemas.NovoAluno, {"nome": "Ana", "email": "x", "senha": "x" * 10}),
        (esquemas.NovaPrescricao, {}),
        (esquemas.NovaSerie, {"reps": "oito"}),
        (esquemas.MarcacaoDaRefeicao, {"seguiu": "talvez"}),
        (esquemas.PedidoDeEstimativa, {"carga_kg": 0, "reps": 5}),
        (esquemas.NovaPeriodizacao, {"nome": "x", "semanas": 99}),
        (esquemas.TrocaDeSenha, {"senha_atual": "a", "senha_nova": "curta"}),
    ]
    for modelo, dados in casos:
        for frase in mensagens(modelo, **dados):
            for suspeita in suspeitas:
                assert suspeita not in frase, f"{frase!r} tem {suspeita!r}"


# ------------------------------------------------------- pela API mesmo


def teste_a_api_devolve_a_frase_traduzida(cliente, criar_usuario, criar_aluno):
    joao = criar_usuario("João Filho", "joao@exemplo.com", Papel.TREINADOR)
    filipe = criar_aluno("Filipe", "filipe@exemplo.com", joao)

    resposta = cliente("filipe@exemplo.com").post(
        f"/api/alunos/{filipe.id}/checkins", json={"peso_kg": 900}
    )
    assert resposta.status_code == 422
    assert resposta.json()["detail"][0]["msg"] == "O peso precisa ser menor que 400."


def teste_a_api_mantem_o_formato_por_campo(cliente, criar_usuario):
    """A tela sabe achatar `detail`; trocar a forma para trocar o idioma quebraria."""
    criar_usuario("João Filho", "joao@exemplo.com", Papel.TREINADOR)
    resposta = cliente().post("/api/entrar", json={"email": "a@b.com"})

    corpo = resposta.json()
    assert resposta.status_code == 422
    assert isinstance(corpo["detail"], list)
    assert corpo["detail"][0]["loc"] == ["body", "senha"]
    assert corpo["detail"][0]["msg"] == "Falta preencher a senha."
