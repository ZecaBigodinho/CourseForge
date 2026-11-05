"""Tratamento das capturas da aula 01 do Canva (Módulo 01): destaques e marcadores roxos (#4F35B5),
cobre o avatar da conta e embaça os designs pessoais de "Continue criando".

Captura: viewport do navegador do app (977x854, escala 100%), pela região da tela com
CopyFromScreen — o painel entrega capturas reduzidas. Ver ferramentas/midia/README.md.
Uso: python tratar_aula01.py <pasta_capturas> <pasta_saida>; depois converta cada PNG com
ferramentas/midia/preparar_imagem.py."""
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


def cobrir(img, caixa, amostra):
    """Pinta a caixa com a cor de um ponto vizinho (avatar, nomes)."""
    ImageDraw.Draw(img).rectangle(caixa, fill=img.getpixel(amostra))


def embacar(img, caixa, raio=14):
    img.paste(img.crop(caixa).filter(ImageFilter.GaussianBlur(raio)), caixa[:2])


# 1. Tela inicial: áreas principais
img = abrir("01_tela_inicial").crop((0, 0, 977, 680))
embacar(img, (90, 480, 945, 680))          # designs pessoais em "Continue criando"
destaque(img, (8, 64, 68, 124)); marcador(img, 1, 72, 70)
destaque(img, (6, 214, 70, 662)); marcador(img, 2, 74, 220)
destaque(img, (137, 194, 891, 262)); marcador(img, 3, 137, 194)
destaque(img, (100, 298, 940, 408)); marcador(img, 4, 100, 298)
destaque(img, (90, 432, 945, 676)); marcador(img, 5, 90, 432)
destaque(img, (666, 22, 933, 68)); marcador(img, 6, 666, 22)
img.save(OUT / "01_tela_inicial.png")

# 2. Janela Criar um design
img = abrir("02_criar_um_design")
cobrir(img, (14, 796, 62, 846), (8, 760))  # avatar esmaecido ao fundo
destaque(img, (383, 64, 892, 109)); marcador(img, 1, 383, 64)
destaque(img, (86, 128, 357, 744)); marcador(img, 2, 86, 128)
destaque(img, (88, 660, 357, 700)); marcador(img, 3, 357, 680)
destaque(img, (380, 552, 900, 766)); marcador(img, 4, 380, 552)
img.save(OUT / "01_criar_um_design.png")

# 3. Busca de modelos: filtros e a coroa dos modelos Pro
img = abrir("03_busca_modelos").crop((0, 0, 977, 650))
destaque(img, (137, 194, 891, 262)); marcador(img, 1, 137, 194)
destaque(img, (350, 268, 678, 316)); marcador(img, 2, 350, 268)
destaque(img, (250, 600, 292, 634)); marcador(img, 3, 236, 600)
destaque(img, (680, 600, 718, 634)); marcador(img, 3, 666, 600)
img.save(OUT / "01_busca_modelos.png")
print("ok")
