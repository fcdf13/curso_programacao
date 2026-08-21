"""Um banco de demonstração, para o app abrir com algo dentro.

Serve para ver o app funcionando em um comando, sem cadastrar nada à mão. As
senhas são fracas e estão escritas aqui de propósito — é dado de brinquedo, e
`montar` se recusa a rodar em produção.
"""

from __future__ import annotations

from datetime import date, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from jf.auth import hash_de_senha
from jf.config import config
from jf.dados import semear_tudo
from jf.dieta_texto import ler_protocolo
from jf.leitura import ler
from jf.privacidade import versao_do_termo
from jf.modelos import (
    Aluno,
    CheckinSemanal,
    Consentimento,
    MedidaCorporal,
    Exercicio,
    FaseDaPeriodizacao,
    Papel,
    Periodizacao,
    ProtocoloAlimentar,
    Prescricao,
    SerieDaPrescricao,
    SessaoModelo,
    Sexo,
    Tecnica,
    Usuario,
)

TREINADOR = ("João Filho", "joao@jftreino.com.br", "demonstracao-2026")
ALUNO = ("Filipe", "filipe@jftreino.com.br", "demonstracao-2026")


class DemonstracaoRecusada(RuntimeError):
    pass


# Os treinos saem escritos no formato do João e passam pelo mesmo leitor que a
# tela usa — se o leitor quebrar, a demonstração quebra junto, o que é o aviso
# que a gente quer.
TREINO_A = [
    ("Supino reto com barra", None, "Aquecimento 20 a 60kg\n8x70kg\n6x80kg\n5x85kg"),
    ("Supino inclinado com halteres", "A", "12x26kg\n10x30kg\n10x30kg"),
    ("Crucifixo na máquina", "A", "15x35kg\n12x45kg\n12x45kg"),
    ("Tríceps na polia com corda", None, "12x30kg\n10x35kg\n9x40kg cluster set"),
    ("Tríceps testa com barra W", None, "12x20kg\n10x25kg\n8x30kg"),
]

TREINO_B = [
    ("Abdução na máquina", None, "Up set de 40 a 100kg\n10x100kg\n12x100kg cluster set"),
    ("Cadeira flexora", None, "12x50 a 92kg\n10x100kg\n8x109kg"),
    ("Mesa flexora", None, "12x20kg\n10x15kg\n8x10kg"),
    ("Leg press 45", None, "12x120kg\n10x160kg\n8x200kg"),
    ("Elevação pélvica", None, "12x60kg\n10x80kg\n8x100kg"),
]


def _usuario(sessao: Session, nome: str, email: str, senha: str, papel: Papel) -> Usuario:
    usuario = Usuario(
        nome=nome, email=email, senha_hash=hash_de_senha(senha), papel=papel
    )
    sessao.add(usuario)
    sessao.flush()
    return usuario


def _prescrever(
    sessao: Session,
    treino: SessaoModelo,
    ordem: int,
    nome_do_exercicio: str,
    bloco: str | None,
    texto: str,
    catalogo: dict[str, Exercicio],
    tecnicas: dict[str, Tecnica],
    biset: Tecnica,
) -> None:
    exercicio = catalogo[nome_do_exercicio]
    prescricao = Prescricao(
        sessao_modelo_id=treino.id,
        exercicio_id=exercicio.id,
        ordem=ordem,
        bloco=bloco,
        agrupamento_id=biset.id if bloco else None,
        descanso_s=0 if bloco else 90,
        rir_alvo=1,
    )
    sessao.add(prescricao)
    sessao.flush()

    for posicao, linha in enumerate(ler(texto, list(tecnicas))):
        if not linha.entendida:
            raise DemonstracaoRecusada(
                f"O leitor não entendeu {linha.texto!r} em {nome_do_exercicio}."
            )
        sessao.add(
            SerieDaPrescricao(
                prescricao_id=prescricao.id,
                ordem=posicao,
                reps=linha.reps,
                carga_kg=linha.carga_kg,
                carga_ate_kg=linha.carga_ate_kg,
                tipo=linha.tipo,
                rir=1,
                observacao=linha.observacao,
                tecnicas=[tecnicas[nome] for nome in linha.tecnicas],
            )
        )

    # O resumo acompanha as séries de trabalho, como faz a rota `/series`.
    de_trabalho = [
        s for s in prescricao.series_detalhadas if s.tipo.conta_no_volume
    ]
    if de_trabalho:
        prescricao.series = len(de_trabalho)
        repeticoes = [s.reps for s in de_trabalho if s.reps is not None]
        if repeticoes:
            prescricao.reps_min, prescricao.reps_max = min(repeticoes), max(repeticoes)
        cargas = [s.carga_media_kg for s in de_trabalho if s.carga_media_kg is not None]
        prescricao.carga_alvo_kg = max(cargas) if cargas else None


# Dez semanas de corte: o peso cai com o vaivém de sempre — a semana 5 sobe
# 300 g — para a média móvel ter o que resolver. Uma linha perfeitamente
# descendente daria a impressão errada de como o dado real se parece.
SEMANAS = [
    # peso, sono, qualidade, disposição, recuperação, passos, dieta, treino
    (86.4, 6.5, 3, 3, 3, 7200, 80, 80),
    (85.9, 7.0, 4, 4, 3, 8100, 90, 100),
    (85.5, 7.5, 4, 4, 4, 8800, 95, 100),
    (85.6, 6.0, 2, 3, 3, 6400, 75, 80),
    (85.0, 7.0, 4, 4, 4, 9000, 90, 100),
    (84.6, 7.5, 5, 4, 4, 9400, 95, 100),
    (84.7, 6.5, 3, 3, 3, 7000, 85, 60),
    (84.1, 7.5, 4, 5, 4, 9800, 100, 100),
    (83.7, 8.0, 5, 5, 5, 10200, 95, 100),
    (83.4, 7.5, 4, 4, 4, 9600, 90, 100),
]


def _checkins(sessao: Session, aluno: Aluno) -> None:
    hoje = date.today()
    segunda_desta_semana = hoje - timedelta(days=hoje.weekday())

    for recuo, valores in enumerate(reversed(SEMANAS)):
        peso, sono, qualidade, disposicao, recuperacao, passos, dieta, treino = valores
        checkin = CheckinSemanal(
            aluno_id=aluno.id,
            semana=segunda_desta_semana - timedelta(weeks=recuo),
            peso_kg=peso,
            horas_de_sono=sono,
            qualidade_do_sono=qualidade,
            disposicao=disposicao,
            recuperacao=recuperacao,
            passos_por_dia=passos,
            aderencia_dieta=dieta,
            aderencia_treino=treino,
        )
        sessao.add(checkin)
        sessao.flush()

        # Medida de fita a cada quatro semanas, que é como se mede de verdade.
        if recuo % 4 == 0:
            sessao.add(
                MedidaCorporal(
                    checkin_id=checkin.id,
                    cintura_cm=round(88 - (len(SEMANAS) - 1 - recuo) * 0.35, 1),
                    braco_cm=38.5,
                    coxa_cm=59.0,
                )
            )


# O protocolo alimentar sai escrito como o João escreve e passa pelo mesmo
# leitor da tela, pela mesma gravação da API — se qualquer um dos dois quebrar,
# a demonstração quebra junto.
PROTOCOLO = """
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
Maçã: 1 und
Melão: 200g
Morango: 200g

Fibras:
Aveia: 30g

Gorduras:
Azeite: 1 colher

1° refeição café
Ovos
Pão francês
(Azeite)
Legumes a gosto

2° refeição almoço
Arroz branco
Frango
Salada a gosto

3° refeição lanche
Aveia
Maçã

4° refeição janta
Batata Doce
Peixe
Legumes a gosto

5° refeição ceia
Ovos
Morango

Suplementos:
Multi vitaminico: dose diária
Homega 3: 2 cps
Ioimbina: 5mg
"""


def _dieta(sessao: Session, aluno: Aluno) -> None:
    from jf.api.dieta import escrever_protocolo, rascunho_do_lido

    lido = ler_protocolo(PROTOCOLO)
    rascunho = rascunho_do_lido(lido, "Corte — protocolo 1")

    protocolo = ProtocoloAlimentar(aluno_id=aluno.id, nome=rascunho.nome)
    sessao.add(protocolo)
    sessao.flush()
    escrever_protocolo(sessao, protocolo, rascunho)


def montar(sessao: Session) -> dict[str, str]:
    """Cria o treinador, um aluno e um bloco de treino com progressão."""
    if config.producao:
        raise DemonstracaoRecusada(
            "A demonstração não roda com JF_PRODUCAO=1: ela cria contas com "
            "senha conhecida."
        )

    if sessao.scalar(select(Usuario).limit(1)) is not None:
        raise DemonstracaoRecusada(
            "Já existe conta neste banco. Apague o arquivo jf.db (ou aponte "
            "JF_BANCO para outro) antes de montar a demonstração."
        )

    semear_tudo(sessao)
    catalogo = {e.nome: e for e in sessao.scalars(select(Exercicio)).all()}
    tecnicas = {t.nome: t for t in sessao.scalars(select(Tecnica)).all()}
    biset = tecnicas["Bi-set"]

    joao = _usuario(sessao, *TREINADOR, Papel.TREINADOR)
    filipe_usuario = _usuario(sessao, *ALUNO, Papel.ALUNO)

    aluno = Aluno(
        usuario_id=filipe_usuario.id,
        treinador_id=joao.id,
        nascimento=date(1994, 7, 12),
        sexo=Sexo.MASCULINO,
        altura_cm=178,
        objetivo="Corte com 500 kcal de déficit",
        observacoes="Treina de segunda a sexta, de manhã.",
    )
    sessao.add(aluno)
    sessao.flush()

    # Sem isto o app recusaria os check-ins da demonstração — que é exatamente
    # o comportamento certo, e por isso a demonstração aceita o termo.
    sessao.add(
        Consentimento(usuario_id=filipe_usuario.id, versao_do_termo=versao_do_termo())
    )

    bloco = Periodizacao(
        aluno_id=aluno.id,
        nome="Corte — bloco 1",
        objetivo="Manter força enquanto reduz o percentual de gordura",
        fase=FaseDaPeriodizacao.ACUMULACAO,
        inicio=date.today() - timedelta(days=7),
        semanas=4,
    )
    sessao.add(bloco)
    sessao.flush()

    for ordem_do_treino, (nome, dia, itens) in enumerate(
        [
            ("Treino A — peito e tríceps", 0, TREINO_A),
            ("Treino B — posterior e glúteo", 2, TREINO_B),
        ]
    ):
        treino = SessaoModelo(
            periodizacao_id=bloco.id, nome=nome, ordem=ordem_do_treino, dia_da_semana=dia
        )
        sessao.add(treino)
        sessao.flush()
        for ordem, (exercicio, bloco_do_exercicio, texto) in enumerate(itens):
            _prescrever(
                sessao, treino, ordem, exercicio, bloco_do_exercicio, texto,
                catalogo, tecnicas, biset,
            )

    _checkins(sessao, aluno)
    _dieta(sessao, aluno)

    sessao.commit()

    return {
        "treinador": f"{TREINADOR[1]} / {TREINADOR[2]}",
        "aluno": f"{ALUNO[1]} / {ALUNO[2]}",
    }
