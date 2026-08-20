"""Linha de comando do curso.

    curso web         abre a interface no navegador
    curso setup       prepara o dataset (rode uma vez)
    curso hoje        o plano do dia: revisões vencidas + material novo
    curso proximo     abre o próximo exercício
    curso check       corrige o exercício em que você está
    curso dica        libera a próxima dica
    curso solucao     mostra o gabarito comentado
    curso revisar     sessão de revisão espaçada
    curso progresso   painel de progresso
    curso listar      índice dos exercícios
    curso buscar      procura por tema, tag ou id
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

from curso import caminhos, executor, painel, registro
from curso import progresso as prog
from curso.registro import Exercicio, ErroDeCatalogo


# --------------------------------------------------------------------------- #
# Auxiliares
# --------------------------------------------------------------------------- #

def _abrir_resposta(ex: Exercicio) -> Path:
    """Garante que exista uma cópia editável do exercício em respostas/."""
    destino = ex.caminho_resposta
    if not destino.exists():
        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ex.caminho, destino)
    return destino


def _resolver_alvo(identificador: str | None, p: prog.Progresso) -> Exercicio:
    """O exercício pedido, ou aquele em que você está trabalhando agora."""
    if identificador:
        return registro.por_id(identificador)

    em_andamento = [
        ex for ex in registro.catalogo()
        if p.fichas.get(ex.id, prog.Ficha(id=ex.id)).estado == prog.EM_ANDAMENTO
    ]
    if em_andamento:
        return em_andamento[0]

    proximo = _proximo_nao_resolvido(p)
    if proximo is None:
        raise ErroDeCatalogo("Você resolveu todos os exercícios. Rode `curso revisar`.")
    return proximo


def _proximo_nao_resolvido(p: prog.Progresso, bloco: str | None = None) -> Exercicio | None:
    resolvidos = p.resolvidos()
    for ex in registro.catalogo():
        if bloco and ex.bloco != bloco.upper():
            continue
        if ex.id not in resolvidos:
            return ex
    return None


def _pendencias(p: prog.Progresso) -> list[tuple[Exercicio, prog.Ficha]]:
    por_id = {ex.id: ex for ex in registro.catalogo()}
    return [(por_id[f.id], f) for f in p.vencidas() if f.id in por_id]


# --------------------------------------------------------------------------- #
# Comandos
# --------------------------------------------------------------------------- #

def comando_setup(args) -> int:
    from dados import gerar

    gerar.construir(forcar=args.forcar)
    return 0


def comando_web(args) -> int:
    from curso import servidor

    servidor.subir(porta=args.porta, dev=args.dev, abrir=not args.sem_navegador)
    return 0


def comando_hoje(args) -> int:
    p = prog.Progresso.carregar()
    revisoes = _pendencias(p)

    resolvidos = p.resolvidos()
    novos: list[Exercicio] = []
    for ex in registro.catalogo():
        if len(novos) >= args.quantidade:
            break
        if ex.id not in resolvidos:
            novos.append(ex)

    painel.mostrar_plano(novos, revisoes, p.sequencia_de_dias())
    return 0


def comando_proximo(args) -> int:
    p = prog.Progresso.carregar()
    ex = _proximo_nao_resolvido(p, args.bloco)
    if ex is None:
        painel.ok("Nenhum exercício novo por aqui. Rode `curso revisar`.")
        return 0
    painel.mostrar_exercicio(ex, _abrir_resposta(ex), p.fichas.get(ex.id))
    return 0


def comando_ver(args) -> int:
    p = prog.Progresso.carregar()
    ex = registro.por_id(args.id)
    painel.mostrar_exercicio(ex, _abrir_resposta(ex), p.fichas.get(ex.id))
    return 0


def comando_check(args) -> int:
    p = prog.Progresso.carregar()
    ex = _resolver_alvo(args.id, p)
    _abrir_resposta(ex)

    resultado = executor.corrigir(ex)
    ficha = p.registrar_tentativa(ex.id, resultado.ok)
    p.salvar()

    if resultado.ok:
        painel.mostrar_acerto(ex, ficha, resultado.passaram)
        return 0

    painel.mostrar_falha(
        ex, resultado.primeira_falha, resultado.nome_da_falha,
        dicas_restantes=max(0, len(ex.dicas) - ficha.dicas_vistas),
    )
    return 1


def comando_dica(args) -> int:
    p = prog.Progresso.carregar()
    ex = _resolver_alvo(args.id, p)

    if not ex.dicas:
        painel.aviso(f"{ex.id} não tem dicas cadastradas.")
        return 0

    ficha = p.ficha(ex.id)
    if ficha.dicas_vistas >= len(ex.dicas):
        painel.aviso(
            f"Você já viu as {len(ex.dicas)} dicas. "
            f"O gabarito está em `curso solucao {ex.id}`."
        )
        return 0

    numero = p.registrar_dica(ex.id)
    p.salvar()
    painel.mostrar_dica(ex, numero, ex.dicas[numero - 1], len(ex.dicas))
    return 0


def comando_solucao(args) -> int:
    p = prog.Progresso.carregar()
    ex = _resolver_alvo(args.id, p)
    ficha = p.ficha(ex.id)

    if not ex.caminho_solucao.exists():
        painel.erro(f"O gabarito de {ex.id} está faltando no repositório.")
        return 1

    if ficha.estado != prog.RESOLVIDO and ficha.tentativas < 1 and not args.forcar:
        painel.aviso(
            "Tente pelo menos uma vez antes de olhar a solução — "
            "errar é o que fixa.\n    Rode `curso check` primeiro, "
            f"ou insista com `curso solucao {ex.id} --forcar`."
        )
        return 1

    if ficha.estado != prog.RESOLVIDO:
        p.registrar_solucao_vista(ex.id)
        p.salvar()

    painel.mostrar_solucao(ex, ex.codigo_da_solucao())
    return 0


def comando_revisar(args) -> int:
    p = prog.Progresso.carregar()
    pendentes = _pendencias(p)

    if not pendentes:
        proxima = sorted(
            (f for f in p.fichas.values() if f.estado == prog.RESOLVIDO and f.proxima_revisao),
            key=lambda f: f.proxima_revisao,
        )
        if proxima:
            painel.ok(f"Nada vencido hoje. A próxima revisão é em {proxima[0].proxima_revisao}.")
        else:
            painel.aviso("Você ainda não resolveu nada — não há o que revisar.")
        return 0

    ex, _ = pendentes[0]
    guardado = p.preparar_revisao(ex.id)
    p.salvar()

    painel.console.print()
    painel.console.print(
        f"  [yellow]Revisão[/] — {len(pendentes)} exercício(s) vencido(s)."
    )
    if guardado:
        painel.console.print(
            f"  [dim]Sua resposta anterior foi guardada em {guardado.relative_to(caminhos.raiz())}"
            f" — resolva de novo, do zero.[/]"
        )
    painel.mostrar_exercicio(ex, _abrir_resposta(ex), p.fichas.get(ex.id))
    return 0


def comando_progresso(args) -> int:
    p = prog.Progresso.carregar()
    painel.mostrar_progresso(registro.catalogo(), p)
    return 0


def comando_listar(args) -> int:
    p = prog.Progresso.carregar()
    exercicios = list(registro.catalogo())
    titulo = "Todos os exercícios"
    if args.bloco:
        exercicios = [e for e in exercicios if e.bloco == args.bloco.upper()]
        titulo = f"Bloco {args.bloco.upper()} — {registro.NOMES_DOS_BLOCOS.get(args.bloco.upper(), '')}"
    painel.mostrar_lista(exercicios, p, titulo)
    return 0


def comando_buscar(args) -> int:
    p = prog.Progresso.carregar()
    achados = registro.buscar(args.termo)
    if not achados:
        painel.aviso(f"Nada encontrado para {args.termo!r}.")
        return 1
    painel.mostrar_lista(achados, p, f"Resultados para {args.termo!r}")
    return 0


# --------------------------------------------------------------------------- #
# Montagem do parser
# --------------------------------------------------------------------------- #

def construir_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="curso",
        description="Curso progressivo de Python, Pandas e SQL — dataset Loja Aurora.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Comece por:  curso setup  →  curso hoje  →  curso proximo",
    )
    sub = parser.add_subparsers(dest="comando", required=True, metavar="<comando>")

    p_setup = sub.add_parser("setup", help="gera o dataset e o banco (rode uma vez)")
    p_setup.add_argument("--forcar", action="store_true", help="regenera mesmo se já existir")
    p_setup.set_defaults(funcao=comando_setup)

    p_web = sub.add_parser("web", help="abre a interface no navegador")
    p_web.add_argument("-p", "--porta", type=int, default=8765)
    p_web.add_argument("--dev", action="store_true",
                       help="só a API; o front roda em `npm run dev`")
    p_web.add_argument("--sem-navegador", action="store_true",
                       help="não abre o navegador sozinho")
    p_web.set_defaults(funcao=comando_web)

    p_hoje = sub.add_parser("hoje", help="o plano do dia")
    p_hoje.add_argument("-n", "--quantidade", type=int, default=5,
                        help="quantos exercícios novos sugerir (padrão: 5)")
    p_hoje.set_defaults(funcao=comando_hoje)

    p_proximo = sub.add_parser("proximo", help="abre o próximo exercício não resolvido")
    p_proximo.add_argument("-b", "--bloco", help="limita a um bloco: A, B, C ou D")
    p_proximo.set_defaults(funcao=comando_proximo)

    p_ver = sub.add_parser("ver", help="mostra o enunciado de um exercício")
    p_ver.add_argument("id")
    p_ver.set_defaults(funcao=comando_ver)

    p_check = sub.add_parser("check", help="corrige sua resposta")
    p_check.add_argument("id", nargs="?", help="id do exercício (padrão: o atual)")
    p_check.set_defaults(funcao=comando_check)

    p_dica = sub.add_parser("dica", help="libera a próxima dica")
    p_dica.add_argument("id", nargs="?")
    p_dica.set_defaults(funcao=comando_dica)

    p_solucao = sub.add_parser("solucao", help="mostra o gabarito comentado")
    p_solucao.add_argument("id", nargs="?")
    p_solucao.add_argument("--forcar", action="store_true",
                           help="mostra mesmo sem ter tentado")
    p_solucao.set_defaults(funcao=comando_solucao)

    p_revisar = sub.add_parser("revisar", help="sessão de revisão espaçada")
    p_revisar.set_defaults(funcao=comando_revisar)

    p_progresso = sub.add_parser("progresso", help="painel de progresso")
    p_progresso.set_defaults(funcao=comando_progresso)

    p_listar = sub.add_parser("listar", help="índice dos exercícios")
    p_listar.add_argument("-b", "--bloco", help="A, B, C ou D")
    p_listar.set_defaults(funcao=comando_listar)

    p_buscar = sub.add_parser("buscar", help="procura por tema, tag ou id")
    p_buscar.add_argument("termo")
    p_buscar.set_defaults(funcao=comando_buscar)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = construir_parser().parse_args(argv)
    try:
        return args.funcao(args)
    except (ErroDeCatalogo, FileNotFoundError, RuntimeError, ValueError) as erro:
        painel.erro(str(erro))
        return 2
    except KeyboardInterrupt:
        painel.console.print("\n  [dim]interrompido[/]\n")
        return 130


if __name__ == "__main__":
    sys.exit(main())
