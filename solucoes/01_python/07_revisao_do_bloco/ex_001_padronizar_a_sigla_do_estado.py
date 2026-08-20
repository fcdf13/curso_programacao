"""
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
"""

META = {
    "id": "A07-001",
    "titulo": "Padronizar a sigla do estado",
    "nivel": 3,
    "tempo_min": 8,
    "tags": ["strings", "condicionais", "limpeza", "revisao"],
    "requer": ["A03-005", "A04-005"],
    "dicas": [
        "Limpe primeiro, valide depois: strip e upper antes de conferir o tamanho.",
        "Guarde o texto já limpo numa variável — você vai usá-lo duas vezes.",
        'if len(limpa) != 2: return "??" — e devolva a sigla no fim.',
    ],
}


def resolver(uf: str) -> str:
    # Normalizar antes de validar evita rejeitar ' sp ' por causa dos espaços.
    limpa = uf.strip().upper()
    if len(limpa) != 2:
        return "??"
    return limpa
