"""
Testes: ênfase das aulas que o Markdown não entende.

O padrão `*Menu ➔ **Botão***` (itálico que termina num negrito) deixa `**` à vista no site.
A forma certa é `*Menu* ➔ **Botão**`.
"""
from __future__ import annotations

import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
CURSOS = RAIZ / "cursos"

# *texto **negrito***  (itálico simples aberto antes de um negrito que fecha com três asteriscos)
_RE_QUEBRADO = re.compile(r"(?<!\*)\*(?!\*)[^*\n]*?\*\*[^*\n]+?\*\*\*(?!\*)")
_RE_CODIGO = re.compile(r"^(`{3,}|~{3,}).*?^\1", re.S | re.M)


def enfases_quebradas(texto: str) -> list[str]:
    """Trechos com o padrão quebrado, fora de blocos de código."""
    return _RE_QUEBRADO.findall(_RE_CODIGO.sub("", texto))


def test_detecta_o_padrao_quebrado():
    assert enfases_quebradas("Use *Layout ➔ Quebras ➔ **Próxima Página***.")
    assert not enfases_quebradas("Use *Layout ➔ Quebras* ➔ **Próxima Página**.")
    assert not enfases_quebradas("**desligue *Vincular ao Anterior***")


def test_aulas_sem_enfase_quebrada():
    problemas = []
    for md in sorted(CURSOS.rglob("*.md")):
        if "site" in md.parts:
            continue
        for trecho in enfases_quebradas(md.read_text(encoding="utf-8")):
            problemas.append(f"{md.relative_to(RAIZ)}: {trecho}")
    assert not problemas, "Troque por *Menu* ➔ **Botão**:\n" + "\n".join(problemas)
