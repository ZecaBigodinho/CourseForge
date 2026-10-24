"""Casos de teste dos gabaritos da aula 04 de Banco (Projeto de Dados MVC): aplicados sobre o projeto da aula."""

import re

from extrair import gabarito
from patch_classe import aplicar
from projetos_base import projeto_dados

MODULO = "modulo_03_banco_de_dados"


def G(aula, nivel):
    """Código do gabarito, lido da própria aula."""
    return gabarito(MODULO, aula, nivel)


BASE = projeto_dados()  # {"config.py": ..., "models/database.py": ..., ...}
INITS = ("models/__init__.py", "views/__init__.py", "controllers/__init__.py", "utils/__init__.py")


def _montar(arquivos: dict, env: str, verificacoes: str) -> str:
    partes = [f"# === arquivo: {n} ===\n{c}" for n, c in arquivos.items()]
    partes += [f"# === arquivo: {n} ===\n" for n in INITS if n not in arquivos]
    partes.append(f"# === arquivo: .env ===\n{env}")
    partes.append("# === arquivo: teste.py ===\nimport _gui\n" + verificacoes)
    return "\n".join(partes)


def _corpo(trecho: str, rotulo: str) -> str:
    """Parte de um gabarito entre '# >>> rotulo' e o próximo '# >>>' (ou o fim)."""
    m = re.search(rf"^# >>> {re.escape(rotulo)}.*?\n(.*?)(?=^# >>> |\Z)", trecho, re.S | re.M)
    return m.group(1)


ENV_PADRAO = "DB_PATH=produtos.db\nTEMA=dark\nCOR_TEMA=dark-blue\nTITULO_APP=Gerenciador de Produtos\n"

# =============================================================== Básico
BASICO = G("04_projeto_final.md", "Básico")


def _arquivos_basico():
    arq = dict(BASE)
    arq["views/main_view.py"] = aplicar(arq["views/main_view.py"], "MainView", _corpo(BASICO, "views/"))
    arq["controllers/produto_controller.py"] = aplicar(
        arq["controllers/produto_controller.py"], "ProdutoController", _corpo(BASICO, "controllers/"))
    return arq


TESTE_BASICO = _montar(_arquivos_basico(), ENV_PADRAO.replace("dark\n", "light\n", 1).replace("dark-blue", "green"), '''
import customtkinter as ctk
from models.database import inicializar_banco
from controllers.produto_controller import ProdutoController
inicializar_banco()
c = ProdutoController(); v = c.view
assert ctk.get_appearance_mode() == "Light" and v.title() == "Gerenciador de Produtos"
v.entry_nome.insert(0, "Caneta"); v.entry_descricao.insert(0, "Azul, ponta fina")
v.entry_preco.insert(0, "2.5"); v.entry_quantidade.insert(0, "10"); c.adicionar()
linha = v.tree.item(v.tree.get_children()[0], "values")
assert linha[1:3] == ("Caneta", "Azul, ponta fina"), linha
v.tree.selection_set(v.tree.get_children()[0]); v.update(); c._ao_selecionar(None)
assert v.entry_descricao.get() == "Azul, ponta fina"
v.entry_quantidade.delete(0, "end"); v.entry_quantidade.insert(0, "7"); c.atualizar()
linha = v.tree.item(v.tree.get_children()[0], "values")
assert linha[2] == "Azul, ponta fina" and str(linha[4]) == "7", linha
print("tema do .env aplicado; descrição gravada, exibida e preservada na atualização")
''')

# =============================================================== Intermediário
INTERMEDIARIO = G("04_projeto_final.md", "Intermediário")


def _arquivos_intermediario():
    arq = dict(BASE)
    for nome, conteudo in re.findall(r"^# === arquivo: (\S+) ===\n(.*?)(?=^# === arquivo: |^# >>> |\Z)",
                                     INTERMEDIARIO, re.S | re.M):
        arq[nome] = conteudo
    arq["views/main_view.py"] = aplicar(arq["views/main_view.py"], "MainView", _corpo(INTERMEDIARIO, "views/"))
    controller = _corpo(INTERMEDIARIO, "controllers/").split("# No topo de")[0]
    arq["controllers/produto_controller.py"] = aplicar(
        arq["controllers/produto_controller.py"].replace(
            "from models.produto import Produto",
            "from models.produto import Produto\nfrom models.categoria import Categoria\n"
            "from controllers.categoria_controller import CategoriaController"),
        "ProdutoController", controller)
    return arq


TESTE_INTERMEDIARIO = _montar(_arquivos_intermediario(), ENV_PADRAO, '''
import sqlite3
# Banco "antigo", criado pela versão da aula (sem categoria_id): a migração precisa preservá-lo
with sqlite3.connect("produtos.db") as conn:
    conn.execute("CREATE TABLE produtos (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, "
                 "descricao TEXT, preco REAL NOT NULL, quantidade INTEGER NOT NULL DEFAULT 0)")
    conn.execute("INSERT INTO produtos (nome, preco, quantidade) VALUES ('Produto antigo', 1, 1)")
from models.database import inicializar_banco
from controllers.produto_controller import ProdutoController
inicializar_banco()
c = ProdutoController(); v = c.view
assert [v.tree.item(i, "values")[1] for i in v.tree.get_children()] == ["Produto antigo"]
c.abrir_categorias(); v.update()
janela_cat = [w for w in v.winfo_children() if type(w).__name__ == "CategoriaView"][0]
janela_cat.entry_nome.insert(0, "Papelaria"); janela_cat.btn_salvar.invoke()
janela_cat.entry_nome.insert(0, "Papelaria"); janela_cat.btn_salvar.invoke()      # duplicada
assert any("já existe" in m for m in _gui.MENSAGENS)
assert "Papelaria" in v.menu_categoria.cget("values")
v.menu_categoria.set("Papelaria")
for campo, valor in ((v.entry_nome, "Caderno"), (v.entry_preco, "18.9"), (v.entry_quantidade, "5")):
    campo.insert(0, valor)
c.adicionar()
v.entry_busca.insert(0, "cad"); c.buscar()
linhas = [v.tree.item(i, "values") for i in v.tree.get_children()]
assert len(linhas) == 1 and linhas[0][1:3] == ("Caderno", "Papelaria"), linhas
v.entry_busca.delete(0, "end"); c.buscar(); assert len(v.tree.get_children()) == 2
print("migração do banco, categorias (com duplicada recusada), JOIN e busca funcionando")
''')

# =============================================================== Avançado
AVANCADO = G("04_projeto_final.md", "Avançado")


def _arquivos_avancado():
    arq = dict(BASE)
    arq["utils/log.py"] = re.search(r"^# === arquivo: utils/log\.py ===\n(.*?)(?=^# >>> )",
                                    AVANCADO, re.S | re.M).group(1)
    arq["views/main_view.py"] = aplicar(arq["views/main_view.py"], "MainView", _corpo(AVANCADO, "views/"))
    arq["controllers/produto_controller.py"] = aplicar(
        arq["controllers/produto_controller.py"].replace(
            "from models.produto import Produto",
            "from models.produto import Produto\nfrom utils.log import configurar_log, ligar_barra_de_status"),
        "ProdutoController", _corpo(AVANCADO, "controllers/"))
    return arq


TESTE_AVANCADO = _montar(_arquivos_avancado(), ENV_PADRAO + "LOG_NIVEL=INFO\nLOG_ARQUIVO=registro.log\n", '''
from models.database import inicializar_banco
from controllers.produto_controller import ProdutoController
inicializar_banco()
c = ProdutoController(); v = c.view
v.entry_nome.insert(0, ""); c.adicionar()                                  # validação falha
assert "Nome do produto é obrigatório" in v.status.cget("text"), v.status.cget("text")
v.entry_nome.insert(0, "Régua"); v.entry_preco.insert(0, "4"); v.entry_quantidade.insert(0, "3"); c.adicionar()
assert v.status.cget("text").startswith("Produto adicionado: Régua")
v.tree.selection_set(v.tree.get_children()[0]); v.update(); c._ao_selecionar(None); c.excluir()
log = open("registro.log", encoding="utf-8").read()
for trecho in ("[INFO] Aplicação iniciada.", "[WARNING] Validação:", "[INFO] Produto adicionado: Régua", "[INFO] Produto excluído"):
    assert trecho in log, (trecho, log)
print("log no arquivo definido no .env e na barra de status funcionando")
''')

GABARITOS = [
    ("04_projeto_final.md", "Básico", BASICO, "", TESTE_BASICO),
    ("04_projeto_final.md", "Intermediário", INTERMEDIARIO, "", TESTE_INTERMEDIARIO),
    ("04_projeto_final.md", "Avançado", AVANCADO, "", TESTE_AVANCADO),
]
