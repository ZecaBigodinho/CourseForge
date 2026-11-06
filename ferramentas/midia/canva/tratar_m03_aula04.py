"""Tratamento das capturas da aula 04 do Módulo 03 do Canva (vídeo curto / Reels).
Capturas do próprio painel do navegador (800x744, JPG).
Uso: python tratar_m03_aula04.py <pasta_capturas> <pasta_saida>"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

CAP = Path(sys.argv[1]); OUT = Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
ROXO = (79, 53, 181)
FONTE = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 18)


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
    img.save(OUT / f"04_{nome}.png")


img = abrir("v_01_busca").crop((60, 0, 800, 744))
destaque(img, (58, 170, 666, 228)); marcador(img, 1, 58, 170)
destaque(img, (299, 512, 346, 534)); marcador(img, 2, 358, 523)
destaque(img, (23, 546, 148, 744)); marcador(img, 3, 148, 550)
salvar(img, "busca_reels")

img = abrir("v_02_previa").crop((48, 14, 760, 500))
embacar(img, (324, 142, 572, 176))
destaque(img, (326, 96, 530, 116)); marcador(img, 1, 542, 106)
destaque(img, (40, 440, 74, 470)); marcador(img, 2, 86, 455)
destaque(img, (326, 192, 580, 230)); marcador(img, 3, 326, 192)
salvar(img, "previa_reels")

img = abrir("v_03_editor_video")
embacar(img, (434, 10, 466, 40), 5)
destaque(img, (352, 98, 511, 378)); marcador(img, 1, 511, 102)
destaque(img, (376, 390, 488, 428)); marcador(img, 2, 500, 409)
destaque(img, (76, 444, 778, 450)); marcador(img, 3, 76, 444)
destaque(img, (77, 460, 330, 618)); marcador(img, 4, 330, 464)
destaque(img, (77, 621, 330, 678)); marcador(img, 5, 330, 625)
destaque(img, (77, 682, 330, 704)); marcador(img, 6, 342, 693)
salvar(img, "editor_video")

img = abrir("v_04_clipe")
destaque(img, (276, 60, 342, 88)); marcador(img, 1, 309, 100)
destaque(img, (512, 60, 590, 88)); marcador(img, 2, 602, 74)
destaque(img, (77, 662, 330, 710)); marcador(img, 3, 330, 666)
salvar(img, "clipe_video")

img = abrir("v_05_audios")
destaque(img, (77, 186, 349, 262)); marcador(img, 1, 349, 190)
destaque(img, (77, 270, 349, 346)); marcador(img, 2, 349, 274)
destaque(img, (77, 392, 349, 450)); marcador(img, 3, 349, 396)
destaque(img, (314, 668, 342, 684)); marcador(img, 4, 302, 676)
salvar(img, "audios")

img = abrir("v_06_audio_no_meio").crop((388, 430, 800, 744))
destaque(img, (72, 10, 82, 300)); marcador(img, 1, 77, 22)
destaque(img, (74, 252, 254, 276)); marcador(img, 2, 266, 264)
salvar(img, "audio_no_meio")

img = abrir("v_07_efeito_gradual")
destaque(img, (533, 60, 628, 88)); marcador(img, 1, 533, 60)
destaque(img, (430, 178, 730, 232)); marcador(img, 2, 730, 182)
destaque(img, (392, 682, 642, 708)); marcador(img, 3, 654, 695)
salvar(img, "efeito_gradual")

img = abrir("v_08_baixar_mp4").crop((430, 50, 795, 335))
destaque(img, (14, 79, 348, 113)); marcador(img, 1, 348, 83)
destaque(img, (14, 148, 348, 182)); marcador(img, 2, 348, 152)
destaque(img, (14, 236, 348, 270)); marcador(img, 3, 348, 240)
salvar(img, "baixar_mp4")

abrir("v_04_clipe").crop((352, 98, 511, 380)).save(OUT / "04_video_pronto.png")
print("ok")
