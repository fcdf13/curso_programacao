"""Materializa os exercícios declarados em autoria/ nas três árvores do curso.

    python -m autoria.construir            # gera tudo
    python -m autoria.construir --limpar   # apaga o gerado antes (remove órfãos)

Os arquivos em exercicios/, solucoes/ e nos testes/ são **gerados**: editá-los à
mão funciona até a próxima geração. A fonte da verdade são os módulos de autoria.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

from autoria import (
    a01_a03,
    a04_a06,
    a07_revisao,
    a08_dicionarios_conjuntos,
    a09_complexidade,
    a10_tuplas,
    a11_funcoes,
    a12_compreensoes,
    a13_erros_e_excecoes,
    vitrine,
)
from autoria.modelo import Modulo, materializar_modulo
from curso import caminhos

MODULOS: list[Modulo] = [
    *a01_a03.MODULOS,
    *a04_a06.MODULOS,
    *a07_revisao.MODULOS,
    *a08_dicionarios_conjuntos.MODULOS,
    *a09_complexidade.MODULOS,
    *a10_tuplas.MODULOS,
    *a11_funcoes.MODULOS,
    *a12_compreensoes.MODULOS,
    *a13_erros_e_excecoes.MODULOS,
    *vitrine.MODULOS,
]


def _limpar_arvores() -> None:
    for arvore in (caminhos.EXERCICIOS, caminhos.SOLUCOES):
        alvo = caminhos.raiz() / arvore
        if alvo.exists():
            shutil.rmtree(alvo)
        alvo.mkdir(parents=True)


def conferir_consistencia() -> list[str]:
    """Erros que só aparecem olhando o conjunto: ids repetidos, pré-requisito futuro."""
    problemas: list[str] = []
    vistos: set[str] = set()
    todos = [ex for modulo in MODULOS for ex in modulo.exercicios]
    conhecidos = {ex.id for ex in todos}

    for ex in todos:
        if ex.id in vistos:
            problemas.append(f"id duplicado: {ex.id}")
        vistos.add(ex.id)

        for pre in ex.requer:
            if pre not in conhecidos:
                problemas.append(f"{ex.id} exige {pre}, que não existe")
            elif pre >= ex.id:
                problemas.append(f"{ex.id} exige {pre}, que vem depois dele")

        if not ex.dicas:
            problemas.append(f"{ex.id} não tem dicas")
        if ex.linguagem == "python" and not ex.solucao.strip():
            problemas.append(f"{ex.id} não tem solução")
        if "def teste_" not in ex.testes:
            problemas.append(f"{ex.id} não tem nenhuma função de teste")

    return problemas


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limpar", action="store_true",
                        help="apaga exercicios/ e solucoes/ antes de gerar")
    args = parser.parse_args(argv)

    problemas = conferir_consistencia()
    if problemas:
        print("Inconsistências na autoria:", file=sys.stderr)
        for p in problemas:
            print(f"  - {p}", file=sys.stderr)
        return 1

    if args.limpar:
        _limpar_arvores()

    total_de_arquivos = 0
    for modulo in MODULOS:
        criados = materializar_modulo(modulo)
        total_de_arquivos += len(criados)
        print(f"  {modulo.id}  {len(modulo.exercicios):>3} exercícios  {modulo.titulo}")

    total_de_exercicios = sum(len(m.exercicios) for m in MODULOS)
    print(f"\n  {total_de_exercicios} exercícios · "
          f"{total_de_arquivos} arquivos · {len(MODULOS)} módulos")
    print("\n  Confira o gabarito com:  pytest --solucoes\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
