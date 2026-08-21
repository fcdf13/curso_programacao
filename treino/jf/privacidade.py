"""Consentimento, exportação e exclusão — o que a LGPD exige em código.

A versão do termo é o **hash do próprio texto**, não um número que alguém
precisa lembrar de incrementar. Editar o termo muda a versão sozinho, o
consentimento anterior deixa de valer para o texto novo, e o app volta a
perguntar. É o comportamento que a lei pede (o consentimento é para uma
finalidade específica, art. 8º §4º) e o único que não depende de disciplina.
"""

from __future__ import annotations

import hashlib
from functools import lru_cache
from pathlib import Path

TERMO = Path(__file__).resolve().parent / "dados" / "termo.md"


@lru_cache(maxsize=1)
def texto_do_termo() -> str:
    return TERMO.read_text(encoding="utf-8")


@lru_cache(maxsize=1)
def versao_do_termo() -> str:
    """Doze caracteres do sha256 do texto. Curto para caber numa coluna e ser
    lido num log, e longo o bastante para não colidir na prática."""
    return hashlib.sha256(texto_do_termo().encode("utf-8")).hexdigest()[:12]
