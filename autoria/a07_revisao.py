"""Bloco A, módulo 7: a prova do bloco.

Cada exercício aqui obriga a combinar pelo menos dois módulos anteriores. É de
propósito: saber `for` e saber `strip` separadamente não é o mesmo que resolver
um problema que precisa dos dois.
"""

from autoria.modelo import Exercicio as Ex
from autoria.modelo import Modulo

A07 = Modulo(
    id="A07",
    titulo="Módulo A7 — Revisão do bloco (A1 a A6)",
    resumo="Oito problemas que só saem combinando o que veio antes.",
    teoria="""
## Como usar este módulo

Estes exercícios não ensinam nada novo — eles cobram. Cada um precisa de duas ou
três ferramentas dos módulos anteriores ao mesmo tempo, que é como os problemas
aparecem fora de um curso.

Se travar em algum, o caminho não é adivinhar: volte ao `README.md` do módulo
correspondente (a tag do exercício diz qual), releia e volte. Reler depois de
travar fixa muito mais do que ler antes.

### O que se espera de você aqui

- decompor o problema em passos antes de escrever a primeira linha;
- reconhecer o padrão do acumulador quando ele aparece disfarçado;
- lembrar dos casos de borda sem que o enunciado precise apontá-los —
  lista vazia, texto vazio, item único, valor no limite exato.

Depois deste módulo, o próximo passo é o Bloco B (Pandas), onde tudo isso
volta em escala: em vez de uma lista de 5 preços, uma tabela de 135 mil itens.
""",
    exercicios=[
        Ex(
            id="A07-001", titulo="Padronizar a sigla do estado", nivel=3, tempo_min=8,
            tags=["strings", "condicionais", "limpeza", "revisao"],
            requer=["A03-005", "A04-005"],
            enunciado="""
            O cadastro recebe UF digitada de qualquer jeito: `" sp "`, `"SP"`, `"Sp"`.

            Devolva a sigla padronizada em maiúsculas e sem espaços. Se, depois de
            limpar, o resultado não tiver exatamente 2 letras, devolva `"??"`.

            Exemplos:

                resolver(" sp ")   ->  "SP"
                resolver("Rj")     ->  "RJ"
                resolver("  ")     ->  "??"
                resolver("Brasil") ->  "??"
                resolver("s")      ->  "??"

            Combina limpeza de texto (A3) com validação (A4).
            """,
            assinatura="def resolver(uf: str) -> str:",
            dicas=[
                "Limpe primeiro, valide depois: strip e upper antes de conferir o tamanho.",
                "Guarde o texto já limpo numa variável — você vai usá-lo duas vezes.",
                "if len(limpa) != 2: return \"??\" — e devolva a sigla no fim.",
            ],
            solucao="""
            limpa = uf.strip().upper()
            if len(limpa) != 2:
                return "??"
            return limpa
            """,
            nota_da_solucao="Normalizar antes de validar evita rejeitar ' sp ' por causa dos espaços.",
            testes="""
def teste_espacos_e_minuscula():
    verificar(ex.resolver(" sp "), "SP")


def teste_caixa_mista():
    verificar(ex.resolver("Rj"), "RJ")


def teste_so_espacos():
    verificar(ex.resolver("  "), "??")


def teste_palavra_inteira():
    verificar(ex.resolver("Brasil"), "??")


def teste_uma_letra_so():
    verificar(ex.resolver("s"), "??")


def teste_ja_padronizada():
    verificar(ex.resolver("MG"), "MG")
""",
        ),
        Ex(
            id="A07-002", titulo="Validar e-mail", nivel=3, tempo_min=9,
            tags=["strings", "booleano", "validacao", "revisao"],
            requer=["A03-009", "A04-004"],
            enunciado="""
            Uma validação simples de e-mail, do tipo que todo formulário faz.

            Devolva `True` quando o texto satisfizer **todas** as regras:

                - contém exatamente um "@"
                - tem pelo menos um caractere antes do "@"
                - depois do "@" existe um "."
                - não tem espaços

            Exemplos:

                resolver("ana@loja.com")   ->  True
                resolver("analoja.com")    ->  False   (sem @)
                resolver("@loja.com")      ->  False   (nada antes do @)
                resolver("ana@lojacom")    ->  False   (sem ponto no domínio)
                resolver("a na@loja.com")  ->  False   (tem espaço)
                resolver("a@b@loja.com")   ->  False   (dois @)

            Dica de estratégia: separe o texto no "@" e analise as duas partes.
            """,
            assinatura="def resolver(email: str) -> bool:",
            dicas=[
                "email.count(\"@\") diz quantos arrobas existem — comece por aí.",
                "email.split(\"@\") devolve uma lista; com exatamente um @, ela tem 2 partes.",
                "Guarde antes, depois = email.split(\"@\") e teste cada parte separadamente.",
            ],
            solucao="""
            if email.count("@") != 1:
                return False
            if " " in email:
                return False
            antes, depois = email.split("@")
            return len(antes) > 0 and "." in depois
            """,
            nota_da_solucao="Rejeitar cedo os casos impossíveis deixa o resto do código simples e legível.",
            testes="""
def teste_email_valido():
    verificar(ex.resolver("ana@loja.com"), True)


def teste_sem_arroba():
    verificar(ex.resolver("analoja.com"), False)


def teste_nada_antes_do_arroba():
    verificar(ex.resolver("@loja.com"), False)


def teste_dominio_sem_ponto():
    verificar(ex.resolver("ana@lojacom"), False)


def teste_com_espaco():
    verificar(ex.resolver("a na@loja.com"), False)


def teste_dois_arrobas():
    verificar(ex.resolver("a@b@loja.com"), False,
              dica="Com dois @, o split devolveria 3 partes — trate isso antes.")


def teste_subdominio():
    verificar(ex.resolver("ana@mail.loja.com.br"), True)
""",
        ),
        Ex(
            id="A07-003", titulo="Formatar CPF", nivel=3, tempo_min=8,
            tags=["strings", "fatiamento", "validacao", "revisao"],
            requer=["A03-003", "A03-011"],
            enunciado="""
            Um CPF chega como 11 dígitos grudados. Devolva no formato
            `000.000.000-00`.

            Se o texto não tiver exatamente 11 caracteres, devolva `"invalido"`.

            Exemplos:

                resolver("12345678901")   ->  "123.456.789-01"
                resolver("00000000000")   ->  "000.000.000-00"
                resolver("123")           ->  "invalido"
                resolver("")              ->  "invalido"

            Fatiamento (A3) mais validação de tamanho (A4).
            """,
            assinatura="def resolver(cpf: str) -> str:",
            dicas=[
                "Valide o tamanho antes de fatiar.",
                "São quatro pedaços: 0:3, 3:6, 6:9 e 9:11.",
                'Monte o resultado com f-string: f"{cpf[0:3]}.{cpf[3:6]}..."',
            ],
            solucao="""
            if len(cpf) != 11:
                return "invalido"
            return f"{cpf[0:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}"
            """,
            testes="""
def teste_cpf_normal():
    verificar(ex.resolver("12345678901"), "123.456.789-01")


def teste_cpf_de_zeros():
    verificar(ex.resolver("00000000000"), "000.000.000-00")


def teste_curto_demais():
    verificar(ex.resolver("123"), "invalido")


def teste_vazio():
    verificar(ex.resolver(""), "invalido")


def teste_longo_demais():
    verificar(ex.resolver("123456789012"), "invalido")
""",
        ),
        Ex(
            id="A07-004", titulo="Buscar produtos pelo nome", nivel=3, tempo_min=9,
            tags=["laco", "strings", "lista", "revisao"],
            requer=["A06-005", "A03-004"],
            enunciado="""
            Devolva a lista de produtos cujo nome contém o termo procurado,
            **ignorando maiúsculas e minúsculas**.

            Os nomes devolvidos mantêm a grafia original.

            Exemplos:

                resolver(["Fone Aurora", "Capa Slim", "Fone Pro"], "fone")
                ->  ["Fone Aurora", "Fone Pro"]

                resolver(["Capa Slim"], "FONE")   ->  []
                resolver([], "fone")              ->  []
                resolver(["Capa Slim"], "")       ->  ["Capa Slim"]

            No último caso: todo texto contém o texto vazio.
            """,
            assinatura="def resolver(nomes: list, termo: str) -> list:",
            dicas=[
                "Padronize os dois lados da comparação para minúsculas.",
                "Padronizar o nome só para comparar não muda o que você acrescenta\\nna lista de resultados.",
                "if termo.lower() in nome.lower(): encontrados.append(nome)",
            ],
            solucao="""
            encontrados = []
            procurado = termo.lower()
            for nome in nomes:
                if procurado in nome.lower():
                    encontrados.append(nome)
            return encontrados
            """,
            nota_da_solucao="Comparar em minúsculas mas guardar o original é o padrão de toda busca amigável.",
            testes="""
def teste_encontra_dois():
    verificar(ex.resolver(["Fone Aurora", "Capa Slim", "Fone Pro"], "fone"),
              ["Fone Aurora", "Fone Pro"])


def teste_termo_em_maiusculas():
    verificar(ex.resolver(["Fone Aurora"], "FONE"), ["Fone Aurora"],
              dica="Passe os dois lados para minúsculas antes de comparar.")


def teste_nao_encontra():
    verificar(ex.resolver(["Capa Slim"], "fone"), [])


def teste_lista_vazia():
    verificar(ex.resolver([], "fone"), [])


def teste_termo_vazio_acha_tudo():
    verificar(ex.resolver(["Capa Slim"], ""), ["Capa Slim"])


def teste_preserva_a_grafia_original():
    verificar(ex.resolver(["FONE AURORA"], "fone"), ["FONE AURORA"],
              dica="Devolva o nome como ele chegou, não em minúsculas.")
""",
        ),
        Ex(
            id="A07-005", titulo="Relatório do estoque", nivel=3, tempo_min=10,
            tags=["zip", "laco", "f-string", "condicional", "revisao"],
            requer=["A06-011", "A04-003"],
            enunciado="""
            Monte um relatório de estoque, uma linha por produto, no formato:

                nome: quantidade (situação)

            A situação depende da quantidade:

                0            ->  "esgotado"
                1 a 9        ->  "critico"
                10 ou mais   ->  "ok"

            Exemplos:

                resolver(["Fone", "Capa"], [0, 25])
                ->  ["Fone: 0 (esgotado)", "Capa: 25 (ok)"]

                resolver(["Livro"], [3])   ->  ["Livro: 3 (critico)"]
                resolver([], [])           ->  []
            """,
            assinatura="def resolver(nomes: list, quantidades: list) -> list:",
            dicas=[
                "zip percorre nome e quantidade em paralelo.",
                "Decida a situação num if/elif dentro do laço, guardando numa variável.",
                'Monte a linha com f"{nome}: {quantidade} ({situacao})".',
            ],
            solucao="""
            linhas = []
            for nome, quantidade in zip(nomes, quantidades):
                if quantidade == 0:
                    situacao = "esgotado"
                elif quantidade < 10:
                    situacao = "critico"
                else:
                    situacao = "ok"
                linhas.append(f"{nome}: {quantidade} ({situacao})")
            return linhas
            """,
            testes="""
def teste_esgotado_e_ok():
    verificar(ex.resolver(["Fone", "Capa"], [0, 25]),
              ["Fone: 0 (esgotado)", "Capa: 25 (ok)"])


def teste_critico():
    verificar(ex.resolver(["Livro"], [3]), ["Livro: 3 (critico)"])


def teste_listas_vazias():
    verificar(ex.resolver([], []), [])


def teste_limite_do_critico():
    verificar(ex.resolver(["A", "B"], [9, 10]),
              ["A: 9 (critico)", "B: 10 (ok)"],
              dica="9 ainda é crítico; 10 já é ok.")
""",
        ),
        Ex(
            id="A07-006", titulo="Estatísticas das vendas", nivel=4, tempo_min=12,
            tags=["laco", "lista", "media", "condicional", "revisao"],
            requer=["A06-004", "A05-013"],
            enunciado="""
            Você recebe os valores de venda do mês. Devolva uma tupla com quatro
            informações, nesta ordem:

                (quantidade de vendas,
                 total vendido,
                 média por venda arredondada em 2 casas,
                 quantas vendas ficaram acima da média)

            Se a lista estiver vazia, devolva `(0, 0, 0.0, 0)`.

            Exemplos:

                resolver([100, 200, 300])   ->  (3, 600, 200.0, 1)
                resolver([50])              ->  (1, 50, 50.0, 0)
                resolver([])                ->  (0, 0, 0.0, 0)

            No primeiro caso a média é 200, e só o 300 fica acima dela.
            Repare que a comparação é com a média **antes** do arredondamento —
            aqui os dois valores coincidem, mas o teste tem um caso onde não.
            """,
            assinatura="def resolver(vendas: list) -> tuple:",
            dicas=[
                "Trate a lista vazia primeiro e devolva a tupla de zeros.",
                "Calcule a média em uma variável e só depois percorra de novo\\npara contar quantas passam dela.",
                "São duas passadas pela lista: uma para somar, outra para contar.\\nNão dá para fazer as duas ao mesmo tempo — você precisa da média pronta.",
            ],
            solucao="""
            if not vendas:
                return 0, 0, 0.0, 0

            quantidade = len(vendas)
            total = sum(vendas)
            media = total / quantidade

            acima = 0
            for venda in vendas:
                if venda > media:
                    acima += 1

            return quantidade, total, round(media, 2), acima
            """,
            nota_da_solucao="Comparar com a média exata (e arredondar só na saída) evita erros de fronteira.",
            testes="""
def teste_tres_vendas():
    verificar(ex.resolver([100, 200, 300]), (3, 600, 200.0, 1))


def teste_uma_venda():
    verificar(ex.resolver([50]), (1, 50, 50.0, 0),
              dica="Uma venda sozinha é exatamente a média — não fica acima dela.")


def teste_lista_vazia():
    verificar(ex.resolver([]), (0, 0, 0.0, 0))


def teste_todas_iguais():
    verificar(ex.resolver([10, 10, 10]), (3, 30, 10.0, 0))


def teste_media_com_dizima():
    verificar(ex.resolver([1, 2, 2]), (3, 5, 1.67, 2),
              dica="Compare com a média exata (1.666...), não com o valor arredondado.")
""",
        ),
        Ex(
            id="A07-007", titulo="Maior sequência sem vendas", nivel=4, tempo_min=12,
            tags=["laco", "acumulador", "maximo", "revisao"],
            requer=["A06-009", "A06-004"],
            enunciado="""
            Você recebe as vendas diárias do mês. Devolva o tamanho da **maior
            sequência de dias seguidos com zero vendas**.

            Exemplos:

                resolver([5, 0, 0, 3, 0])        ->  2
                resolver([0, 0, 0])              ->  3
                resolver([1, 2, 3])              ->  0
                resolver([])                     ->  0
                resolver([0, 1, 0, 0, 0, 1, 0])  ->  3

            Este é o problema que em SQL se chama *gaps and islands*, e você vai
            reencontrá-lo no Bloco C. Aqui ele sai com dois contadores.

            A armadilha: se a maior sequência terminar no último dia, é fácil
            esquecer de contabilizá-la.
            """,
            assinatura="def resolver(vendas_por_dia: list) -> int:",
            dicas=[
                "Você precisa de duas variáveis: a sequência atual e a maior já vista.",
                "Dia com zero: a atual cresce. Dia com venda: a atual volta a zero.",
                "Atualize a maior a CADA volta, e não só quando a sequência quebra —\\nsenão a sequência que termina no último dia se perde.",
            ],
            solucao="""
            maior = 0
            atual = 0
            for vendas in vendas_por_dia:
                if vendas == 0:
                    atual += 1
                else:
                    atual = 0
                if atual > maior:
                    maior = atual
            return maior
            """,
            nota_da_solucao="Comparar dentro do laço, e não ao quebrar a sequência, elimina o caso especial do último dia.",
            testes="""
def teste_sequencia_no_meio():
    verificar(ex.resolver([5, 0, 0, 3, 0]), 2)


def teste_mes_inteiro_sem_venda():
    verificar(ex.resolver([0, 0, 0]), 3)


def teste_sem_dias_zerados():
    verificar(ex.resolver([1, 2, 3]), 0)


def teste_lista_vazia():
    verificar(ex.resolver([]), 0)


def teste_duas_sequencias():
    verificar(ex.resolver([0, 1, 0, 0, 0, 1, 0]), 3)


def teste_sequencia_termina_no_ultimo_dia():
    verificar(ex.resolver([1, 0, 0, 0]), 3,
              dica="A maior sequência acaba junto com a lista — atualize o máximo\\ndentro do laço, a cada volta.")
""",
        ),
        Ex(
            id="A07-008", titulo="Fechamento do mês", nivel=4, tempo_min=14,
            tags=["zip", "laco", "condicional", "f-string", "composicao", "revisao"],
            requer=["A06-016", "A07-006"],
            enunciado="""
            O exercício final do bloco. Você recebe três listas alinhadas:
            categorias, valores vendidos e quantidades de pedidos.

            Devolva um texto de uma linha por categoria, mais uma linha de total,
            **tudo junto numa lista de textos**, no formato:

                CATEGORIA: R$ 1234.50 em 10 pedidos (ticket R$ 123.45)
                ...
                TOTAL: R$ 9999.99 em 99 pedidos

            Regras:

                - a categoria sai em MAIÚSCULAS
                - o ticket médio é valor ÷ pedidos, com 2 casas
                - categorias com zero pedidos são **ignoradas** (não entram no relatório
                  nem no total)
                - se nenhuma categoria sobrar, devolva `["TOTAL: R$ 0.00 em 0 pedidos"]`

            Exemplo:

                resolver(["moda", "casa"], [1000.0, 500.0], [10, 5])
                ->  ["MODA: R$ 1000.00 em 10 pedidos (ticket R$ 100.00)",
                     "CASA: R$ 500.00 em 5 pedidos (ticket R$ 100.00)",
                     "TOTAL: R$ 1500.00 em 15 pedidos"]
            """,
            assinatura="def resolver(categorias: list, valores: list, pedidos: list) -> list:",
            dicas=[
                "Três acumuladores: as linhas do relatório, o total em dinheiro e o\\ntotal de pedidos.",
                "O continue resolve as categorias com zero pedidos — e de quebra evita\\na divisão por zero do ticket.",
                "A linha do TOTAL é montada depois do laço e acrescentada por último.",
            ],
            solucao="""
            linhas = []
            total_valor = 0.0
            total_pedidos = 0

            for categoria, valor, quantidade in zip(categorias, valores, pedidos):
                if quantidade == 0:
                    continue
                ticket = valor / quantidade
                linhas.append(
                    f"{categoria.upper()}: R$ {valor:.2f} em {quantidade} pedidos "
                    f"(ticket R$ {ticket:.2f})"
                )
                total_valor += valor
                total_pedidos += quantidade

            linhas.append(f"TOTAL: R$ {total_valor:.2f} em {total_pedidos} pedidos")
            return linhas
            """,
            nota_da_solucao="Pular a categoria vazia com continue mata dois coelhos: o filtro do relatório e a divisão por zero.",
            testes="""
def teste_duas_categorias():
    verificar(
        ex.resolver(["moda", "casa"], [1000.0, 500.0], [10, 5]),
        ["MODA: R$ 1000.00 em 10 pedidos (ticket R$ 100.00)",
         "CASA: R$ 500.00 em 5 pedidos (ticket R$ 100.00)",
         "TOTAL: R$ 1500.00 em 15 pedidos"],
    )


def teste_ignora_categoria_sem_pedidos():
    verificar(
        ex.resolver(["moda", "vazia"], [100.0, 0.0], [2, 0]),
        ["MODA: R$ 100.00 em 2 pedidos (ticket R$ 50.00)",
         "TOTAL: R$ 100.00 em 2 pedidos"],
        dica="Categoria com 0 pedidos sai do relatório e não entra no total.",
    )


def teste_tudo_vazio():
    verificar(ex.resolver([], [], []), ["TOTAL: R$ 0.00 em 0 pedidos"])


def teste_todas_sem_pedidos():
    verificar(ex.resolver(["a"], [0.0], [0]), ["TOTAL: R$ 0.00 em 0 pedidos"])


def teste_ticket_quebrado():
    verificar(
        ex.resolver(["livros"], [100.0], [3]),
        ["LIVROS: R$ 100.00 em 3 pedidos (ticket R$ 33.33)",
         "TOTAL: R$ 100.00 em 3 pedidos"],
    )
""",
        ),
    ],
)

MODULOS = [A07]
