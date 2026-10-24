"""Casos de teste dos gabaritos de Interfaces, aulas 01–04 (janelas abertas de verdade)."""

from extrair import gabarito

MODULO = "modulo_02_interfaces_graficas"


def G(aula, nivel):
    """Código do gabarito, lido da própria aula."""
    return gabarito(MODULO, aula, nivel)


def _t(teste: str) -> str:
    """Teste num arquivo só: camada _gui + gabarito + verificações."""
    return "import _gui\n# === gabarito ===\n" + teste


def _multi(*modulos: str, extra: str = "") -> str:
    """Teste para gabaritos em vários arquivos: importa cada exercício depois da camada _gui."""
    imports = "\n".join(f"import {m}" for m in modulos)
    return f"# === gabarito ===\n# === arquivo: teste.py ===\nimport _gui\n{imports}\n{extra}"


GABARITOS = [
# ============================================================ 01 Tkinter básico
("01_tkinter_basico.md", "Básico", G('01_tkinter_basico.md', 'Básico'), "", _t('''
_gui.ver("Bem-vindo ao Tkinter!")
_gui.ver("Nome:")
assert len(_gui.entradas()) == 1
_gui.clicar("Fechar")  # destrói a janela
'''.replace('_gui.clicar("Fechar")  # destrói a janela', '_gui.widget("Fechar").invoke()\nprint("janela fechada pelo botão")'))),
("01_tkinter_basico.md", "Intermediário", G('01_tkinter_basico.md', 'Intermediário'), "", _t('''
_gui.digitar(0, "100")
_gui.clicar("Celsius para Fahrenheit"); _gui.ver("100.0 °C = 212.0 °F")
_gui.digitar(0, "32")
_gui.clicar("Fahrenheit para Celsius"); _gui.ver("32.0 °F = 0.0 °C")
_gui.digitar(0, "abc")
_gui.clicar("Celsius para Fahrenheit"); _gui.ver("Digite um número válido.")
''')),
("01_tkinter_basico.md", "Avançado", G('01_tkinter_basico.md', 'Avançado'), "", _t('''
_gui.digitar(0, "70"); _gui.digitar(1, "1,75")
_gui.clicar("Calcular"); _gui.ver("IMC: 22.86 — Normal")
_gui.digitar(1, "-1"); _gui.clicar("Calcular"); _gui.ver("Informe peso e altura positivos")
_gui.clicar("Limpar"); assert entrada_peso.get() == "" and resultado.cget("text") == ""; print("limpou")
assert classificar(17) == "Abaixo do peso" and classificar(27) == "Sobrepeso" and classificar(31) == "Obesidade"
''')),
# ============================================================ 02 layout managers
("02_layout_managers.md", "Básico", G('02_layout_managers.md', 'Básico'), "", _multi("exercicio1_pack", "exercicio2_grid", "exercicio3_place", extra='''
for j in (exercicio1_pack.janela, exercicio2_grid.janela, exercicio3_place.janela):
    j.update()
botao = [w for w in exercicio3_place.janela.winfo_children()][0]
assert botao.winfo_x() > 200 and botao.winfo_y() < 20, (botao.winfo_x(), botao.winfo_y())
print("três janelas criadas; 'Ajuda' no canto superior direito")
''')),
("02_layout_managers.md", "Intermediário", G('02_layout_managers.md', 'Intermediário'), "", _t('''
_gui.digitar(0, "547")
_gui.clicar("Converter"); _gui.ver("547.00 BRL = 100.00 USD")
destino.set("EUR"); origem.set("USD"); _gui.digitar(0, "100")
_gui.clicar("Converter"); _gui.ver("100.00 USD = 92.40 EUR")
_gui.clicar("Limpar"); assert resultado.cget("text") == ""
''')),
("02_layout_managers.md", "Avançado", G('02_layout_managers.md', 'Avançado'), "", _t('''
app.peso.insert(0, "95"); app.altura.insert(0, "1.70"); _gui.clicar("Calcular")
assert "Classificação: Obesidade" in app.texto.get("1.0", "end"), app.texto.get("1.0", "end")
janela.geometry("360x500"); janela.update(); alto = app.texto.winfo_height()
janela.geometry("360x320"); janela.update(); baixo = app.texto.winfo_height()
assert alto > baixo, (alto, baixo)
print("resultado correto e área de texto cresce com a janela:", baixo, "->", alto)
''')),
# ============================================================ 03 eventos
("03_eventos_interatividade.md", "Básico", G('03_eventos_interatividade.md', 'Básico'), "", _t('''
texto.set("olá, mundo"); janela.update(); _gui.ver("OLÁ, MUNDO")
rotulo.event_generate("<Enter>"); assert rotulo.cget("bg") == "lightblue"
rotulo.event_generate("<Leave>"); assert rotulo.cget("bg") == "lightgray"
janela.event_generate("<Escape>"); print("hover ok; Esc fechou a janela")
''')),
("03_eventos_interatividade.md", "Intermediário", G('03_eventos_interatividade.md', 'Intermediário'), "", _t('''
assert botao.cget("state") == "disabled"
nome.set("Ana"); email.set("ana@if.edu.br"); assert botao.cget("state") == "disabled"
aceito.set(True); assert botao.cget("state") == "normal"
_gui.clicar("Cadastrar")
nome.set(""); assert botao.cget("state") == "disabled"; print("botão segue os campos")
''')),
("03_eventos_interatividade.md", "Avançado", G('03_eventos_interatividade.md', 'Avançado'), "", _t('''
class Clique:
    def __init__(self, x, y): self.x, self.y = x, y

for _ in range(3): ao_clicar(Clique(alvo["x"], alvo["y"]))      # 3 acertos
ao_clicar(Clique(alvo["x"] + RAIO + 1, alvo["y"]))               # 1 erro
assert (acertos.get(), erros.get()) == (3, 1)
for _ in range(7): ao_clicar(Clique(alvo["x"], alvo["y"]))      # chega a 10
assert acertos.get() == 10 and any("venceu" in m for m in _gui.MENSAGENS)
print("placar e fim de jogo corretos")
''')),
# ============================================================ 04 CustomTkinter
("04_customtkinter.md", "Básico", G('04_customtkinter.md', 'Básico'), "", _multi("exercicio1_tema", "exercicio2_conversor", "exercicio3_slider", extra='''
c = exercicio2_conversor
c.entrada_f.insert(0, "212"); c.para_celsius()
assert c.resultado.cget("text") == "212.0 °F = 100.0 °C", c.resultado.cget("text")
s = exercicio3_slider
s.valor.set(73); assert s.rotulo.cget("text") == "73"
print("conversor e slider funcionando")
''')),
("04_customtkinter.md", "Intermediário", G('04_customtkinter.md', 'Intermediário'), "", _t('''
_gui.clicar("Enviar Avaliação"); assert any("Preencha o nome" in m for m in _gui.MENSAGENS)
entrada_nome.insert(0, "Ana"); nota.set("4"); novidades.select()
_gui.clicar("Enviar Avaliação"); app.update()
_gui.ver("Nota: 4 de 5"); _gui.ver("Novidades por e-mail: Sim")
''')),
("04_customtkinter.md", "Avançado", G('04_customtkinter.md', 'Avançado'), "", _t('''
texto.insert("1.0", "Olá mundo do Python")
texto._textbox.focus_force(); app.update()                         # a tecla chega ao Text interno
texto._textbox.event_generate("<KeyRelease>", keysym="n"); app.update()
assert contador.cget("text") == "19 caracteres · 4 palavras", contador.cget("text")
_gui.clicar("Salvar")
assert open("teste_dialogo.txt", encoding="utf-8").read() == "Olá mundo do Python"
_gui.clicar("Novo"); assert conteudo() == ""
_gui.clicar("Abrir"); assert conteudo() == "Olá mundo do Python"
tema.toggle(); assert ctk.get_appearance_mode() == "Light"
print("contador, salvar/abrir e tema funcionando")
''')),
]
