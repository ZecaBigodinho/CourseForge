"""Casos de teste do curso Automação com Python, Módulo 05 (projeto final: Secretaria automática).

O pacote `secretaria` e os testes com pytest vêm das próprias aulas. Cada caso roda numa pasta
temporária com a planilha de treino criada pelo criar_treino_secretaria.py da aula 01.
Precisa de openpyxl, fpdf2, python-dotenv, aiosmtpd e pytest (a CI instala).
"""
import re

from extrair import gabarito, texto_aula

MODULO = "../automacao_com_python/modulo_05_projeto_final"


def G(aula, nivel):
    return gabarito(MODULO, aula, nivel)


def bloco_titulo(aula, titulo):
    """O bloco de código da aula com o título (title="...") dado."""
    texto = texto_aula(MODULO, aula)
    achados = re.findall(rf'```python title="{re.escape(titulo)}"\n(.*?)```', texto, re.S)
    assert len(achados) == 1, f"{aula}: esperava 1 bloco {titulo!r}, achei {len(achados)}"
    return achados[0]


A01, A02, A03, A04 = (
    "01_planejando_a_secretaria.md", "02_pacote_e_dados.md",
    "03_documentos_e_emails.md", "04_linha_de_comando_e_testes.md",
)

CRIAR = bloco_titulo(A01, "criar_treino_secretaria.py")
PACOTE = {
    "secretaria/__init__.py": bloco_titulo(A02, "secretaria/__init__.py"),
    "secretaria/__main__.py": bloco_titulo(A02, "secretaria/__main__.py"),
    "secretaria/dados.py": bloco_titulo(A02, "secretaria/dados.py"),
    "secretaria/documentos.py": bloco_titulo(A03, "secretaria/documentos.py"),
    "secretaria/emails.py": bloco_titulo(A03, "secretaria/emails.py"),
    "secretaria/cli.py": bloco_titulo(A04, "secretaria/cli.py"),
    "testes/test_secretaria.py": bloco_titulo(A04, "testes/test_secretaria.py"),
}
ARQUIVOS = "".join(f"# === arquivo: {nome} ===\n{codigo}\n" for nome, codigo in PACOTE.items())


def com_treino(verificacao: str = "", preparo: str = "") -> str:
    verificacao = verificacao.strip().removeprefix("# === gabarito ===").strip()
    return (f"# === arquivo: criar_treino_secretaria.py ===\n{CRIAR}\n{ARQUIVOS}"
            f"# === arquivo: teste.py ===\nimport sys\nfrom pathlib import Path\nsys.path.insert(0, str(Path.cwd()))\n"
            f"import criar_treino_secretaria\ncriar_treino_secretaria.main()\n{preparo}\n"
            f"# === gabarito ===\n{verificacao}\n")


GABARITOS = [
# ============================================================ pacote inteiro
(A04, "python -m secretaria tudo (simulação)", "", "", com_treino("""
import subprocess
r = subprocess.run([sys.executable, "-X", "utf8", "-m", "secretaria", "tudo", "treino_secretaria/turma_1A.xlsx"],
                   capture_output=True, text=True, encoding="utf-8")
assert r.returncode == 0, r.stdout + r.stderr
pasta = next(Path("saida").iterdir())
assert len(list(pasta.glob("certificado_*.pdf"))) == 4 and len(list((pasta / "rascunhos").iterdir())) == 6
assert "Heitor Alves: e-mail inválido" in (pasta / "secretaria.log").read_text(encoding="utf-8")
print("secretaria tudo ok")""")),
(A04, "python -m secretaria com comando errado", "", "", com_treino("""
import subprocess
r = subprocess.run([sys.executable, "-m", "secretaria", "boletins", "x.xlsx"], capture_output=True, text=True)
assert r.returncode == 2 and "invalid choice" in r.stderr""")),
(A04, "testes da aula (pytest)", "", "", com_treino("""
import pytest
assert pytest.main(["-q", "-p", "no:cacheprovider", "testes"]) == 0""")),
# ============================================================ 01
(A01, "Básico", G(A01, "Básico"), "", com_treino()),
(A01, "Intermediário", G(A01, "Intermediário"), "", com_treino("assert not erros")),
# ============================================================ 02
(A02, "Básico", G(A02, "Básico"), "", com_treino("assert ana.aprovado and not bruno.aprovado")),
(A02, "Intermediário", G(A02, "Intermediário"), "", com_treino(
    "assert dados == {'Aprovado': 4, 'Recuperação': 2, 'Pendente': 1, 'Reprovado': 1, 'Média da turma': 6.6}, dados")),
(A02, "Avançado", G(A02, "Avançado"), "", com_treino("assert homenageados == ['Carla Mendes']")),
# ============================================================ 03
(A03, "Básico", G(A03, "Básico"), "", com_treino("assert assunto == 'Resultado final — Turma 1A (2026)'")),
(A03, "Intermediário", G(A03, "Intermediário"), "", com_treino(
    "assert arquivo.read_bytes().startswith(b'%PDF')")),
(A03, "Avançado", G(A03, "Avançado"), "", com_treino(
    "assert 'Suas notas: 1º bim: 5,0, 2º bim: 6,5, 3º bim: 4,5, 4º bim: 6,0.' in msg.get_content()")),
# ============================================================ 04
(A04, "Básico", G(A04, "Básico"), "", com_treino("assert com.silencioso and not sem.silencioso")),
(A04, "Intermediário", G(A04, "Intermediário"), "", com_treino("""
import tempfile
import pytest
with pytest.MonkeyPatch.context() as mp:
    test_aprovados(Path(tempfile.mkdtemp()), mp)
print("teste de aprovados ok")""")),
(A04, "Avançado", G(A04, "Avançado"), "", com_treino("""
import tempfile
import pytest
with pytest.MonkeyPatch.context() as mp:
    test_envio(Path(tempfile.mkdtemp()), mp)
print("teste de envio ok")""")),
]
