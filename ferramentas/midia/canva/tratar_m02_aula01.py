"""Tratamento das capturas da aula 01 do Módulo 02 do Canva (catálogo de produtos).
Mesmo estilo de tratar_aula01.py. Capturas de 945x854 (painel do navegador nesta sessão).
Uso: python tratar_m02_aula01.py <pasta_capturas> <pasta_saida>"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

CAP = Path(sys.argv[1]); OUT = Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
ROXO = (79, 53, 181)
FONTE = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 20)


def abrir(nome):
    return Image.open(CAP / f"{nome}.png").convert("RGB")


def destaque(img, caixa):
    ImageDraw.Draw(img).rounded_rectangle(caixa, radius=8, outline=ROXO, width=4)


def marcador(img, n, x, y):
    d = ImageDraw.Draw(img); r = 15
    d.ellipse((x - r, y - r, x + r, y + r), fill=ROXO, outline=(255, 255, 255), width=3)
    d.text((x, y), str(n), fill=(255, 255, 255), font=FONTE, anchor="mm")


def embacar(img, caixa, raio=8):
    img.paste(img.crop(caixa).filter(ImageFilter.GaussianBlur(raio)), caixa[:2])


def salvar(img, nome):
    img.save(OUT / f"01_{nome}.png")


img = abrir("c01_busca").crop((0, 0, 945, 700))
destaque(img, (135, 194, 861, 262)); marcador(img, 1, 135, 194)
destaque(img, (92, 360, 904, 400)); marcador(img, 2, 92, 360)
destaque(img, (300, 412, 487, 676)); marcador(img, 3, 300, 412)
destaque(img, (244, 644, 276, 668)); destaque(img, (650, 644, 684, 668)); marcador(img, 4, 230, 690)
salvar(img, "busca_catalogo")

img = abrir("c01_previa").crop((0, 0, 945, 470))
embacar(img, (456, 210, 760, 248))                  # foto e nome de quem criou o modelo
destaque(img, (454, 54, 820, 154)); marcador(img, 1, 454, 54)
destaque(img, (454, 158, 742, 184)); marcador(img, 2, 756, 171)
destaque(img, (454, 402, 751, 450)); marcador(img, 3, 454, 402)
salvar(img, "previa_catalogo")

img = abrir("c02_editor")
embacar(img, (486, 10, 524, 46))
destaque(img, (350, 167, 665, 215)); marcador(img, 1, 350, 167)
destaque(img, (336, 223, 681, 643)); marcador(img, 2, 336, 223)
destaque(img, (298, 649, 720, 738)); marcador(img, 3, 298, 649)
destaque(img, (298, 756, 720, 800)); marcador(img, 4, 298, 756)
salvar(img, "editor_catalogo")

img = abrir("c03_menu_mais").crop((240, 60, 945, 740))
destaque(img, (258, 588, 300, 626)); marcador(img, 1, 244, 606)
destaque(img, (272, 66, 568, 104)); marcador(img, 2, 582, 85)
destaque(img, (272, 134, 568, 172)); marcador(img, 3, 582, 153)
destaque(img, (272, 394, 568, 432)); marcador(img, 4, 582, 413)
salvar(img, "menu_mais")

img = abrir("c04_link").crop((300, 380, 945, 740))
destaque(img, (222, 64, 550, 112)); marcador(img, 1, 222, 64)
destaque(img, (222, 140, 550, 188)); marcador(img, 2, 222, 140)
destaque(img, (462, 196, 550, 244)); marcador(img, 3, 450, 220)
destaque(img, (36, 322, 152, 342)); marcador(img, 4, 166, 332)
salvar(img, "adicionar_link")

img = abrir("c05_substituir")
destaque(img, (522, 67, 611, 104)); marcador(img, 1, 522, 67)
destaque(img, (750, 225, 860, 333)); marcador(img, 2, 866, 228)
destaque(img, (84, 240, 414, 374)); marcador(img, 3, 414, 244)
destaque(img, (120, 500, 160, 530)); marcador(img, 4, 172, 515)
destaque(img, (614, 67, 798, 104)); marcador(img, 5, 798, 67)
salvar(img, "substituir_foto")

img = abrir("c07_adicionar_pagina").crop((280, 440, 945, 810))
destaque(img, (402, 316, 442, 360)); marcador(img, 1, 456, 338)
destaque(img, (278, 20, 564, 307)); marcador(img, 2, 278, 20)
salvar(img, "outro_tipo_de_pagina")

img = abrir("c09_catalogo_final")
destaque(img, (296, 110, 722, 144)); marcador(img, 1, 296, 110)
destaque(img, (617, 113, 647, 142)); marcador(img, 2, 632, 160)
destaque(img, (296, 758, 722, 788)); marcador(img, 3, 296, 758)
destaque(img, (838, 816, 870, 850)); marcador(img, 4, 824, 816)
salvar(img, "paginas")

img = abrir("c08_grade").crop((0, 56, 945, 460))
destaque(img, (314, 6, 634, 52)); marcador(img, 1, 314, 6)
destaque(img, (264, 68, 465, 352)); marcador(img, 2, 465, 72)
salvar(img, "grade")

abrir("c09_catalogo_final").crop((301, 146, 718, 734)).save(OUT / "01_catalogo_pronto.png")

img = abrir("c10_nivel_acesso").crop((520, 56, 945, 700))
embacar(img, (18, 142, 50, 174))
destaque(img, (18, 272, 402, 354)); marcador(img, 1, 402, 276)
destaque(img, (18, 354, 402, 436)); marcador(img, 2, 402, 358)
salvar(img, "nivel_de_acesso")

img = abrir("c11_baixar").crop((520, 56, 945, 600))
destaque(img, (16, 90, 404, 134)); marcador(img, 1, 404, 94)
destaque(img, (16, 174, 210, 218)); marcador(img, 2, 216, 196)
destaque(img, (16, 228, 186, 258)); destaque(img, (16, 268, 314, 298)); marcador(img, 3, 330, 263)
destaque(img, (16, 336, 404, 382)); marcador(img, 4, 404, 340)
destaque(img, (16, 460, 404, 506)); marcador(img, 5, 404, 464)
salvar(img, "baixar_pdf")
print("ok")
