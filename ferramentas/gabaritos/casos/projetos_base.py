"""Roda os projetos das aulas como estão (Dashboard e Projeto de Dados): a base dos outros testes."""

import re

from extrair import blocos_python


def projeto_dados():
    """Arquivos do Projeto de Dados (Banco 04), pelo comentário '# caminho.py' da 1ª linha."""
    arquivos = {}
    for b in blocos_python("modulo_03_banco_de_dados", "04_projeto_final.md"):
        m = re.match(r"# ([\w/]+\.py)\n", b)
        if m:
            arquivos[m.group(1)] = b
    return arquivos


def dashboard():
    """Maior bloco da aula 05 de Interfaces = código completo do Dashboard."""
    return max(blocos_python("modulo_02_interfaces_graficas", "05_projeto_pratico.md"), key=len)


def _multi(arquivos: dict, principal: str, extra: str) -> str:
    partes = [f"# === arquivo: {n} ===\n{c}" for n, c in arquivos.items() if n != principal]
    partes += [f"# === arquivo: {n} ===\n" for n in ("models/__init__.py", "views/__init__.py",
                                                       "controllers/__init__.py") if n not in arquivos]
    partes.append(f"# === arquivo: {principal} ===\nimport _gui\n{arquivos[principal]}\n{extra}")
    return "\n".join(partes)


GABARITOS = [
    ("base", "Dashboard (Interfaces 05)", "", "",
     "# === arquivo: main.py ===\nimport _gui\n# === gabarito ===\n" + dashboard() + "\nprint(_gui.textos()[:25])\n"),
    ("base", "Projeto de Dados (Banco 04)", "", "",
     _multi(projeto_dados(), "app.py", "print(_gui.textos()[:25])")),
]
