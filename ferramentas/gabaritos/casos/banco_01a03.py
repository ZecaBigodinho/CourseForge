"""Casos de teste dos gabaritos de Banco de Dados, aulas 01–03. O código vem das aulas."""

from extrair import gabarito
from patch_classe import aplicar

MODULO = "modulo_03_banco_de_dados"


def G(aula, nivel):
    """Código do gabarito, lido da própria aula."""
    return gabarito(MODULO, aula, nivel)


def _multi_teste(extra: str) -> str:
    return f"# === gabarito ===\n# === arquivo: teste.py ===\nimport _gui\n{extra}"


# ---------------------------------------------------------------- 02 intermediário (base do avançado)
CRUD_DB = G("02_integracao_interface.md", "Intermediário").split("# === arquivo: app_clientes.py ===")[0]

CRUD_APP = "# === arquivo: app_clientes.py ===" + G("02_integracao_interface.md", "Intermediário").split("# === arquivo: app_clientes.py ===")[1]

AVANCADO_02 = G("02_integracao_interface.md", "Avançado")

GABARITOS = [
# ============================================================ 01 SQLite
("01_introducao_sqlite.md", "Básico", G('01_introducao_sqlite.md', 'Básico'), ""),
("01_introducao_sqlite.md", "Intermediário", G('01_introducao_sqlite.md', 'Intermediário'), ""),
("01_introducao_sqlite.md", "Avançado", G('01_introducao_sqlite.md', 'Avançado'), ""),
# ============================================================ 02 integração
("02_integracao_interface.md", "Básico", G('02_integracao_interface.md', 'Básico'), "", "import _gui\n# === gabarito ===\n" + '''
_gui.digitar(0, "Caneta"); _gui.digitar(1, "2,50"); _gui.clicar("Salvar")
_gui.digitar(0, "Borracha"); _gui.digitar(1, "1.2"); _gui.clicar("Salvar")
_gui.digitar(0, "Caneta"); _gui.digitar(1, "3"); _gui.clicar("Salvar")
assert any("Já existe um produto 'Caneta'" in m for m in _gui.MENSAGENS)
assert [tree.item(i, "values")[1] for i in tree.get_children()] == ["Borracha", "Caneta"]
tree.selection_set(tree.get_children()[0]); _gui.clicar("Excluir")
assert [tree.item(i, "values")[1] for i in tree.get_children()] == ["Caneta"]
print("inserir, duplicado e excluir com confirmação funcionando")
'''),
("02_integracao_interface.md", "Intermediário", CRUD_DB + "\n" + CRUD_APP, "", _multi_teste('''
import app_clientes
app = app_clientes.AppClientes()
c = app.campos
c["Nome"].insert(0, "Bruno"); c["E-mail"].insert(0, "bruno.if.edu.br"); c["Telefone"].insert(0, "11999990000")
app.salvar(); assert any("falta o @" in m for m in _gui.MENSAGENS)
c["E-mail"].delete(0, "end"); c["E-mail"].insert(0, "bruno@if.edu.br"); c["Telefone"].delete(0, "end"); c["Telefone"].insert(0, "123")
app.salvar(); assert any("mínimo 10" in m for m in _gui.MENSAGENS)
c["Telefone"].delete(0, "end"); c["Telefone"].insert(0, "11999990000"); app.salvar()
assert len(app.tree.get_children()) == 1
app.tree.selection_set(app.tree.get_children()[0]); app.janela.update(); app.ao_selecionar()
assert app.btn_salvar.cget("text") == "Atualizar" and c["Nome"].get() == "Bruno"
c["Nome"].delete(0, "end"); c["Nome"].insert(0, "Bruno Lima"); app.salvar()
assert app.tree.item(app.tree.get_children()[0], "values")[1] == "Bruno Lima"
assert app.btn_salvar.cget("text") == "Salvar"
print("validação, inserção e edição inline funcionando")
''')),
("02_integracao_interface.md", "Avançado", AVANCADO_02, "", None),  # teste montado abaixo
# ============================================================ 03 .env
("03_variaveis_ambiente.md", "Básico", G('03_variaveis_ambiente.md', 'Básico'), ""),
("03_variaveis_ambiente.md", "Intermediário", G('03_variaveis_ambiente.md', 'Intermediário'), "", '''\
# === gabarito ===
# === arquivo: teste.py ===
import importlib, os, pathlib
import app_notas
import config
pathlib.Path(".env").unlink()
os.environ.pop("API_KEY", None)
try:
    importlib.reload(config)
    raise AssertionError("deveria exigir a API_KEY")
except RuntimeError as erro:
    print("Sem API_KEY:", erro)
'''),
("03_variaveis_ambiente.md", "Avançado", G('03_variaveis_ambiente.md', 'Avançado'), "app.db\ndark\n\n", '''\
# === gabarito ===
# === arquivo: teste.py ===
import gerenciador_env as g
assert g.check() == ["DB_PATH", "TEMA", "API_KEY"]      # ainda não há .env
g.main(["--init"])                                       # responde: app.db, dark, (vazio)
assert g.check() == ["API_KEY"]
print("init e check funcionando")
'''),
]

# Avançado da aula 02 = métodos novos aplicados sobre o app do Intermediário
_app_avancado = aplicar(CRUD_APP, "AppClientes", AVANCADO_02.split("# Em AppClientes")[1].split("\n", 1)[1])
_db_avancado = CRUD_DB + "\n\n" + AVANCADO_02.split("# Em AppClientes")[0].split("\n", 1)[1]
_I_AVANCADO_02 = next(i for i, g in enumerate(GABARITOS) if g[0].startswith("02_") and g[1] == "Avançado")
GABARITOS[_I_AVANCADO_02] = GABARITOS[_I_AVANCADO_02][:4] + (_db_avancado + "\n" + _app_avancado + "\n" + _multi_teste('''
import clientes_db as db, app_clientes
db.criar_tabela()
for nome, email, tel in (("Carla Souza", "c@x.com", "1199999000"), ("ana lima", "a@x.com", "1199999001"),
                         ("Bruno Souza", "b@x.com", "1199999002")):
    db.inserir(nome, email, tel)
app = app_clientes.AppClientes()
nomes = lambda: [app.tree.item(i, "values")[1] for i in app.tree.get_children()]
app.entrada_busca.insert(0, "souza"); app.buscar(); assert nomes() == ["Bruno Souza", "Carla Souza"], nomes()
app.ordenar("nome"); assert nomes() == ["Bruno Souza", "Carla Souza"]
app.ordenar("nome"); assert nomes() == ["Carla Souza", "Bruno Souza"]          # alterna para ▼
assert app.tree.heading("nome")["text"] == "Nome ▼"
app.entrada_busca.delete(0, "end"); app.buscar(); assert len(nomes()) == 3     # busca vazia = todos
app.ordenar("nome"); assert nomes() == ["ana lima", "Bruno Souza", "Carla Souza"]  # sem diferenciar maiúsculas
print("busca com LIKE e ordenação local alternando funcionando")
'''),)
