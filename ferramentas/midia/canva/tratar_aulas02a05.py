"""Tratamento das capturas das aulas 02 a 05 do Canva (Módulo 01). Mesmo estilo de
tratar_aula01.py: destaques e marcadores roxos (#4F35B5), avatar e nome da conta cobertos,
designs pessoais e "Usados recentemente" embaçados.

Captura: python cap.py <nome> — ImageGrab da região do navegador do app (977x854), sem abrir
janela (uma janela do PowerShell rouba o foco e fecha os menus do Canva).
Uso: python tratar_aulas02a05.py <pasta_capturas> <pasta_saida>"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

CAP = Path(sys.argv[1]); OUT = Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
ROXO = (79, 53, 181)
FONTE = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 20)
TEXTO = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 15)
TEXTO_P = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 13)

AVATAR_TOPO = (519, 10, 555, 46)        # foto de perfil na barra do editor
USADOS = (86, 170, 418, 264)            # "Usados recentemente" no painel Elementos


def abrir(nome):
    return Image.open(CAP / f"{nome}.png").convert("RGB")


def destaque(img, caixa):
    ImageDraw.Draw(img).rounded_rectangle(caixa, radius=8, outline=ROXO, width=4)


def marcador(img, n, x, y):
    d = ImageDraw.Draw(img); r = 15
    d.ellipse((x - r, y - r, x + r, y + r), fill=ROXO, outline=(255, 255, 255), width=3)
    d.text((x, y), str(n), fill=(255, 255, 255), font=FONTE, anchor="mm")


def embacar(img, caixa, raio=12):
    img.paste(img.crop(caixa).filter(ImageFilter.GaussianBlur(raio)), caixa[:2])


def cobrir(img, caixa, amostra):
    ImageDraw.Draw(img).rectangle(caixa, fill=img.getpixel(amostra))


def salvar(img, nome):
    img.save(OUT / f"{nome}.png")


# ---------- Aula 02 ----------
img = abrir("a02_busca_cartao").crop((0, 0, 977, 610))
cobrir(img, (14, 796, 62, 846), (8, 760)) if img.height > 846 else None
destaque(img, (137, 194, 889, 261)); marcador(img, 1, 137, 194)
destaque(img, (94, 358, 506, 594)); marcador(img, 2, 94, 358)
salvar(img, "02_busca_cartao")

img = abrir("a02_previa_modelo").crop((0, 0, 977, 500))
embacar(img, (488, 180, 760, 218), 8)                # foto e nome de quem criou o modelo
destaque(img, (486, 54, 830, 124)); marcador(img, 1, 486, 54)
destaque(img, (486, 126, 670, 152)); marcador(img, 2, 670, 139)
destaque(img, (486, 432, 782, 480)); marcador(img, 3, 486, 432)
salvar(img, "02_previa_modelo")

img = abrir("a02_tamanho_personalizado").crop((0, 0, 977, 820))
cobrir(img, (14, 796, 62, 820), (8, 760))
destaque(img, (87, 657, 355, 701)); marcador(img, 1, 87, 657)
destaque(img, (382, 120, 688, 196)); marcador(img, 2, 382, 120)
destaque(img, (696, 154, 726, 188)); marcador(img, 3, 711, 210)
destaque(img, (736, 147, 893, 195)); marcador(img, 4, 893, 147)
salvar(img, "02_tamanho_personalizado")

img = abrir("a02_redimensionar").crop((0, 0, 977, 400))
embacar(img, AVATAR_TOPO, 6)
destaque(img, (150, 4, 282, 52)); marcador(img, 1, 150, 8)
destaque(img, (156, 66, 548, 250)); marcador(img, 2, 548, 70)
destaque(img, (164, 276, 538, 322)); marcador(img, 3, 538, 280)
salvar(img, "02_redimensionar")

# ---------- Aula 03 ----------
img = abrir("a03_editor")
embacar(img, AVATAR_TOPO, 6)
destaque(img, (2, 2, 975, 56)); marcador(img, 1, 958, 64)
destaque(img, (2, 68, 72, 716)); marcador(img, 2, 76, 74)
destaque(img, (92, 162, 956, 660)); marcador(img, 3, 92, 162)
destaque(img, (400, 732, 646, 806)); marcador(img, 4, 400, 732)
destaque(img, (74, 812, 975, 852)); marcador(img, 5, 74, 812)
salvar(img, "03_editor")

img = abrir("a03_texto_selecionado").crop((0, 0, 977, 520))
embacar(img, AVATAR_TOPO, 6)
destaque(img, (98, 62, 951, 108)); marcador(img, 1, 98, 62)
destaque(img, (580, 300, 975, 348)); marcador(img, 2, 580, 352)
destaque(img, (638, 244, 928, 283)); marcador(img, 3, 638, 244)
salvar(img, "03_texto_selecionado")

img = abrir("a03_painel_elementos")
embacar(img, AVATAR_TOPO, 6); embacar(img, USADOS, 10)
destaque(img, (4, 212, 70, 278)); marcador(img, 1, 70, 214)
destaque(img, (86, 70, 418, 132)); marcador(img, 2, 418, 74)
destaque(img, (86, 412, 418, 852)); marcador(img, 3, 418, 416)
salvar(img, "03_painel_elementos")

# ---------- Aula 04 ----------
img = abrir("a04_menu_arquivo")
embacar(img, AVATAR_TOPO, 6)                         # o menu cobre "Usados recentemente"
embacar(img, (78, 104, 372, 146), 6)                 # "De <nome do professor>"
destaque(img, (330, 66, 366, 100)); marcador(img, 1, 384, 70)
destaque(img, (72, 376, 372, 424)); marcador(img, 2, 384, 380)
destaque(img, (72, 498, 372, 528)); marcador(img, 3, 384, 502)
destaque(img, (72, 600, 372, 630)); marcador(img, 4, 384, 604)
salvar(img, "04_menu_arquivo")

img = abrir("a04_projetos")
embacar(img, (566, 418, 977, 615), 14)               # designs pessoais em Recentes
embacar(img, (360, 760, 960, 854), 14)               # lista de designs
embacar(img, (104, 166, 130, 194), 5); embacar(img, (16, 798, 58, 840), 6)
destaque(img, (14, 280, 60, 338)); marcador(img, 1, 64, 284)
destaque(img, (86, 70, 324, 334)); marcador(img, 2, 324, 74)
destaque(img, (388, 140, 904, 206)); marcador(img, 3, 388, 140)
destaque(img, (888, 316, 930, 359)); marcador(img, 4, 888, 316)
destaque(img, (362, 640, 600, 760)); marcador(img, 5, 362, 640)
salvar(img, "04_projetos")

img = abrir("a04_botao_mais").crop((0, 0, 977, 700))
embacar(img, (560, 418, 612, 620), 10)
embacar(img, (104, 166, 130, 194), 5)
destaque(img, (888, 316, 932, 360)); marcador(img, 1, 870, 316)
destaque(img, (622, 416, 920, 450)); marcador(img, 2, 606, 433)
salvar(img, "04_botao_mais")

img = abrir("a04_nova_pasta").crop((240, 210, 790, 640))
d = ImageDraw.Draw(img)
d.rectangle((40, 262, 380, 318), fill=(255, 255, 255))   # nome e e-mail do professor
d.ellipse((50, 272, 90, 312), fill=(79, 53, 181)); d.text((70, 292), "A", fill="white", font=FONTE, anchor="mm")
d.text((102, 274), "Ana Souza", fill=(13, 18, 22), font=TEXTO)
d.text((102, 296), "ana.souza@example.com", fill=(90, 90, 90), font=TEXTO_P)
destaque(img, (38, 115, 462, 163)); marcador(img, 1, 38, 115)
destaque(img, (38, 341, 462, 389)); marcador(img, 2, 38, 341)
salvar(img, "04_nova_pasta")

img = abrir("a04_menu_design").crop((330, 280, 977, 854))
embacar(img, (225, 46, 420, 66), 5)                  # "De <nome do professor>"
destaque(img, (468, 18, 506, 52)); marcador(img, 1, 520, 22)
destaque(img, (216, 214, 512, 248)); marcador(img, 2, 528, 231)
destaque(img, (216, 344, 512, 378)); marcador(img, 3, 528, 361)
salvar(img, "04_menu_design")

img = abrir("a04_mover_pasta").crop((180, 110, 800, 745))
destaque(img, (236, 186, 360, 220)); marcador(img, 1, 370, 190)
destaque(img, (24, 562, 124, 600)); marcador(img, 2, 136, 566)
destaque(img, (506, 559, 594, 607)); marcador(img, 3, 494, 563)
salvar(img, "04_mover_pasta")

img = abrir("a04_pasta_aberta").crop((0, 0, 977, 600))
embacar(img, (104, 166, 130, 194), 5); embacar(img, (580, 66, 616, 102), 6)
destaque(img, (94, 202, 324, 246)); marcador(img, 1, 328, 206)
destaque(img, (364, 106, 660, 156)); marcador(img, 2, 664, 110)
destaque(img, (750, 62, 878, 106)); marcador(img, 3, 750, 62)
destaque(img, (364, 272, 642, 536)); marcador(img, 4, 364, 272)
salvar(img, "04_pasta_aberta")

# ---------- Aula 05 ----------
img = abrir("a05_cartao_final").crop((96, 164, 954, 658))
salvar(img, "05_cartao_final")

img = abrir("a05_compartilhar").crop((430, 0, 977, 710))
embacar(img, (89, 10, 125, 46), 6); embacar(img, (138, 196, 172, 230), 6)
destaque(img, (414, 4, 545, 52)); marcador(img, 1, 414, 62)
destaque(img, (136, 270, 528, 320)); marcador(img, 2, 136, 270)
destaque(img, (136, 334, 528, 380)); marcador(img, 3, 136, 334)
destaque(img, (150, 462, 228, 562)); marcador(img, 4, 150, 462)
destaque(img, (240, 576, 330, 676)); marcador(img, 5, 240, 576)
salvar(img, "05_compartilhar")

img = abrir("a05_formatos").crop((550, 50, 977, 690))
destaque(img, (18, 154, 406, 214)); marcador(img, 1, 18, 154)
destaque(img, (18, 270, 406, 328)); marcador(img, 2, 18, 270)
destaque(img, (18, 328, 406, 386)); marcador(img, 3, 406, 357)
salvar(img, "05_formatos")

img = abrir("a05_pdf_avancado").crop((550, 50, 977, 670))
destaque(img, (205, 184, 390, 220)); marcador(img, 1, 390, 188)
destaque(img, (18, 264, 392, 308)); marcador(img, 2, 392, 268)
destaque(img, (18, 374, 392, 408)); marcador(img, 3, 18, 374)
destaque(img, (18, 558, 406, 600)); marcador(img, 4, 18, 558)
salvar(img, "05_pdf_avancado")

img = abrir("a05_baixar").crop((550, 50, 977, 460))
destaque(img, (18, 152, 230, 178)); marcador(img, 1, 240, 165)
destaque(img, (18, 232, 106, 256)); marcador(img, 2, 116, 244)
destaque(img, (18, 312, 182, 340)); marcador(img, 3, 192, 326)
salvar(img, "05_baixar_png")
print("ok")
