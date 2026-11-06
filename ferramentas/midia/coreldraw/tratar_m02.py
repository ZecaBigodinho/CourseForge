"""Tratamento das capturas do Módulo 02 do CorelDRAW (curvas, modelagem, PowerTRACE, texto, logotipo).
Capturas feitas com servidor_corel.ps1 (janela 1388x894, sem a borda invisível).
Uso: python tratar_m02.py <pasta_capturas> <pasta_saida>"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

CAP = Path(sys.argv[1]); OUT = Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
ROXO = (79, 53, 181)
FONTE = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 18)


def abrir(nome, recorte=None):
    img = Image.open(next(CAP.glob(f"{nome}.*"))).convert("RGB")
    return img.crop(recorte) if recorte else img


def destaque(img, caixa):
    ImageDraw.Draw(img).rounded_rectangle(caixa, radius=8, outline=ROXO, width=4)


def marcador(img, n, x, y):
    d = ImageDraw.Draw(img); r = 14
    d.ellipse((x - r, y - r, x + r, y + r), fill=ROXO, outline=(255, 255, 255), width=3)
    d.text((x, y), str(n), fill=(255, 255, 255), font=FONTE, anchor="mm")


def salvar(img, nome):
    img.save(OUT / f"{nome}.png")


# ---------- Aula 01: curvas ----------
img = abrir("a_13_menu_curvas", (0, 250, 420, 500))      # menu desdobrável da Mão livre
destaque(img, (36, 32, 270, 54)); marcador(img, 1, 282, 43)
destaque(img, (36, 76, 270, 98)); marcador(img, 2, 282, 87)
destaque(img, (36, 98, 270, 120)); marcador(img, 3, 282, 109)
salvar(img, "01_ferramentas_curva")

img = abrir("a_12_menu_forma", (0, 130, 420, 330))       # grupo da ferramenta Forma
destaque(img, (32, 34, 192, 60)); marcador(img, 1, 204, 47)
salvar(img, "01_ferramenta_forma")

img = abrir("a_14_menu_converter", (300, 200, 1000, 700))
destaque(img, (166, 150, 452, 174)); marcador(img, 1, 464, 162)
destaque(img, (166, 378, 452, 400)); marcador(img, 2, 464, 389)
salvar(img, "01_converter_em_curvas")

img = abrir("a_15_nos_curva")
destaque(img, (4, 132, 32, 192)); marcador(img, 1, 46, 178)
destaque(img, (120, 90, 650, 122)); marcador(img, 2, 662, 106)
destaque(img, (388, 436, 628, 510)); marcador(img, 3, 640, 446)
destaque(img, (1300, 864, 1386, 892)); marcador(img, 4, 1288, 878)
destaque(img, (984, 228, 1320, 548)); marcador(img, 5, 984, 238)
salvar(img, "01_nos_da_curva")

img = abrir("a_16_nos_retangulo_curvas", (300, 230, 720, 430))
salvar(img, "01_retangulo_em_curvas")

# ---------- Aula 02: soldar, aparar e interseção ----------
img = abrir("a_20_dois_selecionados")
destaque(img, (600, 90, 694, 122)); marcador(img, 1, 600, 90)
destaque(img, (694, 90, 820, 122)); marcador(img, 2, 832, 106)
salvar(img, "02_botoes_modelagem")

img = abrir("a_23_resultados", (330, 236, 686, 734))
salvar(img, "02_resultados")

# ---------- Aula 03: PowerTRACE ----------
img = abrir("b_01_bitmap_selecionado")
destaque(img, (554, 92, 668, 120)); marcador(img, 1, 554, 92)
destaque(img, (318, 296, 694, 670)); marcador(img, 2, 694, 300)
salvar(img, "03_bitmap_importado")

img = abrir("b_03_rastreio_contorno", (520, 90, 1220, 400))
destaque(img, (40, 30, 362, 52)); marcador(img, 1, 28, 41)
destaque(img, (40, 118, 362, 142)); marcador(img, 2, 28, 130)
destaque(img, (364, 144, 600, 168)); marcador(img, 3, 612, 156)
salvar(img, "03_menu_rastrear")

img = abrir("b_04_powertrace")
destaque(img, (28, 44, 236, 72)); marcador(img, 1, 248, 58)
destaque(img, (28, 76, 630, 614)); marcador(img, 2, 28, 88)
destaque(img, (652, 70, 994, 130)); marcador(img, 3, 1006, 100)
destaque(img, (650, 194, 856, 214)); marcador(img, 4, 868, 204)
destaque(img, (650, 294, 994, 452)); marcador(img, 5, 1006, 372)
destaque(img, (848, 654, 932, 682)); marcador(img, 6, 836, 668)
salvar(img, "03_powertrace")

img = abrir("b_05_bitmap_e_vetor", (350, 330, 680, 490))
salvar(img, "03_bitmap_e_vetor")

# ---------- Aula 04: texto artístico × parágrafo ----------
img = abrir("b_10_artistico_e_paragrafo")
destaque(img, (362, 270, 660, 310)); marcador(img, 1, 672, 290)
destaque(img, (360, 342, 656, 494)); marcador(img, 2, 668, 418)
salvar(img, "04_artistico_e_paragrafo")

img = abrir("b_11_menu_texto", (410, 30, 860, 575))
destaque(img, (8, 188, 278, 212)); marcador(img, 1, 290, 200)
destaque(img, (8, 22, 278, 66)); marcador(img, 2, 290, 44)
destaque(img, (8, 270, 278, 292)); marcador(img, 3, 290, 281)
destaque(img, (8, 496, 278, 518)); marcador(img, 4, 290, 507)
salvar(img, "04_menu_texto")

# ---------- Aula 05: projeto logotipo ----------
img = abrir("b_20_logotipo", (380, 290, 634, 540))
salvar(img, "05_logotipo_no_corel")

logo = Image.open(CAP / "saida" / "logo_pao_quente_vetor.png").convert("RGBA")
fundo = Image.new("RGBA", (logo.width + 160, logo.height + 160), (255, 255, 255, 255))
xadrez = ImageDraw.Draw(fundo)
for y in range(0, fundo.height, 40):                      # xadrez = área transparente
    for x in range(0, fundo.width, 40):
        if (x // 40 + y // 40) % 2:
            xadrez.rectangle((x, y, x + 39, y + 39), fill=(225, 225, 225, 255))
fundo.alpha_composite(logo, (80, 80))
fundo.convert("RGB").resize((700, 700)).save(OUT / "05_logotipo_png_transparente.png")

img = abrir("b_21_exportar_png_transparente")
destaque(img, (122, 388, 944, 441)); marcador(img, 1, 66, 414)
destaque(img, (122, 482, 262, 502)); marcador(img, 2, 274, 492)
destaque(img, (372, 482, 520, 516)); marcador(img, 3, 532, 492)
destaque(img, (738, 555, 830, 585)); marcador(img, 4, 738, 555)
salvar(img, "05_exportar_png")

img = abrir("b_22_opcoes_png_logo")
destaque(img, (804, 54, 1000, 80)); marcador(img, 1, 1012, 66)
destaque(img, (810, 166, 906, 190)); marcador(img, 2, 918, 178)
destaque(img, (806, 380, 984, 408)); marcador(img, 3, 996, 394)
destaque(img, (862, 489, 946, 517)); marcador(img, 4, 850, 503)
salvar(img, "05_opcoes_png")
print("ok")
