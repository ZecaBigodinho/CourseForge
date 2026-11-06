"""Tratamento das capturas da aula 02 do Módulo 03 do Canva (carrossel para o Instagram).
Mesmo estilo de tratar_aula01.py. Parte das capturas é de 918x854 (região da tela) e parte
vem do próprio painel do navegador (800x744, JPG), usada quando a tela do computador
estava com outras janelas por cima.
Uso: python tratar_m03_aula02.py <pasta_capturas> <pasta_saida>"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

CAP = Path(sys.argv[1]); OUT = Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
ROXO = (79, 53, 181)
FONTE = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 18)


def abrir(nome):
    arq = next(CAP.glob(f"{nome}.*"))
    return Image.open(arq).convert("RGB")


def destaque(img, caixa):
    ImageDraw.Draw(img).rounded_rectangle(caixa, radius=8, outline=ROXO, width=4)


def marcador(img, n, x, y):
    d = ImageDraw.Draw(img); r = 14
    d.ellipse((x - r, y - r, x + r, y + r), fill=ROXO, outline=(255, 255, 255), width=3)
    d.text((x, y), str(n), fill=(255, 255, 255), font=FONTE, anchor="mm")


def embacar(img, caixa, raio=8):
    img.paste(img.crop(caixa).filter(ImageFilter.GaussianBlur(raio)), caixa[:2])


def salvar(img, nome):
    img.save(OUT / f"02_{nome}.png")


img = abrir("k01_busca").crop((0, 0, 918, 600))
destaque(img, (137, 196, 833, 260)); marcador(img, 1, 137, 196)
destaque(img, (689, 359, 873, 588)); marcador(img, 2, 873, 363)
destaque(img, (244, 562, 274, 586)); marcador(img, 3, 230, 574)
salvar(img, "busca_carrossel")

img = abrir("k02_previa").crop((0, 0, 918, 600))
embacar(img, (430, 214, 740, 258))
destaque(img, (430, 158, 736, 184)); marcador(img, 1, 748, 171)
destaque(img, (87, 467, 397, 583)); marcador(img, 2, 87, 467)
destaque(img, (430, 280, 722, 324)); marcador(img, 3, 430, 280)
salvar(img, "previa_carrossel")

img = abrir("k03_grade_original").crop((0, 56, 918, 700))
destaque(img, (47, 70, 239, 310)); marcador(img, 1, 47, 70)
destaque(img, (259, 70, 873, 310)); marcador(img, 2, 873, 74)
destaque(img, (471, 360, 661, 600)); marcador(img, 3, 661, 364)
salvar(img, "estrutura")

img = abrir("k05_excluir_pagina").crop((0, 56, 918, 700))
destaque(img, (259, 360, 449, 600)); marcador(img, 1, 449, 364)
destaque(img, (509, 12, 539, 46)); marcador(img, 2, 524, 64)
salvar(img, "excluir_pagina")

img = abrir("k08_duplicar_posicao")
destaque(img, (527, 262, 754, 310)); marcador(img, 1, 754, 266)
destaque(img, (74, 568, 268, 610)); marcador(img, 2, 268, 572)
salvar(img, "duplicar_texto")

img = abrir("k07_cta_posicao")
destaque(img, (451, 436, 726, 491)); marcador(img, 1, 726, 440)
destaque(img, (74, 455, 170, 494)); marcador(img, 2, 170, 459)
destaque(img, (220, 309, 365, 348)); marcador(img, 3, 365, 313)
salvar(img, "chamada_final")

img = abrir("k09_grade_final").crop((0, 56, 800, 600))
destaque(img, (40, 54, 207, 262)); marcador(img, 1, 40, 58)
destaque(img, (224, 54, 761, 262)); marcador(img, 2, 761, 58)
destaque(img, (40, 307, 207, 515)); marcador(img, 3, 207, 311)
destaque(img, (224, 307, 392, 515)); marcador(img, 4, 392, 311)
salvar(img, "carrossel_pronto")

img = abrir("k10_compartilhar").crop((430, 50, 795, 610))
embacar(img, (14, 120, 64, 152), 6)
destaque(img, (25, 352, 90, 430)); marcador(img, 1, 25, 352)
destaque(img, (108, 352, 175, 430)); marcador(img, 2, 175, 356)
destaque(img, (194, 452, 258, 535)); marcador(img, 3, 258, 456)
destaque(img, (278, 352, 340, 430)); marcador(img, 4, 340, 356)
salvar(img, "compartilhar")

img = abrir("k11_baixar").crop((430, 50, 795, 515))
destaque(img, (14, 79, 348, 113)); marcador(img, 1, 348, 83)
destaque(img, (14, 128, 190, 148)); marcador(img, 2, 202, 138)
destaque(img, (18, 368, 125, 396)); marcador(img, 3, 125, 372)
destaque(img, (14, 417, 348, 451)); marcador(img, 4, 348, 421)
salvar(img, "baixar_png")
print("ok")
