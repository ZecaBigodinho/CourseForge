"""Tratamento das capturas da aula 04 do Módulo 02 do Canva (post e story de oferta).
Mesmo estilo de tratar_aula01.py. Capturas de 918x854. As faixas vermelhas no story marcam
as zonas que o Instagram cobre (nome do perfil em cima, caixa de resposta embaixo).
Uso: python tratar_m02_aula04.py <pasta_capturas> <pasta_saida>"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

CAP = Path(sys.argv[1]); OUT = Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
ROXO = (79, 53, 181)
FONTE = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 20)
FONTE_P = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 13)
AVATAR = (459, 9, 497, 47)


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


def zona_de_risco(img, caixa, texto):
    """Faixa vermelha semitransparente sobre a área que o Instagram cobre."""
    camada = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(camada)
    d.rectangle(caixa, fill=(220, 38, 38, 110), outline=(220, 38, 38, 255), width=2)
    x0, y0, x1, y1 = caixa
    d.text(((x0 + x1) // 2, (y0 + y1) // 2), texto, fill=(255, 255, 255, 255), font=FONTE_P, anchor="mm")
    img.paste(Image.alpha_composite(img.convert("RGBA"), camada).convert("RGB"))


def salvar(img, nome):
    img.save(OUT / f"04_{nome}.png")


img = abrir("s02_redes_sociais").crop((56, 40, 864, 812))
destaque(img, (33, 179, 296, 219)); marcador(img, 1, 33, 179)
destaque(img, (329, 203, 462, 348)); marcador(img, 2, 462, 207)
destaque(img, (478, 203, 611, 330)); marcador(img, 3, 611, 207)
destaque(img, (329, 91, 775, 131)); marcador(img, 4, 775, 95)
salvar(img, "redes_sociais")

img = abrir("s04_tipo_pagina")
embacar(img, AVATAR, 6)
destaque(img, (670, 760, 704, 797)); marcador(img, 1, 716, 778)
destaque(img, (548, 464, 827, 744)); marcador(img, 2, 548, 468)
destaque(img, (641, 570, 710, 690)); marcador(img, 3, 676, 700)
destaque(img, (722, 570, 792, 690)); marcador(img, 4, 757, 700)
salvar(img, "outro_tipo_de_pagina")

img = abrir("s05_pagina_post")
destaque(img, (259, 116, 492, 142)); marcador(img, 1, 259, 116)
destaque(img, (258, 145, 733, 738)); marcador(img, 2, 733, 149)
salvar(img, "pagina_post")

img = abrir("s06_colado_post")
destaque(img, (79, 316, 842, 538)); marcador(img, 1, 79, 316)
salvar(img, "aviso_copiar_colar")

img = abrir("s07_modelos_post")
destaque(img, (89, 73, 417, 187)); marcador(img, 1, 417, 77)
destaque(img, (250, 440, 402, 628)); marcador(img, 2, 402, 444)
destaque(img, (210, 408, 240, 430)); marcador(img, 3, 196, 418)
salvar(img, "modelos_post")

img = abrir("s08_modelo_aplicado")
embacar(img, (89, 212, 300, 238))
destaque(img, (89, 184, 300, 206)); marcador(img, 1, 312, 195)
destaque(img, (89, 288, 402, 408)); marcador(img, 2, 402, 292)
destaque(img, (538, 395, 818, 740)); marcador(img, 3, 818, 399)
salvar(img, "modelo_aplicado")

img = abrir("s09_preco_pequeno")
embacar(img, (89, 212, 300, 238))
destaque(img, (577, 67, 670, 103)); marcador(img, 1, 577, 67)
destaque(img, (604, 612, 750, 656)); marcador(img, 2, 762, 634)
salvar(img, "preco_pequeno")

img = abrir("s11_camadas")
destaque(img, (89, 113, 417, 153)); marcador(img, 1, 417, 117)
destaque(img, (89, 228, 417, 412)); marcador(img, 2, 417, 232)
salvar(img, "camadas")

img = abrir("s12_posicao_y")
destaque(img, (89, 466, 417, 642)); marcador(img, 1, 417, 470)
destaque(img, (202, 600, 306, 642)); marcador(img, 2, 318, 621)
destaque(img, (633, 572, 720, 605)); marcador(img, 3, 732, 588)
salvar(img, "posicao_y")

img = abrir("s16_story_antes").crop((434, 220, 918, 760))
zona_de_risco(img, (108, 36, 378, 98), "ÁREA DO PERFIL")
zona_de_risco(img, (108, 430, 378, 516), "CAIXA DE RESPOSTA")
destaque(img, (124, 454, 360, 506)); marcador(img, 1, 360, 458)
salvar(img, "story_antes")

img = abrir("s17_story_depois").crop((434, 220, 918, 760))
zona_de_risco(img, (108, 36, 378, 98), "ÁREA DO PERFIL")
zona_de_risco(img, (108, 430, 378, 516), "CAIXA DE RESPOSTA")
destaque(img, (124, 320, 360, 424)); marcador(img, 1, 360, 324)
salvar(img, "story_depois")

img = abrir("s18_grade").crop((0, 56, 918, 320))
destaque(img, (47, 70, 239, 240)); marcador(img, 1, 47, 70)
destaque(img, (259, 70, 451, 240)); marcador(img, 2, 259, 70)
destaque(img, (471, 70, 661, 240)); marcador(img, 3, 471, 70)
salvar(img, "grade_tres_formatos")

img = abrir("s20_selecao_paginas").crop((495, 56, 918, 690))
destaque(img, (16, 360, 400, 422)); marcador(img, 1, 400, 364)
destaque(img, (16, 428, 250, 470)); marcador(img, 2, 262, 449)
destaque(img, (147, 476, 400, 546)); marcador(img, 3, 400, 480)
destaque(img, (16, 572, 400, 612)); marcador(img, 4, 400, 576)
salvar(img, "baixar_selecao")

abrir("s17_story_depois").crop((542, 256, 812, 736)).save(OUT / "04_story_pronto.png")
# 04_post_pronto.png: recorte do print do navegador (a captura de tela do Windows falhou nessa hora)
print("ok")
