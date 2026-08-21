"""Traduz o 422 do Pydantic para uma frase que o aluno entenda.

O padrão é `Input should be less than 400` — em inglês, com o nome cru do
campo. Quem lê é alguém no vestiário tentando registrar o peso, e mostrar isso
é o mesmo que mostrar nada: a pessoa não descobre o que fazer.

Aqui a mensagem vira "O peso precisa ser menor que 400." e o nome do campo vira
o nome que a tela usa.

As validações escritas à mão no `jf/esquemas.py` já saem em português — essas
passam inteiras, sem tradução por cima.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

# Só o que a regra abaixo não acerta sozinha: nome que a tela escreve
# diferente, acento que o nome do campo não tem, e gênero que a terminação não
# entrega. O resto sai da regra, para isto não virar um cadastro paralelo de
# todo campo do app.
NOMES: dict[str, tuple[str, str]] = {
    "reps": ("as", "repetições"),
    "reps_min": ("o", "mínimo de repetições"),
    "reps_max": ("o", "máximo de repetições"),
    "series": ("as", "séries"),
    "rir_alvo": ("o", "RIR alvo"),
    "rir": ("o", "RIR"),
    "descanso_s": ("o", "descanso"),
    "carga_alvo_kg": ("a", "carga alvo"),
    "carga_ate_kg": ("a", "carga final"),
    "percentual_1rm": ("o", "percentual de 1RM"),
    "senha": ("a", "senha"),
    "senha_nova": ("a", "senha nova"),
    "senha_atual": ("a", "senha atual"),
    "email": ("o", "email"),
    "nascimento": ("a", "data de nascimento"),
    "kcal_alvo": ("a", "meta de calorias"),
    "deficit_kcal": ("o", "déficit"),
    "proteina_g": ("a", "proteína"),
    "gordura_g": ("a", "gordura"),
    "a_gosto": ("o", "“à gosto”"),
    "tecnica_ids": ("as", "técnicas"),
    "aluno_id": ("o", "aluno"),
    "exercicio_id": ("o", "exercício"),
    "grupo_id": ("o", "grupo"),
    "refeicao_id": ("a", "refeição"),
    "dia_da_semana": ("o", "dia da semana"),
    "aderencia_dieta": ("a", "aderência à dieta"),
    "aderencia_treino": ("a", "aderência ao treino"),
    "horas_de_sono": ("as", "horas de sono"),
    "passos_por_dia": ("os", "passos por dia"),
    "observacoes": ("as", "observações"),
    "observacao": ("a", "observação"),
    "ordem": ("a", "ordem"),
    "chave_local": ("a", "chave da série"),
    "disposicao": ("a", "disposição"),
    "recuperacao": ("a", "recuperação"),
    "cadencia": ("a", "cadência"),
    "descricao": ("a", "descrição"),
    "seguiu": ("a", "marcação da refeição"),
    "opcional": ("o", "“opcional”"),
    "dose": ("a", "dose"),
    "itens": ("os", "itens"),
}

# Sufixos de unidade: quem lê a tela vê "peso", não "peso_kg".
UNIDADES = ("_kg", "_cm", "_g", "_s", "_id", "_pct")

# Terminações que entregam o feminino em português. Cobrem o grosso dos campos
# do app — "qualidade", "disposicao", "carga", "série" —, e o que escapa entra
# em `NOMES` de propósito.
FEMININAS = ("a", "cao", "sao", "dade", "gem", "ie", "ncia")


@dataclass(frozen=True)
class Campo:
    """O nome do campo já com artigo e número, para a frase concordar.

    Sem isto sai "Os horas de sono precisa ser no máximo 16" — que denuncia o
    robô e, pior, faz a pessoa reler para entender.
    """

    artigo: str
    nome: str

    @property
    def plural(self) -> bool:
        return self.artigo.endswith("s")

    @property
    def com_artigo(self) -> str:
        return f"{self.artigo} {self.nome}"

    @property
    def maiuscula(self) -> str:
        return f"{self.artigo.capitalize()} {self.nome}"

    def precisa(self) -> str:
        return "precisam" if self.plural else "precisa"

    def passa(self) -> str:
        return "passam" if self.plural else "passa"

    def esta(self) -> str:
        return "estão" if self.plural else "está"

    def aceita(self) -> str:
        return "aceitam" if self.plural else "aceita"


def nome_do_campo(bruto: str) -> Campo:
    """"horas_de_sono" → as horas de sono; "peso_kg" → o peso."""
    if bruto in NOMES:
        artigo, nome = NOMES[bruto]
        return Campo(artigo, nome)

    limpo = bruto
    for sufixo in UNIDADES:
        if limpo.endswith(sufixo):
            limpo = limpo[: -len(sufixo)]
            break

    palavras = limpo.replace("_", " ")
    primeira = palavras.split(" ")[0]

    plural = primeira.endswith("s")
    # Para decidir o gênero vale o singular: "passos" → "passo" (masculino),
    # "horas" → "hora" (feminino).
    raiz = primeira[:-1] if plural else primeira
    feminino = raiz.endswith(FEMININAS)

    artigo = ("a" if feminino else "o") + ("s" if plural else "")
    return Campo(artigo, palavras)


def _onde(erro: dict[str, Any]) -> str | None:
    """O último pedaço do `loc` que é nome de campo, ignorando índices."""
    for parte in reversed(erro.get("loc", ())):
        if isinstance(parte, str) and parte not in {"body", "query", "path"}:
            return parte
    return None


def _opcoes(esperado: Any) -> str:
    """O Pydantic monta "'a', 'b' or 'c'" — o "or" fica em inglês na frase."""
    return str(esperado).replace("' or '", "' ou '")


def _numero(valor: Any) -> str:
    if isinstance(valor, float) and valor.is_integer():
        return str(int(valor))
    return str(valor)


def traduzir(erro: dict[str, Any]) -> str:
    tipo = erro.get("type", "")
    bruto = _onde(erro)
    campo = nome_do_campo(bruto) if bruto else Campo("o", "valor")
    contexto = erro.get("ctx") or {}

    if tipo == "missing":
        return f"Falta preencher {campo.com_artigo}."

    if tipo in {"greater_than", "greater_than_equal"}:
        limite = _numero(contexto.get("gt", contexto.get("ge", "")))
        relacao = "maior que" if tipo == "greater_than" else "pelo menos"
        return f"{campo.maiuscula} {campo.precisa()} ser {relacao} {limite}."

    if tipo in {"less_than", "less_than_equal"}:
        limite = _numero(contexto.get("lt", contexto.get("le", "")))
        relacao = "menor que" if tipo == "less_than" else "no máximo"
        return f"{campo.maiuscula} {campo.precisa()} ser {relacao} {limite}."

    if tipo == "string_too_short":
        minimo = contexto.get("min_length", "")
        return f"{campo.maiuscula} {campo.precisa()} de pelo menos {minimo} caracteres."

    if tipo == "string_too_long":
        maximo = contexto.get("max_length", "")
        return f"{campo.maiuscula} {campo.passa()} de {maximo} caracteres."

    if tipo in {"too_short", "too_long"}:
        return f"{campo.maiuscula} {campo.esta()} com itens demais ou de menos."

    if tipo in {"int_parsing", "float_parsing", "int_type", "float_type", "decimal_parsing"}:
        return f"Escreva {campo.com_artigo} como número."

    if tipo == "int_from_float":
        return f"Escreva {campo.com_artigo} como número inteiro, sem casas decimais."

    if tipo in {"bool_parsing", "bool_type"}:
        return f"{campo.maiuscula} {campo.precisa()} ser sim ou não."

    if tipo in {"date_parsing", "date_type", "date_from_datetime_parsing"}:
        return f"{campo.maiuscula} {campo.precisa()} ser uma data válida."

    if tipo in {"datetime_parsing", "datetime_type"}:
        return f"{campo.maiuscula} {campo.precisa()} ser uma data e hora válidas."

    if tipo in {"enum", "literal_error"}:
        return (
            f"{campo.maiuscula} não {campo.aceita()} esse valor. "
            f"Use {_opcoes(contexto.get('expected', ''))}."
        )

    if tipo in {"string_type", "string_pattern_mismatch"}:
        return f"{campo.maiuscula} {campo.esta()} num formato que o app não entende."

    if tipo == "json_invalid":
        return "O conteúdo enviado não é um JSON válido."

    if tipo == "value_error":
        # As validações escritas à mão já saem em português; repassar é o certo.
        # A do EmailStr não sai, e é a única que aparece na prática.
        motivo = str(contexto.get("error", "")) or erro.get("msg", "")
        if bruto == "email" or "email address" in motivo.lower():
            return "Esse email não parece um email."
        return motivo or f"{campo.maiuscula} não é válido."

    return f"{campo.maiuscula} não {campo.esta()} num valor aceito."


async def tratar(_: Request, erro: RequestValidationError) -> JSONResponse:
    """Devolve o mesmo formato do FastAPI, com `msg` já traduzida.

    Mantém a lista por campo em vez de virar uma string só: o formato é o que a
    tela já sabe achatar, e trocar a forma da resposta para trocar o idioma
    quebraria quem lê `loc`.
    """
    detalhes = [
        {
            "type": item.get("type", ""),
            "loc": list(item.get("loc", ())),
            "msg": traduzir(item),
        }
        for item in erro.errors()
    ]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"detail": detalhes},
    )
