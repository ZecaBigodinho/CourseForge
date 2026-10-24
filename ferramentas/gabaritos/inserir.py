"""
Insere gabaritos novos nas aulas, no fim de cada subseção "### <nível>" da seção "## Exercícios",
como bloco recolhível "Gabarito — <nível>" (o formato que extrair.py lê).

    python ferramentas/gabaritos/inserir.py <pasta do módulo> <rascunho.py>            # simula
    python ferramentas/gabaritos/inserir.py <pasta do módulo> <rascunho.py> --aplicar  # grava

O rascunho define GABARITOS = [(aula, nível, código, ...)], com o código como texto.
Níveis que já têm gabarito na aula são pulados. Depois de inserir, o rascunho pode ser
apagado: o caso de teste em casos/ passa a ler o código da aula com G(aula, nível).
"""
import importlib.util
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
pasta = Path(sys.argv[1])
_spec = importlib.util.spec_from_file_location("rascunho", sys.argv[2])
_rascunho = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_rascunho)
gabaritos = _rascunho.GABARITOS
aplicar = "--aplicar" in sys.argv
MARCA = "<!-- gabarito -->"


# "# === arquivo: x.py ===" = arquivo completo; "# >>> x.py — Classe" = trecho a alterar em x.py
RE_ARQ = re.compile(r"^# (?:=== arquivo: (\S+) ===|>>> (.+))$", re.M)


def _partes(codigo: str) -> list[tuple[str | None, str]]:
    marcas = list(RE_ARQ.finditer(codigo))
    if not marcas:
        return [(None, codigo)]
    partes = []
    if codigo[:marcas[0].start()].strip():
        partes.append((None, codigo[:marcas[0].start()]))
    for i, m in enumerate(marcas):
        fim = marcas[i + 1].start() if i + 1 < len(marcas) else len(codigo)
        partes.append((m.group(1) or m.group(2).strip(), codigo[m.end():fim]))
    return partes


def bloco(nivel: str, codigo: str) -> list[str]:
    linhas = ["", MARCA, f'??? success "Gabarito — {nivel}"',
              "    Uma solução possível — compare com a sua. Outras formas também podem estar certas."]
    for nome, conteudo in _partes(codigo):
        titulo = f' title="{nome}"' if nome else ""
        arquivo = (nome or "").split(" ")[0]
        linguagem = ("python" if not nome or arquivo.endswith(".py")
                     else "ini" if ".env" in arquivo else "text")
        linhas += ["", f"    ```{linguagem}{titulo}"]
        linhas += [("    " + l) if l.strip() else "" for l in conteudo.strip("\n").rstrip().splitlines()]
        linhas += ["    ```"]
    return linhas + [""]


por_aula: dict[str, list] = {}
for aula, nivel, codigo, *_ in gabaritos:
    por_aula.setdefault(aula, []).append((nivel, codigo))

for aula, itens in por_aula.items():
    arq = pasta / aula
    bruto = arq.read_bytes().decode("utf-8")
    eol = "\r\n" if "\r\n" in bruto else "\n"
    existentes = [n for n, _ in itens if f'??? success "Gabarito — {n}"' in bruto]
    if existentes:
        print(f"{aula}: já tem gabarito {', '.join(existentes)} — pulando esse(s) nível(is)")
        itens = [(n, c) for n, c in itens if n not in existentes]
    if not itens:
        continue
    linhas = bruto.split(eol)

    # Limites da seção de exercícios
    ini = next(i for i, l in enumerate(linhas) if re.match(r"^## Exerc[ií]cios", l))
    fim = next((i for i in range(ini + 1, len(linhas)) if linhas[i].startswith("## ")), len(linhas))

    # Insere de baixo para cima para não deslocar índices
    for nivel, codigo in reversed(itens):
        h = next(i for i in range(ini, fim) if re.match(rf"^###\s+{nivel}\b", linhas[i]))
        fim_sub = next((i for i in range(h + 1, fim) if linhas[i].startswith("### ")), fim)
        while fim_sub > h + 1 and not linhas[fim_sub - 1].strip():
            fim_sub -= 1
        linhas[fim_sub:fim_sub] = bloco(nivel, codigo)
        fim += len(bloco(nivel, codigo))
    print(f"{'ok' if aplicar else 'simulado'}: {aula} ({len(itens)} gabaritos)")
    if aplicar:
        arq.write_bytes(eol.join(linhas).encode("utf-8"))
