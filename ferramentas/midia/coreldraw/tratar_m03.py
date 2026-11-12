"""Tratamento das capturas do Módulo 03 do CorelDRAW (arquivos para gráfica) e de uma imagem nova do M02.
Capturas feitas com servidor_corel.ps1 em 12/11/2026 (janela 1388x894, sem a borda invisível):
c_* = rodada C (cor, sangria, PDF, PowerClip), d_* = rodada D (adesivo, panfleto, kit), e_* = conferências do M02.
Nenhuma imagem usada aqui mostra pastas ou o nome de usuário do professor (c_13 mostrava e foi apagada;
c_15 mostra o caminho com o usuário e NÃO é usada).
Uso: python tratar_m03.py <pasta_capturas> <pasta_saida_png>"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

CAP = Path(sys.argv[1]); OUT = Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
ROXO = (79, 53, 181)
FONTE = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 18)
FONTE_TITULO = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 22)


def abrir(nome, recorte=None):
    img = Image.open(CAP / f"{nome}.png").convert("RGB")
    return img.crop(recorte) if recorte else img


def destaque(img, caixa):
    ImageDraw.Draw(img).rounded_rectangle(caixa, radius=8, outline=ROXO, width=4)


def marcador(img, n, x, y):
    d = ImageDraw.Draw(img); r = 14
    d.ellipse((x - r, y - r, x + r, y + r), fill=ROXO, outline=(255, 255, 255), width=3)
    d.text((x, y), str(n), fill=(255, 255, 255), font=FONTE, anchor="mm")


def lado_a_lado(esquerda, direita, titulos, margem=24):
    """Duas imagens lado a lado, cada uma com um título em cima."""
    alt = max(esquerda.height, direita.height) + 50
    tela = Image.new("RGB", (esquerda.width + direita.width + margem * 3, alt + margem), (255, 255, 255))
    d = ImageDraw.Draw(tela)
    for i, (img, titulo) in enumerate(zip((esquerda, direita), titulos)):
        x = margem + i * (esquerda.width + margem)
        d.text((x, 14), titulo, fill=ROXO, font=FONTE_TITULO)
        tela.paste(img, (x, 50))
    return tela


def salvar(img, nome):
    img.save(OUT / f"{nome}.png")


# ---------- Aula 01: cores para impressão ----------
img = abrir("c_08_novo_doc_cores2")
destaque(img, (510, 243, 772, 268)); marcador(img, 1, 498, 255)
destaque(img, (510, 566, 888, 592)); marcador(img, 2, 498, 579)
salvar(img, "01_novo_documento_cmyk")

img = abrir("c_22_menu_powerclip", (760, 860, 1388, 894))
destaque(img, (292, 2, 488, 32)); marcador(img, 1, 276, 17)
salvar(img, "01_foto_rgb")

img = abrir("c_25_janela_cor")
destaque(img, (340, 120, 632, 172)); marcador(img, 1, 650, 146)
destaque(img, (464, 250, 534, 378)); marcador(img, 2, 548, 264)
destaque(img, (356, 250, 432, 378)); marcador(img, 3, 342, 264)
salvar(img, "01_editar_preenchimento")

img = abrir("c_26_menu_exibir", (120, 40, 422, 606))
destaque(img, (6, 250, 300, 274)); marcador(img, 1, 284, 262)
salvar(img, "01_cores_de_prova")

# ---------- Aula 02: sangria e marcas de corte ----------
img = abrir("c_01_menu_layout", (170, 45, 470, 370))
destaque(img, (6, 226, 292, 248)); marcador(img, 1, 276, 237)
salvar(img, "02_menu_layout")

img = abrir("c_04_sangramento_3mm")
destaque(img, (204, 466, 484, 522)); marcador(img, 1, 500, 482)
salvar(img, "02_sangramento")

img = abrir("c_11_canto_transparente", (270, 400, 720, 690))
marcador(img, 1, 112, 150)      # canto da página (onde a gráfica corta)
marcador(img, 2, 60, 236)       # linha tracejada: limite do sangramento
salvar(img, "02_canto_da_pagina")

img = abrir("c_14_predefinicoes_pdf", (0, 380, 946, 662))
destaque(img, (148, 128, 320, 146)); marcador(img, 1, 336, 137)
destaque(img, (148, 186, 320, 228)); marcador(img, 2, 336, 207)
destaque(img, (632, 152, 730, 180)); marcador(img, 3, 746, 166)
salvar(img, "02_publicar_em_pdf")

img = abrir("c_19_preimpressao_marcas")
destaque(img, (300, 36, 404, 62)); marcador(img, 1, 300, 36)
destaque(img, (22, 80, 272, 104)); marcador(img, 2, 288, 92)
destaque(img, (30, 150, 140, 170)); marcador(img, 3, 156, 160)
salvar(img, "02_preimpressao")

pdf = Image.open(CAP / "d_16_pdf_pagina1.png").convert("RGB")      # PDF com marcas (página 1)
pdf.thumbnail((620, 900))
salvar(pdf, "02_pdf_com_marcas")

# ---------- Aula 03: PowerClip ----------
img = abrir("c_22_menu_powerclip", (300, 280, 760, 894))
destaque(img, (112, 375, 432, 397)); marcador(img, 1, 96, 386)
salvar(img, "03_menu_powerclip")

img = abrir("c_24_ajustar_conteudo", (40, 175, 720, 600))
destaque(img, (16, 6, 92, 36)); marcador(img, 1, 108, 8)
destaque(img, (210, 32, 456, 128)); marcador(img, 2, 472, 70)
destaque(img, (394, 230, 544, 385)); marcador(img, 3, 560, 240)
salvar(img, "03_powerclip_pronto")

img = abrir("d_07_panfleto_frente", (300, 215, 712, 755))
salvar(img, "03_panfleto_frente")

# ---------- Aula 04: adesivo com linha de corte ----------
img = abrir("d_01_menu_efeitos", (290, 45, 500, 620))
destaque(img, (6, 439, 204, 461)); marcador(img, 1, 188, 450)
salvar(img, "04_menu_efeitos")

img = abrir("d_03_contorno_config", (978, 130, 1336, 800))
destaque(img, (66, 52, 98, 80)); marcador(img, 1, 114, 66)
destaque(img, (60, 96, 284, 156)); marcador(img, 2, 46, 126)
destaque(img, (6, 638, 352, 664)); marcador(img, 3, 20, 625)
salvar(img, "04_painel_contorno")

img = abrir("d_04_contorno_aplicado", (250, 230, 770, 740))
salvar(img, "04_contorno_aplicado")

img = abrir("d_06_painel_objetos", (250, 130, 1336, 740))
marcador(img, 1, 56, 340)                       # a linha de corte magenta
destaque(img, (738, 140, 1080, 192)); marcador(img, 2, 722, 166)
salvar(img, "04_linha_de_corte_e_camadas")

# ---------- Aula 05: kit para a gráfica ----------
img = abrir("d_09_varias_paginas", (40, 170, 980, 835))
destaque(img, (96, 74, 172, 94)); marcador(img, 1, 80, 84)
destaque(img, (496, 74, 572, 94)); marcador(img, 2, 590, 84)
destaque(img, (186, 640, 392, 664)); marcador(img, 3, 408, 652)
salvar(img, "05_frente_e_verso")

img = abrir("d_10_publicar_pdfx4")
destaque(img, (148, 482, 290, 508)); marcador(img, 1, 132, 495)
destaque(img, (146, 510, 292, 574)); marcador(img, 2, 308, 542)
destaque(img, (632, 588, 730, 616)); marcador(img, 3, 746, 602)
salvar(img, "05_publicar_pdfx4")

img = abrir("d_11_questoes_pdfx4")
destaque(img, (490, 36, 590, 64)); marcador(img, 1, 606, 50)
destaque(img, (24, 110, 640, 148)); marcador(img, 2, 22, 160)
salvar(img, "05_questoes")

como_vem = abrir("d_13_preimpressao_pdfx4", (0, 60, 663, 205))
como_fica = abrir("d_15_pdfx4_sangria_marcas", (0, 60, 663, 205))
salvar(lado_a_lado(como_vem, como_fica, ("Como o PDF/X-4 vem", "Como deve ficar")), "05_pdfx4_preimpressao")

img = abrir("d_14_cor_pdfx4")
destaque(img, (216, 142, 302, 170)); marcador(img, 1, 318, 156)
destaque(img, (214, 206, 420, 232)); marcador(img, 2, 436, 219)
salvar(img, "05_pdfx4_cor")

img = abrir("d_17_propriedades_autor", (0, 0, 381, 330))
destaque(img, (118, 64, 374, 92)); marcador(img, 1, 100, 78)
destaque(img, (118, 129, 374, 157)); marcador(img, 2, 100, 143)
salvar(img, "05_propriedades_do_documento")

p1 = Image.open(CAP / "d_16_pdf_pagina1.png").convert("RGB"); p1.thumbnail((520, 760))
p2 = Image.open(CAP / "d_16_pdf_pagina2.png").convert("RGB"); p2.thumbnail((520, 760))
salvar(lado_a_lado(p1, p2, ("Página 1 — Frente", "Página 2 — Verso")), "05_pdf_final")

# ---------- M02, aula 04: moldura do parágrafo que não cabe ----------
img = abrir("e_01_paragrafo_nao_cabe", (110, 330, 830, 560))
destaque(img, (14, 18, 696, 208)); marcador(img, 1, 14, 18)
salvar(img, "m02_04_paragrafo_nao_cabe")
print("ok")
