"""O protocolo alimentar pela API: o João escreve, o aluno lê e marca."""

from __future__ import annotations

from datetime import date, timedelta

import pytest

from jf.modelos import Papel

PROTOCOLO = {
    "nome": "Corte — agosto",
    "deficit_kcal": 500,
    "grupos": [
        {
            "nome": "Carboidratos",
            "itens": [
                {"descricao": "Arroz branco", "quantidade": 200, "unidade": "g"},
                {"descricao": "Cuscuz", "quantidade": 225, "unidade": "g"},
                {"descricao": "Pão francês", "quantidade": 2, "unidade": "unidades"},
            ],
        },
        {
            "nome": "Proteínas",
            "itens": [
                {"descricao": "Ovos", "quantidade": 5, "unidade": "und"},
                {"descricao": "Frango", "quantidade": 200, "unidade": "g"},
            ],
        },
    ],
    "refeicoes": [
        {
            "nome": "1ª refeição — Café",
            "itens": [
                {"descricao": "Ovos"},
                {"descricao": "Pão francês"},
                {"descricao": "Azeite", "opcional": True},
                {"descricao": "Legumes", "a_gosto": True},
            ],
        },
        {
            "nome": "2ª refeição — Almoço",
            "itens": [{"descricao": "Arroz branco"}, {"descricao": "Frango"}],
        },
    ],
    "suplementos": [{"nome": "Ioimbina", "dose": "5 mg", "momento": "em jejum"}],
}


@pytest.fixture
def joao(criar_usuario):
    return criar_usuario("João Filho", "joao@exemplo.com", Papel.TREINADOR)


@pytest.fixture
def filipe(criar_aluno, joao):
    return criar_aluno("Filipe", "filipe@exemplo.com", joao)


@pytest.fixture
def protocolo(cliente, joao, filipe):
    treinador = cliente(joao.email)
    resposta = treinador.post(f"/api/alunos/{filipe.id}/protocolos", json=PROTOCOLO)
    assert resposta.status_code == 201, resposta.text
    return resposta.json()


# ---------------------------------------------------------------- gravação


def teste_criar_guarda_grupos_refeicoes_e_suplementos(protocolo):
    assert protocolo["deficit_kcal"] == 500
    assert [g["nome"] for g in protocolo["grupos"]] == ["Carboidratos", "Proteínas"]
    assert [r["nome"] for r in protocolo["refeicoes"]] == [
        "1ª refeição — Café",
        "2ª refeição — Almoço",
    ]
    assert protocolo["suplementos"][0]["dose"] == "5 mg"


def teste_a_porcao_de_cada_item_e_preservada(protocolo):
    carboidratos = protocolo["grupos"][0]
    porcoes = [i["porcao"] for i in carboidratos["itens"]]
    # A diferença entre 200 g e 225 g **é** a equivalência: se as quantidades
    # virassem uma só, a substituição passaria a mentir.
    assert porcoes == ["Arroz branco 200 g", "Cuscuz 225 g", "Pão francês 2 unidades"]


def teste_item_da_refeicao_encontra_o_grupo_do_alimento(protocolo):
    grupos = {g["nome"]: g["id"] for g in protocolo["grupos"]}
    cafe = protocolo["refeicoes"][0]
    por_nome = {i["descricao"]: i for i in cafe["itens"]}

    # "Ovos" na refeição aponta para Proteínas — é isso que permite ao aluno
    # ver por que pode trocar por frango.
    assert por_nome["Ovos"]["grupo_id"] == grupos["Proteínas"]
    assert por_nome["Pão francês"]["grupo_id"] == grupos["Carboidratos"]
    # O que não está em grupo nenhum não ganha grupo inventado.
    assert por_nome["Azeite"]["grupo_id"] is None
    assert por_nome["Legumes"]["a_gosto"] is True
    assert por_nome["Azeite"]["opcional"] is True


def teste_o_nome_do_alimento_ganha_do_nome_do_grupo(protocolo):
    """O aluno lê "Ovos", não "Proteínas": o João escolheu o alimento."""
    cafe = protocolo["refeicoes"][0]
    assert [i["descricao"] for i in cafe["itens"]][:2] == ["Ovos", "Pão francês"]


def teste_ligacao_por_nome_ignora_acento_e_caixa(cliente, joao, filipe):
    treinador = cliente(joao.email)
    resposta = treinador.post(
        f"/api/alunos/{filipe.id}/protocolos",
        json={
            "grupos": [
                {
                    "nome": "Carboidratos",
                    "itens": [{"descricao": "Pão francês", "quantidade": 2}],
                }
            ],
            "refeicoes": [{"nome": "Café", "itens": [{"descricao": "pao FRANCES"}]}],
        },
    )
    assert resposta.status_code == 201, resposta.text
    corpo = resposta.json()
    assert corpo["refeicoes"][0]["itens"][0]["grupo_id"] == corpo["grupos"][0]["id"]


def teste_item_pode_apontar_para_o_grupo_pelo_nome(cliente, joao, filipe):
    """"Coma um carboidrato" — sem escolher qual."""
    treinador = cliente(joao.email)
    resposta = treinador.post(
        f"/api/alunos/{filipe.id}/protocolos",
        json={
            "grupos": [
                {"nome": "Carboidratos", "itens": [{"descricao": "Arroz", "quantidade": 200}]}
            ],
            "refeicoes": [{"nome": "Almoço", "itens": [{"grupo": "Carboidratos"}]}],
        },
    )
    assert resposta.status_code == 201, resposta.text
    item = resposta.json()["refeicoes"][0]["itens"][0]
    assert item["descricao"] == "Carboidratos"


def teste_grupo_inexistente_e_recusado(cliente, joao, filipe):
    treinador = cliente(joao.email)
    resposta = treinador.post(
        f"/api/alunos/{filipe.id}/protocolos",
        json={"refeicoes": [{"nome": "Almoço", "itens": [{"grupo": "Nada disso"}]}]},
    )
    assert resposta.status_code == 422
    assert "Nada disso" in resposta.text


def teste_item_sem_descricao_e_sem_grupo_e_recusado(cliente, joao, filipe):
    treinador = cliente(joao.email)
    resposta = treinador.post(
        f"/api/alunos/{filipe.id}/protocolos",
        json={"refeicoes": [{"nome": "Almoço", "itens": [{"quantidade": 100}]}]},
    )
    assert resposta.status_code == 422


def teste_editar_substitui_o_conteudo_inteiro(cliente, joao, filipe, protocolo):
    treinador = cliente(joao.email)
    resposta = treinador.put(
        f"/api/protocolos/{protocolo['id']}",
        json={
            "nome": "Corte — setembro",
            "grupos": [{"nome": "Frutas", "itens": [{"descricao": "Maçã", "quantidade": 1}]}],
        },
    )
    assert resposta.status_code == 200, resposta.text
    corpo = resposta.json()
    assert corpo["nome"] == "Corte — setembro"
    assert [g["nome"] for g in corpo["grupos"]] == ["Frutas"]
    # O que saiu da tela sai do banco: um grupo órfão apareceria na tela do
    # aluno como comida que o João já tirou do protocolo.
    assert corpo["refeicoes"] == []
    assert corpo["suplementos"] == []


def teste_um_protocolo_ativo_por_aluno(cliente, joao, filipe, protocolo):
    treinador = cliente(joao.email)
    novo = treinador.post(
        f"/api/alunos/{filipe.id}/protocolos", json={"nome": "Manutenção"}
    )
    assert novo.status_code == 201

    atual = treinador.get(f"/api/alunos/{filipe.id}/protocolo").json()
    assert atual["nome"] == "Manutenção"

    lista = treinador.get(f"/api/alunos/{filipe.id}/protocolos").json()
    assert [(p["nome"], p["ativo"]) for p in lista] == [
        ("Manutenção", True),
        ("Corte — agosto", False),
    ]


def teste_protocolo_novo_inativo_nao_derruba_o_ativo(cliente, joao, filipe, protocolo):
    treinador = cliente(joao.email)
    treinador.post(
        f"/api/alunos/{filipe.id}/protocolos", json={"nome": "Rascunho", "ativo": False}
    )
    assert treinador.get(f"/api/alunos/{filipe.id}/protocolo").json()["nome"] == (
        "Corte — agosto"
    )


def teste_apagar(cliente, joao, filipe, protocolo):
    treinador = cliente(joao.email)
    assert treinador.delete(f"/api/protocolos/{protocolo['id']}").status_code == 204
    assert treinador.get(f"/api/alunos/{filipe.id}/protocolo").status_code == 404


def teste_sem_protocolo_o_aluno_recebe_404(cliente, joao, criar_aluno):
    outro = criar_aluno("Sem dieta", "sem@exemplo.com", joao)
    resposta = cliente("sem@exemplo.com").get(f"/api/alunos/{outro.id}/protocolo")
    assert resposta.status_code == 404


# -------------------------------------------------------------- permissão


def teste_aluno_le_o_proprio_protocolo(cliente, filipe, protocolo):
    resposta = cliente("filipe@exemplo.com").get(f"/api/alunos/{filipe.id}/protocolo")
    assert resposta.status_code == 200
    assert resposta.json()["id"] == protocolo["id"]


def teste_aluno_nao_escreve_protocolo(cliente, filipe, protocolo):
    aluno = cliente("filipe@exemplo.com")
    assert aluno.post(f"/api/alunos/{filipe.id}/protocolos", json=PROTOCOLO).status_code == 403
    assert aluno.put(f"/api/protocolos/{protocolo['id']}", json=PROTOCOLO).status_code == 403
    assert aluno.delete(f"/api/protocolos/{protocolo['id']}").status_code == 403


def teste_aluno_de_outro_treinador_nao_ve_o_protocolo(
    cliente, criar_usuario, criar_aluno, protocolo
):
    outro_treinador = criar_usuario("Outro", "outro@exemplo.com", Papel.TREINADOR)
    criar_aluno("Alheio", "alheio@exemplo.com", outro_treinador)

    resposta = cliente("alheio@exemplo.com").get(f"/api/protocolos/{protocolo['id']}")
    # 404 e não 403: quem não pode ver também não fica sabendo que existe.
    assert resposta.status_code == 404


def teste_sem_login_nao_ve_nada(cliente, protocolo):
    assert cliente().get(f"/api/protocolos/{protocolo['id']}").status_code == 401


# -------------------------------------------------------- leitura do texto


TEXTO = """
500 calorias total de déficit por dia

Carboidratos substituição
Arroz branco: 200g
Cuscuz: 225g

Carboidratos de baixo teor molecular:
Doce leite: 20g

1° refeição café
Arroz branco
(Azeite)

Suplementos:
Ioimbina: 5mg

Só basta fazer o que é preciso!
"""


def teste_ler_texto_devolve_rascunho(cliente, joao):
    resposta = cliente(joao.email).post(
        "/api/protocolos/ler-texto", json={"texto": TEXTO}
    )
    assert resposta.status_code == 200, resposta.text
    corpo = resposta.json()

    rascunho = corpo["protocolo"]
    assert rascunho["deficit_kcal"] == 500
    assert [g["nome"] for g in rascunho["grupos"]] == [
        "Carboidratos",
        "Carboidratos de baixo teor molecular",
    ]
    assert rascunho["refeicoes"][0]["itens"][1]["opcional"] is True
    assert rascunho["suplementos"][0] == {
        "nome": "Ioimbina",
        "dose": "5 mg",
        "momento": None,
        "observacao": None,
    }
    # O que não foi entendido volta à vista, para o João conferir.
    assert "Só basta fazer o que é preciso!" in corpo["nao_entendidas"]


def teste_o_rascunho_lido_pode_ser_gravado_direto(cliente, joao, filipe):
    """A ponte entre as duas rotas é o contrato que interessa aqui."""
    treinador = cliente(joao.email)
    rascunho = treinador.post("/api/protocolos/ler-texto", json={"texto": TEXTO}).json()[
        "protocolo"
    ]

    resposta = treinador.post(f"/api/alunos/{filipe.id}/protocolos", json=rascunho)
    assert resposta.status_code == 201, resposta.text
    corpo = resposta.json()
    assert corpo["grupos"][0]["itens"][0]["porcao"] == "Arroz branco 200 g"
    assert corpo["refeicoes"][0]["itens"][0]["grupo_id"] == corpo["grupos"][0]["id"]


def teste_aluno_nao_usa_o_leitor(cliente, filipe):
    resposta = cliente("filipe@exemplo.com").post(
        "/api/protocolos/ler-texto", json={"texto": TEXTO}
    )
    assert resposta.status_code == 403


# ------------------------------------------------------------- aderência


def teste_aluno_marca_refeicao(cliente, filipe, protocolo):
    aluno = cliente("filipe@exemplo.com")
    refeicao = protocolo["refeicoes"][0]["id"]

    resposta = aluno.put(f"/api/refeicoes/{refeicao}/aderencia", json={"seguiu": True})
    assert resposta.status_code == 200, resposta.text
    assert resposta.json()["dia"] == date.today().isoformat()

    marcas = aluno.get(f"/api/alunos/{filipe.id}/aderencia").json()
    assert [(m["refeicao_id"], m["seguiu"]) for m in marcas] == [(refeicao, True)]


def teste_marcar_de_novo_corrige_em_vez_de_duplicar(cliente, filipe, protocolo):
    aluno = cliente("filipe@exemplo.com")
    refeicao = protocolo["refeicoes"][0]["id"]
    dia = date.today().isoformat()

    aluno.put(f"/api/refeicoes/{refeicao}/aderencia", json={"dia": dia, "seguiu": True})
    aluno.put(
        f"/api/refeicoes/{refeicao}/aderencia",
        json={"dia": dia, "seguiu": False, "observacao": "comi fora"},
    )

    marcas = aluno.get(f"/api/alunos/{filipe.id}/aderencia").json()
    # Duas marcações do mesmo dia inflariam a aderência acima de 100%.
    assert len(marcas) == 1
    assert marcas[0]["seguiu"] is False
    assert marcas[0]["observacao"] == "comi fora"


def teste_nao_da_para_marcar_o_futuro(cliente, filipe, protocolo):
    amanha = (date.today() + timedelta(days=1)).isoformat()
    resposta = cliente("filipe@exemplo.com").put(
        f"/api/refeicoes/{protocolo['refeicoes'][0]['id']}/aderencia",
        json={"dia": amanha},
    )
    assert resposta.status_code == 422


def teste_aderencia_exige_consentimento(cliente, joao, criar_aluno):
    """Aderência é dado de saúde: sem consentimento em vigor, não entra."""
    sem_termo = criar_aluno("Sem termo", "semtermo@exemplo.com", joao, consentiu=False)
    treinador = cliente(joao.email)
    protocolo = treinador.post(
        f"/api/alunos/{sem_termo.id}/protocolos", json=PROTOCOLO
    ).json()

    resposta = cliente("semtermo@exemplo.com").put(
        f"/api/refeicoes/{protocolo['refeicoes'][0]['id']}/aderencia", json={}
    )
    assert resposta.status_code == 451


def teste_aluno_nao_marca_refeicao_de_outro(cliente, criar_usuario, criar_aluno, protocolo):
    outro_treinador = criar_usuario("Outro", "outro@exemplo.com", Papel.TREINADOR)
    criar_aluno("Alheio", "alheio@exemplo.com", outro_treinador)

    resposta = cliente("alheio@exemplo.com").put(
        f"/api/refeicoes/{protocolo['refeicoes'][0]['id']}/aderencia", json={}
    )
    assert resposta.status_code == 404


def teste_apagar_o_protocolo_leva_as_marcacoes(cliente, joao, filipe, protocolo, sessao_de_banco):
    from jf.modelos import AderenciaDaRefeicao

    aluno = cliente("filipe@exemplo.com")
    aluno.put(f"/api/refeicoes/{protocolo['refeicoes'][0]['id']}/aderencia", json={})

    cliente(joao.email).delete(f"/api/protocolos/{protocolo['id']}")

    sessao_de_banco.expire_all()
    assert sessao_de_banco.query(AderenciaDaRefeicao).count() == 0
