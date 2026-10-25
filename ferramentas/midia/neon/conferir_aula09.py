"""Confere o código da aula 09 (Neon) sem servidor: sintaxe, SQL (analisador do PostgreSQL) e caminhos de erro."""
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import pglast

AULA = Path(__file__).resolve().parents[3] / "cursos/python_para_desktop/modulo_04_projeto_finalizador/09_banco_em_nuvem.md"
texto = AULA.read_text(encoding="utf-8")
blocos = re.findall(r"^( *)```(\w+)\n(.*?)^\1```", texto, re.S | re.M)
py = [(ind, b) for ind, lang, b in blocos if lang == "python"]
sql = [b for ind, lang, b in blocos if lang == "sql"]

def tira_indent(ind, b):
    return "\n".join(l[len(ind):] if l.startswith(ind) else l for l in b.splitlines())

modulos = {}
for ind, b in py:
    codigo = tira_indent(ind, b)
    m = re.search(r"^# (\w+\.py) — ", codigo, re.M)
    if m:
        modulos[m.group(1)] = codigo
print("módulos completos:", list(modulos))

# 1. Sintaxe de todos os blocos Python (trechos soltos são compilados dentro de uma função)
for ind, b in py:
    codigo = tira_indent(ind, b)
    try:
        compile(codigo, "bloco", "exec")
    except SyntaxError:
        corpo = "\n".join("    " + l for l in codigo.splitlines())
        compile("def _f():\n" + corpo, "bloco", "exec")
print("sintaxe ok:", len(py), "blocos Python")

# 2. SQL: todos os textos SQL dos módulos e dos blocos ```sql passam no analisador do PostgreSQL
consultas = list(sql)
for codigo in modulos.values():
    consultas += re.findall(r'"""(.*?)"""', codigo, re.S)
    consultas += re.findall(r'"((?:SELECT|INSERT|UPDATE|DELETE)[^"]*)"', codigo)
n = 0
for c in consultas:
    if not re.search(r"\b(SELECT|INSERT|UPDATE|DELETE|CREATE|ALTER)\b", c):
        continue
    contador = iter(range(1, 50))
    c2 = re.sub(r"%s", lambda _: f"${next(contador)}", c)
    pglast.parse_sql(c2)
    n += 1
print("SQL ok (analisador do PostgreSQL):", n, "comandos")

# 3. Caminhos de erro, rodando os módulos de verdade
with tempfile.TemporaryDirectory() as pasta:
    p = Path(pasta)
    (p / "database").mkdir()
    (p / "database" / "__init__.py").write_text("")
    (p / "database" / "conexao.py").write_text(modulos["conexao.py"], encoding="utf-8")
    (p / "database" / "operacoes.py").write_text(modulos["operacoes.py"], encoding="utf-8")
    (p / "migrar_para_nuvem.py").write_text(modulos["migrar_para_nuvem.py"], encoding="utf-8")
    teste = r'''
import time, psycopg
from database import conexao, operacoes
print("sem .env -> verificar_conexao:", conexao.verificar_conexao())
try:
    conexao.conectar()
except RuntimeError as e:
    print("sem .env -> conectar:", type(e).__name__, "|", e)
import os
os.environ["DATABASE_URL"] = "postgresql://aluno:senha@127.0.0.1:1/neondb?sslmode=require"
t = time.time()
print("servidor inacessível -> verificar_conexao:", conexao.verificar_conexao(), f"({time.time()-t:.1f}s)")
for f, args in [(operacoes.inserir_aluno, ("Ana", 15, "1A")), (operacoes.listar_alunos, ()), (operacoes.contar_alunos, ("a",))]:
    try:
        f(*args)
    except psycopg.OperationalError as e:
        print(f.__name__, "-> OperationalError (como a aula espera)")
'''
    r = subprocess.run([sys.executable, "-c", teste], cwd=pasta, capture_output=True, text=True,
                       env={**os.environ, "PYTHONPATH": os.environ.get("PYTHONPATH", "")}, timeout=60)
    print(r.stdout, r.stderr[-1500:])
    # migração sem escola.db
    r = subprocess.run([sys.executable, "migrar_para_nuvem.py"], cwd=pasta, capture_output=True, text=True, timeout=60)
    print("migração sem escola.db:", r.stdout.strip(), r.stderr[-500:])
