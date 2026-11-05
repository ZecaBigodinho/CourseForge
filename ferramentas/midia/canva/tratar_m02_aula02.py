"""Tratamento das capturas da aula 02 do Módulo 02 do Canva (cardápio).
Mesmo estilo de tratar_aula01.py. Capturas de 945x854.
Uso: python tratar_m02_aula02.py <pasta_capturas> <pasta_saida>"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

CAP = Path(sys.argv[1]); OUT = Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
ROXO = (79, 53, 181)
FONTE = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 20)
AVATAR = (486, 10, 524, 46)


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
    img.save(OUT / f"02_{nome}.png")


img = abrir("d01_busca_cardapios")
destaque(img, (95, 14, 243, 274)); marcador(img, 1, 95, 18)
destaque(img, (92, 298, 904, 336)); marcador(img, 2, 92, 298)
destaque(img, (481, 350, 665, 609)); marcador(img, 3, 665, 354)
destaque(img, (92, 634, 904, 672)); marcador(img, 4, 92, 634)
salvar(img, "busca_cardapio")

img = abrir("d02_previa").crop((0, 0, 945, 470))
embacar(img, (459, 180, 730, 214))
destaque(img, (455, 54, 795, 124)); marcador(img, 1, 455, 54)
destaque(img, (455, 128, 620, 152)); marcador(img, 2, 634, 140)
destaque(img, (457, 404, 749, 448)); marcador(img, 3, 457, 404)
salvar(img, "previa_cardapio")

img = abrir("d03_editor")
embacar(img, AVATAR, 6)
destaque(img, (507, 207, 670, 288)); marcador(img, 1, 670, 211)
destaque(img, (347, 315, 549, 413)); marcador(img, 2, 347, 315)
destaque(img, (347, 425, 646, 543)); marcador(img, 3, 347, 425)
destaque(img, (514, 550, 689, 644)); marcador(img, 4, 689, 554)
destaque(img, (340, 650, 468, 701)); marcador(img, 5, 340, 650)
destaque(img, (514, 655, 685, 695)); marcador(img, 6, 685, 659)
salvar(img, "editor_cardapio")

img = abrir("d04_pix_estourado").crop((300, 520, 718, 740))
destaque(img, (34, 124, 194, 186)); marcador(img, 1, 194, 128)
salvar(img, "texto_estourado")

img = abrir("d05_lista")
destaque(img, (366, 538, 470, 557)); marcador(img, 1, 480, 548)
destaque(img, (350, 552, 495, 582)); marcador(img, 2, 505, 570)
destaque(img, (213, 69, 309, 101)); marcador(img, 3, 213, 69)
destaque(img, (564, 69, 598, 101)); marcador(img, 4, 598, 69)
salvar(img, "lista_cresceu")

img = abrir("d06_cor")
destaque(img, (345, 69, 379, 101)); marcador(img, 1, 391, 70)
destaque(img, (87, 230, 404, 312)); marcador(img, 2, 404, 234)
destaque(img, (87, 316, 404, 384)); marcador(img, 3, 404, 320)
destaque(img, (87, 610, 404, 804)); marcador(img, 4, 404, 614)
destaque(img, (810, 136, 906, 742)); marcador(img, 5, 810, 140)
salvar(img, "painel_cor")

img = abrir("d08_qr_elementos").crop((0, 56, 945, 854))
destaque(img, (88, 17, 418, 131)); marcador(img, 1, 418, 21)
destaque(img, (88, 198, 403, 411)); marcador(img, 2, 403, 202)
destaque(img, (100, 356, 244, 400)); marcador(img, 3, 100, 356)
destaque(img, (248, 356, 391, 400)); marcador(img, 4, 391, 356)
destaque(img, (88, 456, 404, 542)); marcador(img, 5, 404, 460)
salvar(img, "qr_elementos")

img = abrir("d09_qr_app").crop((0, 56, 440, 854))
destaque(img, (86, 334, 270, 362)); marcador(img, 1, 282, 348)
destaque(img, (86, 508, 268, 548)); marcador(img, 2, 282, 528)
destaque(img, (87, 740, 419, 784)); marcador(img, 3, 87, 740)
salvar(img, "qr_app")

img = abrir("d10_qr_url").crop((0, 56, 440, 400))
destaque(img, (87, 161, 404, 205)); marcador(img, 1, 404, 165)
destaque(img, (87, 218, 404, 260)); marcador(img, 2, 404, 222)
destaque(img, (87, 273, 404, 317)); marcador(img, 3, 404, 277)
salvar(img, "qr_url")

img = abrir("d11_qr_gerado")
destaque(img, (604, 354, 776, 527)); marcador(img, 1, 776, 358)
destaque(img, (87, 329, 404, 373)); marcador(img, 2, 404, 333)
salvar(img, "qr_gerado")

img = abrir("d12_painel_texto")
destaque(img, (14, 292, 60, 345)); marcador(img, 1, 62, 296)
destaque(img, (85, 143, 417, 186)); marcador(img, 2, 417, 147)
destaque(img, (85, 370, 403, 545)); marcador(img, 3, 403, 374)
salvar(img, "painel_texto")

abrir("d13_final").crop((300, 146, 718, 734)).save(OUT / "02_cardapio_pronto.png")

img = abrir("d14_baixar_jpg").crop((520, 56, 945, 600))
destaque(img, (16, 90, 404, 134)); marcador(img, 1, 404, 94)
destaque(img, (16, 145, 226, 170)); marcador(img, 2, 238, 158)
destaque(img, (16, 228, 104, 250)); marcador(img, 3, 116, 239)
destaque(img, (16, 350, 404, 394)); marcador(img, 4, 404, 354)
salvar(img, "baixar_jpg")
print("ok")
