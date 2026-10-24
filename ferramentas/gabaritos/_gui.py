"""
Camada de teste para janelas Tkinter/CustomTkinter. Importar ANTES do código testado.

- mainloop() só desenha a janela e volta (o script de teste continua com a janela viva);
- messagebox e filedialog respondem sozinhos;
- helpers para achar widgets pelo texto, digitar e clicar.
"""
import os
import tkinter as tk
from tkinter import filedialog, messagebox

os.environ.setdefault("TK_SILENCE_DEPRECATION", "1")

MENSAGENS: list[str] = []
RESPOSTA_SIM_NAO = True
ARQUIVO_DIALOGO = "teste_dialogo.txt"


def _mainloop(self, n=0):
    self.update()


tk.Misc.mainloop = _mainloop


def _registrar(tipo):
    def f(title=None, message=None, **_):
        MENSAGENS.append(f"{tipo}: {title} | {message}")
        print(f"[{tipo}] {title}: {message}")
        return RESPOSTA_SIM_NAO if tipo.startswith("ask") else "ok"
    return f


for _nome in ("showinfo", "showwarning", "showerror", "askyesno", "askokcancel", "askquestion"):
    setattr(messagebox, _nome, _registrar(_nome))
filedialog.askopenfilename = lambda *a, **k: ARQUIVO_DIALOGO
filedialog.asksaveasfilename = lambda *a, **k: ARQUIVO_DIALOGO


def raiz():
    return tk._default_root


def todos(w=None):
    w = w or raiz()
    for filho in w.winfo_children():
        yield filho
        yield from todos(filho)


def _texto(w):
    try:
        return str(w.cget("text"))
    except Exception:
        return None


def widget(texto):
    for w in todos():
        if _texto(w) == texto:
            return w
    raise LookupError(f"widget com texto {texto!r} não encontrado")


def clicar(texto):
    w = widget(texto)
    w.invoke()
    raiz().update()


def entradas():
    """Campos de texto na ordem de criação (Entry do Tk e CTkEntry, sem duplicar o Entry interno)."""
    lista = []
    for w in todos():
        nome = type(w).__name__
        if nome == "CTkEntry" or (nome == "Entry" and type(w.master).__name__ != "CTkEntry"):
            lista.append(w)
    return lista


def digitar(indice, valor):
    e = entradas()[indice]
    e.delete(0, "end")
    e.insert(0, valor)
    raiz().update()


def textos():
    return [t for w in todos() if (t := _texto(w))]


def ver(trecho):
    """Confere se algum widget mostra um texto que contém o trecho."""
    achados = [t for t in textos() if trecho in t]
    assert achados, f"nenhum widget contém {trecho!r}. Textos: {textos()[:30]}"
    print("OK, tela mostra:", achados[0])
