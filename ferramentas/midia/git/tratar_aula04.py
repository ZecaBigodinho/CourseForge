"""Tratamento das capturas da aula 04 de Git (repositório remoto e equipe), no estilo aprovado:
destaques e marcadores roxos (#4F35B5), fotos de perfil cobertas e o e-mail real trocado pelo de
exemplo. Uso: python tratar_aula04.py <pasta_capturas> <pasta_saida>; depois converta cada PNG com
ferramentas/midia/preparar_imagem.py. As capturas do site vêm do painel do navegador (970x853);
as do terminal, de terminal_git.ps1 (1100x640, uma linha a cada 16 px a partir de y=31)."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

CAP = Path(sys.argv[1]); OUT = Path(sys.argv[2]); OUT.mkdir(exist_ok=True)
ROXO = (79, 53, 181)
FONTE = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 22)
FONTE_CAMPO = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 15)


def abrir(nome):
    return Image.open(CAP / f"{nome}.png").convert("RGB")


def destaque(img, caixa):
    ImageDraw.Draw(img).rounded_rectangle(caixa, radius=6, outline=ROXO, width=4)


def marcador(img, n, x, y):
    d = ImageDraw.Draw(img); r = 16
    d.ellipse((x - r, y - r, x + r, y + r), fill=ROXO, outline=(255, 255, 255), width=3)
    d.text((x, y), str(n), fill=(255, 255, 255), font=FONTE, anchor="mm")


def sem_foto(img, caixa):
    """Cobre a foto de perfil com um círculo cinza neutro."""
    x0, y0, x1, y1 = caixa
    d = ImageDraw.Draw(img)
    d.rectangle(caixa, fill=img.getpixel((x0 - 3, y0 + 2)))
    d.ellipse(caixa, fill=(175, 184, 193))


def linhas(primeira, ultima):
    """Faixa vertical das linhas do terminal (contadas a partir de 0)."""
    return 31 + 16 * primeira, 31 + 16 * (ultima + 1)


MARGEM = 46  # faixa à esquerda do terminal, onde ficam os marcadores (o texto não é coberto)


def terminal(img, altura, blocos):
    """Tira as bordas invisíveis da janela, abre uma margem à esquerda e marca cada bloco de linhas
    com uma barra roxa e o número. blocos = [(primeira_linha, ultima_linha), ...], numerados em ordem."""
    w, _ = img.size
    corpo = img.crop((8, 0, w - 8, altura))
    fundo = corpo.getpixel((corpo.width // 2, corpo.height - 4))
    saida = Image.new("RGB", (corpo.width + MARGEM, corpo.height), fundo)
    saida.paste(corpo, (MARGEM, 0))
    ImageDraw.Draw(saida).rectangle((0, 0, MARGEM, 30), fill=corpo.getpixel((corpo.width // 2, 4)))
    d = ImageDraw.Draw(saida)
    for n, (primeira, ultima) in enumerate(blocos, 1):
        y0, y1 = linhas(primeira, ultima)
        d.rounded_rectangle((37, y0 + 2, 42, y1 - 2), radius=2, fill=(255, 255, 255))
        marcador(saida, n, 18, y0 + 14)
    return saida


# 1. Formulário de novo repositório
img = abrir("04_novo_repo")
sem_foto(img, (177, 248, 199, 270))
destaque(img, (356, 241, 848, 278)); marcador(img, 1, 870, 259)
destaque(img, (710, 497, 831, 535)); marcador(img, 2, 853, 516)
destaque(img, (163, 564, 847, 768)); marcador(img, 3, 870, 590)
img.crop((0, 70, 969, 780)).save(OUT / "04_novo_repositorio.png")

# 2. Quick setup: endereço HTTPS e os comandos para um repositório que já existe
img = abrir("04_quick_setup")
destaque(img, (260, 284, 931, 322)); marcador(img, 1, 931, 284)
destaque(img, (36, 600, 932, 722)); marcador(img, 2, 20, 612)
img.crop((0, 215, 969, 735)).save(OUT / "04_quick_setup.png")

# 3. remote add, remote -v e o primeiro push
terminal(abrir("04_primeiro_push"), 305, [(0, 1), (2, 4), (13, 15)]).save(OUT / "04_primeiro_push.png")

# 4. O repositório no GitHub depois do push
img = abrir("04_repo_depois_do_push")
sem_foto(img, (14, 110, 40, 136))
destaque(img, (226, 110, 286, 138)); marcador(img, 1, 306, 124)
destaque(img, (14, 230, 691, 285)); marcador(img, 2, 16, 232)
destaque(img, (14, 287, 691, 368)); marcador(img, 3, 16, 289)
img.crop((0, 95, 969, 675)).save(OUT / "04_repositorio_no_github.png")

# 5. Commit pelo site, com o e-mail de exemplo no lugar do real
img = abrir("04_commit_no_site")
d = ImageDraw.Draw(img)
d.rectangle((271, 527, 482, 552), fill=(255, 255, 255))
d.text((281, 539), "ana.souza@example.com", fill=(31, 35, 40), font=FONTE_CAMPO, anchor="lm")
destaque(img, (264, 213, 720, 253)); marcador(img, 1, 248, 200)
destaque(img, (262, 568, 516, 596)); marcador(img, 2, 536, 582)
destaque(img, (579, 672, 720, 711)); marcador(img, 3, 650, 652)
img.crop((236, 112, 748, 738)).save(OUT / "04_commit_no_site.png")

# 6. Push recusado, git pull --rebase e o push que dá certo
blocos = [(3, 11), (12, 20), (21, 30), (31, 35)]
terminal(abrir("04_pull_e_push"), 628, blocos).save(OUT / "04_push_recusado.png")

# 7. clone numa segunda pasta
terminal(abrir("04_clone"), 325, [(1, 2), (10, 13), (14, 16)]).save(OUT / "04_clone.png")

# 8. O colega envia, você recebe com git pull (sem as linhas do Add-Content: a linha 5 vira a 0)
img = abrir("04_pull")
topo = img.crop((0, 0, img.width, 31))
corpo = img.crop((0, linhas(5, 5)[0], img.width, linhas(31, 31)[1] + 3))
junta = Image.new("RGB", (img.width, topo.height + corpo.height))
junta.paste(topo, (0, 0)); junta.paste(corpo, (0, topo.height))
terminal(junta, junta.height, [(0, 9), (11, 22), (23, 26)]).save(OUT / "04_pull.png")

# 9. Colaboradores: menu e janela Add people
img = abrir("04_add_people")
sem_foto(img, (921, 14, 953, 46))
destaque(img, (20, 200, 266, 239)); marcador(img, 1, 286, 220)
destaque(img, (184, 416, 800, 456)); marcador(img, 2, 168, 400)
img.crop((0, 0, 969, 680)).save(OUT / "04_colaboradores.png")
print("ok")
