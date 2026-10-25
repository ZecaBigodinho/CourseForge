"""Monta o Sistema Escolar seguindo as aulas 02–09 do módulo 04 (como o aluno faria)."""
import re
import sqlite3
import sys
from pathlib import Path

M = Path(__file__).resolve().parents[3] / "cursos/python_para_desktop/modulo_04_projeto_finalizador"
DEST = Path(sys.argv[1]); DEST.mkdir(parents=True, exist_ok=True)


def blocos(aula):
    texto = (M / aula).read_text(encoding="utf-8")
    saida = []
    for ind, lang, b in re.findall(r"^( *)```(\w+)\n(.*?)^\1```", texto, re.S | re.M):
        linhas = [l[len(ind):] if l.startswith(ind) else l for l in b.splitlines()]
        saida.append((lang, "\n".join(linhas) + "\n"))
    return saida


def arquivo(aula, cabecalho):
    for lang, b in blocos(aula):
        if lang == "python" and re.search(rf"^# {re.escape(cabecalho)} — ", b, re.M):
            return b
    raise SystemExit(f"não achei {cabecalho} em {aula}")


def bloco_com(aula, trecho):
    for lang, b in blocos(aula):
        if trecho in b:
            return b
    raise SystemExit(f"não achei '{trecho}' em {aula}")


def grava(rel, conteudo):
    p = DEST / rel; p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(conteudo, encoding="utf-8")


for pasta in ("views", "controllers", "database", "utils"):
    grava(f"{pasta}/__init__.py", "")

grava("controllers/auth.py", arquivo("03_tela_de_login.md", "auth.py"))
# login.py (Cap. 03) + Cap. 04: callback on_success
login = arquivo("03_tela_de_login.md", "login.py")
login = login.replace("def criar_tela_login(janela):", "def criar_tela_login(janela, on_success=None):", 1)
novo_if = bloco_com("04_menu_principal.md", "CÓDIGO NOVO (substitua a partir do if)").split("# ===== CÓDIGO NOVO (substitua a partir do if) =====\n")[1]
login = re.sub(r"        if validar_login\(usuario, senha\):\n.*?f\"Bem-vindo\(a\), \{usuario\}!\"\n            \)\n",
               lambda _: novo_if, login, count=1, flags=re.S)
assert "on_success(usuario)" in login
grava("views/login.py", login)
grava("utils/helpers.py", arquivo("05_multiplas_janelas.md", "helpers.py"))

# menu.py (Cap. 05) + Cap. 06: importar a tela real e remover o placeholder
menu = arquivo("05_multiplas_janelas.md", "menu.py")
menu = re.sub(r"\ndef abrir_janela_cadastro\(janela_pai\):.*?(?=\ndef ao_clicar_sair)", "\n", menu, flags=re.S)
menu = re.sub(r"\n# -+ CONTROLE.*?\njanela_cadastro_aberta = None\n", "\n", menu, flags=re.S)
menu = menu.replace("janela_cadastro_aberta = None\n", "")
menu = re.sub(r"^(import tkinter as tk.*?\n)", r"\1from views.cadastro import abrir_janela_cadastro\n", menu, count=1, flags=re.S | re.M)
grava("views/menu.py", menu)

grava("controllers/aluno.py", arquivo("08_crud_completo.md", "aluno.py"))

# Cap. 09
grava("database/conexao.py", arquivo("09_banco_em_nuvem.md", "conexao.py"))
grava("database/operacoes.py", arquivo("09_banco_em_nuvem.md", "operacoes.py"))
grava("migrar_para_nuvem.py", arquivo("09_banco_em_nuvem.md", "migrar_para_nuvem.py"))

# main.py (Cap. 05) + Cap. 07/09: preparar o banco logo depois de criar a janela
main = arquivo("05_multiplas_janelas.md", "main.py")
inicio = bloco_com("09_banco_em_nuvem.md", "SUBSTITUA a chamada inicializar_banco()")
main = main.replace("janela.resizable(False, False)\n", "janela.resizable(False, False)\n\n" + inicio, 1)
grava("main.py", main)

# cadastro.py (Cap. 08) + alterações do Cap. 09
cad = arquivo("08_crud_completo.md", "cadastro.py")
imp = bloco_com("09_banco_em_nuvem.md", "ADICIONE ESTES IMPORTS no topo de views/cadastro.py")
cad = cad.replace("from utils.helpers import centralizar_janela\n", "from utils.helpers import centralizar_janela\n" + imp, 1)
faixa = bloco_com("09_banco_em_nuvem.md", "FAIXA DE STATUS DA NUVEM")
m = re.search(r"    frame_busca\.pack\(.*?\)\n", cad)
cad = cad[:m.end()] + "\n" + faixa + cad[m.end():]
status = bloco_com("09_banco_em_nuvem.md", "===== STATUS DA NUVEM =====")
cad = cad.replace("    # ===== OPERAÇÕES CRUD =====\n", status + "\n    # ===== OPERAÇÕES CRUD =====\n", 1)
salvar = bloco_com("09_banco_em_nuvem.md", "Os campos continuam preenchidos")
cad = re.sub(r"    def ao_clicar_salvar\(\):.*?(?=\n    def ao_clicar_editar)", lambda _: salvar.rstrip("\n"), cad, flags=re.S)
final = bloco_com("09_banco_em_nuvem.md", "if verificar_status():")
cad = re.sub(r"    # ===== CARREGAMENTO INICIAL =====\n    atualizar_tabela\(\)\n", lambda _: final, cad)
grava("views/cadastro.py", cad)

# .gitignore e .env.exemplo do Cap. 09
grava(".gitignore", bloco_com("09_banco_em_nuvem.md", "# Segredos"))
grava(".env.exemplo", bloco_com("09_banco_em_nuvem.md", "Copie este arquivo para .env"))

# escola.db com alunos inventados, como ficaria depois do Cap. 08
db = DEST / "escola.db"
if not db.exists():
    c = sqlite3.connect(db)
    c.execute("CREATE TABLE alunos (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, idade INTEGER NOT NULL, turma TEXT NOT NULL)")
    c.executemany("INSERT INTO alunos (nome, idade, turma) VALUES (?, ?, ?)", [
        ("Ana Souza", 15, "1A"), ("Bruno Lima", 16, "2A"), ("Carla Dias", 14, "9B"),
        ("Diego Rocha", 15, "1B"), ("Elisa Martins", 17, "3A")])
    c.commit(); c.close()
print("montado em", DEST)
for p in sorted(DEST.rglob("*")):
    if p.is_file():
        print(" ", p.relative_to(DEST))
