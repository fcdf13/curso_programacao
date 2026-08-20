"""O estado do aluno: tentativas, agendamento e o arquivamento da revisão."""

from datetime import date, timedelta

import pytest

from curso import progresso as prog

HOJE = date(2026, 3, 1)


@pytest.fixture
def p(tmp_path):
    return prog.Progresso(arquivo=tmp_path / "progresso.json")


def teste_exercicio_novo_comeca_zerado(p):
    ficha = p.ficha("A01-001")
    assert ficha.estado == prog.NOVO
    assert ficha.tentativas == 0
    assert not ficha.vencida(HOJE)


def teste_errar_marca_em_andamento_e_nao_agenda(p):
    ficha = p.registrar_tentativa("A01-001", acertou=False, hoje=HOJE)
    assert ficha.estado == prog.EM_ANDAMENTO
    assert ficha.tentativas == 1
    assert ficha.proxima_revisao == ""


def teste_acertar_de_primeira_agenda_para_amanha(p):
    ficha = p.registrar_tentativa("A01-001", acertou=True, hoje=HOJE)
    assert ficha.estado == prog.RESOLVIDO
    assert ficha.tentativas_ate_acertar == 1
    assert ficha.proxima_revisao == "2026-03-02"


def teste_tentativas_ate_acertar_conta_so_a_primeira_rodada(p):
    p.registrar_tentativa("A01-001", acertou=False, hoje=HOJE)
    p.registrar_tentativa("A01-001", acertou=False, hoje=HOJE)
    ficha = p.registrar_tentativa("A01-001", acertou=True, hoje=HOJE)
    assert ficha.tentativas_ate_acertar == 3
    assert ficha.facilidade < prog.srs.FACILIDADE_INICIAL, "errar duas vezes penaliza"


def teste_revisao_bem_sucedida_estica_o_intervalo(p):
    p.registrar_tentativa("A01-001", acertou=True, hoje=HOJE)
    primeiro = p.ficha("A01-001").intervalo_dias

    depois = HOJE + timedelta(days=1)
    ficha = p.registrar_tentativa("A01-001", acertou=True, hoje=depois)
    assert ficha.revisoes == 1
    assert ficha.intervalo_dias > primeiro


def teste_vencidas_traz_so_o_que_passou_da_data(p):
    p.registrar_tentativa("A01-001", acertou=True, hoje=HOJE)
    assert p.vencidas(HOJE) == []
    assert [f.id for f in p.vencidas(HOJE + timedelta(days=1))] == ["A01-001"]


def teste_quem_viu_a_solucao_volta_para_amanha(p):
    p.registrar_solucao_vista("A01-001")
    ficha = p.registrar_tentativa("A01-001", acertou=True, hoje=HOJE)
    assert ficha.intervalo_dias == 1
    assert ficha.viu_solucao is False, "a marca vale só para a rodada em que foi vista"


def teste_estado_sobrevive_ao_disco(p):
    p.registrar_tentativa("A05-006", acertou=True, hoje=HOJE)
    p.registrar_dica("A05-006")
    p.salvar()

    relido = prog.Progresso.carregar(p.arquivo)
    assert relido.ficha("A05-006").estado == prog.RESOLVIDO
    assert relido.ficha("A05-006").dicas_vistas == 1
    assert relido.resolvidos() == {"A05-006"}


def teste_arquivo_de_outra_versao_e_recusado(p):
    p.arquivo.write_text('{"versao": 999, "exercicios": {}}', encoding="utf-8")
    with pytest.raises(ValueError, match="outra versão"):
        prog.Progresso.carregar(p.arquivo)


def teste_sequencia_de_dias(p):
    p.dias_praticados = [
        (HOJE - timedelta(days=n)).isoformat() for n in (0, 1, 2, 5)
    ]
    assert p.sequencia_de_dias(HOJE) == 3


def teste_sequencia_zera_depois_de_dois_dias_parado(p):
    p.dias_praticados = [(HOJE - timedelta(days=3)).isoformat()]
    assert p.sequencia_de_dias(HOJE) == 0


def teste_preparar_revisao_arquiva_a_resposta(p):
    from curso import registro

    exercicio = registro.por_id("A01-001")
    exercicio.caminho_resposta.parent.mkdir(parents=True, exist_ok=True)
    exercicio.caminho_resposta.write_text("# minha tentativa\n", encoding="utf-8")

    guardado = p.preparar_revisao("A01-001")

    assert guardado is not None and guardado.exists()
    assert guardado.read_text(encoding="utf-8") == "# minha tentativa\n"
    assert not exercicio.caminho_resposta.exists(), "a resposta some para você refazer"
    guardado.unlink()


def teste_preparar_revisao_sem_resposta_nao_quebra(p):
    from curso import registro

    registro.por_id("A02-001").caminho_resposta.unlink(missing_ok=True)
    assert p.preparar_revisao("A02-001") is None
