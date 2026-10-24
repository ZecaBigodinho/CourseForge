"""
Lê os gabaritos direto das aulas (a aula é a fonte única).

Um gabarito é um bloco recolhível com o título "Gabarito — <nível>":

    ??? success "Gabarito — Básico"
        Texto opcional.

        ```python title="modulo.py"
        ...
        ```

Cada bloco de código vira uma parte. O título do bloco diz o que ela é:
- sem título              → código solto;
- "arquivo.py" (sem espaço) → arquivo completo   → "# === arquivo: arquivo.py ===";
- "arquivo.py — descrição"  → trecho a alterar    → "# >>> arquivo.py — descrição".
"""
from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
CURSO = RAIZ / "cursos" / "python_para_desktop"

_RE_FENCE = re.compile(r'^```\w*(?:\s+title="([^"]*)")?\s*$')


@lru_cache(maxsize=None)
def texto_aula(modulo: str, aula: str) -> str:
    return (CURSO / modulo / aula).read_text(encoding="utf-8").replace("\r\n", "\n")


def blocos_python(modulo: str, aula: str) -> list[str]:
    """Todos os blocos ```python``` da aula, fora dos gabaritos (o código que a aula ensina)."""
    texto = texto_aula(modulo, aula)
    texto = re.sub(r'^\?\?\? success "Gabarito.*?(?=^\S)', "", texto + "\n.", flags=re.S | re.M)
    return re.findall(r"```python\n(.*?)```", texto, re.S)


def partes_gabarito(modulo: str, aula: str, nivel: str) -> list[tuple[str | None, str]]:
    """[(título ou None, código)] do bloco "Gabarito — <nível>" da aula."""
    linhas = texto_aula(modulo, aula).split("\n")
    cabecalho = f'??? success "Gabarito — {nivel}"'
    try:
        inicio = linhas.index(cabecalho) + 1
    except ValueError:
        raise LookupError(f"{modulo}/{aula}: não há gabarito '{nivel}'") from None

    # O bloco termina na primeira linha não vazia sem os 4 espaços de recuo
    corpo = []
    for linha in linhas[inicio:]:
        if linha.strip() and not linha.startswith("    "):
            break
        corpo.append(linha[4:] if linha.startswith("    ") else "")

    partes, atual, titulo = [], None, None
    for linha in corpo:
        m = _RE_FENCE.match(linha)
        if m and atual is None:
            atual, titulo = [], m.group(1)
        elif linha.startswith("```") and atual is not None:
            partes.append((titulo, "\n".join(atual)))
            atual = None
        elif atual is not None:
            atual.append(linha)
    if not partes:
        raise LookupError(f"{modulo}/{aula}: o gabarito '{nivel}' não tem código")
    return partes


def gabarito(modulo: str, aula: str, nivel: str) -> str:
    """Código do gabarito no formato de várias partes usado pelos testes."""
    saida = []
    for titulo, codigo in partes_gabarito(modulo, aula, nivel):
        if titulo is None:
            saida.append(codigo)
        elif " " not in titulo:
            saida.append(f"# === arquivo: {titulo} ===\n{codigo}")
        else:
            saida.append(f"# >>> {titulo}\n{codigo}")
    return "\n\n".join(saida) + "\n"


def niveis(modulo: str, aula: str) -> list[str]:
    return re.findall(r'^\?\?\? success "Gabarito — (\w+)"', texto_aula(modulo, aula), re.M)
