"""Seu estado no curso: o que já resolveu, quantas tentativas levou, o que vence hoje.

Tudo mora em `.curso/progresso.json` — texto simples, seu, local, fácil de inspecionar.
"""

from __future__ import annotations

import json
import shutil
from dataclasses import asdict, dataclass
from datetime import date, datetime, timedelta
from pathlib import Path

from curso import caminhos, srs

VERSAO = 1

NOVO = "novo"
EM_ANDAMENTO = "em_andamento"
RESOLVIDO = "resolvido"


@dataclass
class Ficha:
    """O histórico de um exercício."""
    id: str
    estado: str = NOVO
    tentativas: int = 0
    tentativas_ate_acertar: int = 0
    viu_solucao: bool = False
    dicas_vistas: int = 0
    primeira_em: str = ""
    ultima_em: str = ""
    facilidade: float = srs.FACILIDADE_INICIAL
    intervalo_dias: int = 0
    repeticoes: int = 0
    proxima_revisao: str = ""
    revisoes: int = 0

    def vencida(self, hoje: date | None = None) -> bool:
        if self.estado != RESOLVIDO or not self.proxima_revisao:
            return False
        return date.fromisoformat(self.proxima_revisao) <= (hoje or date.today())

    def dias_ate_revisao(self, hoje: date | None = None) -> int | None:
        if self.estado != RESOLVIDO or not self.proxima_revisao:
            return None
        return (date.fromisoformat(self.proxima_revisao) - (hoje or date.today())).days


class Progresso:
    def __init__(self, dados: dict | None = None, arquivo: Path | None = None):
        self.arquivo = arquivo or (caminhos.pasta_estado() / "progresso.json")
        dados = dados or {}
        self.fichas: dict[str, Ficha] = {
            id_: Ficha(**valores) for id_, valores in dados.get("exercicios", {}).items()
        }
        self.dias_praticados: list[str] = dados.get("dias_praticados", [])

    # ---------------------------------------------------------------- carga --
    @classmethod
    def carregar(cls, arquivo: Path | None = None) -> "Progresso":
        alvo = arquivo or (caminhos.pasta_estado() / "progresso.json")
        if not alvo.exists():
            return cls(arquivo=alvo)
        dados = json.loads(alvo.read_text(encoding="utf-8"))
        if dados.get("versao") != VERSAO:
            raise ValueError(
                f"{alvo} foi gravado por outra versão do curso "
                f"(versao={dados.get('versao')}, esperada={VERSAO})."
            )
        return cls(dados, arquivo=alvo)

    def salvar(self) -> None:
        self.arquivo.parent.mkdir(parents=True, exist_ok=True)
        conteudo = {
            "versao": VERSAO,
            "dias_praticados": self.dias_praticados,
            "exercicios": {id_: asdict(f) for id_, f in sorted(self.fichas.items())},
        }
        temporario = self.arquivo.with_suffix(".json.tmp")
        temporario.write_text(
            json.dumps(conteudo, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        temporario.replace(self.arquivo)

    # --------------------------------------------------------------- acesso --
    def ficha(self, id_exercicio: str) -> Ficha:
        return self.fichas.setdefault(id_exercicio, Ficha(id=id_exercicio))

    def resolvidos(self) -> set[str]:
        return {id_ for id_, f in self.fichas.items() if f.estado == RESOLVIDO}

    def vencidas(self, hoje: date | None = None) -> list[Ficha]:
        pendentes = [f for f in self.fichas.values() if f.vencida(hoje)]
        return sorted(pendentes, key=lambda f: (f.proxima_revisao, f.id))

    # ------------------------------------------------------------- registro --
    def _marcar_dia(self) -> None:
        hoje = date.today().isoformat()
        if hoje not in self.dias_praticados:
            self.dias_praticados.append(hoje)
            self.dias_praticados = sorted(self.dias_praticados)[-400:]

    def registrar_tentativa(self, id_exercicio: str, acertou: bool,
                            hoje: date | None = None) -> Ficha:
        """Contabiliza uma execução de `curso check` e reagenda se acertou."""
        agora = datetime.now().isoformat(timespec="seconds")
        ficha = self.ficha(id_exercicio)
        ficha.tentativas += 1
        ficha.ultima_em = agora
        if not ficha.primeira_em:
            ficha.primeira_em = agora
        self._marcar_dia()

        if not acertou:
            if ficha.estado != RESOLVIDO:
                ficha.estado = EM_ANDAMENTO
            return ficha

        era_revisao = ficha.estado == RESOLVIDO
        if era_revisao:
            ficha.revisoes += 1
            tentativas_da_rodada = ficha.tentativas - ficha.tentativas_ate_acertar
        else:
            tentativas_da_rodada = ficha.tentativas
            ficha.tentativas_ate_acertar = ficha.tentativas

        nota = srs.qualidade(
            max(1, tentativas_da_rodada), acertou=True, viu_solucao=ficha.viu_solucao
        )
        agendamento, repeticoes = srs.agendar(
            nota,
            facilidade=ficha.facilidade,
            intervalo_dias=ficha.intervalo_dias,
            repeticoes=ficha.repeticoes,
            hoje=hoje,
        )
        ficha.estado = RESOLVIDO
        ficha.facilidade = round(agendamento.facilidade, 3)
        ficha.intervalo_dias = agendamento.intervalo_dias
        ficha.repeticoes = repeticoes
        ficha.proxima_revisao = agendamento.proxima_revisao.isoformat()
        ficha.viu_solucao = False  # zera para a próxima rodada de revisão
        return ficha

    def registrar_dica(self, id_exercicio: str) -> int:
        ficha = self.ficha(id_exercicio)
        ficha.dicas_vistas += 1
        return ficha.dicas_vistas

    def registrar_solucao_vista(self, id_exercicio: str) -> None:
        self.ficha(id_exercicio).viu_solucao = True

    def preparar_revisao(self, id_exercicio: str) -> Path | None:
        """Arquiva sua resposta atual e a remove, para você resolver do zero.

        Devolve o caminho do arquivo guardado (ou None se não havia resposta).
        """
        from curso import registro

        exercicio = registro.por_id(id_exercicio)
        resposta = exercicio.caminho_resposta
        if not resposta.exists():
            return None

        carimbo = datetime.now().strftime("%Y%m%d-%H%M%S")
        destino = (caminhos.pasta_estado() / "historico" / id_exercicio /
                   f"{carimbo}{resposta.suffix}")
        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(resposta), destino)

        ficha = self.ficha(id_exercicio)
        ficha.dicas_vistas = 0
        return destino

    # ------------------------------------------------------------ relatório --
    def sequencia_de_dias(self, hoje: date | None = None) -> int:
        """Quantos dias seguidos você praticou, contando de hoje (ou ontem) para trás."""
        if not self.dias_praticados:
            return 0
        hoje = hoje or date.today()
        praticados = {date.fromisoformat(d) for d in self.dias_praticados}

        inicio = hoje if hoje in praticados else hoje - timedelta(days=1)
        if inicio not in praticados:
            return 0
        total, dia = 0, inicio
        while dia in praticados:
            total += 1
            dia -= timedelta(days=1)
        return total
