"""Casos de teste do curso Automação com Python, Módulo 03 (documentos e PDFs).

O código vem das aulas. Cada caso roda numa pasta temporária com os arquivos de treino criados pelo
próprio criar_treino_documentos.py da aula 01 e com os scripts das aulas que os gabaritos importam.
Precisa de openpyxl, python-docx, fpdf2 e Pillow (a CI instala).
"""
import re

from extrair import gabarito, texto_aula

MODULO = "../automacao_com_python/modulo_03_documentos_e_pdfs"


def G(aula, nivel):
    return gabarito(MODULO, aula, nivel)


def bloco(aula, trecho):
    """O bloco de código da aula (fora dos gabaritos) que contém o trecho."""
    texto = re.sub(r'^\?\?\? success "Gabarito.*?(?=^\S)', "", texto_aula(MODULO, aula) + "\n.", flags=re.S | re.M)
    achados = [b for b in re.findall(r"```python[^\n]*\n(.*?)```", texto, re.S) if trecho in b]
    assert len(achados) == 1, f"{aula}: esperava 1 bloco com {trecho!r}, achei {len(achados)}"
    return achados[0]


A01, A02, A03, A04, A05 = (
    "01_documentos_word.md", "02_pdf_com_fpdf2.md", "03_imagens_em_lote.md",
    "04_certificados_e_crachas.md", "05_projeto_emissao.md",
)

CRIAR = bloco(A01, 'TREINO = Path("treino_docs")')
SCRIPTS = {  # os arquivos que as aulas ensinam e que outros scripts importam
    "preencher_declaracoes.py": bloco(A01, "def substituir"),
    "certificado.py": bloco(A02, "def desenhar_certificado"),
    "certificados_em_lote.py": bloco(A04, "def nome_de_arquivo"),
    "emitir_certificados.py": bloco(A05, "def codigo_de_validacao"),
}
ARQUIVOS = "".join(f"# === arquivo: {nome} ===\n{codigo}\n" for nome, codigo in SCRIPTS.items())


def com_treino(verificacao: str = "", preparo: str = "") -> str:
    """Programa de teste: cria os arquivos de treino, roda o código e confere o resultado."""
    verificacao = verificacao.strip().removeprefix("# === gabarito ===").strip()
    return (f"# === arquivo: criar_treino_documentos.py ===\n{CRIAR}\n{ARQUIVOS}"
            f"# === arquivo: teste.py ===\nfrom pathlib import Path\n"
            f"import criar_treino_documentos\ncriar_treino_documentos.main()\n{preparo}\n"
            f"# === gabarito ===\n{verificacao}\n")


def paginas(caminho: str) -> str:
    """Expressão que conta as páginas de um PDF gerado pelo fpdf2 (sem biblioteca extra)."""
    return f"Path({caminho!r}).read_bytes().count(b'/Type /Page\\n')"


SAIDA = "treino_docs/saida"

GABARITOS = [
# ============================================================ 01 Word
(A01, "criar_treino_documentos.py", CRIAR, "", com_treino("""
from PIL import Image
assert len(list(Path('treino_docs/fotos').iterdir())) == 5
assert Image.open('treino_docs/fotos/IMG_0101.jpg').getexif().get_ifd(0x8769)[0x9003] == '2026:09:12 14:05:10'
criar_treino_documentos.main()""")),
(A01, "primeiro_documento.py", bloco(A01, "Lista de materiais"), "", com_treino("""
from docx import Document
d = Document(destino)
assert d.paragraphs[0].text == 'Lista de materiais da oficina' and len(d.tables[0].rows) == 4""")),
(A01, "preencher_declaracoes.py", SCRIPTS["preencher_declaracoes.py"], "", com_treino(f"""
from docx import Document
arquivos = sorted(Path('{SAIDA}/declaracoes').iterdir())
assert len(arquivos) == 10
texto = ' '.join(p.text for p in Document(arquivos[0]).paragraphs)
assert 'Ana Souza, matrícula 2026001' in texto and '{{{{' not in texto and 'Prof. Pedro Paulo' in texto, texto
assert data_por_extenso(__import__('datetime').date(2026, 3, 1)) == '1 de março de 2026'""")),
(A01, "Básico", G(A01, "Básico"), "", com_treino("assert destino.exists()")),
(A01, "Intermediário", G(A01, "Intermediário"), "", com_treino(
    "assert marcadores == ['carga', 'curso', 'data', 'fim', 'frequencia', 'inicio', 'matricula', 'nome', 'responsavel']")),
(A01, "Avançado", G(A01, "Avançado"), "", com_treino("assert sobrando == ['data']")),
# ============================================================ 02 PDF
(A02, "certificado.py", SCRIPTS["certificado.py"], "", com_treino(
    f"assert {paginas(SAIDA + '/certificado_teste.pdf')} == 1")),
(A02, "acentos ok, travessão não (fonte padrão)", "", "", com_treino("""
from fpdf import FPDF
from fpdf.errors import FPDFUnicodeEncodingException
pdf = FPDF(); pdf.add_page(); pdf.set_font('Helvetica', '', 12)
pdf.cell(0, 10, 'Certificação, ç, ã, º')
try:
    pdf.cell(0, 10, 'Curso — módulo')
    raise SystemExit('o travessão deveria dar erro')
except FPDFUnicodeEncodingException:
    print('travessão recusado, como a aula diz')""")),
(A02, "Básico", G(A02, "Básico"), "", com_treino(f"assert {paginas(SAIDA + '/certificado_bruno.pdf')} == 1")),
(A02, "Intermediário", G(A02, "Intermediário"), "", com_treino("assert destino.stat().st_size > 1000")),
(A02, "Avançado", G(A02, "Avançado"), "", com_treino(f"assert {paginas(SAIDA + '/dois_tipos.pdf')} == 2")),
# ============================================================ 03 imagens
(A03, "preparar_fotos.py (duas vezes)", bloco(A03, "def preparar"), "", com_treino(f"""
from PIL import Image
prontas = sorted(p.name for p in Path('{SAIDA}/fotos_prontas').iterdir())
assert len(prontas) == 5 and prontas[0] == '2026-09-12_140510_IMG_0101.jpg', prontas
main()
assert sorted(p.name for p in Path('{SAIDA}/fotos_prontas').iterdir()) == prontas  # não duplica
foto = Image.open(Path('{SAIDA}/fotos_prontas') / prontas[0])
assert foto.size == (1600, 1067) and not dict(foto.getexif().get_ifd(0x8769))  # sem EXIF na cópia
png = Image.open(next(Path('{SAIDA}/fotos_prontas').glob('*print_tela.jpg')))
assert png.mode == 'RGB' and png.getpixel((5, 5)) == (255, 255, 255)  # transparente virou branco
print('fotos ok')""")),
(A03, "Básico", G(A03, "Básico"), "", com_treino()),
(A03, "Intermediário", G(A03, "Intermediário"), "", com_treino("assert sem_data == ['IMG_0104.jpg', 'print_tela.png']")),
(A03, "Avançado", G(A03, "Avançado"), "", com_treino(f"""
from PIL import Image
miniaturas = list(Path('{SAIDA}/miniaturas').iterdir())
assert len(miniaturas) == 5 and all(Image.open(m).size == (300, 300) for m in miniaturas)""")),
# ============================================================ 04 lote e crachás
(A04, "certificados_em_lote.py", SCRIPTS["certificados_em_lote.py"], "", com_treino(f"""
assert len(list(Path('{SAIDA}/certificados').glob('certificado_*.pdf'))) == 10
assert {paginas(SAIDA + '/certificados/todos_os_certificados.pdf')} == 10
assert nome_de_arquivo('João Pedro Melo') == 'joao_pedro_melo'""")),
(A04, "crachas.py", bloco(A04, "COLUNAS, LINHAS"), "", com_treino(
    f"assert {paginas(SAIDA + '/crachas.pdf')} == 2 and pdf.pages_count == 2")),
(A04, "Básico", G(A04, "Básico"), "", com_treino(
    "assert list(resultados.values()) == ['maria_d_avila', 'jose_da_conceicao', 'ana__souza', 'turma_1_a'], resultados")),
(A04, "Intermediário", G(A04, "Intermediário"), "", com_treino(f"assert {paginas(SAIDA + '/crachas_visitantes.pdf')} == 1")),
(A04, "Avançado", G(A04, "Avançado"), "", com_treino(
    "assert len(emitidos) == 7 and 'Felipe Torres' in emitidos and len(de_fora) == 3\n"
    f"assert not Path('{SAIDA}/certificados').exists()  # importar não gerou os certificados da aula")),
# ============================================================ 05 projeto
(A05, "emitir_certificados.py", SCRIPTS["emitir_certificados.py"], "", com_treino(f"""
import csv
pasta = Path('{SAIDA}/emissao')
with open(pasta / 'relatorio_emissao.csv', newline='', encoding='utf-8-sig') as arq:
    linhas = list(csv.DictReader(arq, delimiter=';'))
assert [l['Documento'] for l in linhas].count('Certificado') == 7
assert linhas[0]['Código'] == 'F0907-66A16', linhas[0]
assert (pasta / 'declaracao_diego_rocha.docx').exists() and (pasta / 'certificado_felipe_torres.pdf').exists()
assert {paginas(SAIDA + '/emissao/certificados_para_imprimir.pdf')} == 7
assert not Path('{SAIDA}/certificados').exists()  # nenhum import gerou arquivos de outras aulas
print('emissão ok')""")),
(A05, "Básico", G(A05, "Básico"), "", "# === gabarito ===\nassert FREQUENCIA_MINIMA == 80\n"),
(A05, "Intermediário", G(A05, "Intermediário"), "  f0907-66a16 \n", com_treino(
    "assert encontrado['Nome'] == 'Ana Souza'", "import emitir_certificados\nemitir_certificados.main()")),
(A05, "Avançado", G(A05, "Avançado"), "", com_treino("assert len(set(primeira)) == 10")),
]
