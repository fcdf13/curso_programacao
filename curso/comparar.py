"""Comparação de resultados com mensagens de erro que ensinam.

O pytest padrão diz `assert 3 == 5`. Aqui a falha explica *o quê* diferiu e *onde*:
qual coluna sumiu, quantas linhas faltam, qual célula divergiu. É a diferença entre
um teste que reprova e um teste que corrige.
"""

from __future__ import annotations

import math
from typing import Any

TOLERANCIA_PADRAO = 1e-9
MAX_LINHAS_MOSTRADAS = 8
MAX_CELULAS_RELATADAS = 3


class ErroDidatico(AssertionError):
    """Falha de exercício com explicação em português."""


# --------------------------------------------------------------------------- #
# Comparação de valores soltos
# --------------------------------------------------------------------------- #

def _e_nulo(v: Any) -> bool:
    if v is None:
        return True
    try:
        return bool(v != v)  # NaN e NaT são os únicos valores diferentes de si mesmos
    except Exception:
        return False


def _e_booleano(v: Any) -> bool:
    # numpy.bool_ não é subclasse de bool, mas para o aluno é a mesma coisa.
    return isinstance(v, bool) or type(v).__name__ == "bool_"


def _iguais(a: Any, b: Any, tolerancia: float | None) -> bool:
    if _e_nulo(a) or _e_nulo(b):
        return _e_nulo(a) and _e_nulo(b)
    if _e_booleano(a) != _e_booleano(b):
        # True não é 1: quando o exercício pede booleano, devolver 1 é outra coisa.
        return False
    if _e_booleano(a):
        return bool(a) == bool(b)
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        if tolerancia is None:
            return a == b
        return math.isclose(float(a), float(b), rel_tol=tolerancia, abs_tol=tolerancia)
    try:
        return bool(a == b)
    except Exception:
        return repr(a) == repr(b)


def _mostrar(v: Any) -> str:
    if _e_nulo(v):
        return "vazio (NaN/None)"
    return repr(v)


def _tipo(v: Any) -> str:
    return type(v).__name__


# --------------------------------------------------------------------------- #
# Renderização de tabelas
# --------------------------------------------------------------------------- #

def _tabela_texto(df, titulo: str) -> str:
    import pandas as pd

    n = len(df)
    corpo = df.head(MAX_LINHAS_MOSTRADAS)
    with pd.option_context("display.max_columns", 20, "display.width", 120):
        texto = corpo.to_string()
    if n > MAX_LINHAS_MOSTRADAS:
        texto += f"\n  ... (+{n - MAX_LINHAS_MOSTRADAS} linhas)"
    plural = "linha" if n == 1 else "linhas"
    cabecalho = f"{titulo} ({n} {plural}):"
    recuado = "\n".join("    " + linha for linha in texto.splitlines())
    return f"  {cabecalho}\n{recuado}"


def _lado_a_lado(obtido, esperado) -> str:
    return _tabela_texto(esperado, "esperado") + "\n\n" + _tabela_texto(obtido, "obtido")


# --------------------------------------------------------------------------- #
# API pública
# --------------------------------------------------------------------------- #

def verificar(
    obtido: Any,
    esperado: Any,
    *,
    ignorar_ordem: bool = False,
    ignorar_indice: bool = True,
    tolerancia: float | None = TOLERANCIA_PADRAO,
    checar_tipo_coluna: bool = False,
    nome: str = "resultado",
    dica: str | None = None,
) -> None:
    """Compara `obtido` com `esperado` e levanta ErroDidatico explicando a diferença.

    ignorar_ordem      a ordem das linhas não importa (ordena os dois antes de comparar)
    ignorar_indice     o índice do DataFrame/Series não importa (padrão: True)
    tolerancia         margem para floats; None exige igualdade exata
    checar_tipo_coluna exige que os dtypes batam, não só os valores
    dica               frase extra anexada à mensagem de falha
    """
    import pandas as pd

    try:
        if isinstance(esperado, pd.DataFrame):
            _verificar_df(obtido, esperado, ignorar_ordem, ignorar_indice,
                          tolerancia, checar_tipo_coluna, nome)
        elif isinstance(esperado, pd.Series):
            _verificar_series(obtido, esperado, ignorar_ordem, ignorar_indice,
                              tolerancia, checar_tipo_coluna, nome)
        elif isinstance(esperado, (list, tuple)):
            _verificar_sequencia(obtido, esperado, ignorar_ordem, tolerancia, nome)
        elif isinstance(esperado, (set, frozenset)):
            _verificar_conjunto(obtido, esperado, nome)
        elif isinstance(esperado, dict):
            _verificar_dicionario(obtido, esperado, tolerancia, nome)
        else:
            _verificar_escalar(obtido, esperado, tolerancia, nome)
    except ErroDidatico as erro:
        if dica:
            raise ErroDidatico(f"{erro}\n\n  Dica: {dica}") from None
        raise


def _nada_devolvido(obtido: Any, nome: str) -> None:
    raise ErroDidatico(
        f"A função devolveu None — ou seja, nada.\n\n"
        f"  Isso quase sempre significa uma destas duas coisas:\n"
        f"    1. o corpo da função ainda está com `...` (você não escreveu a resposta);\n"
        f"    2. você calculou o {nome}, mas esqueceu do `return`."
    )


def _verificar_escalar(obtido, esperado, tolerancia, nome) -> None:
    if obtido is None and esperado is not None:
        _nada_devolvido(obtido, nome)
    if _iguais(obtido, esperado, tolerancia):
        return
    detalhe = ""
    if _tipo(obtido) != _tipo(esperado) and not _e_nulo(obtido):
        detalhe = (
            f"\n\n  Repare no tipo: esperado é {_tipo(esperado)}, "
            f"o seu é {_tipo(obtido)}."
        )
        if isinstance(esperado, (int, float)) and isinstance(obtido, str):
            detalhe += "\n  Números lidos como texto precisam de int(...) ou float(...)."
    raise ErroDidatico(
        f"O {nome} não bate.\n\n"
        f"    esperado: {_mostrar(esperado)}\n"
        f"    obtido:   {_mostrar(obtido)}{detalhe}"
    )


def _verificar_sequencia(obtido, esperado, ignorar_ordem, tolerancia, nome) -> None:
    if obtido is None:
        _nada_devolvido(obtido, nome)
    if not isinstance(obtido, (list, tuple)):
        raise ErroDidatico(
            f"Esperava uma {type(esperado).__name__} e recebi {_tipo(obtido)}.\n\n"
            f"    esperado: {_mostrar(esperado)}\n"
            f"    obtido:   {_mostrar(obtido)}"
        )

    a, b = list(obtido), list(esperado)
    if ignorar_ordem:
        try:
            a, b = sorted(a), sorted(b)
        except TypeError:
            pass

    if len(a) != len(b):
        raise ErroDidatico(
            f"O tamanho do {nome} não bate.\n\n"
            f"    esperado: {len(b)} itens -> {_mostrar(esperado)}\n"
            f"    obtido:   {len(a)} itens -> {_mostrar(obtido)}"
        )

    for i, (x, y) in enumerate(zip(a, b)):
        if not _iguais(x, y, tolerancia):
            posicao = f"na posição {i}" if not ignorar_ordem else f"no {i+1}º item (já ordenado)"
            raise ErroDidatico(
                f"O {nome} tem o tamanho certo, mas difere {posicao}.\n\n"
                f"    esperado[{i}]: {_mostrar(y)}\n"
                f"    obtido[{i}]:   {_mostrar(x)}\n\n"
                f"  completo:\n"
                f"    esperado: {_mostrar(esperado)}\n"
                f"    obtido:   {_mostrar(obtido)}"
            )


def _verificar_conjunto(obtido, esperado, nome) -> None:
    if obtido is None:
        _nada_devolvido(obtido, nome)
    try:
        a = set(obtido)
    except TypeError:
        raise ErroDidatico(
            f"Esperava um conjunto (set) e recebi {_tipo(obtido)}: {_mostrar(obtido)}"
        ) from None
    b = set(esperado)
    if a == b:
        return
    faltando = sorted(b - a, key=repr)
    sobrando = sorted(a - b, key=repr)
    linhas = [f"O {nome} não bate.", ""]
    if faltando:
        linhas.append(f"    itens que faltam: {faltando}")
    if sobrando:
        linhas.append(f"    itens a mais:     {sobrando}")
    linhas += ["", f"    esperado: {sorted(b, key=repr)}",
               f"    obtido:   {sorted(a, key=repr)}"]
    raise ErroDidatico("\n".join(linhas))


def _verificar_dicionario(obtido, esperado, tolerancia, nome) -> None:
    if obtido is None:
        _nada_devolvido(obtido, nome)
    if not isinstance(obtido, dict):
        raise ErroDidatico(
            f"Esperava um dicionário e recebi {_tipo(obtido)}: {_mostrar(obtido)}"
        )

    faltando = sorted(set(esperado) - set(obtido), key=repr)
    sobrando = sorted(set(obtido) - set(esperado), key=repr)
    if faltando or sobrando:
        partes = [f"As chaves do {nome} não batem.", ""]
        if faltando:
            partes.append(f"    chaves que faltam:  {faltando}")
        if sobrando:
            partes.append(f"    chaves a mais:      {sobrando}")
        raise ErroDidatico("\n".join(partes))

    for chave in esperado:
        if not _iguais(obtido[chave], esperado[chave], tolerancia):
            raise ErroDidatico(
                f"As chaves do {nome} estão certas, mas um valor difere.\n\n"
                f"    na chave {chave!r}:\n"
                f"      esperado: {_mostrar(esperado[chave])}\n"
                f"      obtido:   {_mostrar(obtido[chave])}"
            )


# --------------------------------------------------------------------------- #
# Pandas
# --------------------------------------------------------------------------- #

def _preparar(df, ignorar_ordem: bool, ignorar_indice: bool):
    if ignorar_ordem:
        colunas = list(df.columns)
        if colunas:
            df = df.sort_values(colunas, kind="stable", na_position="last")
    if ignorar_ordem or ignorar_indice:
        df = df.reset_index(drop=True)
    return df


def _verificar_df(obtido, esperado, ignorar_ordem, ignorar_indice,
                  tolerancia, checar_tipo_coluna, nome) -> None:
    import pandas as pd

    if obtido is None:
        _nada_devolvido(obtido, nome)

    if isinstance(obtido, pd.Series):
        raise ErroDidatico(
            f"Esperava um DataFrame e recebi uma Series.\n\n"
            f"  Uma Series é uma coluna só. Selecionar com colchetes duplos —\n"
            f"  df[['coluna']] em vez de df['coluna'] — devolve um DataFrame.\n\n"
            + _tabela_texto(esperado, "esperado")
        )
    if not isinstance(obtido, pd.DataFrame):
        raise ErroDidatico(
            f"Esperava um DataFrame e recebi {_tipo(obtido)}: {_mostrar(obtido)}"
        )

    # 1. Colunas
    faltando = [c for c in esperado.columns if c not in obtido.columns]
    sobrando = [c for c in obtido.columns if c not in esperado.columns]
    if faltando or sobrando:
        partes = ["As colunas do resultado não batem.", ""]
        if faltando:
            partes.append(f"    colunas que faltam: {faltando}")
        if sobrando:
            partes.append(f"    colunas a mais:     {sobrando}")
        partes += ["", f"    esperado: {list(esperado.columns)}",
                   f"    obtido:   {list(obtido.columns)}"]
        raise ErroDidatico("\n".join(partes))

    if list(obtido.columns) != list(esperado.columns):
        raise ErroDidatico(
            "As colunas certas estão lá, mas fora de ordem.\n\n"
            f"    esperado: {list(esperado.columns)}\n"
            f"    obtido:   {list(obtido.columns)}\n\n"
            "  Reordene selecionando com uma lista: df[['a', 'b', 'c']]"
        )

    esp = _preparar(esperado, ignorar_ordem, ignorar_indice)
    obt = _preparar(obtido, ignorar_ordem, ignorar_indice)

    # 2. Número de linhas
    if len(obt) != len(esp):
        diferenca = len(obt) - len(esp)
        veredito = (f"Faltam {-diferenca} linha(s)." if diferenca < 0
                    else f"Sobram {diferenca} linha(s).")
        pista = ("\n\n  Filtro apertado demais, ou uma junção que perdeu linhas\n"
                 "  (o `how=` do merge, o tipo do JOIN)."
                 if diferenca < 0 else
                 "\n\n  Filtro frouxo demais, ou uma junção que multiplicou linhas —\n"
                 "  confira se a chave do outro lado tem duplicatas.")
        raise ErroDidatico(
            f"O número de linhas não bate. {veredito}\n\n"
            + _lado_a_lado(obtido, esperado) + pista
        )

    # 3. Índice (quando importa)
    if not ignorar_indice and not obt.index.equals(esp.index):
        raise ErroDidatico(
            "As linhas batem, mas o índice não.\n\n"
            f"    esperado: {list(esp.index)[:10]}\n"
            f"    obtido:   {list(obt.index)[:10]}\n\n"
            "  Depois de filtrar, o índice guarda os números originais.\n"
            "  Use .reset_index(drop=True) para renumerar de 0 em diante."
        )

    # 4. Valores
    problemas = []
    for coluna in esp.columns:
        col_esp, col_obt = esp[coluna], obt[coluna]
        for i in range(len(esp)):
            if not _iguais(col_obt.iloc[i], col_esp.iloc[i], tolerancia):
                problemas.append((i, coluna, col_esp.iloc[i], col_obt.iloc[i]))
                if len(problemas) >= MAX_CELULAS_RELATADAS:
                    break
        if len(problemas) >= MAX_CELULAS_RELATADAS:
            break

    if problemas:
        linhas = [
            f"      linha {i}, coluna {coluna!r}: "
            f"esperado {_mostrar(valor_esp)}, obtido {_mostrar(valor_obt)}"
            for i, coluna, valor_esp, valor_obt in problemas
        ]
        ordenado = " (comparado sem levar a ordem em conta)" if ignorar_ordem else ""
        raise ErroDidatico(
            f"A forma da tabela está certa, mas há valores diferentes{ordenado}.\n\n"
            "    primeiras diferenças:\n" + "\n".join(linhas) + "\n\n"
            + _lado_a_lado(obtido, esperado)
        )

    # 5. Tipos das colunas (só se o exercício exigir)
    if checar_tipo_coluna:
        for coluna in esp.columns:
            if str(obt[coluna].dtype) != str(esp[coluna].dtype):
                raise ErroDidatico(
                    f"Os valores estão certos, mas o tipo da coluna {coluna!r} não.\n\n"
                    f"    esperado: {esp[coluna].dtype}\n"
                    f"    obtido:   {obt[coluna].dtype}\n\n"
                    "  Converta com .astype(...) ou pd.to_numeric / pd.to_datetime."
                )


def _verificar_series(obtido, esperado, ignorar_ordem, ignorar_indice,
                      tolerancia, checar_tipo_coluna, nome) -> None:
    import pandas as pd

    if obtido is None:
        _nada_devolvido(obtido, nome)

    if isinstance(obtido, pd.DataFrame):
        if obtido.shape[1] == 1:
            raise ErroDidatico(
                "Esperava uma Series e recebi um DataFrame de uma coluna só.\n\n"
                "  df[['coluna']] devolve DataFrame; df['coluna'] devolve Series.\n"
                "  Aqui o exercício pede a Series — use colchetes simples."
            )
        raise ErroDidatico(
            f"Esperava uma Series (uma coluna) e recebi um DataFrame "
            f"com {obtido.shape[1]} colunas."
        )
    if not isinstance(obtido, pd.Series):
        raise ErroDidatico(
            f"Esperava uma Series e recebi {_tipo(obtido)}: {_mostrar(obtido)}"
        )

    esp = esperado.sort_values(kind="stable") if ignorar_ordem else esperado
    obt = obtido.sort_values(kind="stable") if ignorar_ordem else obtido
    if ignorar_ordem or ignorar_indice:
        esp, obt = esp.reset_index(drop=True), obt.reset_index(drop=True)

    if len(obt) != len(esp):
        raise ErroDidatico(
            f"O tamanho da Series não bate: esperado {len(esp)}, obtido {len(obt)}.\n\n"
            + _lado_a_lado(obtido.to_frame(name=obtido.name or "valor"),
                           esperado.to_frame(name=esperado.name or "valor"))
        )

    if not ignorar_indice and not obt.index.equals(esp.index):
        raise ErroDidatico(
            "Os valores batem em quantidade, mas o índice não.\n\n"
            f"    esperado: {list(esp.index)[:10]}\n"
            f"    obtido:   {list(obt.index)[:10]}"
        )

    for i in range(len(esp)):
        if not _iguais(obt.iloc[i], esp.iloc[i], tolerancia):
            rotulo = esp.index[i]
            raise ErroDidatico(
                f"A Series tem o tamanho certo, mas difere na posição {i} "
                f"(índice {rotulo!r}).\n\n"
                f"    esperado: {_mostrar(esp.iloc[i])}\n"
                f"    obtido:   {_mostrar(obt.iloc[i])}\n\n"
                + _lado_a_lado(obtido.to_frame(name=obtido.name or "valor"),
                               esperado.to_frame(name=esperado.name or "valor"))
            )

    if checar_tipo_coluna and str(obt.dtype) != str(esp.dtype):
        raise ErroDidatico(
            f"Os valores estão certos, mas o tipo não.\n\n"
            f"    esperado: {esp.dtype}\n    obtido:   {obt.dtype}"
        )
