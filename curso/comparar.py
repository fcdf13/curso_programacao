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
MAX_LINHAS_ESTRUTURADAS = 50


class ErroDidatico(AssertionError):
    """Falha de exercício com explicação em português.

    `mensagem` é o texto pronto para o terminal. `dados` é a mesma falha em forma
    estruturada — é o que permite à interface web desenhar tabelas de verdade em vez
    de despejar o texto do terminal dentro de um <pre>.
    """

    def __init__(self, mensagem: str, dados: dict | None = None):
        super().__init__(mensagem)
        self.dados = dados or {}


def _erro(mensagem: str, **dados: Any) -> ErroDidatico:
    """Levanta a falha carregando junto a versão estruturada dela."""
    return ErroDidatico(mensagem, dados)


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
# Serialização da falha (consumida pela API web)
# --------------------------------------------------------------------------- #

def _para_json(valor: Any) -> Any:
    """Converte um valor de célula em algo que o json aceite."""
    if _e_nulo(valor):
        return None
    if _e_booleano(valor):
        return bool(valor)
    if isinstance(valor, float):
        return valor if math.isfinite(valor) else str(valor)
    if isinstance(valor, (int, str)):
        return valor
    if hasattr(valor, "item"):          # numpy escalar
        try:
            return _para_json(valor.item())
        except (ValueError, AttributeError):
            pass
    if hasattr(valor, "isoformat"):     # data, hora, Timestamp
        return valor.isoformat()
    return str(valor)


def _tabela_json(df, limite: int = MAX_LINHAS_ESTRUTURADAS) -> dict:
    """Um DataFrame em forma serializável, truncado mas informando o total real."""
    recorte = df.head(limite)
    return {
        "colunas": [str(c) for c in df.columns],
        "linhas": [
            [_para_json(v) for v in linha]
            for linha in recorte.itertuples(index=False, name=None)
        ],
        "total": int(len(df)),
    }


def _como_quadro(serie):
    return serie.to_frame(name=serie.name if serie.name is not None else "valor")


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
            raise ErroDidatico(f"{erro}\n\n  Dica: {dica}", erro.dados) from None
        raise


def _nada_devolvido(obtido: Any, nome: str) -> None:
    raise _erro(
        f"A função devolveu None — ou seja, nada.\n\n"
        f"  Isso quase sempre significa uma destas duas coisas:\n"
        f"    1. o corpo da função ainda está com `...` (você não escreveu a resposta);\n"
        f"    2. você calculou o {nome}, mas esqueceu do `return`.",
        tipo="sem_retorno",
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
    raise _erro(
        f"O {nome} não bate.\n\n"
        f"    esperado: {_mostrar(esperado)}\n"
        f"    obtido:   {_mostrar(obtido)}{detalhe}",
        tipo="valor_escalar",
        esperado=_para_json(esperado),
        obtido=_para_json(obtido),
        tipo_esperado=_tipo(esperado),
        tipo_obtido=_tipo(obtido),
    )


def _verificar_sequencia(obtido, esperado, ignorar_ordem, tolerancia, nome) -> None:
    if obtido is None:
        _nada_devolvido(obtido, nome)
    if not isinstance(obtido, (list, tuple)):
        raise _erro(
            f"Esperava uma {type(esperado).__name__} e recebi {_tipo(obtido)}.\n\n"
            f"    esperado: {_mostrar(esperado)}\n"
            f"    obtido:   {_mostrar(obtido)}",
            tipo="tipo_errado",
            tipo_esperado=type(esperado).__name__,
            tipo_obtido=_tipo(obtido),
        )

    a, b = list(obtido), list(esperado)
    if ignorar_ordem:
        try:
            a, b = sorted(a), sorted(b)
        except TypeError:
            pass

    if len(a) != len(b):
        raise _erro(
            f"O tamanho do {nome} não bate.\n\n"
            f"    esperado: {len(b)} itens -> {_mostrar(esperado)}\n"
            f"    obtido:   {len(a)} itens -> {_mostrar(obtido)}",
            tipo="tamanho_da_lista",
            esperado=[_para_json(v) for v in esperado],
            obtido=[_para_json(v) for v in obtido],
        )

    for i, (x, y) in enumerate(zip(a, b)):
        if not _iguais(x, y, tolerancia):
            posicao = f"na posição {i}" if not ignorar_ordem else f"no {i+1}º item (já ordenado)"
            raise _erro(
                f"O {nome} tem o tamanho certo, mas difere {posicao}.\n\n"
                f"    esperado[{i}]: {_mostrar(y)}\n"
                f"    obtido[{i}]:   {_mostrar(x)}\n\n"
                f"  completo:\n"
                f"    esperado: {_mostrar(esperado)}\n"
                f"    obtido:   {_mostrar(obtido)}",
                tipo="item_da_lista",
                posicao=i,
                esperado=[_para_json(v) for v in esperado],
                obtido=[_para_json(v) for v in obtido],
            )


def _verificar_conjunto(obtido, esperado, nome) -> None:
    if obtido is None:
        _nada_devolvido(obtido, nome)
    try:
        a = set(obtido)
    except TypeError:
        raise _erro(
            f"Esperava um conjunto (set) e recebi {_tipo(obtido)}: {_mostrar(obtido)}",
            tipo="tipo_errado", tipo_esperado="set", tipo_obtido=_tipo(obtido),
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
    raise _erro(
        "\n".join(linhas),
        tipo="conjunto",
        faltando=[_para_json(v) for v in faltando],
        sobrando=[_para_json(v) for v in sobrando],
    )


def _verificar_dicionario(obtido, esperado, tolerancia, nome) -> None:
    if obtido is None:
        _nada_devolvido(obtido, nome)
    if not isinstance(obtido, dict):
        raise _erro(
            f"Esperava um dicionário e recebi {_tipo(obtido)}: {_mostrar(obtido)}",
            tipo="tipo_errado", tipo_esperado="dict", tipo_obtido=_tipo(obtido),
        )

    faltando = sorted(set(esperado) - set(obtido), key=repr)
    sobrando = sorted(set(obtido) - set(esperado), key=repr)
    if faltando or sobrando:
        partes = [f"As chaves do {nome} não batem.", ""]
        if faltando:
            partes.append(f"    chaves que faltam:  {faltando}")
        if sobrando:
            partes.append(f"    chaves a mais:      {sobrando}")
        raise _erro(
            "\n".join(partes),
            tipo="chaves_do_dicionario",
            faltando=[_para_json(c) for c in faltando],
            sobrando=[_para_json(c) for c in sobrando],
        )

    for chave in esperado:
        if not _iguais(obtido[chave], esperado[chave], tolerancia):
            raise _erro(
                f"As chaves do {nome} estão certas, mas um valor difere.\n\n"
                f"    na chave {chave!r}:\n"
                f"      esperado: {_mostrar(esperado[chave])}\n"
                f"      obtido:   {_mostrar(obtido[chave])}",
                tipo="valor_do_dicionario",
                chave=_para_json(chave),
                esperado=_para_json(esperado[chave]),
                obtido=_para_json(obtido[chave]),
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
        raise _erro(
            f"Esperava um DataFrame e recebi uma Series.\n\n"
            f"  Uma Series é uma coluna só. Selecionar com colchetes duplos —\n"
            f"  df[['coluna']] em vez de df['coluna'] — devolve um DataFrame.\n\n"
            + _tabela_texto(esperado, "esperado"),
            tipo="esperava_dataframe",
            esperado=_tabela_json(esperado),
            obtido=_tabela_json(_como_quadro(obtido)),
        )
    if not isinstance(obtido, pd.DataFrame):
        raise _erro(
            f"Esperava um DataFrame e recebi {_tipo(obtido)}: {_mostrar(obtido)}",
            tipo="esperava_dataframe",
            esperado=_tabela_json(esperado),
            tipo_obtido=_tipo(obtido),
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
        raise _erro(
            "\n".join(partes),
            tipo="colunas_diferentes",
            faltando=[str(c) for c in faltando],
            sobrando=[str(c) for c in sobrando],
            esperado=_tabela_json(esperado),
            obtido=_tabela_json(obtido),
        )

    if list(obtido.columns) != list(esperado.columns):
        raise _erro(
            "As colunas certas estão lá, mas fora de ordem.\n\n"
            f"    esperado: {list(esperado.columns)}\n"
            f"    obtido:   {list(obtido.columns)}\n\n"
            "  Reordene selecionando com uma lista: df[['a', 'b', 'c']]",
            tipo="ordem_das_colunas",
            esperado=_tabela_json(esperado),
            obtido=_tabela_json(obtido),
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
        raise _erro(
            f"O número de linhas não bate. {veredito}\n\n"
            + _lado_a_lado(obtido, esperado) + pista,
            tipo="numero_de_linhas",
            esperado=_tabela_json(esp),
            obtido=_tabela_json(obt),
        )

    # 3. Índice (quando importa)
    if not ignorar_indice and not obt.index.equals(esp.index):
        raise _erro(
            "As linhas batem, mas o índice não.\n\n"
            f"    esperado: {list(esp.index)[:10]}\n"
            f"    obtido:   {list(obt.index)[:10]}\n\n"
            "  Depois de filtrar, o índice guarda os números originais.\n"
            "  Use .reset_index(drop=True) para renumerar de 0 em diante.",
            tipo="indice_diferente",
            indice_esperado=[_para_json(v) for v in list(esp.index)[:20]],
            indice_obtido=[_para_json(v) for v in list(obt.index)[:20]],
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
        raise _erro(
            f"A forma da tabela está certa, mas há valores diferentes{ordenado}.\n\n"
            "    primeiras diferenças:\n" + "\n".join(linhas) + "\n\n"
            + _lado_a_lado(obtido, esperado),
            tipo="valores_diferentes",
            esperado=_tabela_json(esp),
            obtido=_tabela_json(obt),
            celulas=[
                {"linha": int(i), "coluna": str(coluna),
                 "esperado": _para_json(valor_esp), "obtido": _para_json(valor_obt)}
                for i, coluna, valor_esp, valor_obt in problemas
            ],
            comparado_sem_ordem=bool(ignorar_ordem),
        )

    # 5. Tipos das colunas (só se o exercício exigir)
    if checar_tipo_coluna:
        for coluna in esp.columns:
            if str(obt[coluna].dtype) != str(esp[coluna].dtype):
                raise _erro(
                    f"Os valores estão certos, mas o tipo da coluna {coluna!r} não.\n\n"
                    f"    esperado: {esp[coluna].dtype}\n"
                    f"    obtido:   {obt[coluna].dtype}\n\n"
                    "  Converta com .astype(...) ou pd.to_numeric / pd.to_datetime.",
                    tipo="tipo_da_coluna",
                    coluna=str(coluna),
                    tipo_esperado=str(esp[coluna].dtype),
                    tipo_obtido=str(obt[coluna].dtype),
                )


def _verificar_series(obtido, esperado, ignorar_ordem, ignorar_indice,
                      tolerancia, checar_tipo_coluna, nome) -> None:
    import pandas as pd

    if obtido is None:
        _nada_devolvido(obtido, nome)

    if isinstance(obtido, pd.DataFrame):
        if obtido.shape[1] == 1:
            raise _erro(
                "Esperava uma Series e recebi um DataFrame de uma coluna só.\n\n"
                "  df[['coluna']] devolve DataFrame; df['coluna'] devolve Series.\n"
                "  Aqui o exercício pede a Series — use colchetes simples.",
                tipo="esperava_series",
                esperado=_tabela_json(_como_quadro(esperado)),
                obtido=_tabela_json(obtido),
            )
        raise _erro(
            f"Esperava uma Series (uma coluna) e recebi um DataFrame "
            f"com {obtido.shape[1]} colunas.",
            tipo="esperava_series",
            esperado=_tabela_json(_como_quadro(esperado)),
            obtido=_tabela_json(obtido),
        )
    if not isinstance(obtido, pd.Series):
        raise _erro(
            f"Esperava uma Series e recebi {_tipo(obtido)}: {_mostrar(obtido)}",
            tipo="esperava_series",
            esperado=_tabela_json(_como_quadro(esperado)),
            tipo_obtido=_tipo(obtido),
        )

    esp = esperado.sort_values(kind="stable") if ignorar_ordem else esperado
    obt = obtido.sort_values(kind="stable") if ignorar_ordem else obtido
    if ignorar_ordem or ignorar_indice:
        esp, obt = esp.reset_index(drop=True), obt.reset_index(drop=True)

    if len(obt) != len(esp):
        raise _erro(
            f"O tamanho da Series não bate: esperado {len(esp)}, obtido {len(obt)}.\n\n"
            + _lado_a_lado(_como_quadro(obtido), _como_quadro(esperado)),
            tipo="numero_de_linhas",
            esperado=_tabela_json(_como_quadro(esp)),
            obtido=_tabela_json(_como_quadro(obt)),
        )

    if not ignorar_indice and not obt.index.equals(esp.index):
        raise _erro(
            "Os valores batem em quantidade, mas o índice não.\n\n"
            f"    esperado: {list(esp.index)[:10]}\n"
            f"    obtido:   {list(obt.index)[:10]}",
            tipo="indice_diferente",
            indice_esperado=[_para_json(v) for v in list(esp.index)[:20]],
            indice_obtido=[_para_json(v) for v in list(obt.index)[:20]],
        )

    for i in range(len(esp)):
        if not _iguais(obt.iloc[i], esp.iloc[i], tolerancia):
            rotulo = esp.index[i]
            nome_da_coluna = str(esp.name if esp.name is not None else "valor")
            raise _erro(
                f"A Series tem o tamanho certo, mas difere na posição {i} "
                f"(índice {rotulo!r}).\n\n"
                f"    esperado: {_mostrar(esp.iloc[i])}\n"
                f"    obtido:   {_mostrar(obt.iloc[i])}\n\n"
                + _lado_a_lado(_como_quadro(obtido), _como_quadro(esperado)),
                tipo="valores_diferentes",
                esperado=_tabela_json(_como_quadro(esp)),
                obtido=_tabela_json(_como_quadro(obt)),
                celulas=[{
                    "linha": int(i), "coluna": nome_da_coluna,
                    "esperado": _para_json(esp.iloc[i]),
                    "obtido": _para_json(obt.iloc[i]),
                }],
                comparado_sem_ordem=bool(ignorar_ordem),
            )

    if checar_tipo_coluna and str(obt.dtype) != str(esp.dtype):
        raise _erro(
            f"Os valores estão certos, mas o tipo não.\n\n"
            f"    esperado: {esp.dtype}\n    obtido:   {obt.dtype}",
            tipo="tipo_da_coluna",
            coluna=str(esp.name if esp.name is not None else "valor"),
            tipo_esperado=str(esp.dtype),
            tipo_obtido=str(obt.dtype),
        )
