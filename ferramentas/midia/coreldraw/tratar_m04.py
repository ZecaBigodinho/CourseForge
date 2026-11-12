"""Tratamento das capturas do Módulo 04 do CorelDRAW (peças comerciais).
Capturas feitas com servidor_corel.ps1 em 12/11/2026 (rodada E, prefixo g_), janela 1388x894.
Nenhuma imagem usada mostra pastas ou o nome de usuário do professor.
Uso: python tratar_m04.py <pasta_capturas> <pasta_saida_png>"""
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


# ---------- Aula 01: catálogo de várias páginas ----------
img = abrir("g_01_inserir_numero_pagina", (170, 40, 900, 380))
destaque(img, (6, 128, 292, 151)); marcador(img, 1, 26, 118)
destaque(img, (294, 159, 524, 183)); marcador(img, 2, 540, 171)
salvar(img, "01_inserir_numero_de_pagina")

img = abrir("g_03_config_numero")
salvar(img, "01_configuracoes_numero")

img = abrir("g_02_catalogo_varias_paginas", (100, 340, 900, 840))
marcador(img, 1, 30, 43)            # cabeçalho, vindo da página principal
marcador(img, 2, 136, 236)          # número da página
destaque(img, (126, 468, 542, 494)); marcador(img, 3, 558, 481)
salvar(img, "01_catalogo_quatro_paginas")

img = abrir("g_04_pagina_principal", (980, 130, 1336, 860))
destaque(img, (8, 463, 344, 488)); marcador(img, 1, 330, 452)
destaque(img, (8, 540, 344, 566)); marcador(img, 2, 330, 528)
destaque(img, (20, 645, 210, 670)); marcador(img, 3, 226, 657)
salvar(img, "01_pagina_principal")

# ---------- Aula 02: impressão mesclada ----------
img = abrir("g_05_menu_impressao_mesclada", (0, 40, 560, 620))
destaque(img, (6, 480, 248, 502)); marcador(img, 1, 22, 470)
destaque(img, (252, 482, 542, 505)); marcador(img, 2, 556, 493)
destaque(img, (252, 549, 542, 571)); marcador(img, 3, 556, 560)
salvar(img, "02_menu_impressao_mesclada")

img = abrir("g_07_depois_importar")
destaque(img, (342, 66, 525, 95)); marcador(img, 1, 328, 80)
destaque(img, (10, 156, 690, 280)); marcador(img, 2, 670, 300)
destaque(img, (522, 571, 610, 600)); marcador(img, 3, 506, 585)
salvar(img, "02_fonte_de_dados")

img = abrir("g_09_janela_mesclagem")
destaque(img, (144, 92, 214, 116)); marcador(img, 1, 230, 104)
destaque(img, (10, 146, 288, 177)); marcador(img, 2, 22, 134)
destaque(img, (8, 185, 294, 213))
marcador(img, 3, 280, 186)
destaque(img, (8, 276, 294, 305)); marcador(img, 4, 280, 268)
salvar(img, "02_janela_impressao_mesclada")

img = abrir("g_10_campos_no_cracha", (140, 250, 880, 720))
salvar(img, "02_campos_no_cracha")

img = abrir("g_11_documento_mesclado", (100, 410, 900, 540))
salvar(img, "02_documento_mesclado")

# ---------- Aula 03: post para redes sociais ----------
img = abrir("g_12_novo_post_rgb_px")
destaque(img, (718, 274, 772, 297)); marcador(img, 1, 786, 285)
destaque(img, (650, 346, 844, 405)); marcador(img, 2, 860, 360)
destaque(img, (650, 442, 736, 469)); marcador(img, 3, 752, 455)
salvar(img, "03_novo_documento_post")

post = Image.open(CAP / "g_post_padaria.jpg").convert("RGB")
post.thumbnail((640, 640))
salvar(post, "03_post_pronto")

img = abrir("g_15_exportar_para_jpeg")
destaque(img, (802, 52, 1084, 80)); marcador(img, 1, 788, 66)
destaque(img, (900, 136, 1098, 164)); marcador(img, 2, 886, 150)
destaque(img, (810, 268, 1070, 296)); marcador(img, 3, 796, 282)
destaque(img, (810, 448, 1070, 476)); marcador(img, 4, 796, 462)
salvar(img, "03_exportar_para_jpeg")

# ---------- Aula 04: faixa em lona e QR code ----------
img = abrir("g_21_faixa_3x1", (0, 85, 980, 640))
destaque(img, (180, 2, 298, 38)); marcador(img, 1, 314, 20)
salvar(img, "04_faixa_tamanho_real")

img = abrir("g_23_ilhos_marcado")
destaque(img, (518, 260, 624, 282)); marcador(img, 1, 640, 271)
destaque(img, (518, 310, 718, 366)); marcador(img, 2, 734, 338)
destaque(img, (558, 410, 718, 437)); marcador(img, 3, 542, 423)
destaque(img, (518, 440, 718, 548)); marcador(img, 4, 734, 494)
salvar(img, "04_borda_e_ilho")

img = abrir("g_25_ilhos_canto", (60, 300, 520, 560))
marcador(img, 1, 100, 60)
salvar(img, "04_ilho_no_canto")

img = abrir("g_16_menu_inserir_qr", (230, 40, 900, 330))
destaque(img, (6, 34, 308, 56))
marcador(img, 1, 294, 24)
destaque(img, (316, 36, 528, 60)); marcador(img, 2, 544, 48)
salvar(img, "04_menu_inserir_qr")

img = abrir("g_19_qr_url", (380, 130, 1336, 560))
destaque(img, (100, 270, 220, 380)); marcador(img, 1, 84, 270)
destaque(img, (604, 88, 950, 112)); marcador(img, 2, 590, 78)
destaque(img, (604, 120, 950, 146)); marcador(img, 3, 590, 132)
destaque(img, (726, 352, 830, 378)); marcador(img, 4, 846, 365)
salvar(img, "04_propriedades_qr")

img = abrir("g_20_qr_validar")
salvar(img, "04_validar_qr")
print("ok")
