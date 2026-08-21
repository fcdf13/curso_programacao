"""Os direitos do titular, em botão — não em pedido por email.

A LGPD dá ao titular o direito de acessar, corrigir, portar, revogar o
consentimento e eliminar os dados (art. 18). Um app que atende isso por
formulário de contato atende no papel; aqui cada direito é uma rota, e a
exclusão apaga de verdade.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.orm import Session

from jf.auth import usuario_atual
from jf.banco import obter_sessao
from jf.esquemas import EstadoDoConsentimento, MeusDados, TermoEmResposta
from jf.modelos import (
    AderenciaDaRefeicao,
    Aluno,
    CheckinSemanal,
    Consentimento,
    Papel,
    Periodizacao,
    ProtocoloAlimentar,
    SessaoRealizada,
    Usuario,
    agora,
)
from jf.privacidade import texto_do_termo, versao_do_termo

rotas = APIRouter(tags=["privacidade"])


@rotas.get("/termo", response_model=TermoEmResposta)
def termo() -> TermoEmResposta:
    """O termo é público de propósito: é preciso poder lê-lo antes de aceitar."""
    return TermoEmResposta(versao=versao_do_termo(), texto=texto_do_termo())


def _estado(usuario: Usuario) -> EstadoDoConsentimento:
    ativo = usuario.consentimento_ativo
    anteriores = [c for c in usuario.consentimentos if c.versao_do_termo != versao_do_termo()]

    return EstadoDoConsentimento(
        versao_atual=versao_do_termo(),
        consentido=ativo is not None,
        aceito_em=ativo.aceito_em if ativo else None,
        # Distingue quem nunca aceitou de quem aceitou um texto que mudou: são
        # conversas diferentes na tela.
        precisa_reaceitar=ativo is None and bool(anteriores),
    )


@rotas.get("/eu/consentimento", response_model=EstadoDoConsentimento)
def ver_consentimento(usuario: Usuario = Depends(usuario_atual)) -> EstadoDoConsentimento:
    return _estado(usuario)


@rotas.post("/eu/consentimento", response_model=EstadoDoConsentimento)
def consentir(
    usuario: Usuario = Depends(usuario_atual),
    sessao: Session = Depends(obter_sessao),
) -> EstadoDoConsentimento:
    if usuario.consentimento_ativo is not None:
        return _estado(usuario)

    sessao.add(
        Consentimento(usuario_id=usuario.id, versao_do_termo=versao_do_termo())
    )
    sessao.commit()
    sessao.refresh(usuario)
    return _estado(usuario)


@rotas.delete("/eu/consentimento", response_model=EstadoDoConsentimento)
def revogar(
    usuario: Usuario = Depends(usuario_atual),
    sessao: Session = Depends(obter_sessao),
) -> EstadoDoConsentimento:
    """Revoga sem apagar nada.

    Revogar e eliminar são direitos diferentes (art. 18, VI e IX). Apagar o
    histórico de quem só quis parar de mandar dado novo seria destruir o que a
    pessoa não pediu para destruir — e é irreversível.
    """
    ativo = usuario.consentimento_ativo
    if ativo is not None:
        ativo.revogado_em = agora()
        sessao.commit()
        sessao.refresh(usuario)
    return _estado(usuario)


# ------------------------------------------------------------------ exportar


def _do_aluno(aluno: Aluno, sessao: Session) -> dict:
    checkins = (
        sessao.query(CheckinSemanal)
        .filter(CheckinSemanal.aluno_id == aluno.id)
        .order_by(CheckinSemanal.semana)
        .all()
    )
    blocos = (
        sessao.query(Periodizacao)
        .filter(Periodizacao.aluno_id == aluno.id)
        .order_by(Periodizacao.criada_em)
        .all()
    )
    protocolos = (
        sessao.query(ProtocoloAlimentar)
        .filter(ProtocoloAlimentar.aluno_id == aluno.id)
        .order_by(ProtocoloAlimentar.criado_em)
        .all()
    )
    executados = (
        sessao.query(SessaoRealizada)
        .filter(SessaoRealizada.aluno_id == aluno.id)
        .order_by(SessaoRealizada.dia)
        .all()
    )
    marcacoes = (
        sessao.query(AderenciaDaRefeicao)
        .filter(AderenciaDaRefeicao.aluno_id == aluno.id)
        .order_by(AderenciaDaRefeicao.dia)
        .all()
    )

    return {
        "perfil": {
            "nascimento": aluno.nascimento,
            "sexo": aluno.sexo.value if aluno.sexo else None,
            "altura_cm": aluno.altura_cm,
            "objetivo": aluno.objetivo,
            "observacoes": aluno.observacoes,
            "treinador": aluno.treinador.nome,
        },
        "checkins": [
            {
                "semana": c.semana,
                "peso_kg": c.peso_kg,
                "horas_de_sono": c.horas_de_sono,
                "qualidade_do_sono": c.qualidade_do_sono,
                "disposicao": c.disposicao,
                "recuperacao": c.recuperacao,
                "passos_por_dia": c.passos_por_dia,
                "aderencia_dieta": c.aderencia_dieta,
                "aderencia_treino": c.aderencia_treino,
                "observacoes": c.observacoes,
                "medidas": (
                    {
                        "cintura_cm": c.medidas.cintura_cm,
                        "quadril_cm": c.medidas.quadril_cm,
                        "torax_cm": c.medidas.torax_cm,
                        "braco_cm": c.medidas.braco_cm,
                        "coxa_cm": c.medidas.coxa_cm,
                        "panturrilha_cm": c.medidas.panturrilha_cm,
                    }
                    if c.medidas
                    else None
                ),
            }
            for c in checkins
        ],
        "treinos": [
            {
                "nome": bloco.nome,
                "objetivo": bloco.objetivo,
                "fase": bloco.fase.value,
                "inicio": bloco.inicio,
                "semanas": bloco.semanas,
                "sessoes": [
                    {
                        "nome": treino.nome,
                        "dia_da_semana": treino.dia_da_semana,
                        "exercicios": [
                            {
                                "exercicio": p.exercicio.nome,
                                "bloco": p.bloco,
                                "agrupamento": p.agrupamento.nome if p.agrupamento else None,
                                "series": p.series,
                                "reps": [p.reps_min, p.reps_max],
                                "carga_alvo_kg": p.carga_alvo_kg,
                                "rir_alvo": p.rir_alvo,
                                "descanso_s": p.descanso_s,
                                "cadencia": p.cadencia,
                                "observacao": p.observacao,
                                "tecnicas": [t.nome for t in p.tecnicas],
                                "progressao": [
                                    {
                                        "reps": s.reps,
                                        "carga_kg": s.carga_kg,
                                        "carga_ate_kg": s.carga_ate_kg,
                                        "tipo": s.tipo.value,
                                        "rir": s.rir,
                                        "tecnicas": [t.nome for t in s.tecnicas],
                                        "observacao": s.observacao,
                                    }
                                    for s in p.series_detalhadas
                                ],
                            }
                            for p in treino.prescricoes
                        ],
                    }
                    for treino in bloco.sessoes
                ],
            }
            for bloco in blocos
        ],
        # A dieta entra por inteiro: as substituições sem as quantidades não
        # são o protocolo, são uma lista de compras.
        "dieta": [
            {
                "nome": protocolo.nome,
                "criado_em": protocolo.criado_em,
                "ativo": protocolo.ativo,
                "kcal_alvo": protocolo.kcal_alvo,
                "deficit_kcal": protocolo.deficit_kcal,
                "proteina_g": protocolo.proteina_g,
                "carboidrato_g": protocolo.carboidrato_g,
                "gordura_g": protocolo.gordura_g,
                "observacoes": protocolo.observacoes,
                "grupos_de_substituicao": [
                    {
                        "nome": grupo.nome,
                        "observacao": grupo.observacao,
                        "itens": [item.porcao for item in grupo.itens],
                    }
                    for grupo in protocolo.grupos
                ],
                "refeicoes": [
                    {
                        "nome": refeicao.nome,
                        "horario": refeicao.horario,
                        "observacoes": refeicao.observacoes,
                        "itens": [
                            {
                                "descricao": item.rotulo,
                                "quantidade": item.quantidade,
                                "unidade": item.unidade,
                                "grupo": item.grupo.nome if item.grupo else None,
                                "a_gosto": item.a_gosto,
                                "opcional": item.opcional,
                                "observacao": item.observacao,
                            }
                            for item in refeicao.itens
                        ],
                    }
                    for refeicao in protocolo.refeicoes
                ],
                "suplementos": [
                    {
                        "nome": s.nome,
                        "dose": s.dose,
                        "momento": s.momento,
                        "observacao": s.observacao,
                    }
                    for s in protocolo.suplementos
                ],
            }
            for protocolo in protocolos
        ],
        # O que ele levantou de verdade. É o dado mais difícil de recriar de
        # todos: ninguém lembra a carga de uma terça-feira de março.
        "treinos_executados": [
            {
                "dia": feito.dia,
                "treino": feito.nome,
                "iniciado_em": feito.iniciada_em,
                "encerrado_em": feito.encerrada_em,
                "observacoes": feito.observacoes,
                "tonelagem": feito.tonelagem,
                "series": [
                    {
                        "exercicio": s.exercicio.nome,
                        "reps": s.reps,
                        "carga_kg": s.carga_kg,
                        "rir": s.rir,
                        "tipo": s.tipo.value,
                        "tecnicas": [t.nome for t in s.tecnicas],
                        "observacao": s.observacao,
                    }
                    for s in feito.series
                ],
            }
            for feito in executados
        ],
        "aderencia_as_refeicoes": [
            {
                "dia": m.dia,
                "refeicao": m.refeicao.nome,
                "seguiu": m.seguiu,
                "observacao": m.observacao,
            }
            for m in marcacoes
        ],
    }


@rotas.get("/eu/dados", response_model=MeusDados)
def exportar(
    usuario: Usuario = Depends(usuario_atual),
    sessao: Session = Depends(obter_sessao),
) -> MeusDados:
    """Tudo que o app guarda sobre quem pediu, em JSON.

    JSON porque a lei pede formato "interoperável e de uso comum" (art. 18, V):
    qualquer planilha ou linguagem lê, e nada se perde no caminho como
    aconteceria num PDF.

    A senha não entra — nem embaralhada. Ela não é um dado sobre a pessoa, é a
    credencial dela, e exportá-la só criaria uma cópia a mais para vazar.
    """
    dados = MeusDados(
        exportado_em=agora(),
        conta={
            "nome": usuario.nome,
            "email": usuario.email,
            "papel": usuario.papel.value,
            "criado_em": usuario.criado_em,
        },
        consentimentos=[
            {
                "versao_do_termo": c.versao_do_termo,
                "aceito_em": c.aceito_em,
                "revogado_em": c.revogado_em,
            }
            for c in usuario.consentimentos
        ],
        aluno=None,
    )

    if usuario.papel is Papel.ALUNO and usuario.perfil is not None:
        dados.aluno = _do_aluno(usuario.perfil, sessao)

    return dados


# -------------------------------------------------------------------- apagar


@rotas.delete("/eu", status_code=status.HTTP_204_NO_CONTENT)
def apagar_a_propria_conta(
    request: Request,
    confirmacao: str,
    usuario: Usuario = Depends(usuario_atual),
    sessao: Session = Depends(obter_sessao),
) -> Response:
    """Apaga a conta e tudo que pende dela. Imediato e definitivo.

    Exige o email como confirmação na query — não como segurança (quem está
    logado já é a pessoa), mas porque um DELETE sem atrito é fácil demais de
    disparar por engano numa ação que não tem volta.

    O treinador não pode se apagar enquanto tiver aluno: a conta dele é o que
    prende o vínculo, e removê-la levaria o histórico dos alunos junto.
    """
    if confirmacao.strip().lower() != usuario.email:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Para confirmar, digite o seu email exatamente como ele aparece na conta.",
        )

    if usuario.papel is Papel.TREINADOR:
        alunos = sessao.query(Aluno).filter(Aluno.treinador_id == usuario.id).count()
        if alunos:
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                f"Você ainda tem {alunos} aluno(s) vinculado(s). Apagar a sua "
                "conta levaria o histórico deles junto. Remova os vínculos primeiro.",
            )

    sessao.delete(usuario)
    sessao.commit()
    request.session.clear()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
