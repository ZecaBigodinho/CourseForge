"""Tratamento das capturas da aula 03 do Módulo 02 do Canva (panfleto de promoção).
Mesmo estilo de tratar_aula01.py. Capturas de 918x854.
Uso: python tratar_m02_aula03.py <pasta_capturas> <pasta_saida>"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

CAP = Path(sys.argv[1]); OUT = Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
ROXO = (79, 53, 181)
FONTE = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 20)
AVATAR = (459, 9, 497, 47)


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
    img.save(OUT / f"03_{nome}.png")


img = abrir("p02_categoria")
destaque(img, (322, 270, 443, 314)); marcador(img, 1, 322, 270)
destaque(img, (324, 386, 469, 524)); marcador(img, 2, 469, 390)
destaque(img, (162, 542, 308, 682)); marcador(img, 3, 162, 546)
salvar(img, "categoria")

img = abrir("p03_filtrado")
destaque(img, (350, 270, 463, 314)); marcador(img, 1, 463, 274)
destaque(img, (302, 270, 346, 314)); marcador(img, 2, 302, 274)
destaque(img, (95, 358, 281, 619)); marcador(img, 3, 95, 362)
destaque(img, (491, 358, 677, 619)); marcador(img, 4, 677, 362)
salvar(img, "filtro_panfleto")

img = abrir("p04_previa").crop((0, 0, 918, 440))
embacar(img, (432, 212, 705, 248))
destaque(img, (430, 56, 802, 154)); marcador(img, 1, 430, 56)
destaque(img, (430, 158, 710, 184)); marcador(img, 2, 722, 171)
destaque(img, (430, 383, 723, 427)); marcador(img, 3, 430, 383)
salvar(img, "previa_panfleto")

img = abrir("p05_editor")
embacar(img, AVATAR, 6)
destaque(img, (596, 6, 782, 50)); marcador(img, 1, 596, 10)
destaque(img, (572, 64, 910, 140)); marcador(img, 2, 572, 68)
destaque(img, (572, 742, 908, 792)); marcador(img, 3, 572, 746)
destaque(img, (872, 62, 908, 100)); marcador(img, 4, 860, 112)
salvar(img, "painel_grafica")

img = abrir("p06_editor_limpo")
embacar(img, AVATAR, 6)
destaque(img, (336, 176, 656, 310)); marcador(img, 1, 336, 180)
destaque(img, (356, 372, 636, 438)); marcador(img, 2, 636, 376)
destaque(img, (314, 442, 684, 672)); marcador(img, 3, 684, 446)
destaque(img, (376, 686, 624, 718)); marcador(img, 4, 624, 690)
salvar(img, "hierarquia")

img = abrir("p07_selos")
destaque(img, (87, 285, 404, 368)); marcador(img, 1, 404, 289)
destaque(img, (87, 558, 404, 642)); marcador(img, 2, 404, 562)
salvar(img, "selos_com_coroa")

img = abrir("p08_filtro")
destaque(img, (147, 133, 191, 177)); marcador(img, 1, 135, 133)
destaque(img, (152, 188, 466, 650)); marcador(img, 2, 466, 192)
salvar(img, "filtro_elementos")

img = abrir("p09_selos_todos")
destaque(img, (87, 498, 185, 602)); marcador(img, 1, 87, 502)
destaque(img, (195, 390, 404, 602)); marcador(img, 2, 404, 394)
salvar(img, "selo_ambiguo")

img = abrir("p10_explosao")
destaque(img, (87, 72, 419, 188)); marcador(img, 1, 419, 76)
destaque(img, (301, 393, 404, 499)); marcador(img, 2, 404, 397)
salvar(img, "busca_explosao")

img = abrir("p11_elemento_no_meio")
destaque(img, (590, 354, 760, 525)); marcador(img, 1, 760, 358)
destaque(img, (300, 393, 402, 495)); marcador(img, 2, 300, 397)
destaque(img, (87, 509, 402, 654)); marcador(img, 3, 402, 513)
salvar(img, "elemento_no_meio")

img = abrir("p12_alterar_tudo")
destaque(img, (178, 211, 219, 252)); marcador(img, 1, 231, 222)
destaque(img, (468, 480, 573, 514)); marcador(img, 2, 585, 482)
destaque(img, (100, 762, 395, 796)); marcador(img, 3, 100, 766)
destaque(img, (87, 801, 403, 843)); marcador(img, 4, 403, 805)
salvar(img, "alterar_tudo")

img = abrir("p13_agrupar")
destaque(img, (441, 391, 515, 423)); marcador(img, 1, 441, 391)
destaque(img, (466, 444, 576, 553)); marcador(img, 2, 466, 557)
salvar(img, "agrupar")

abrir("p14_final").crop((468, 146, 885, 735)).save(OUT / "03_panfleto_pronto.png")

img = abrir("p15_zoom")
destaque(img, (615, 657, 746, 720)); marcador(img, 1, 758, 680)
destaque(img, (615, 722, 746, 808)); marcador(img, 2, 758, 760)
destaque(img, (615, 817, 674, 851)); marcador(img, 3, 603, 834)
salvar(img, "zoom")

img = abrir("p16_zoom10").crop((434, 300, 918, 620))
destaque(img, (196, 66, 262, 194)); marcador(img, 1, 262, 70)
salvar(img, "teste_distancia")
print("ok")
