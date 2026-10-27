"""Casos de teste dos gabaritos do Módulo 00 (VS Code). O código vem das aulas."""

from extrair import gabarito

MODULO = "modulo_06_vscode_config"

# Código "bagunçado" do enunciado do Intermediário da aula 01
BAGUNCA = """x=10;y  =  20
print( "soma:",x+y )
nomes=['ana','bia'  ,'caio']
print(len( nomes ))
"""


def G(aula, nivel):
    """Código do gabarito, lido da própria aula."""
    return gabarito(MODULO, aula, nivel)


def _gabarito_em(arquivo: str, teste: str) -> str:
    """Gabarito num arquivo próprio e o teste em teste.py (o último, que é o executado)."""
    return f"# === arquivo: {arquivo} ===\n# === gabarito ===\n# === arquivo: teste.py ===\n{teste}"


GABARITOS = [
    ("01_instalacao_e_configuracao_vscode.md", "Básico", G("01_instalacao_e_configuracao_vscode.md", "Básico"), ""),
    # O código formatado precisa produzir exatamente a mesma saída que o bagunçado
    ("01_instalacao_e_configuracao_vscode.md", "Intermediário",
     G("01_instalacao_e_configuracao_vscode.md", "Intermediário"), "", _gabarito_em("formatado.py", f'''\
import contextlib, io, runpy
antes, depois = io.StringIO(), io.StringIO()
with contextlib.redirect_stdout(antes):
    exec({BAGUNCA!r})
with contextlib.redirect_stdout(depois):
    runpy.run_path("formatado.py")
assert antes.getvalue() == depois.getvalue() == "soma: 30\\n3\\n", (antes.getvalue(), depois.getvalue())
print("mesma saída antes e depois da formatação")
''')),
    ("01_instalacao_e_configuracao_vscode.md", "Avançado", G("01_instalacao_e_configuracao_vscode.md", "Avançado"), ""),
    # O Básico da aula 02 é uma sequência de comandos de terminal: não há o que executar aqui
    ("02_ambiente_virtual_e_terminal.md", "Intermediário",
     G("02_ambiente_virtual_e_terminal.md", "Intermediário"), "", _gabarito_em("estou_no_venv.py", '''\
import pathlib, subprocess, sys, venv
# Python base: mesmo que os testes rodem dentro de um venv, "fora" tem de ser fora
base = getattr(sys, "_base_executable", sys.executable)
fora = subprocess.run([base, "-X", "utf8", "estou_no_venv.py"],
                      capture_output=True, text=True, encoding="utf-8").stdout
assert "Fora de um ambiente virtual" in fora, fora
venv.create("venv_teste", with_pip=False)  # sem pip: só para o teste ser rápido
py = pathlib.Path("venv_teste") / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
dentro = subprocess.run([str(py), "-X", "utf8", "estou_no_venv.py"],
                        capture_output=True, text=True, encoding="utf-8").stdout
assert "Dentro de um ambiente virtual" in dentro, dentro
print(fora + dentro)
''')),
    ("02_ambiente_virtual_e_terminal.md", "Avançado", G("02_ambiente_virtual_e_terminal.md", "Avançado"), "", '''\
import pathlib
pathlib.Path("requirements.txt").write_text(
    "# dependências\\ncustomtkinter==5.2.2\\npython-dotenv==0.0.1\\npacote-que-nao-existe==1.0\\nsemversao\\n",
    encoding="utf-8")
# === gabarito ===
'''),
]
