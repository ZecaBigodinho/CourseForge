"""Exemplo de tratamento das capturas (aula 03 do Word), no estilo aprovado pelo professor:
destaques e marcadores roxos (#4F35B5), recorte das bordas invisíveis das janelas (8 px) e
emenda de capturas. Uso: python tratar_exemplo.py <pasta_capturas> <pasta_saida>; depois converta
cada PNG com ferramentas/midia/preparar_imagem.py. Nas capturas da janela inteira, cubra a foto de
perfil e o aviso da barra de título: retângulo (1180, 6, 1255, 44) pintado com a cor de (1100, 12)."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

CAP = Path(sys.argv[1]); OUT = Path(sys.argv[2]); OUT.mkdir(exist_ok=True)
ROXO = (79, 53, 181)
FONTE = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 22)


def abrir(nome):
    return Image.open(CAP / f"{nome}.png").convert("RGB")


def destaque(img, caixa):
    ImageDraw.Draw(img).rounded_rectangle(caixa, radius=6, outline=ROXO, width=4)


def marcador(img, n, x, y):
    d = ImageDraw.Draw(img); r = 16
    d.ellipse((x - r, y - r, x + r, y + r), fill=ROXO, outline=(255, 255, 255), width=3)
    d.text((x, y), str(n), fill=(255, 255, 255), font=FONTE, anchor="mm")


def sem_borda(img):
    w, h = img.size
    return img.crop((8, 0, w - 8, h - 8))


# 1. Menu Referências > Sumário, com Personalizar Sumário em destaque
img = abrir("01_menu_sumario")
destaque(img, (20, 83, 71, 159)); destaque(img, (32, 631, 422, 658))
img.crop((0, 50, 440, 722)).save(OUT / "03_menu_sumario.png")

# 2. Janela Sumário com Mostrar níveis: 2
img = sem_borda(abrir("02_dialogo_sumario"))
destaque(img, (22, 338, 196, 364))
img.save(OUT / "03_janela_sumario.png")

# 3. Sumário desalinhado (erro comum) — só o trecho da página
abrir("03_sumario_desalinhado").crop((560, 280, 1180, 620)).save(OUT / "03_sumario_desalinhado.png")

# 4. Sumário certo + botão Atualizar Sumário
img = abrir("04_sumario_certo")
destaque(img, (74, 110, 194, 133)); marcador(img, 1, 134, 152)
destaque(img, (578, 286, 1154, 452)); marcador(img, 2, 1172, 300)
img.crop((0, 50, 1270, 480)).save(OUT / "03_sumario_atualizar.png")

# 5. Janela Legenda: posição Acima do item selecionado
img = sem_borda(abrir("05_inserir_legenda"))
destaque(img, (6, 120, 298, 145))
img.save(OUT / "03_inserir_legenda.png")

# 6. Figura com legenda acima e fonte abaixo (duas capturas emendadas)
topo = abrir("b8_figura_100").crop((560, 578, 1180, 830))
baixo = abrir("b9_nota_100").crop((560, 330, 1180, 402))
fig = Image.new("RGB", (620, topo.height + baixo.height), "white")
fig.paste(topo, (0, 0)); fig.paste(baixo, (0, topo.height))
fig.save(OUT / "03_figura_legenda_fonte.png")

# 7. Nota de rodapé no fim da página
abrir("b9_nota_100").crop((560, 510, 1180, 780)).save(OUT / "03_nota_de_rodape.png")
print("ok")
