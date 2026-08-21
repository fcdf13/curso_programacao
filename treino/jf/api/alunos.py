"""Os alunos do treinador: listar, cadastrar e editar o perfil."""

from __future__ import annotations

from datetime import date, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from jf.alertas import avaliar, pontuacao
from jf.auth import (
    aluno_permitido,
    consentimento_em_dia,
    hash_de_senha,
    normalizar_email,
    treinador_atual,
    trocar_senha,
)
from jf.banco import obter_sessao
from jf.esquemas import (
    AlertaEmResposta,
    AlunoComAlertas,
    AlunoEmResposta,
    EdicaoDoAluno,
    NovoAluno,
    SenhaDefinidaPeloTreinador,
)
from jf.modelos import (
    Aluno,
    CheckinSemanal,
    Papel,
    ProtocoloAlimentar,
    Usuario,
)

rotas = APIRouter(prefix="/alunos", tags=["alunos"])


def resposta(aluno: Aluno) -> AlunoEmResposta:
    """Junta o perfil com o nome e o email, que moram em `Usuario`."""
    return AlunoEmResposta(
        id=aluno.id,
        nome=aluno.usuario.nome,
        email=aluno.usuario.email,
        nascimento=aluno.nascimento,
        sexo=aluno.sexo,
        altura_cm=aluno.altura_cm,
        objetivo=aluno.objetivo,
        observacoes=aluno.observacoes,
    )


@rotas.get("", response_model=list[AlunoEmResposta])
def listar(
    treinador: Usuario = Depends(treinador_atual),
    sessao: Session = Depends(obter_sessao),
) -> list[AlunoEmResposta]:
    alunos = sessao.scalars(
        select(Aluno)
        .where(Aluno.treinador_id == treinador.id)
        .join(Aluno.usuario)
        .order_by(Usuario.nome)
    ).all()
    return [resposta(aluno) for aluno in alunos]


@rotas.post("", response_model=AlunoEmResposta, status_code=status.HTTP_201_CREATED)
def cadastrar(
    dados: NovoAluno,
    treinador: Usuario = Depends(treinador_atual),
    sessao: Session = Depends(obter_sessao),
) -> AlunoEmResposta:
    usuario = Usuario(
        nome=dados.nome.strip(),
        email=normalizar_email(dados.email),
        senha_hash=hash_de_senha(dados.senha),
        papel=Papel.ALUNO,
        # Quem escolheu esta senha foi o treinador, não o aluno. O app diz isso
        # ao aluno e pede a troca — até lá, outra pessoa consegue entrar como ele.
        senha_provisoria=True,
    )
    aluno = Aluno(
        usuario=usuario,
        treinador_id=treinador.id,
        nascimento=dados.nascimento,
        sexo=dados.sexo,
        altura_cm=dados.altura_cm,
        objetivo=dados.objetivo,
        observacoes=dados.observacoes,
    )
    sessao.add(aluno)

    try:
        sessao.commit()
    except IntegrityError:
        # O índice único de `usuario.email` é quem decide de verdade; conferir
        # antes com um SELECT deixaria uma corrida entre dois cadastros
        # simultâneos do mesmo email.
        sessao.rollback()
        raise HTTPException(
            status.HTTP_409_CONFLICT, "Já existe uma conta com esse email."
        ) from None

    sessao.refresh(aluno)
    return resposta(aluno)


@rotas.get("/alertas", response_model=list[AlunoComAlertas])
def alertas(
    treinador: Usuario = Depends(treinador_atual),
    sessao: Session = Depends(obter_sessao),
) -> list[AlunoComAlertas]:
    """Os alunos do João, ordenados por quem precisa de atenção primeiro.

    Antes de `/{aluno_id}` de propósito: sem isso, `/alunos/alertas` seria
    interpretado como `aluno_id="alertas"` e devolveria 404.
    """
    from jf.api.execucao import resumo_de_forca

    hoje = date.today()
    janela_de_peso = timedelta(weeks=8)
    resultado = []

    alunos = sessao.scalars(
        select(Aluno)
        .where(Aluno.treinador_id == treinador.id)
        .join(Aluno.usuario)
        .order_by(Usuario.nome)
    ).all()

    for aluno in alunos:
        checkins = list(
            sessao.scalars(
                select(CheckinSemanal)
                .where(CheckinSemanal.aluno_id == aluno.id)
                .where(CheckinSemanal.semana >= hoje - janela_de_peso)
                .order_by(CheckinSemanal.semana)
            ).all()
        )
        ultimo = checkins[-1] if checkins else None
        anterior = checkins[-2] if len(checkins) >= 2 else None

        pesos = [c.peso_kg for c in checkins if c.peso_kg is not None]
        tendencia = _tendencia_de_peso(pesos)

        protocolo_ativo = sessao.scalars(
            select(ProtocoloAlimentar)
            .where(ProtocoloAlimentar.aluno_id == aluno.id)
            .where(ProtocoloAlimentar.ativo.is_(True))
        ).first()

        forca = {
            item.exercicio: [p.e1rm for p in item.pontos]
            for item in resumo_de_forca(sessao, aluno.id, semanas=12)
        }

        achados = avaliar(
            hoje=hoje,
            ultimo_checkin=ultimo.semana if ultimo else None,
            horas_de_sono=ultimo.horas_de_sono if ultimo else None,
            em_corte=protocolo_ativo is not None
            and protocolo_ativo.deficit_kcal is not None,
            tendencia_de_peso_kg=tendencia,
            forca_por_exercicio=forca,
            aderencia_dieta_atual=ultimo.aderencia_dieta if ultimo else None,
            aderencia_dieta_anterior=anterior.aderencia_dieta if anterior else None,
        )

        resultado.append(
            AlunoComAlertas(
                aluno_id=aluno.id,
                nome=aluno.usuario.nome,
                objetivo=aluno.objetivo,
                alertas=[AlertaEmResposta(**a.__dict__) for a in achados],
                pontuacao=pontuacao(achados),
            )
        )

    # Quem tem mais sinal primeiro; empate resolve por nome, para a lista não
    # embaralhar a cada carregamento.
    resultado.sort(key=lambda a: (-a.pontuacao, a.nome))
    return resultado


def _tendencia_de_peso(pesos: list[float], janela: int = 4) -> list[float]:
    """Média móvel simples — mesma janela do gráfico de evolução.

    Só a partir do ponto em que a janela está cheia: começar antes desenharia
    tendência a partir de duas semanas, que é exatamente o ruído que a média
    existe para tirar.
    """
    if len(pesos) < janela:
        return []
    return [
        round(sum(pesos[fim - janela : fim]) / janela, 2)
        for fim in range(janela, len(pesos) + 1)
    ]


@rotas.get("/{aluno_id}", response_model=AlunoEmResposta)
def detalhar(aluno: Aluno = Depends(aluno_permitido)) -> AlunoEmResposta:
    return resposta(aluno)


@rotas.patch("/{aluno_id}", response_model=AlunoEmResposta)
def editar(
    dados: EdicaoDoAluno,
    aluno: Aluno = Depends(aluno_permitido),
    _: Usuario = Depends(consentimento_em_dia),
    sessao: Session = Depends(obter_sessao),
) -> AlunoEmResposta:
    # `exclude_unset` para que não mandar um campo signifique "deixa como está",
    # e mandar `null` signifique "apaga".
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(aluno, campo, valor)
    sessao.commit()
    sessao.refresh(aluno)
    return resposta(aluno)


@rotas.post("/{aluno_id}/senha", status_code=status.HTTP_204_NO_CONTENT)
def redefinir_senha(
    dados: SenhaDefinidaPeloTreinador,
    aluno: Aluno = Depends(aluno_permitido),
    _: Usuario = Depends(treinador_atual),
    sessao: Session = Depends(obter_sessao),
) -> None:
    """O caminho de recuperação de senha, enquanto não há envio de email.

    O aluno esqueceu a senha e não existe "esqueci minha senha" automático: sem
    um provedor de email configurado, mandar link de redefinição é promessa que
    o app não cumpre. Então quem redefine é o treinador, que passa a nova pelo
    mesmo canal por onde já passa o treino.

    A senha nasce marcada como provisória de propósito: até o aluno trocá-la, o
    treinador consegue entrar como ele, e o app diz isso ao aluno em vez de
    deixar a porta aberta em silêncio.
    """
    trocar_senha(aluno.usuario, dados.senha, provisoria=True)
    sessao.commit()
