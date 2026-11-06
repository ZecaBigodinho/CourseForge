"""Tratamento das capturas da aula 01 do Módulo 03 do Canva (convite virtual de aniversário).
Mesmo estilo de tratar_aula01.py. Capturas de 918x854.
Uso: python tratar_m03_aula01.py <pasta_capturas> <pasta_saida>"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

CAP = Path(sys.argv[1]); OUT = Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
ROXO = (79, 53, 181)
FONTE = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 20)
AVATAR = (650, 10, 686, 46)


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


img = abrir("v01_busca").crop((0, 0, 918, 700))
destaque(img, (137, 196, 833, 260)); marcador(img, 1, 137, 196)
destaque(img, (547, 271, 645, 313)); marcador(img, 2, 657, 292)
destaque(img, (95, 362, 205, 398)); marcador(img, 3, 217, 380)
salvar(img, "busca_convite")

img = abrir("v02_virtuais").crop((0, 280, 918, 630))
destaque(img, (95, 22, 300, 58)); marcador(img, 1, 312, 40)
destaque(img, (95, 70, 874, 330)); marcador(img, 2, 874, 74)
destaque(img, (654, 298, 686, 322)); marcador(img, 3, 640, 310)
salvar(img, "convites_virtuais")

img = abrir("v03_previa").crop((0, 0, 918, 500))
embacar(img, (430, 212, 712, 248))
destaque(img, (430, 56, 760, 152)); marcador(img, 1, 430, 56)
destaque(img, (430, 158, 728, 184)); marcador(img, 2, 740, 171)
destaque(img, (430, 268, 722, 312)); marcador(img, 3, 430, 268)
salvar(img, "previa_convite")

img = abrir("v04_editor")
embacar(img, AVATAR, 6)
destaque(img, (355, 305, 645, 405)); marcador(img, 1, 645, 309)
destaque(img, (335, 478, 500, 560)); marcador(img, 2, 500, 482)
destaque(img, (350, 596, 500, 648)); marcador(img, 3, 500, 600)
salvar(img, "partes_convite")

img = abrir("v05_link_rsvp")
embacar(img, AVATAR, 6)
destaque(img, (567, 419, 891, 463)); marcador(img, 1, 891, 423)
destaque(img, (567, 495, 891, 539)); marcador(img, 2, 891, 499)
destaque(img, (807, 551, 891, 595)); marcador(img, 3, 795, 573)
destaque(img, (536, 676, 772, 700)); marcador(img, 4, 784, 688)
salvar(img, "link_confirmacao")

img = abrir("v06_animar")
embacar(img, AVATAR, 6)
destaque(img, (716, 109, 786, 149)); marcador(img, 1, 728, 162)
destaque(img, (90, 115, 402, 153)); marcador(img, 2, 402, 119)
destaque(img, (88, 402, 404, 792)); marcador(img, 3, 404, 406)
salvar(img, "painel_animar")

img = abrir("v07_animado")
destaque(img, (195, 351, 297, 457)); marcador(img, 1, 297, 355)
destaque(img, (88, 538, 374, 592)); marcador(img, 2, 386, 565)
destaque(img, (88, 603, 404, 657)); marcador(img, 3, 404, 607)
destaque(img, (88, 683, 404, 767)); marcador(img, 4, 404, 687)
destaque(img, (635, 6, 782, 50)); marcador(img, 5, 623, 28)
salvar(img, "animacao_aplicada")

img = abrir("v08_baixar").crop((495, 56, 918, 390))
destaque(img, (14, 90, 402, 134)); marcador(img, 1, 402, 94)
destaque(img, (14, 148, 402, 206)); marcador(img, 2, 402, 152)
destaque(img, (14, 270, 402, 314)); marcador(img, 3, 402, 274)
salvar(img, "baixar_mp4")

abrir("v09_final").crop((468, 146, 885, 735)).save(OUT / "01_convite_pronto.png")
print("ok")
