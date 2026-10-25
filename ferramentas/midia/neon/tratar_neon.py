"""Tratamento das capturas da aula 09 (Neon): cobre nome, servidor e ids; destaca e numera em roxo."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

CAP = Path(sys.argv[1]); OUT = Path(sys.argv[2]); OUT.mkdir(exist_ok=True)
ROXO = (79, 53, 181)
FONTE = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 22)
MONO = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 15)


def abrir(nome):
    return Image.open(CAP / f"{nome}.png").convert("RGB")


def cobrir(img, caixa, texto=None, fonte=None, cor_texto=(90, 90, 90)):
    """Pinta a caixa com a cor do fundo ao redor e, se pedido, escreve um texto no lugar."""
    x0, y0, x1, y1 = caixa
    fundo = img.getpixel((max(x0 - 3, 0), (y0 + y1) // 2))
    d = ImageDraw.Draw(img); d.rectangle(caixa, fill=fundo)
    if texto:
        d.text((x0, (y0 + y1) // 2), texto, fill=cor_texto, font=fonte or MONO, anchor="lm")


def destaque(img, caixa):
    ImageDraw.Draw(img).rounded_rectangle(caixa, radius=6, outline=ROXO, width=4)


def marcador(img, n, x, y):
    d = ImageDraw.Draw(img); r = 16
    d.ellipse((x - r, y - r, x + r, y + r), fill=ROXO, outline=(255, 255, 255), width=3)
    d.text((x, y), str(n), fill=(255, 255, 255), font=FONTE, anchor="mm")


def lado_a_lado(partes, espaco=24, fundo="white"):
    w = sum(p.width for p in partes) + espaco * (len(partes) - 1); h = max(p.height for p in partes)
    fig = Image.new("RGB", (w, h), fundo); x = 0
    for p in partes:
        fig.paste(p, (x, (h - p.height) // 2)); x += p.width + espaco
    return fig


# ---------- CONSOLE DO NEON ----------
# 1. Create project: nome, região São Paulo e o que o plano gratuito inclui
img = abrir("n2_formulario")
destaque(img, (46, 180, 507, 216)); marcador(img, 1, 528, 198)
destaque(img, (46, 252, 507, 288)); marcador(img, 2, 528, 270)
destaque(img, (898, 381, 1209, 578)); marcador(img, 3, 1228, 400)
destaque(img, (1136, 728, 1261, 764)); marcador(img, 4, 1198, 712)
img.crop((24, 68, 1284, 786)).save(OUT / "09_neon_criar_projeto.png")

# 2. Painel do projeto: Connect, Tables, SQL Editor, Roles
img = abrir("n3_painel")
cobrir(img, (1178, 12, 1262, 44))            # nome no topo
cobrir(img, (1120, 306, 1200, 328))          # "Created by"
cobrir(img, (1122, 228, 1250, 248))          # id do branch
cobrir(img, (1122, 418, 1250, 438))          # id do projeto
destaque(img, (13, 123, 205, 159)); marcador(img, 1, 222, 141)
destaque(img, (29, 388, 205, 416)); marcador(img, 2, 222, 402)
destaque(img, (29, 420, 205, 448)); marcador(img, 3, 222, 434)
destaque(img, (29, 548, 205, 576)); marcador(img, 4, 222, 562)
img.crop((0, 0, 1300, 660)).save(OUT / "09_neon_painel.png")

# 3. Connect to your branch: senha mascarada, servidor coberto, Copy snippet, Reset password
img = abrir("n4_connect_BRUTO")
cobrir(img, (636, 504, 962, 524), "@ep-xxxxx-pooler.c-2.sa-east-1", cor_texto=(150, 150, 150))
destaque(img, (318, 498, 975, 542)); marcador(img, 1, 300, 520)
destaque(img, (323, 684, 430, 710)); marcador(img, 2, 344, 734)
destaque(img, (440, 684, 562, 710)); marcador(img, 3, 500, 734)
destaque(img, (884, 384, 993, 404)); marcador(img, 4, 1012, 394)
destaque(img, (660, 458, 842, 488)); marcador(img, 5, 862, 473)
img.crop((280, 96, 1040, 760)).save(OUT / "09_neon_connect.png")

# 4. SQL Editor: SELECT com o aluno cadastrado pelo app
img = abrir("n5_sql_select")
destaque(img, (500, 132, 770, 154)); marcador(img, 1, 790, 143)
destaque(img, (493, 372, 575, 405)); marcador(img, 2, 600, 388)
destaque(img, (474, 670, 1288, 706)); marcador(img, 3, 1268, 650)
img.crop((470, 56, 1300, 720)).save(OUT / "09_neon_sql_select.png")

# 5. SQL Editor: INSERT da Bruna
img = abrir("n6_sql_insert")
destaque(img, (500, 132, 1104, 154)); marcador(img, 1, 1124, 143)
destaque(img, (482, 430, 700, 454)); marcador(img, 2, 720, 442)
img.crop((470, 56, 1300, 480)).save(OUT / "09_neon_sql_insert.png")

# 6. Tables: a tabela alunos e o salto do id 5 para o 7
img = abrir("n7_tables")
destaque(img, (232, 338, 477, 370)); marcador(img, 1, 250, 395)
destaque(img, (521, 273, 721, 337)); marcador(img, 2, 690, 305)
img.crop((222, 56, 1300, 420)).save(OUT / "09_neon_tables.png")

# ---------- O SISTEMA ESCOLAR (TKINTER) ----------
# 7. Cadastro online, com os alunos migrados
img = abrir("t3_cadastro_online")
destaque(img, (20, 306, 168, 330)); marcador(img, 1, 190, 318)
destaque(img, (641, 304, 762, 331)); marcador(img, 2, 620, 318)
destaque(img, (38, 395, 728, 497)); marcador(img, 3, 748, 446)
img.save(OUT / "09_app_online.png")

# 8. Depois do Recarregar: a Bruna, inserida pelo SQL Editor
img = abrir("t9_depois_recarregar")
destaque(img, (641, 304, 762, 331)); marcador(img, 1, 620, 318)
destaque(img, (38, 415, 728, 437)); marcador(img, 2, 748, 426)
destaque(img, (28, 334, 216, 356))
img.save(OUT / "09_app_recarregar.png")

# 9. Sem conexão ao salvar: a mensagem e o cadastro com o 🔴 e os campos preenchidos
msg = abrir("u2_msg_sem_conexao")
cad = abrir("u3_offline")
destaque(cad, (20, 306, 172, 330)); marcador(cad, 2, 194, 318)
destaque(cad, (94, 86, 746, 146)); marcador(cad, 3, 766, 116)
fig = lado_a_lado([cad, msg])
marcador(fig, 1, cad.width + 24 + 158, (fig.height - msg.height) // 2 - 20)
fig.save(OUT / "09_app_sem_conexao.png")

# 10. Abrindo o sistema sem conexão (main.py)
abrir("u4_abertura_sem_conexao").save(OUT / "09_app_abertura_sem_conexao.png")
print("ok")
