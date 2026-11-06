"""Tratamento das capturas da aula 03 do Módulo 03 do Canva (capa de vídeo / miniatura do YouTube).
Capturas do próprio painel do navegador (800x744, JPG).
Uso: python tratar_m03_aula03.py <pasta_capturas> <pasta_saida>"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

CAP = Path(sys.argv[1]); OUT = Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
ROXO = (79, 53, 181)
FONTE = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 18)
AVATAR = (566, 10, 598, 40)


def abrir(nome):
    return Image.open(next(CAP.glob(f"{nome}.*"))).convert("RGB")


def destaque(img, caixa):
    ImageDraw.Draw(img).rounded_rectangle(caixa, radius=8, outline=ROXO, width=4)


def marcador(img, n, x, y):
    d = ImageDraw.Draw(img); r = 14
    d.ellipse((x - r, y - r, x + r, y + r), fill=ROXO, outline=(255, 255, 255), width=3)
    d.text((x, y), str(n), fill=(255, 255, 255), font=FONTE, anchor="mm")


def embacar(img, caixa, raio=8):
    img.paste(img.crop(caixa).filter(ImageFilter.GaussianBlur(raio)), caixa[:2])


def salvar(img, nome):
    img.save(OUT / f"03_{nome}.png")


img = abrir("y01_busca").crop((60, 0, 800, 710))
destaque(img, (58, 170, 666, 228)); marcador(img, 1, 58, 170)
destaque(img, (22, 312, 356, 500)); marcador(img, 2, 356, 316)
destaque(img, (323, 476, 350, 494)); marcador(img, 3, 311, 485)
destaque(img, (368, 312, 700, 500)); marcador(img, 4, 700, 316)
salvar(img, "busca_miniatura")

img = abrir("y02_previa").crop((48, 14, 760, 270))
embacar(img, (324, 142, 572, 176))
destaque(img, (326, 96, 566, 116)); marcador(img, 1, 578, 106)
destaque(img, (326, 192, 580, 230)); marcador(img, 2, 326, 192)
salvar(img, "previa_miniatura")

img = abrir("y04_camadas")
embacar(img, AVATAR, 5)
destaque(img, (75, 112, 364, 136)); marcador(img, 1, 364, 116)
destaque(img, (75, 260, 364, 368)); marcador(img, 2, 364, 264)
destaque(img, (75, 484, 364, 536)); marcador(img, 3, 364, 488)
salvar(img, "camadas_miniatura")

img = abrir("y05_substituir")
embacar(img, AVATAR, 5)
destaque(img, (590, 60, 666, 88)); marcador(img, 1, 678, 74)
destaque(img, (76, 98, 362, 146)); marcador(img, 2, 362, 102)
destaque(img, (75, 560, 222, 642)); marcador(img, 3, 222, 564)
destaque(img, (183, 278, 207, 296)); marcador(img, 4, 171, 287)
salvar(img, "substituir_foto")

img = abrir("y06_contraste_ruim").crop((84, 188, 779, 579))
destaque(img, (34, 92, 330, 302)); marcador(img, 1, 330, 96)
salvar(img, "contraste_ruim")

img = abrir("y07_efeito_sombra")
embacar(img, AVATAR, 5)
destaque(img, (528, 60, 586, 88)); marcador(img, 1, 598, 74)
destaque(img, (76, 146, 164, 234)); marcador(img, 2, 164, 150)
destaque(img, (75, 272, 352, 506)); marcador(img, 3, 352, 276)
salvar(img, "efeito_sombra")

abrir("y08_contraste_bom").crop((84, 188, 779, 579)).save(OUT / "03_capa_pronta.png")

img = abrir("y09_baixar").crop((430, 50, 795, 440))
destaque(img, (14, 79, 348, 113)); marcador(img, 1, 348, 83)
destaque(img, (14, 128, 180, 148)); marcador(img, 2, 192, 138)
destaque(img, (14, 340, 348, 374)); marcador(img, 3, 348, 344)
salvar(img, "baixar_miniatura")
print("ok")
