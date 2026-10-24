"""Casos de teste dos gabaritos das aulas 06–11 de Fundamentos. O código vem das aulas."""

from extrair import blocos_python, gabarito

MODULO = "modulo_01_fundamentos"


def G(aula, nivel):
    """Código do gabarito, lido da própria aula."""
    return gabarito(MODULO, aula, nivel)


# Projeto da aula 11 (arquivos que começam com "# nome.py"), para testar as modificações dos gabaritos
_ARQS = {}
for _bloco in blocos_python(MODULO, "11_projeto_final.md"):
    _primeira, _, _resto = _bloco.partition("\n")
    if _primeira.startswith("# ") and _primeira.endswith(".py"):
        _ARQS[_primeira[2:]] = _resto


def _projeto(**trocas) -> str:
    """Monta o projeto da aula 11 no formato multiarquivo do testador, com arquivos trocados."""
    arquivos = dict(_ARQS, **trocas)
    ordem = ["validacao.py", "persistencia.py", "tarefas.py", "main.py"]
    return "\n".join(f"# === arquivo: {n} ===\n{arquivos[n]}" for n in ordem)


GABARITOS = [
# ---------------------------------------------------------------- 06 módulos
("06_modulos.md", "Básico", G('06_modulos.md', 'Básico'), ""),
("06_modulos.md", "Intermediário", G('06_modulos.md', 'Intermediário'), "70\nkg\n"),
("06_modulos.md", "Avançado", G('06_modulos.md', 'Avançado'), ""),
# ---------------------------------------------------------------- 07 coleções
("07_colecoes.md", "Básico", G('07_colecoes.md', 'Básico'), ""),
("07_colecoes.md", "Intermediário", G('07_colecoes.md', 'Intermediário'), ""),
("07_colecoes.md", "Avançado", G('07_colecoes.md', 'Avançado'), "1\nbruno\n9999-1111\n1\nana\n8888-2222\n1\nBruno\nn\n9\n2\nana\n2\nzeca\n3\n4\n"),
# ---------------------------------------------------------------- 08 strings
("08_strings.md", "Básico", G('08_strings.md', 'Básico'), "Maria da Silva Santos\nA casa amarela\n"),
("08_strings.md", "Intermediário", G('08_strings.md', 'Intermediário'), ""),
("08_strings.md", "Avançado", G('08_strings.md', 'Avançado'), ""),
# ---------------------------------------------------------------- 09 arquivos
("09_arquivos.md", "Básico", G('09_arquivos.md', 'Básico'), "Olá, mundo\nPython é legal\nArquivos funcionam\n"),
("09_arquivos.md", "Intermediário", G('09_arquivos.md', 'Intermediário'), "1\nEstudar arquivos\n1\nFazer exercícios\n3\n1\n2\n4\n"),
("09_arquivos.md", "Avançado", G('09_arquivos.md', 'Avançado'), "\n\n", '''\
from pathlib import Path
for nome in ("a.txt", "b.txt"):
    Path(nome).write_text("conteúdo", encoding="utf-8")
# === gabarito ===
'''),
# ---------------------------------------------------------------- 10 exceções
("10_excecoes.md", "Básico", G('10_excecoes.md', 'Básico'), "10\n0\n7\n"),
("10_excecoes.md", "Intermediário", G('10_excecoes.md', 'Intermediário'), "10 20 abc 2,5\n"),
("10_excecoes.md", "Avançado", G('10_excecoes.md', 'Avançado'), "1\nc\n5\n1\nC\n5\n1\nZ\n1\n1\nA\n99\n1\nB\nx\n3\n4\n"),
# ---------------------------------------------------------------- 11 mini-projeto
("11_projeto_final.md", "Básico", G('11_projeto_final.md', 'Básico'), "1\nabc\nbaixa\n1\nEstudar\nalta\n5\n6\n", _projeto(
    **{"validacao.py": _ARQS["validacao.py"].replace(">= 3", ">= 5"),
       "main.py": _ARQS["main.py"]
           .replace('print("5. Sair")', 'print("5. Quantidade de tarefas")\n    print("6. Sair")')
           .replace('elif opcao == "5":\n            print("Encerrando...")',
                    'elif opcao == "5":\n            print(f"Total de tarefas: {len(lista)}")\n'
                    '        elif opcao == "6":\n            print("Encerrando...")')})),
("11_projeto_final.md", "Intermediário", G('11_projeto_final.md', 'Intermediário'), "1\nEstudar Python\n\n1\nLavar louça\n\n5\npython\n6\n", _projeto(
    **{"tarefas.py": _ARQS["tarefas.py"] + '''
def buscar_tarefas(tarefas, termo):
    termo = termo.strip().lower()
    return [t for t in tarefas if termo in t["descricao"].lower()]
''',
       "main.py": _ARQS["main.py"]
           .replace('print("5. Sair")', 'print("5. Buscar tarefas")\n    print("6. Sair")')
           .replace('elif opcao == "5":\n            print("Encerrando...")',
                    'elif opcao == "5":\n            encontradas = tm.buscar_tarefas(lista, input("Palavra-chave: "))\n'
                    '            if not encontradas:\n                print("Nenhuma tarefa encontrada.")\n'
                    '            for t in encontradas:\n                print(f"[{t[\'id\']}] {t[\'descricao\']} - {t[\'status\']}")\n'
                    '        elif opcao == "6":\n            print("Encerrando...")')})),
("11_projeto_final.md", "Avançado", G('11_projeto_final.md', 'Avançado'), "1\nSalário\n2500\nrenda\n05/10/2026\n1\nMercado\n-320,50\nalimentação\n06/10/2026\n"
     "1\nCinema\nabc\n1\nÔnibus\n-4.5\ntransporte\n31/02/2026\n3\n4\nalimentação\n5\n1\n2\n6\n"),
]
