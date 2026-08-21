"""Gera os ícones do PWA a partir da marca.

O monograma do logo — arco vermelho aberto com o JF por cima — redesenhado como
forma vetorial simples, porque o logo original é uma ilustração detalhada que
vira borrão a 192 px.

    python3 gerar-icones.py
"""

from __future__ import annotations

from pathlib import Path

import pymupdf

DESTINO = Path(__file__).resolve().parent / "public"

PRETO = (0x10 / 255, 0x10 / 255, 0x10 / 255)
VERMELHO = (0xAD / 255, 0x01 / 255, 0x01 / 255)
OSSO = (0xF5 / 255, 0xF3 / 255, 0xF4 / 255)

FONTE = "/usr/share/fonts/truetype/freefont/FreeSansBoldOblique.ttf"

LADO = 512.0


def desenhar(escala: float) -> pymupdf.Document:
    """Monta o ícone numa página quadrada.

    `escala` encolhe o desenho para dentro da página: os ícones "maskable" são
    recortados em círculo pelo Android, e o que passa de ~80% do lado some.
    """
    documento = pymupdf.open()
    pagina = documento.new_page(width=LADO, height=LADO)
    centro = pymupdf.Point(LADO / 2, LADO / 2)

    pagina.draw_rect(pagina.rect, color=None, fill=PRETO)

    # Arco: um anel vermelho grosso com um pedaço coberto de novo pelo fundo,
    # que é o que deixa a volta aberta como no logo.
    raio = 190 * escala
    espessura = 30 * escala
    pagina.draw_circle(centro, raio, color=VERMELHO, width=espessura)
    pagina.draw_rect(
        pymupdf.Rect(centro.x, 0, LADO, centro.y - raio * 0.35),
        color=None,
        fill=PRETO,
    )

    texto = "JF"
    tamanho = 210 * escala
    fonte = pymupdf.Font(fontfile=FONTE)
    largura = fonte.text_length(texto, tamanho)
    pagina.insert_text(
        pymupdf.Point(centro.x - largura / 2, centro.y + tamanho * 0.36),
        texto,
        fontsize=tamanho,
        fontfile=FONTE,
        fontname="marca",
        color=OSSO,
    )
    return documento


def salvar(nome: str, lado: int, escala: float = 1.0) -> None:
    documento = desenhar(escala)
    pixels = documento[0].get_pixmap(matrix=pymupdf.Matrix(lado / LADO, lado / LADO))
    pixels.save(DESTINO / nome)
    documento.close()
    print(f"  {nome}  {lado}×{lado}")


def main() -> None:
    DESTINO.mkdir(parents=True, exist_ok=True)
    print("Gerando ícones em web/public:")
    salvar("icone-192.png", 192)
    salvar("icone-512.png", 512)
    salvar("icone-maskable-512.png", 512, escala=0.72)
    salvar("apple-touch-icon.png", 180)
    salvar("favicon-32.png", 32)


if __name__ == "__main__":
    main()
