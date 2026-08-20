"""Gerador do dataset da Loja Aurora.

Determinístico: mesma semente, mesmos bytes. Rodar duas vezes produz arquivos
idênticos — o que importa quando os testes comparam resultados exatos.

Duas camadas convivem de propósito:

  tabelas limpas   clientes, produtos, pedidos, itens_pedido, pagamentos,
                   eventos_web, estoque_diario — tipadas e consistentes, usadas
                   pela maioria esmagadora dos exercícios;
  tabelas sujas    clientes_bruto e avaliacoes_bruto — nulos, datas em três
                   formatos, duplicatas, números como texto, espaços sobrando.
                   São a matéria-prima dos módulos de limpeza.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from curso import caminhos
from dados import vocabulario as voc

SEMENTE = 42

N_CLIENTES = 5_000
N_PRODUTOS = 400
N_PEDIDOS = 50_000
N_SESSOES = 90_000
DIAS_DE_ESTOQUE = 180

INICIO_CADASTROS = pd.Timestamp("2022-01-01")
FIM = pd.Timestamp("2025-12-31")

TABELAS_LIMPAS = ["clientes", "produtos", "pedidos", "itens_pedido",
                  "pagamentos", "eventos_web", "estoque_diario"]
TABELAS_SUJAS = ["clientes_bruto", "avaliacoes_bruto"]


# --------------------------------------------------------------------------- #
# Utilidades
# --------------------------------------------------------------------------- #

def _escolher(rng, opcoes, tamanho, pesos=None):
    p = np.array(pesos, dtype=float) / np.sum(pesos) if pesos is not None else None
    return rng.choice(np.array(opcoes, dtype=object), size=tamanho, p=p)


def _dias_aleatorios(rng, inicio: pd.Timestamp, fim: pd.Timestamp, tamanho: int):
    intervalo = (fim - inicio).days
    return inicio + pd.to_timedelta(rng.integers(0, intervalo + 1, tamanho), unit="D")


def _dinheiro(valores) -> np.ndarray:
    return np.round(np.asarray(valores, dtype=float), 2)


# --------------------------------------------------------------------------- #
# Tabelas limpas
# --------------------------------------------------------------------------- #

def _clientes(rng) -> pd.DataFrame:
    n = N_CLIENTES
    primeiros = _escolher(rng, voc.PRIMEIROS_NOMES, n)
    sobrenomes_a = _escolher(rng, voc.SOBRENOMES, n)
    sobrenomes_b = _escolher(rng, voc.SOBRENOMES, n)
    nomes = np.array([f"{p} {a} {b}" for p, a, b in
                      zip(primeiros, sobrenomes_a, sobrenomes_b)], dtype=object)

    siglas = [uf for uf, _, _ in voc.ESTADOS]
    cidades = {uf: cidade for uf, cidade, _ in voc.ESTADOS}
    pesos = [peso for _, _, peso in voc.ESTADOS]
    ufs = _escolher(rng, siglas, n, pesos)

    provedores = _escolher(rng, voc.PROVEDORES_DE_EMAIL, n)
    sufixos = rng.integers(1, 9999, n)
    emails = np.array([
        f"{p.lower()}.{a.lower()}{s}@{d}".replace("á", "a").replace("é", "e")
        .replace("í", "i").replace("ó", "o").replace("ú", "u").replace("ã", "a")
        .replace("õ", "o").replace("ç", "c").replace("â", "a").replace("ê", "e")
        for p, a, s, d in zip(primeiros, sobrenomes_a, sufixos, provedores)
    ], dtype=object)

    cadastro = _dias_aleatorios(rng, INICIO_CADASTROS, FIM - pd.Timedelta(days=30), n)
    nascimento = _dias_aleatorios(
        rng, pd.Timestamp("1960-01-01"), pd.Timestamp("2006-12-31"), n
    )

    return pd.DataFrame({
        "cliente_id": np.arange(1, n + 1),
        "nome": nomes,
        "email": emails,
        "uf": ufs,
        "cidade": np.array([cidades[uf] for uf in ufs], dtype=object),
        "data_cadastro": cadastro.date,
        "data_nascimento": nascimento.date,
        "canal_aquisicao": _escolher(rng, voc.CANAIS_DE_AQUISICAO, n,
                                     voc.PESOS_DE_AQUISICAO),
    })


def _produtos(rng) -> pd.DataFrame:
    categorias, subcategorias, precos, pesos_kg = [], [], [], []
    nomes = []

    lista_de_categorias = list(voc.CATALOGO)
    escolhidas = _escolher(rng, lista_de_categorias, N_PRODUTOS)

    for categoria in escolhidas:
        subs, (preco_min, preco_max), (peso_min, peso_max) = voc.CATALOGO[categoria]
        sub = subs[rng.integers(0, len(subs))]
        # Preço log-uniforme: muitos produtos baratos, poucos caros — como na vida real.
        preco = float(np.exp(rng.uniform(np.log(preco_min), np.log(preco_max))))
        categorias.append(categoria)
        subcategorias.append(sub)
        precos.append(preco)
        pesos_kg.append(float(rng.uniform(peso_min, peso_max)))
        linha = voc.LINHAS_DE_PRODUTO[rng.integers(0, len(voc.LINHAS_DE_PRODUTO))]
        adjetivo = voc.ADJETIVOS_DE_PRODUTO[rng.integers(0, len(voc.ADJETIVOS_DE_PRODUTO))]
        nomes.append(f"{sub[:-1] if sub.endswith('s') else sub} {linha} {adjetivo}")

    precos = _dinheiro(precos)
    margens = rng.uniform(0.22, 0.58, N_PRODUTOS)

    return pd.DataFrame({
        "produto_id": np.arange(1, N_PRODUTOS + 1),
        "nome": nomes,
        "categoria": categorias,
        "subcategoria": subcategorias,
        "preco": precos,
        "custo": _dinheiro(precos * (1 - margens)),
        "peso_kg": np.round(pesos_kg, 3),
        "ativo": rng.random(N_PRODUTOS) > 0.12,
    })


def _pedidos(rng, clientes: pd.DataFrame) -> pd.DataFrame:
    n = N_PEDIDOS

    # Clientes não compram por igual: uma minoria concentra os pedidos.
    apetite = rng.pareto(1.6, N_CLIENTES) + 0.25
    donos = rng.choice(clientes["cliente_id"].to_numpy(), size=n,
                       p=apetite / apetite.sum())

    cadastro = pd.to_datetime(
        clientes.set_index("cliente_id").loc[donos, "data_cadastro"].to_numpy()
    )
    # Pedidos se espalham depois do cadastro — é o que dá coortes de verdade.
    # Quando a espera sorteada passa do fim da série, redistribuímos de forma
    # uniforme dentro da janela restante: cortar em FIM criaria um pico falso
    # de milhares de pedidos no último dia.
    janela = ((FIM - cadastro).days).to_numpy()
    espera = np.round(rng.exponential(200, n)).astype(int)
    estourou = espera > janela
    espera[estourou] = rng.integers(0, np.maximum(janela[estourou], 1))
    data = pd.Series(cadastro + pd.to_timedelta(espera, unit="D"))

    # Pico de Black Friday: 8% dos pedidos migram para a última semana de novembro,
    # desde que a data promocional já exista para aquele cliente.
    sorteados = rng.random(n) < 0.08
    dia_da_promocao = pd.to_datetime([
        f"{ano}-11-{23 + d}" for ano, d in
        zip(data.dt.year.to_numpy(), rng.integers(0, 7, n))
    ])
    pode_migrar = sorteados & (dia_da_promocao >= cadastro) & (dia_da_promocao <= FIM)
    data[pode_migrar] = dia_da_promocao[pode_migrar]

    tem_cupom = rng.random(n) < 0.23
    cupons = np.where(tem_cupom, _escolher(rng, voc.CUPONS, n), None)

    return pd.DataFrame({
        "pedido_id": np.arange(1, n + 1),
        "cliente_id": donos,
        "data_pedido": data.dt.date.to_numpy(),
        "status": _escolher(rng, voc.STATUS_DE_PEDIDO, n, voc.PESOS_DE_STATUS),
        "canal": _escolher(rng, voc.CANAIS_DE_VENDA, n, voc.PESOS_DE_CANAL),
        "cupom": cupons,
        "valor_frete": _dinheiro(np.where(rng.random(n) < 0.30, 0.0,
                                          rng.uniform(9.9, 79.9, n))),
    }).sort_values("data_pedido").assign(
        pedido_id=lambda d: np.arange(1, len(d) + 1)
    ).reset_index(drop=True)


def _itens_pedido(rng, pedidos: pd.DataFrame, produtos: pd.DataFrame) -> pd.DataFrame:
    quantos = np.clip(1 + rng.poisson(1.7, len(pedidos)), 1, 8)
    pedido_ids = np.repeat(pedidos["pedido_id"].to_numpy(), quantos)
    n = len(pedido_ids)

    # Curva de popularidade: uns poucos produtos respondem pela maior parte das vendas.
    popularidade = rng.pareto(1.3, N_PRODUTOS) + 0.1
    produto_ids = rng.choice(produtos["produto_id"].to_numpy(), size=n,
                             p=popularidade / popularidade.sum())

    preco_tabela = produtos.set_index("produto_id").loc[produto_ids, "preco"].to_numpy()
    # O preço praticado oscila em torno do de tabela (promoções, reajustes).
    preco_praticado = _dinheiro(preco_tabela * rng.uniform(0.85, 1.08, n))

    tem_desconto = rng.random(n) < 0.27
    descontos = np.where(tem_desconto, np.round(rng.uniform(0.05, 0.40, n), 2), 0.0)

    return pd.DataFrame({
        "item_id": np.arange(1, n + 1),
        "pedido_id": pedido_ids,
        "produto_id": produto_ids,
        "quantidade": np.clip(1 + rng.poisson(0.6, n), 1, 10),
        "preco_unitario": preco_praticado,
        "desconto": descontos,
    })


def _pagamentos(rng, pedidos: pd.DataFrame, itens: pd.DataFrame) -> pd.DataFrame:
    bruto = itens.assign(
        total=lambda d: d["quantidade"] * d["preco_unitario"] * (1 - d["desconto"])
    ).groupby("pedido_id", as_index=False)["total"].sum()

    base = pedidos.merge(bruto, on="pedido_id", how="left")
    base["total"] = _dinheiro(base["total"].fillna(0) + base["valor_frete"])

    n = len(base)
    metodos = _escolher(rng, voc.METODOS_DE_PAGAMENTO, n, voc.PESOS_DE_PAGAMENTO)
    parcelas = np.where(
        metodos == "cartao_credito",
        np.clip(1 + rng.poisson(2.2, n), 1, 12),
        1,
    )
    # Pix e débito caem na hora; boleto demora; cartão às vezes trava em análise.
    atraso = np.select(
        [metodos == "pix", metodos == "cartao_debito", metodos == "boleto"],
        [0, 0, rng.integers(1, 4, n)],
        default=rng.integers(0, 2, n),
    )
    data_pagamento = pd.to_datetime(base["data_pedido"]) + pd.to_timedelta(atraso, unit="D")

    aprovado = rng.random(n) > 0.055
    aprovado &= base["status"].to_numpy() != "cancelado"

    return pd.DataFrame({
        "pagamento_id": np.arange(1, n + 1),
        "pedido_id": base["pedido_id"].to_numpy(),
        "metodo": metodos,
        "parcelas": parcelas,
        "valor": base["total"].to_numpy(),
        "data_pagamento": data_pagamento.dt.date.to_numpy(),
        "aprovado": aprovado,
    })


def _eventos_web(rng, clientes: pd.DataFrame, produtos: pd.DataFrame) -> pd.DataFrame:
    # Cada sessão avança pelo funil até desistir. É isso que torna possível
    # exercitar funil, sessionização e janelas de tempo com dados que fazem sentido.
    # RETENCAO_POR_ETAPA é acumulada (fração de *todas* as sessões que chegam ali).
    # O sorteio precisa da taxa condicional: dado que chegou na etapa anterior,
    # qual a chance de avançar mais uma.
    acumulada = np.array(voc.RETENCAO_POR_ETAPA)
    condicional = acumulada / np.concatenate([[1.0], acumulada[:-1]])

    sorteios = rng.random((N_SESSOES, len(voc.ETAPAS_DO_FUNIL)))
    alcancou = sorteios < condicional
    alcancou[:, 0] = True
    alcancou = np.logical_and.accumulate(alcancou, axis=1)

    eventos_por_sessao = alcancou.sum(axis=1)
    sessao_ids = np.repeat(np.arange(1, N_SESSOES + 1), eventos_por_sessao)
    tipos = np.tile(np.array(voc.ETAPAS_DO_FUNIL, dtype=object),
                    (N_SESSOES, 1))[alcancou]
    n = len(sessao_ids)

    inicio_da_sessao = _dias_aleatorios(
        rng, pd.Timestamp("2025-01-01"), FIM, N_SESSOES
    ) + pd.to_timedelta(rng.integers(0, 24 * 3600, N_SESSOES), unit="s")
    base = np.repeat(inicio_da_sessao.to_numpy(), eventos_por_sessao)
    # Segundos decorridos dentro da sessão, crescentes por construção.
    passo = pd.to_timedelta(
        np.concatenate([np.cumsum(rng.integers(5, 240, k)) for k in eventos_por_sessao]),
        unit="s",
    )
    momento = pd.to_datetime(base) + passo

    anonimo = rng.random(N_SESSOES) < 0.42
    dono_da_sessao = np.where(
        anonimo, np.nan, rng.choice(clientes["cliente_id"].to_numpy(), N_SESSOES)
    )
    dispositivo_da_sessao = _escolher(rng, voc.DISPOSITIVOS, N_SESSOES,
                                      voc.PESOS_DE_DISPOSITIVO)

    produto_do_evento = rng.choice(produtos["produto_id"].to_numpy(), n).astype(float)
    produto_do_evento[np.isin(tipos, ["visita"])] = np.nan

    return pd.DataFrame({
        "evento_id": np.arange(1, n + 1),
        "sessao_id": sessao_ids,
        "cliente_id": np.repeat(dono_da_sessao, eventos_por_sessao),
        "momento": momento,
        "tipo_evento": tipos,
        "produto_id": produto_do_evento,
        "dispositivo": np.repeat(dispositivo_da_sessao, eventos_por_sessao),
    }).sort_values("momento").reset_index(drop=True).assign(
        evento_id=lambda d: np.arange(1, len(d) + 1)
    )


def _estoque_diario(rng, produtos: pd.DataFrame) -> pd.DataFrame:
    dias = pd.date_range(FIM - pd.Timedelta(days=DIAS_DE_ESTOQUE - 1), FIM, freq="D")
    n_produtos = len(produtos)

    # Passeio aleatório com reposições: gera períodos de ruptura (estoque zero),
    # que é exatamente o que os exercícios de gaps-and-islands precisam.
    inicial = rng.integers(0, 400, n_produtos).astype(float)
    linhas = np.zeros((len(dias), n_produtos))
    atual = inicial.copy()
    for i in range(len(dias)):
        saida = rng.poisson(6, n_produtos)
        reposicao = np.where(rng.random(n_produtos) < 0.06,
                             rng.integers(50, 300, n_produtos), 0)
        atual = np.clip(atual - saida + reposicao, 0, None)
        linhas[i] = atual

    return pd.DataFrame({
        "data": np.repeat(dias.date, n_produtos),
        "produto_id": np.tile(produtos["produto_id"].to_numpy(), len(dias)),
        "quantidade_disponivel": linhas.reshape(-1).astype(int),
    })


# --------------------------------------------------------------------------- #
# Tabelas propositalmente sujas
# --------------------------------------------------------------------------- #

def _clientes_bruto(rng, clientes: pd.DataFrame) -> pd.DataFrame:
    """Como os dados chegam antes de alguém limpar: é o insumo dos módulos B7-B9."""
    base = clientes.sample(n=3000, random_state=SEMENTE).copy()
    # 200 duplicatas exatas + 60 quase-duplicatas (mesma pessoa, grafia diferente).
    duplicatas = base.sample(n=200, random_state=SEMENTE + 1)
    base = pd.concat([base, duplicatas], ignore_index=True)
    n = len(base)

    nome = base["nome"].to_numpy(dtype=object).copy()
    ruido = rng.random(n)
    nome = np.where(ruido < 0.10, np.char.add("  ", nome.astype(str)), nome)
    nome = np.where((ruido >= 0.10) & (ruido < 0.18),
                    np.char.upper(nome.astype(str)), nome)
    nome = np.where((ruido >= 0.18) & (ruido < 0.24),
                    np.char.lower(nome.astype(str)), nome)

    email = base["email"].to_numpy(dtype=object).copy()
    quebrado = rng.random(n)
    email = np.where(quebrado < 0.05, None, email)                    # ausente
    email = np.where((quebrado >= 0.05) & (quebrado < 0.09),
                     np.char.replace(base["email"].to_numpy().astype(str), "@", ""), email)
    email = np.where((quebrado >= 0.09) & (quebrado < 0.11), "", email)

    uf = base["uf"].to_numpy(dtype=object).copy()
    caixa = rng.random(n)
    uf = np.where(caixa < 0.15, np.char.lower(uf.astype(str)), uf)
    uf = np.where((caixa >= 0.15) & (caixa < 0.20),
                  np.char.add(uf.astype(str), " "), uf)

    # Três formatos de data convivendo na mesma coluna — clássico de planilha.
    cadastro = pd.to_datetime(base["data_cadastro"])
    formato = rng.integers(0, 3, n)
    moldes = ["%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"]
    data_texto = np.array(
        [d.strftime(moldes[f]) for d, f in zip(cadastro, formato)], dtype=object
    )

    renda = rng.lognormal(8.1, 0.6, n)
    renda_texto = np.array([
        f"R$ {v:,.2f}".replace(",", "@").replace(".", ",").replace("@", ".")
        for v in renda
    ], dtype=object)
    renda_texto = np.where(rng.random(n) < 0.07, None, renda_texto)

    ddd = rng.integers(11, 99, n)
    numero = rng.integers(900000000, 999999999, n)
    estilo = rng.integers(0, 3, n)
    telefone = np.array([
        f"({d}) {str(x)[:5]}-{str(x)[5:]}" if e == 0
        else f"{d}{x}" if e == 1
        else f"+55 {d} {x}"
        for d, x, e in zip(ddd, numero, estilo)
    ], dtype=object)

    return pd.DataFrame({
        "cliente_id": base["cliente_id"].to_numpy(),
        "nome": nome,
        "email": email,
        "uf": uf,
        "cidade": np.where(rng.random(n) < 0.08, None,
                           base["cidade"].to_numpy(dtype=object)),
        "data_cadastro": data_texto,
        "telefone": telefone,
        "renda_mensal": renda_texto,
    }).sample(frac=1.0, random_state=SEMENTE + 2).reset_index(drop=True)


def _avaliacoes_bruto(rng, pedidos: pd.DataFrame, itens: pd.DataFrame) -> pd.DataFrame:
    amostra = itens.sample(n=12_000, random_state=SEMENTE + 3)
    n = len(amostra)

    nota = rng.integers(1, 6, n).astype(float)
    nota[rng.random(n) < 0.06] = np.nan
    nota[rng.random(n) < 0.02] = 7          # fora da escala, de propósito
    nota_texto = np.array(
        ["" if np.isnan(v) else str(int(v)) for v in nota], dtype=object
    )

    data = pd.to_datetime(
        pedidos.set_index("pedido_id")
        .loc[amostra["pedido_id"], "data_pedido"].to_numpy()
    ) + pd.to_timedelta(rng.integers(1, 45, n), unit="D")
    formato = rng.integers(0, 2, n)
    data_texto = np.array([
        d.strftime("%Y-%m-%d" if f == 0 else "%d/%m/%Y")
        for d, f in zip(data, formato)
    ], dtype=object)

    return pd.DataFrame({
        "avaliacao_id": np.arange(1, n + 1),
        "pedido_id": amostra["pedido_id"].to_numpy(),
        "produto_id": amostra["produto_id"].to_numpy(),
        "nota": nota_texto,
        "comentario": _escolher(rng, voc.COMENTARIOS_DE_AVALIACAO, n),
        "data_avaliacao": data_texto,
    })


# --------------------------------------------------------------------------- #
# Escrita
# --------------------------------------------------------------------------- #

def _gravar_csv(tabelas: dict[str, pd.DataFrame]) -> None:
    destino = caminhos.pasta_brutos()
    destino.mkdir(parents=True, exist_ok=True)
    for nome, df in tabelas.items():
        df.to_csv(destino / f"{nome}.csv", index=False,
                  date_format="%Y-%m-%d %H:%M:%S")


def _construir_banco(tabelas: dict[str, pd.DataFrame]) -> None:
    import duckdb

    arquivo = caminhos.banco_path()
    arquivo.unlink(missing_ok=True)
    conexao = duckdb.connect(str(arquivo))
    try:
        for nome, df in tabelas.items():
            conexao.register("origem", df)
            conexao.execute(f"CREATE OR REPLACE TABLE {nome} AS SELECT * FROM origem")
            conexao.unregister("origem")

        # Chaves e índices deixam o EXPLAIN dos exercícios de desempenho fazer sentido.
        for tabela, coluna in [("clientes", "cliente_id"), ("produtos", "produto_id"),
                               ("pedidos", "pedido_id"), ("itens_pedido", "item_id"),
                               ("pagamentos", "pagamento_id")]:
            conexao.execute(f"CREATE UNIQUE INDEX idx_{tabela}_pk ON {tabela}({coluna})")
        conexao.execute("CREATE INDEX idx_pedidos_cliente ON pedidos(cliente_id)")
        conexao.execute("CREATE INDEX idx_itens_pedido ON itens_pedido(pedido_id)")
    finally:
        conexao.close()


def construir(forcar: bool = False) -> dict[str, pd.DataFrame]:
    """Gera todo o dataset. Sem `forcar`, não refaz o que já existe."""
    from curso import painel

    if caminhos.banco_path().exists() and not forcar:
        painel.aviso("O dataset já existe. Use `curso setup --forcar` para refazer.")
        return {}

    painel.console.print("\n  [bold]Gerando o dataset da Loja Aurora[/] "
                         f"[dim](semente {SEMENTE})[/]\n")
    rng = np.random.default_rng(SEMENTE)

    tabelas: dict[str, pd.DataFrame] = {}
    tabelas["clientes"] = _clientes(rng)
    tabelas["produtos"] = _produtos(rng)
    tabelas["pedidos"] = _pedidos(rng, tabelas["clientes"])
    tabelas["itens_pedido"] = _itens_pedido(rng, tabelas["pedidos"], tabelas["produtos"])
    tabelas["pagamentos"] = _pagamentos(rng, tabelas["pedidos"], tabelas["itens_pedido"])
    tabelas["eventos_web"] = _eventos_web(rng, tabelas["clientes"], tabelas["produtos"])
    tabelas["estoque_diario"] = _estoque_diario(rng, tabelas["produtos"])
    tabelas["clientes_bruto"] = _clientes_bruto(rng, tabelas["clientes"])
    tabelas["avaliacoes_bruto"] = _avaliacoes_bruto(
        rng, tabelas["pedidos"], tabelas["itens_pedido"]
    )

    _gravar_csv(tabelas)
    _construir_banco(tabelas)

    for nome, df in tabelas.items():
        marca = "[dim](suja de propósito)[/]" if nome in TABELAS_SUJAS else ""
        painel.console.print(
            f"    {nome:<18} {len(df):>8,} linhas  {len(df.columns):>2} colunas  {marca}"
            .replace(",", ".")
        )

    painel.console.print()
    painel.ok(f"CSVs em {caminhos.pasta_brutos()}")
    painel.ok(f"Banco em {caminhos.banco_path()}")
    painel.console.print("\n  Próximo passo: [bold]curso hoje[/]\n")
    return tabelas


if __name__ == "__main__":
    construir(forcar=True)
