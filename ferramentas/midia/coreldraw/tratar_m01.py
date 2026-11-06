"""Tratamento das capturas do Módulo 01 do CorelDRAW (aulas 01 a 05).
Capturas feitas com captura_corel.ps1 (janela 1388x894, sem a borda invisível).
Uso: python tratar_m01.py <pasta_capturas> <pasta_saida>"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

CAP = Path(sys.argv[1]); OUT = Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
ROXO = (79, 53, 181)
FONTE = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 18)
UI = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 12)


def abrir(nome):
    return Image.open(next(CAP.glob(f"{nome}.*"))).convert("RGB")


def destaque(img, caixa):
    ImageDraw.Draw(img).rounded_rectangle(caixa, radius=8, outline=ROXO, width=4)


def marcador(img, n, x, y):
    d = ImageDraw.Draw(img); r = 14
    d.ellipse((x - r, y - r, x + r, y + r), fill=ROXO, outline=(255, 255, 255), width=3)
    d.text((x, y), str(n), fill=(255, 255, 255), font=FONTE, anchor="mm")


def remendo(img, outra, caixa):
    """Cobre um trecho (ex.: balão de dica preso) com o mesmo trecho de outra captura limpa."""
    img.paste(outra.crop(caixa), caixa[:2])


def salvar(img, nome):
    img.save(OUT / f"{nome}.png")


# ---------- Aula 01: tela de boas-vindas e interface ----------
img = abrir("r4_01_boas_vindas")
remendo(img, abrir("r2_01_boas_vindas"), (36, 158, 300, 224))   # balão de dica sobre "Começar"
destaque(img, (288, 186, 390, 310)); marcador(img, 1, 390, 190)
destaque(img, (278, 535, 419, 565)); marcador(img, 2, 278, 535)
destaque(img, (52, 418, 240, 480)); marcador(img, 3, 240, 422)
destaque(img, (40, 132, 192, 156)); marcador(img, 4, 204, 144)
salvar(img, "01_boas_vindas")

img = abrir("r3_03_interface")
destaque(img, (2, 28, 790, 48)); marcador(img, 1, 802, 38)
destaque(img, (2, 52, 1100, 82)); marcador(img, 2, 1112, 67)
destaque(img, (2, 88, 1080, 124)); marcador(img, 3, 1092, 106)
destaque(img, (2, 130, 34, 790)); marcador(img, 4, 46, 700)
destaque(img, (356, 230, 720, 738)); marcador(img, 5, 720, 240)
destaque(img, (1040, 130, 1362, 852)); marcador(img, 6, 1028, 700)
destaque(img, (1364, 205, 1388, 832)); marcador(img, 7, 1364, 215)
destaque(img, (36, 808, 332, 834)); marcador(img, 8, 344, 821)
destaque(img, (2, 862, 1386, 892)); marcador(img, 9, 640, 862)
salvar(img, "01_interface")

# ---------- Aula 02: documento, unidades e páginas ----------
img = abrir("r3_02_novo_documento")
d = ImageDraw.Draw(img)                                           # balão "Duplo" sobre o modelo
fundo = img.getpixel((330, 400))
d.rectangle((340, 408, 440, 446), fill=fundo)
d.text((391, 421), "Duplo", fill=(0, 0, 0), font=UI, anchor="mm")
d.text((391, 434), "11 × 17 pol.", fill=(0, 0, 0), font=UI, anchor="mm")
destaque(img, (120, 126, 210, 232)); marcador(img, 1, 120, 130)
destaque(img, (664, 174, 860, 203)); marcador(img, 2, 872, 188)
destaque(img, (664, 206, 724, 235)); marcador(img, 3, 736, 220)
destaque(img, (664, 274, 780, 298)); marcador(img, 4, 792, 286)
destaque(img, (658, 345, 856, 406)); marcador(img, 5, 868, 375)
destaque(img, (662, 410, 724, 438)); marcador(img, 6, 736, 424)
destaque(img, (658, 442, 752, 470)); marcador(img, 7, 764, 456)
destaque(img, (744, 643, 830, 673)); marcador(img, 8, 744, 643)
salvar(img, "02_novo_documento")

img = abrir("r3_04_paginas")
destaque(img, (4, 90, 168, 122)); marcador(img, 1, 86, 90)
destaque(img, (178, 88, 300, 124)); marcador(img, 2, 300, 90)
destaque(img, (352, 90, 418, 122)); marcador(img, 3, 418, 92)
destaque(img, (498, 90, 662, 122)); marcador(img, 4, 662, 92)
destaque(img, (36, 808, 436, 834)); marcador(img, 5, 448, 821)
salvar(img, "02_paginas")

# ---------- Aula 03: formas, seleção e texto ----------
img = abrir("r3_07_selecao_tudo")
destaque(img, (4, 132, 32, 158)); marcador(img, 1, 46, 166)
destaque(img, (4, 342, 32, 368)); marcador(img, 2, 46, 355)
destaque(img, (4, 374, 32, 400)); marcador(img, 3, 46, 387)
destaque(img, (4, 448, 32, 474)); marcador(img, 4, 46, 461)
destaque(img, (394, 280, 688, 480)); marcador(img, 5, 688, 284)
destaque(img, (4, 88, 334, 124)); marcador(img, 6, 346, 106)
salvar(img, "03_formas_selecao")

img = abrir("r3_06_selecao_texto")
destaque(img, (556, 92, 730, 120)); marcador(img, 1, 556, 92)
destaque(img, (735, 92, 828, 120)); marcador(img, 2, 828, 92)
destaque(img, (868, 90, 968, 122)); marcador(img, 3, 968, 92)
destaque(img, (396, 434, 530, 480)); marcador(img, 4, 530, 438)
salvar(img, "03_texto_selecionado")

# ---------- Aula 04: cor ----------
img = abrir("r5_02_painel_propriedades")
destaque(img, (370, 286, 548, 408)); marcador(img, 1, 370, 290)
destaque(img, (982, 158, 1204, 188)); marcador(img, 2, 1216, 173)
destaque(img, (984, 214, 1188, 280)); marcador(img, 3, 1200, 247)
destaque(img, (944, 90, 1048, 122)); marcador(img, 4, 944, 90)
destaque(img, (1364, 205, 1388, 832)); marcador(img, 5, 1364, 215)
destaque(img, (1078, 864, 1388, 892)); marcador(img, 6, 1062, 878)
salvar(img, "04_propriedades_cor")

img = abrir("r5_04_dialogo_preenchimento")
destaque(img, (16, 42, 272, 72)); marcador(img, 1, 284, 57)
destaque(img, (26, 178, 300, 478)); marcador(img, 2, 300, 182)
destaque(img, (338, 144, 634, 172)); marcador(img, 3, 634, 146)
destaque(img, (356, 250, 436, 378)); marcador(img, 4, 436, 254)
destaque(img, (462, 250, 536, 378)); marcador(img, 5, 536, 254)
salvar(img, "04_editar_preenchimento")

img = abrir("r5_05_dialogo_contorno")
destaque(img, (182, 72, 268, 100)); marcador(img, 1, 280, 86)
destaque(img, (182, 105, 384, 133)); marcador(img, 2, 396, 119)
destaque(img, (182, 138, 412, 164)); marcador(img, 3, 424, 151)
destaque(img, (182, 234, 278, 292)); marcador(img, 4, 290, 263)
destaque(img, (442, 284, 604, 328)); marcador(img, 5, 616, 306)
salvar(img, "04_caneta_contorno")

# ---------- Aula 05: projeto cartão de visita ----------
img = abrir("r5_10_cartao_pronto")
remendo(img, abrir("r5_12_menu_arquivo"), (1356, 176, 1388, 202))  # balão "Aprender"
destaque(img, (4, 90, 168, 122)); marcador(img, 1, 130, 90)
destaque(img, (178, 88, 300, 124)); marcador(img, 2, 300, 90)
destaque(img, (498, 90, 662, 122)); marcador(img, 3, 662, 92)
destaque(img, (108, 806, 168, 834)); marcador(img, 4, 180, 820)
salvar(img, "05_cartao_editor")

img = abrir("r5_12_menu_arquivo").crop((0, 0, 620, 660))
destaque(img, (6, 242, 252, 288)); marcador(img, 1, 264, 265)
destaque(img, (6, 402, 252, 428)); marcador(img, 2, 264, 415)
destaque(img, (6, 490, 252, 516)); marcador(img, 3, 264, 503)
salvar(img, "05_menu_arquivo")

img = abrir("r7_13_dialogo_salvar")
destaque(img, (122, 388, 944, 416)); marcador(img, 1, 66, 402)
destaque(img, (122, 416, 944, 441)); marcador(img, 2, 66, 428)
destaque(img, (646, 516, 790, 546)); marcador(img, 3, 802, 531)
destaque(img, (738, 560, 830, 590)); marcador(img, 4, 738, 560)
salvar(img, "05_salvar_cdr")

img = abrir("r7_14_dialogo_exportar")
destaque(img, (122, 388, 944, 416)); marcador(img, 1, 66, 402)
destaque(img, (122, 416, 944, 441)); marcador(img, 2, 66, 428)
destaque(img, (738, 533, 830, 563)); marcador(img, 3, 738, 533)
salvar(img, "05_exportar")

Image.open(CAP / "saida" / "cartao_ana_souza_pdf.png").convert("RGB").save(OUT / "05_cartao_final.png")
print("ok")
