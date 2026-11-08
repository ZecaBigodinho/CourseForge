"""Casos de teste do curso Automação com Python, Módulo 01 (arquivos e pastas).

O código vem das aulas: tanto os gabaritos quanto os scripts que a aula ensina. Cada caso roda
numa pasta temporária, com a pasta de treino criada pelo próprio criar_treino.py da aula 01.
"""
import re

from extrair import gabarito, texto_aula

# O extrair.py procura as aulas a partir de cursos/python_para_desktop; o ".." leva ao curso de automação.
MODULO = "../automacao_com_python/modulo_01_arquivos_e_pastas"


def G(aula, nivel):
    return gabarito(MODULO, aula, nivel)


def bloco(aula, trecho):
    """O bloco de código da aula (fora dos gabaritos) que contém o trecho."""
    # Como o blocos_python do extrair.py, mas aceitando blocos com título (```python title="x.py")
    texto = re.sub(r'^\?\?\? success "Gabarito.*?(?=^\S)', "", texto_aula(MODULO, aula) + "\n.", flags=re.S | re.M)
    blocos = re.findall(r"```python[^\n]*\n(.*?)```", texto, re.S)
    achados = [b for b in blocos if trecho in b]
    assert len(achados) == 1, f"{aula}: esperava 1 bloco com {trecho!r}, achei {len(achados)}"
    return achados[0]


TREINO = bloco("01_o_que_vale_automatizar.md", 'TREINO = Path("treino")')


def com_treino(verificacao: str, preparo: str = "") -> str:
    """Programa de teste: cria a pasta de treino, roda o código e confere o resultado."""
    verificacao = verificacao.strip().removeprefix("# === gabarito ===").strip()
    return (f"# === arquivo: criar_treino.py ===\n{TREINO}\n"
            f"# === arquivo: teste.py ===\nimport os\nfrom pathlib import Path\n"
            f"import criar_treino\ncriar_treino.main()\n{preparo}\n"
            f"# === gabarito ===\n{verificacao}\n")


def real(codigo: str) -> str:
    return codigo.replace("SIMULAR = True", "SIMULAR = False")


A01, A02, A03, A04, A05 = (
    "01_o_que_vale_automatizar.md", "02_pathlib.md", "03_mover_copiar_com_seguranca.md",
    "04_renomear_fotos_pela_data.md", "05_projeto_organizador.md",
)

DL = 'Path("treino", "Downloads")'
FOTOS = 'Path("treino", "Fotos")'

RENOMEAR = bloco(A04, "def ja_no_padrao")
ORGANIZAR = bloco(A05, "def planejar")
DESFAZER = bloco(A05, "def desfazer")

GABARITOS = [
# ============================================================ 01 pasta de treino
(A01, "criar_treino.py", TREINO, "", com_treino(f"""
assert len(list({DL}.iterdir())) == 16 and len(list({FOTOS}.iterdir())) == 6
criar_treino.main()  # segunda vez: só avisa
print("pasta de treino ok")
""")),
(A01, "Intermediário", G(A01, "Intermediário"), "",
 "# === gabarito ===\nassert len(DOWNLOADS) == 19 and DOWNLOADS[-1] == 'backup_celular.rar'\n"),
# ============================================================ 02 pathlib (só leitura)
(A02, "listar.py", bloco(A02, "tamanho_kb"), "", com_treino("# === gabarito ===")),
(A02, "procurar_pdfs.py", bloco(A02, 'rglob("*.pdf")'), "", com_treino("# === gabarito ===")),
(A02, "datas_das_fotos.py", bloco(A02, "fromtimestamp"), "", com_treino("# === gabarito ===")),
(A02, "resumo_pasta.py", bloco(A02, "Counter"), "", com_treino("# === gabarito ===\nassert tipos['.pdf'] == 3")),
(A02, "Básico", G(A02, "Básico"), "", com_treino("# === gabarito ===")),
(A02, "Intermediário", G(A02, "Intermediário"), "", com_treino(
    "# === gabarito ===\nassert [a.name for a in maiores] == ['sem_extensao', 'certificado_canva.pdf', 'anotacoes.txt']")),
(A02, "Avançado", G(A02, "Avançado"), "", com_treino(
    "# === gabarito ===\nassert sorted(espaco, key=espaco.get, reverse=True)[:3] == ['.pdf', '.txt', '(sem extensão)']")),
# ============================================================ 03 mover e copiar
(A03, "operacoes.py", bloco(A03, "copy2(base"), "", com_treino(
    "# === gabarito ===\nassert Path('treino/anotacoes_copia.txt').exists() and Path('treino/Downloads/anotacoes.txt').exists()")),
(A03, "destino_livre.py", bloco(A03, "while True"), "", com_treino(
    "# === gabarito ===\nassert destino_livre(teste).name == 'anotacoes (2).txt'")),
(A03, "mover_pdfs.py (simulação)", bloco(A03, "PDFs"), "", com_treino(
    "# === gabarito ===\nassert not Path('treino/PDFs').exists()")),
(A03, "mover_pdfs.py (real)", real(bloco(A03, "PDFs")), "", com_treino(
    "# === gabarito ===\nassert len(list(Path('treino/PDFs').glob('*.pdf'))) == 3 and not list(Path('treino/Downloads').glob('*.pdf'))")),
(A03, "Básico", G(A03, "Básico"), "", com_treino(
    "# === gabarito ===\nassert sorted(p.name for p in backup.iterdir()) == ['planilha_gastos.xlsx', 'trabalho_historia.docx']")),
(A03, "Intermediário", real(G(A03, "Intermediário")), "", com_treino(
    "# === gabarito ===\nassert sorted(p.name.lower() for p in destino.iterdir()) == ['foto_festa.jpg', 'img_0042.jpg', 'meme.png']",
    # um meme.png já na pasta de destino: o novo precisa virar "meme (2).png"
    "Path('treino/Imagens').mkdir(); Path('treino/Imagens/meme.png').write_text('antigo')"
).replace("== ['foto_festa.jpg', 'img_0042.jpg', 'meme.png']",
          "== ['foto_festa.jpg', 'img_0042.jpg', 'meme (2).png', 'meme.png'] and Path('treino/Imagens/meme.png').read_text() == 'antigo'")),
(A03, "Avançado", G(A03, "Avançado"), "", com_treino(
    "# === gabarito ===\nassert len(list(REVISAR.rglob('*.exe'))) == 1 and not list(Path('treino/Downloads').glob('*.exe'))")),
# ============================================================ 04 renomear fotos
(A04, "renomear_fotos.py (simulação)", RENOMEAR, "", com_treino(
    "# === gabarito ===\nassert Path('treino/Fotos/IMG_0001.jpg').exists()")),
(A04, "renomear_fotos.py (real, duas vezes)", real(RENOMEAR), "", com_treino(f"""
# === gabarito ===
nomes = sorted(p.name for p in {FOTOS}.iterdir())
assert nomes == ['2026-03-14_091205.jpg', '2026-03-14_091205_2.jpg', '2026-03-15_174031.jpg',
                 '2026-04-02_200344.jpeg', '2026-05-20_080000.jpg', '2026-06-01_123000.png'], nomes
main()  # segunda vez: nada muda
assert sorted(p.name for p in {FOTOS}.iterdir()) == nomes
print("renomeia certo e é idempotente")
""")),
(A04, "Básico", G(A04, "Básico"), "", com_treino("# === gabarito ===")),
(A04, "Intermediário", G(A04, "Intermediário"), "", com_treino(
    "# === gabarito ===\nassert meses == {'2026-03': 3, '2026-04': 1, '2026-05': 1, '2026-06': 1}")),
(A04, "Avançado", real(G(A04, "Avançado")), "", com_treino(f"""
# === gabarito ===
assert sorted(p.name for p in Path('treino/Fotos/2026/03').iterdir()) == ['IMG_0001.jpg', 'IMG_0002.jpg', 'IMG_0003.jpg']
assert not [p for p in {FOTOS}.iterdir() if p.is_file()]
print("organizado por ano e mês")
""")),
# ============================================================ 05 organizador
(A05, "organizar.py (responde n)", ORGANIZAR, "n\n", com_treino(
    "# === gabarito ===\nassert len([p for p in Path('treino/Downloads').iterdir() if p.is_file()]) == 16")),
(A05, "organizar.py + desfazer.py", ORGANIZAR, "s\n", com_treino(
    "# === gabarito ===\n"
    "assert sorted(p.name for p in Path('treino/Downloads/Documentos').iterdir())[:2] == ['anotacoes (2).txt', 'anotacoes.txt']\n"
    "assert Path('treino/Downloads/Documentos/anotacoes.txt').read_text() == 'antigo'\n"
    "relatorio = next(Path('treino/Downloads').glob('relatorio_*.csv'))\n"
    "main()  # segunda vez: nada para organizar\n"
    f"{DESFAZER}\n"
    "desfazer(relatorio)\n"
    "assert len([p for p in Path('treino/Downloads').iterdir() if p.is_file() and not p.name.startswith('relatorio_')]) == 16\n"
    "assert not Path('treino/Downloads/Imagens').exists() and Path('treino/Downloads/Documentos/anotacoes.txt').exists()\n"
    "print('organiza, relatório, desfaz')",
    # um arquivo "antigo" com o mesmo nome já em Documentos
    "Path('treino/Downloads/Documentos').mkdir(); Path('treino/Downloads/Documentos/anotacoes.txt').write_text('antigo')")),
(A05, "Básico", G(A05, "Básico"), "",
 "# === gabarito ===\nassert '.xlsx' in CATEGORIAS['Planilhas'] and '.xlsx' not in CATEGORIAS['Documentos']\n"),
(A05, "Intermediário", G(A05, "Intermediário"), "", com_treino(
    "# === gabarito ===\nassert categorias['Documentos'] == 8 and categorias['Imagens'] == 3",
    f"{ORGANIZAR.replace('if __name__', 'if False and __name__')}\nimport builtins; builtins.input = lambda *_: 's'; main()")),
(A05, "Avançado", G(A05, "Avançado"), "", com_treino(
    "# === gabarito ===\nassert len(plano) == 2 and len(recentes) == 14",
    "import time\nfor nome in ['anotacoes.txt', 'meme.png']:\n    os.utime(Path('treino/Downloads', nome), (time.time() - 30 * 86400,) * 2)")),
]
