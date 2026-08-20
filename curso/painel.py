"""Tudo que o curso mostra no terminal."""

from __future__ import annotations

from datetime import date

from rich.console import Console, Group
from rich.markdown import Markdown
from rich.panel import Panel
from rich.rule import Rule
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text

from curso import progresso as prog
from curso.registro import NOMES_DOS_BLOCOS, Exercicio

console = Console()

COR_DO_NIVEL = {1: "green", 2: "green", 3: "yellow", 4: "dark_orange", 5: "red"}


def _cabecalho(ex: Exercicio) -> Text:
    linha = Text()
    linha.append(ex.id, style="bold cyan")
    linha.append("  ·  ")
    linha.append(ex.titulo, style="bold")
    return linha


def _subtitulo(ex: Exercicio) -> str:
    tags = " ".join(f"#{t}" for t in ex.tags)
    cor = COR_DO_NIVEL.get(ex.nivel, "white")
    return (f"[{cor}]{ex.estrelas}[/] nível {ex.nivel}  ·  ~{ex.tempo_min} min"
            f"  ·  [dim]{tags}[/]")


def mostrar_exercicio(ex: Exercicio, arquivo_resposta, ficha: prog.Ficha | None = None) -> None:
    # O enunciado é escrito em Markdown: blocos indentados viram exemplos de código.
    corpo = [Markdown(ex.enunciado)]

    if ficha and ficha.tentativas:
        corpo.append(Text(""))
        estado = ("já resolvido — isto é uma revisão" if ficha.estado == prog.RESOLVIDO
                  else f"{ficha.tentativas} tentativa(s) até agora")
        corpo.append(Text(f"({estado})", style="dim italic"))

    console.print()
    console.print(Panel(
        Group(*corpo),
        title=_cabecalho(ex),
        subtitle=_subtitulo(ex),
        border_style="cyan",
        padding=(1, 2),
    ))
    console.print(f"  [bold]escreva em:[/] {arquivo_resposta}")
    console.print(f"  [dim]conferir:[/]   curso check {ex.id}"
                  f"    [dim]travou?[/] curso dica {ex.id}")
    console.print()


def mostrar_acerto(ex: Exercicio, ficha: prog.Ficha, passaram: int) -> None:
    dias = ficha.intervalo_dias
    quando = "amanhã" if dias == 1 else f"em {dias} dias"
    plural = "1 teste verde" if passaram == 1 else f"{passaram} testes verdes"

    rodada = ("Revisão em dia." if ficha.revisoes
              else f"Resolvido em {ficha.tentativas_ate_acertar} tentativa(s).")

    console.print()
    console.print(Panel(
        Text.from_markup(
            f"[bold green]Passou.[/]  {plural}.\n\n"
            f"{rodada}\n"
            f"Volta para revisão [bold]{quando}[/] ({ficha.proxima_revisao})."
        ),
        title=_cabecalho(ex),
        border_style="green",
        padding=(1, 2),
    ))
    console.print()


def mostrar_falha(ex: Exercicio, mensagem: str, nome_do_teste: str,
                  dicas_restantes: int) -> None:
    rodape = []
    if dicas_restantes > 0:
        rodape.append(f"[dim]precisa de um empurrão?[/] curso dica {ex.id}")
    rodape.append(f"[dim]desistiu?[/] curso solucao {ex.id}")

    console.print()
    console.print(Panel(
        Text(mensagem),
        title=Text.assemble(("✗ ", "bold red"), _cabecalho(ex)),
        subtitle=f"[dim]falhou em {nome_do_teste}[/]",
        border_style="red",
        padding=(1, 2),
    ))
    console.print("  " + "    ".join(rodape))
    console.print()


def mostrar_dica(ex: Exercicio, numero: int, texto: str, total: int) -> None:
    console.print()
    console.print(Panel(
        Text(texto),
        title=f"Dica {numero} de {total}  ·  {ex.id}",
        border_style="yellow",
        padding=(1, 2),
    ))
    console.print()


def mostrar_solucao(ex: Exercicio, codigo: str) -> None:
    lexer = "python" if ex.linguagem == "python" else "sql"
    console.print()
    console.print(Panel(
        Syntax(codigo, lexer, theme="ansi_dark", line_numbers=False, word_wrap=True),
        title=Text.assemble(("gabarito  ·  ", "dim"), _cabecalho(ex)),
        border_style="magenta",
        padding=(1, 2),
    ))
    console.print(
        "  [dim]Ler a solução zera o intervalo de revisão: este exercício volta amanhã.[/]"
    )
    console.print()


def mostrar_plano(novos: list[Exercicio], revisoes: list[tuple[Exercicio, prog.Ficha]],
                  sequencia: int) -> None:
    console.print()
    titulo = Text("Plano de hoje", style="bold")
    if sequencia:
        titulo.append(f"   {sequencia} dia(s) seguidos", style="dim")
    console.print(titulo)

    if revisoes:
        console.print(Rule(f"[yellow]revisar ({len(revisoes)})[/]", align="left", style="dim"))
        for ex, ficha in revisoes:
            atraso = -(ficha.dias_ate_revisao() or 0)
            nota = "vence hoje" if atraso <= 0 else f"{atraso} dia(s) de atraso"
            console.print(f"  [cyan]{ex.id}[/]  {ex.titulo:<44.44} [dim]{nota}[/]")

    if novos:
        console.print(Rule(f"[green]aprender ({len(novos)})[/]", align="left", style="dim"))
        for ex in novos:
            cor = COR_DO_NIVEL.get(ex.nivel, "white")
            console.print(
                f"  [cyan]{ex.id}[/]  {ex.titulo:<44.44} [{cor}]{ex.estrelas}[/] "
                f"[dim]~{ex.tempo_min} min[/]"
            )

    if not novos and not revisoes:
        console.print("\n  [green]Nada pendente hoje.[/] "
                      "Quer adiantar? [bold]curso proximo[/]\n")
        return

    console.print()
    console.print("  comece com: [bold]curso proximo[/]")
    console.print()


def _barra(feitos: int, total: int, largura: int = 24) -> str:
    if total == 0:
        return "[dim]" + "░" * largura + "[/]"
    # Com pelo menos um resolvido, mostra ao menos um bloco: arredondar para
    # zero faria a barra parecer vazia depois do primeiro acerto.
    cheios = max(1, round(largura * feitos / total)) if feitos else 0
    cor = "green" if feitos == total else "cyan"
    return f"[{cor}]{'█' * cheios}[/][dim]{'░' * (largura - cheios)}[/]"


def mostrar_progresso(exercicios: tuple[Exercicio, ...], p: prog.Progresso) -> None:
    resolvidos = p.resolvidos()
    hoje = date.today()

    tabela = Table(box=None, padding=(0, 2), show_header=True, header_style="dim")
    tabela.add_column("bloco")
    tabela.add_column("módulo")
    tabela.add_column("")
    tabela.add_column("feitos", justify="right")

    bloco_anterior = None
    for ex_bloco in ("A", "B", "C", "D"):
        do_bloco = [e for e in exercicios if e.bloco == ex_bloco]
        if not do_bloco:
            continue
        modulos: dict[str, list[Exercicio]] = {}
        for ex in do_bloco:
            modulos.setdefault(ex.nome_do_modulo, []).append(ex)

        for nome, lista in modulos.items():
            feitos = sum(1 for e in lista if e.id in resolvidos)
            rotulo = NOMES_DOS_BLOCOS[ex_bloco] if ex_bloco != bloco_anterior else ""
            bloco_anterior = ex_bloco
            tabela.add_row(
                f"[bold]{rotulo}[/]" if rotulo else "",
                nome,
                _barra(feitos, len(lista)),
                f"{feitos}/{len(lista)}",
            )

    total = len(exercicios)
    feitos = len(resolvidos & {e.id for e in exercicios})
    vencidas = len(p.vencidas(hoje))
    proximas = sum(1 for f in p.fichas.values()
                   if f.estado == prog.RESOLVIDO and not f.vencida(hoje))

    console.print()
    console.print(tabela)
    console.print()
    console.print(f"  [bold]{feitos}/{total}[/] exercícios  {_barra(feitos, total, 30)}")
    console.print(
        f"  [dim]sequência:[/] {p.sequencia_de_dias(hoje)} dia(s)   "
        f"[dim]a revisar hoje:[/] {vencidas}   "
        f"[dim]agendados:[/] {proximas}"
    )
    console.print()


def mostrar_lista(exercicios: list[Exercicio], p: prog.Progresso, titulo: str) -> None:
    resolvidos = p.resolvidos()
    console.print()
    console.print(f"[bold]{titulo}[/] ({len(exercicios)})")
    console.print()
    for ex in exercicios:
        marca = "[green]✓[/]" if ex.id in resolvidos else " "
        cor = COR_DO_NIVEL.get(ex.nivel, "white")
        console.print(
            f"  {marca} [cyan]{ex.id}[/]  {ex.titulo:<46.46} "
            f"[{cor}]{ex.estrelas}[/]  [dim]{' '.join('#' + t for t in ex.tags[:3])}[/]"
        )
    console.print()


def erro(mensagem: str) -> None:
    console.print(f"\n  [bold red]![/] {mensagem}\n")


def aviso(mensagem: str) -> None:
    console.print(f"  [yellow]·[/] {mensagem}")


def ok(mensagem: str) -> None:
    console.print(f"  [green]✓[/] {mensagem}")
