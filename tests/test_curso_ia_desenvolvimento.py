"""
Testes: o código do curso IA no desenvolvimento de software, lido direto das aulas.

A aula é a fonte única: os blocos são extraídos do Markdown (inclusive de dentro das
caixas recolhíveis, com o recuo removido) e rodados com o pytest num subprocesso.
Confere que os testes da prática FALHAM no código com defeito (5 falhas, como a aula
mostra) e PASSAM na versão corrigida, e que os gabaritos dos exercícios funcionam.
"""
from __future__ import annotations

import re
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

MODULO = (Path(__file__).resolve().parents[1] / "cursos" / "ia_no_desenvolvimento_de_software"
          / "modulo_01_ia_parceira_de_programacao")
AULA_02 = MODULO / "02_pratica_testes_com_ia.md"


def blocos(titulo: str) -> list[str]:
    """Todos os blocos ```python title="<titulo>"```, na ordem da aula, sem o recuo."""
    texto = AULA_02.read_text(encoding="utf-8").replace("\r\n", "\n")
    padrao = rf'^( *)```python title="{re.escape(titulo)}"\n(.*?)^\1```'
    return [textwrap.dedent(m.group(2)) for m in re.finditer(padrao, texto, re.M | re.S)]


def um_bloco(titulo: str) -> str:
    achados = blocos(titulo)
    assert len(achados) == 1, f"esperava 1 bloco {titulo!r}, achei {len(achados)}"
    return achados[0]


def rodar_pytest(pasta: Path, arquivos: dict[str, str]) -> str:
    """Grava os arquivos na pasta, roda o pytest e devolve a última linha (ex.: '9 passed in 0.1s')."""
    for nome, codigo in arquivos.items():
        (pasta / nome).write_text(codigo, encoding="utf-8")
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "-o", "addopts="],
                       cwd=pasta, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.stdout.strip().splitlines()[-1]


def test_aula_tem_as_duas_versoes_de_situacao():
    com_defeito, corrigido = blocos("situacao.py")  # falha se não houver exatamente 2
    assert "frequencia > 75" in com_defeito
    assert "FREQUENCIA_MINIMA" in corrigido


def test_pratica_falha_no_codigo_com_defeito(tmp_path):
    com_defeito = blocos("situacao.py")[0]
    resultado = rodar_pytest(tmp_path, {"situacao.py": com_defeito,
                                        "test_situacao.py": um_bloco("test_situacao.py")})
    assert resultado.startswith("5 failed, 4 passed"), resultado


def test_pratica_passa_no_codigo_corrigido(tmp_path):
    corrigido = blocos("situacao.py")[1]
    resultado = rodar_pytest(tmp_path, {"situacao.py": corrigido,
                                        "test_situacao.py": um_bloco("test_situacao.py")})
    assert resultado.startswith("9 passed"), resultado


def test_teste_feito_so_do_codigo_confirma_o_defeito():
    """O exemplo da nota "E se você tivesse mostrado só o código?" passa no código com defeito."""
    espaco: dict = {}
    exec(blocos("situacao.py")[0], espaco)
    assert espaco["situacao_final"](["D"], 75) == "RP"


def test_gabarito_intermediario(tmp_path):
    corrigido = blocos("situacao.py")[1]
    acrescimo = um_bloco("situacao.py — acrescentar no fim")
    resultado = rodar_pytest(tmp_path, {"situacao.py": corrigido + "\n\n" + acrescimo,
                                        "test_situacao.py": um_bloco("test_situacao.py"),
                                        "test_motivos.py": um_bloco("test_motivos.py")})
    assert resultado.startswith("13 passed"), resultado


@pytest.mark.parametrize("versao, esperado", [(0, "1 failed, 1 passed"), (1, "2 passed")])
def test_gabarito_avancado(tmp_path, versao, esperado):
    """O teste de injeção falha no código da IA e passa no corrigido."""
    resultado = rodar_pytest(tmp_path, {"busca.py": blocos("busca.py")[versao],
                                        "test_busca.py": um_bloco("test_busca.py")})
    assert resultado.startswith(esperado), resultado
