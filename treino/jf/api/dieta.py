"""O protocolo alimentar: o João escreve, o aluno segue e marca.

O protocolo entra e sai **inteiro**. CRUD linha a linha renderia um caminho de
API por tabela e obrigaria a tela a orquestrar seis chamadas para salvar uma
edição — e ainda deixaria o protocolo meio salvo se uma delas falhasse. Aqui
gravar é substituir o conteúdo do protocolo numa transação só.

Quem escreve é o treinador. O aluno lê e marca aderência — que é dado de saúde
e por isso passa pelo consentimento.
"""

from __future__ import annotations

import unicodedata
from datetime import date, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from jf.auth import (
    aluno_permitido,
    consentimento_em_dia,
    exigir_acesso,
    treinador_atual,
    usuario_atual,
)
from jf.banco import obter_sessao
from jf.dieta_texto import ProtocoloLido, ler_protocolo
from jf.esquemas import (
    AderenciaEmResposta,
    AlimentoEmResposta,
    GrupoBase,
    ItemDaRefeicaoBase,
    ItemDeSubstituicaoBase,
    MarcacaoDaRefeicao,
    NovoProtocolo,
    ProtocoloBase,
    ProtocoloEmResposta,
    ProtocoloLidoEmResposta,
    ProtocoloNaLista,
    RefeicaoBase,
    SuplementoBase,
    TextoDoProtocolo,
)
from jf.modelos import (
    AderenciaDaRefeicao,
    Alimento,
    Aluno,
    GrupoDeSubstituicao,
    ItemDaRefeicao,
    ItemDeSubstituicao,
    ProtocoloAlimentar,
    Refeicao,
    Suplemento,
    Usuario,
)

rotas = APIRouter(tags=["dieta"])


def _chave(texto: str) -> str:
    """Nome comparável: sem acento, sem caixa, sem espaço sobrando.

    O João escreve "Pão francês" no grupo e "pao frances" na refeição. Casar só
    por igualdade exata deixaria o aluno sem ver as substituições daquele item.
    """
    decomposto = unicodedata.normalize("NFKD", texto.strip().lower())
    return " ".join("".join(c for c in decomposto if not unicodedata.combining(c)).split())


# ------------------------------------------------------------- gravação


def _escrever(
    sessao: Session, protocolo: ProtocoloAlimentar, dados: ProtocoloBase
) -> None:
    """Substitui o conteúdo do protocolo pelo que veio.

    Apagar e recriar em vez de casar item a item: os itens não têm identidade
    própria para o João — ele reescreve a lista, não edita a linha 3. O
    `delete-orphan` das relações faz a limpeza.
    """
    for campo, valor in dados.model_dump(
        exclude={"grupos", "refeicoes", "suplementos"}
    ).items():
        setattr(protocolo, campo, valor)

    protocolo.grupos.clear()
    protocolo.refeicoes.clear()
    protocolo.suplementos.clear()
    # Sem isto o INSERT dos novos corre antes do DELETE dos antigos e o índice
    # único de aderência bate de frente com linhas que estão de saída.
    sessao.flush()

    # Onde cada alimento mora, para ligar o item da refeição ao grupo dele.
    grupo_do_alimento: dict[str, GrupoDeSubstituicao] = {}
    grupo_por_nome: dict[str, GrupoDeSubstituicao] = {}

    for ordem, entrada in enumerate(dados.grupos):
        grupo = GrupoDeSubstituicao(
            nome=entrada.nome, ordem=ordem, observacao=entrada.observacao
        )
        for posicao, item in enumerate(entrada.itens):
            grupo.itens.append(
                ItemDeSubstituicao(
                    ordem=posicao,
                    descricao=item.descricao,
                    quantidade=item.quantidade,
                    unidade=item.unidade,
                )
            )
            # O primeiro grupo que contém o alimento é o dono dele: um mesmo
            # nome em dois grupos é erro de digitação, não escolha.
            grupo_do_alimento.setdefault(_chave(item.descricao), grupo)
        grupo_por_nome.setdefault(_chave(entrada.nome), grupo)
        protocolo.grupos.append(grupo)

    for ordem, entrada in enumerate(dados.refeicoes):
        refeicao = Refeicao(
            nome=entrada.nome,
            ordem=ordem,
            horario=entrada.horario,
            observacoes=entrada.observacoes,
        )
        for posicao, item in enumerate(entrada.itens):
            grupo = None
            if item.grupo:
                grupo = grupo_por_nome.get(_chave(item.grupo))
                if grupo is None:
                    raise HTTPException(
                        status.HTTP_422_UNPROCESSABLE_CONTENT,
                        f"O grupo “{item.grupo}” não existe neste protocolo.",
                    )
            elif item.descricao:
                grupo = grupo_do_alimento.get(_chave(item.descricao))

            refeicao.itens.append(
                ItemDaRefeicao(
                    ordem=posicao,
                    descricao=item.descricao or (grupo.nome if grupo else None),
                    grupo=grupo,
                    quantidade=item.quantidade,
                    unidade=item.unidade,
                    a_gosto=item.a_gosto,
                    opcional=item.opcional,
                    observacao=item.observacao,
                )
            )
        protocolo.refeicoes.append(refeicao)

    for ordem, entrada in enumerate(dados.suplementos):
        protocolo.suplementos.append(
            Suplemento(
                ordem=ordem,
                nome=entrada.nome,
                dose=entrada.dose,
                momento=entrada.momento,
                observacao=entrada.observacao,
            )
        )


def _desativar_os_outros(
    sessao: Session, aluno_id: int, protocolo: ProtocoloAlimentar
) -> None:
    """Um protocolo ativo por aluno.

    Dois ativos ao mesmo tempo é o aluno abrir o app e não saber o que comer;
    o anterior fica guardado, só sai de cena.
    """
    if not protocolo.ativo:
        return
    for outro in sessao.scalars(
        select(ProtocoloAlimentar)
        .where(ProtocoloAlimentar.aluno_id == aluno_id)
        .where(ProtocoloAlimentar.id != protocolo.id)
    ).all():
        outro.ativo = False


def protocolo_permitido(
    protocolo_id: int,
    usuario: Usuario = Depends(usuario_atual),
    sessao: Session = Depends(obter_sessao),
) -> ProtocoloAlimentar:
    protocolo = sessao.get(ProtocoloAlimentar, protocolo_id)
    if protocolo is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Protocolo não encontrado.")
    exigir_acesso(usuario, protocolo.aluno)
    return protocolo


# --------------------------------------------------------------- leitura


@rotas.get("/alunos/{aluno_id}/protocolos", response_model=list[ProtocoloNaLista])
def listar(
    aluno: Aluno = Depends(aluno_permitido),
    sessao: Session = Depends(obter_sessao),
) -> list[ProtocoloAlimentar]:
    return list(
        sessao.scalars(
            select(ProtocoloAlimentar)
            .where(ProtocoloAlimentar.aluno_id == aluno.id)
            .order_by(ProtocoloAlimentar.ativo.desc(), ProtocoloAlimentar.criado_em.desc())
        ).all()
    )


@rotas.get("/alunos/{aluno_id}/protocolo", response_model=ProtocoloEmResposta)
def atual(
    aluno: Aluno = Depends(aluno_permitido),
    sessao: Session = Depends(obter_sessao),
) -> ProtocoloAlimentar:
    """O protocolo em vigor — a tela que o aluno abre para saber o que comer."""
    protocolo = sessao.scalars(
        select(ProtocoloAlimentar)
        .where(ProtocoloAlimentar.aluno_id == aluno.id)
        .where(ProtocoloAlimentar.ativo.is_(True))
        .order_by(ProtocoloAlimentar.criado_em.desc())
    ).first()
    if protocolo is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "Este aluno ainda não tem protocolo alimentar."
        )
    return protocolo


@rotas.get("/protocolos/{protocolo_id}", response_model=ProtocoloEmResposta)
def detalhar(
    protocolo: ProtocoloAlimentar = Depends(protocolo_permitido),
) -> ProtocoloAlimentar:
    return protocolo


# --------------------------------------------------------------- escrita


@rotas.post(
    "/alunos/{aluno_id}/protocolos",
    response_model=ProtocoloEmResposta,
    status_code=status.HTTP_201_CREATED,
)
def criar(
    dados: NovoProtocolo,
    aluno: Aluno = Depends(aluno_permitido),
    _: Usuario = Depends(treinador_atual),
    sessao: Session = Depends(obter_sessao),
) -> ProtocoloAlimentar:
    protocolo = ProtocoloAlimentar(aluno_id=aluno.id, nome=dados.nome)
    sessao.add(protocolo)
    sessao.flush()
    _escrever(sessao, protocolo, dados)
    _desativar_os_outros(sessao, aluno.id, protocolo)
    sessao.commit()
    sessao.refresh(protocolo)
    return protocolo


@rotas.put("/protocolos/{protocolo_id}", response_model=ProtocoloEmResposta)
def editar(
    dados: NovoProtocolo,
    protocolo: ProtocoloAlimentar = Depends(protocolo_permitido),
    _: Usuario = Depends(treinador_atual),
    sessao: Session = Depends(obter_sessao),
) -> ProtocoloAlimentar:
    _escrever(sessao, protocolo, dados)
    _desativar_os_outros(sessao, protocolo.aluno_id, protocolo)
    sessao.commit()
    sessao.refresh(protocolo)
    return protocolo


@rotas.delete("/protocolos/{protocolo_id}", status_code=status.HTTP_204_NO_CONTENT)
def apagar(
    protocolo: ProtocoloAlimentar = Depends(protocolo_permitido),
    _: Usuario = Depends(treinador_atual),
    sessao: Session = Depends(obter_sessao),
) -> None:
    sessao.delete(protocolo)
    sessao.commit()


# ---------------------------------------------------- leitura do texto


def _rascunho(lido: ProtocoloLido, nome: str) -> ProtocoloBase:
    return ProtocoloBase(
        nome=nome,
        deficit_kcal=lido.deficit_kcal,
        grupos=[
            GrupoBase(
                nome=grupo.nome,
                itens=[
                    ItemDeSubstituicaoBase(
                        descricao=item.descricao,
                        quantidade=item.quantidade,
                        unidade=item.unidade,
                    )
                    for item in grupo.itens
                ],
            )
            for grupo in lido.grupos
        ],
        refeicoes=[
            RefeicaoBase(
                nome=refeicao.nome,
                itens=[
                    ItemDaRefeicaoBase(
                        descricao=item.descricao,
                        quantidade=item.quantidade,
                        unidade=item.unidade,
                        a_gosto=item.a_gosto,
                        opcional=item.opcional,
                        observacao=item.detalhe,
                    )
                    for item in refeicao.itens
                ],
            )
            for refeicao in lido.refeicoes
        ],
        suplementos=[
            SuplementoBase(
                nome=item.descricao,
                dose=_dose(item.quantidade, item.unidade) or item.detalhe,
                momento=item.detalhe if _dose(item.quantidade, item.unidade) else None,
            )
            for item in lido.suplementos
        ],
    )


def _dose(quantidade: float | None, unidade: str | None) -> str | None:
    if quantidade is None:
        return None
    numero = f"{quantidade:g}"
    return f"{numero} {unidade}" if unidade else numero


@rotas.post("/protocolos/ler-texto", response_model=ProtocoloLidoEmResposta)
def ler_texto(
    dados: TextoDoProtocolo,
    _: Usuario = Depends(treinador_atual),
) -> ProtocoloLidoEmResposta:
    """Transforma o protocolo escrito à mão em rascunho editável.

    Não grava nada: devolve o rascunho para o João conferir e corrigir na tela
    antes de salvar. O que o leitor não entendeu volta junto, à vista.
    """
    lido = ler_protocolo(dados.texto)
    return ProtocoloLidoEmResposta(
        protocolo=_rascunho(lido, dados.nome), nao_entendidas=lido.nao_entendidas
    )


# --------------------------------------------------------------- catálogo


@rotas.get("/alimentos", response_model=list[AlimentoEmResposta])
def buscar_alimentos(
    busca: str = "",
    limite: int = 20,
    _: Usuario = Depends(usuario_atual),
    sessao: Session = Depends(obter_sessao),
) -> list[Alimento]:
    """Busca por nome no catálogo nutricional.

    A tabela nasce vazia e só tem o que `jf importar-alimentos` colocou lá.
    Lista vazia aqui é resposta correta, não erro: o protocolo do João funciona
    inteiro sem valor nutricional nenhum.
    """
    termo = busca.strip()
    if len(termo) < 2:
        return []
    return list(
        sessao.scalars(
            select(Alimento)
            .where(Alimento.nome.icontains(termo))
            .order_by(Alimento.nome)
            .limit(max(1, min(limite, 50)))
        ).all()
    )


# ------------------------------------------------------------- aderência


def refeicao_permitida(
    refeicao_id: int,
    usuario: Usuario = Depends(usuario_atual),
    sessao: Session = Depends(obter_sessao),
) -> Refeicao:
    refeicao = sessao.get(Refeicao, refeicao_id)
    if refeicao is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Refeição não encontrada.")
    exigir_acesso(usuario, refeicao.protocolo.aluno)
    return refeicao


@rotas.get("/alunos/{aluno_id}/aderencia", response_model=list[AderenciaEmResposta])
def listar_aderencia(
    aluno: Aluno = Depends(aluno_permitido),
    sessao: Session = Depends(obter_sessao),
    dias: int = 30,
) -> list[AderenciaDaRefeicao]:
    desde = date.today() - timedelta(days=max(dias, 1))
    return list(
        sessao.scalars(
            select(AderenciaDaRefeicao)
            .where(AderenciaDaRefeicao.aluno_id == aluno.id)
            .where(AderenciaDaRefeicao.dia >= desde)
            .order_by(AderenciaDaRefeicao.dia)
        ).all()
    )


@rotas.put("/refeicoes/{refeicao_id}/aderencia", response_model=AderenciaEmResposta)
def marcar(
    dados: MarcacaoDaRefeicao,
    refeicao: Refeicao = Depends(refeicao_permitida),
    _: Usuario = Depends(consentimento_em_dia),
    sessao: Session = Depends(obter_sessao),
) -> AderenciaDaRefeicao:
    """Marca (ou desmarca) uma refeição no dia.

    `PUT` porque marcar duas vezes é a mesma marcação: o aluno que toca de novo
    corrige o que disse, não acrescenta um segundo dia.
    """
    if dados.dia > date.today():
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_CONTENT,
            "Não dá para marcar uma refeição de um dia que ainda não chegou.",
        )

    aluno_id = refeicao.protocolo.aluno_id
    marcacao = sessao.scalars(
        select(AderenciaDaRefeicao)
        .where(AderenciaDaRefeicao.aluno_id == aluno_id)
        .where(AderenciaDaRefeicao.refeicao_id == refeicao.id)
        .where(AderenciaDaRefeicao.dia == dados.dia)
    ).first()

    if marcacao is None:
        marcacao = AderenciaDaRefeicao(
            aluno_id=aluno_id, refeicao_id=refeicao.id, dia=dados.dia
        )
        sessao.add(marcacao)

    marcacao.seguiu = dados.seguiu
    marcacao.observacao = dados.observacao
    sessao.commit()
    sessao.refresh(marcacao)
    return marcacao
