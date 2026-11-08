"""Casos de teste do curso Automação com Python, Módulo 02 (planilhas, openpyxl).

O código vem das aulas. Cada caso roda numa pasta temporária, com as planilhas de treino criadas
pelo próprio criar_planilhas_treino.py da aula 01. Precisa do openpyxl instalado (a CI instala).
"""
import re

from extrair import gabarito, texto_aula

MODULO = "../automacao_com_python/modulo_02_planilhas"


def G(aula, nivel):
    return gabarito(MODULO, aula, nivel)


def bloco(aula, trecho):
    """O bloco de código da aula (fora dos gabaritos) que contém o trecho."""
    texto = re.sub(r'^\?\?\? success "Gabarito.*?(?=^\S)', "", texto_aula(MODULO, aula) + "\n.", flags=re.S | re.M)
    achados = [b for b in re.findall(r"```python[^\n]*\n(.*?)```", texto, re.S) if trecho in b]
    assert len(achados) == 1, f"{aula}: esperava 1 bloco com {trecho!r}, achei {len(achados)}"
    return achados[0]


A01, A02, A03, A04, A05 = (
    "01_ler_planilhas.md", "02_escrever_e_formatar.md", "03_formulas_e_condicional.md",
    "04_juntar_e_limpar.md", "05_projeto_boletim.md",
)

CRIAR = bloco(A01, 'TREINO = Path("treino_planilhas")')
BOLETIM = bloco(A05, "def ler_turma")
JUNTAR = bloco(A04, "todas_as_turmas.csv")


def com_treino(verificacao: str = "", preparo: str = "", arquivos: str = "") -> str:
    """Programa de teste: cria as planilhas de treino, roda o código e confere o resultado."""
    verificacao = verificacao.strip().removeprefix("# === gabarito ===").strip()
    return (f"# === arquivo: criar_planilhas_treino.py ===\n{CRIAR}\n{arquivos}"
            f"# === arquivo: teste.py ===\nfrom pathlib import Path\nfrom openpyxl import load_workbook\n"
            f"import criar_planilhas_treino\ncriar_planilhas_treino.main()\n{preparo}\n"
            f"# === gabarito ===\n{verificacao}\n")


SAIDA = "Path('treino_planilhas/saida')"

GABARITOS = [
# ============================================================ 01 ler
(A01, "criar_planilhas_treino.py", CRIAR, "", com_treino(
    "assert len(list(Path('treino_planilhas/turmas').glob('*.xlsx'))) == 3\ncriar_planilhas_treino.main()")),
(A01, "ler_notas.py", bloco(A01, "sheetnames"), "", com_treino("assert aba.max_row == 13")),
(A01, "ler_como_dicionarios.py", bloco(A01, "def ler_tabela"), "", com_treino(
    "assert len(alunos) == 12 and alunos[4]['2º bim'] == '7,5' and alunos[5]['4º bim'] is None")),
(A01, "Básico", G(A01, "Básico"), "", com_treino()),
(A01, "Intermediário", G(A01, "Intermediário"), "", com_treino("assert mais_faltas[1] == 'Gabriela Nunes'")),
(A01, "Avançado", G(A01, "Avançado"), "", com_treino("assert abaixo == ['Gabriela Nunes', 'Larissa Freitas'], abaixo")),
# ============================================================ 02 escrever
(A02, "lista_de_chamada.py", bloco(A02, "lista_de_chamada_1A"), "", com_treino("""
a = load_workbook(DESTINO)['Chamada']
assert a['A1'].font.b and a.freeze_panes == 'A2' and a['C13'].value == 'Mateus Ribeiro'
print('lista de chamada ok')""")),
(A02, "Básico", G(A02, "Básico"), "", com_treino("assert load_workbook(destino)['Contatos'].max_row == 4")),
(A02, "Intermediário", G(A02, "Intermediário"), "", com_treino(
    "assert [r[0] for r in load_workbook(destino).active.iter_rows(min_row=2, values_only=True)] == "
    "['Diego Rocha', 'Gabriela Nunes', 'Larissa Freitas']")),
(A02, "Avançado", G(A02, "Avançado"), "", com_treino(
    "assert load_workbook(destino).sheetnames == ['1A', '1B', '1C']")),
# ============================================================ 03 fórmulas
(A03, "medias_com_formulas.py", bloco(A03, "fill=vermelho"), "", com_treino("""
b = load_workbook(DESTINO)['Notas']
assert b['H2'].value == '=AVERAGE(C2:F2)' and b['H15'].value == '=AVERAGE(H2:H13)'
assert b['H16'].value == '=COUNTIF(H2:H13,"<6")' and len(b.conditional_formatting) == 1
assert load_workbook(DESTINO, data_only=True)['Notas']['H2'].value is None  # ninguém calculou""")),
(A03, "Básico", G(A03, "Básico"), "", com_treino("assert load_workbook(destino)['Notas']['I2'].value == '=SUM(C2:F2)'")),
(A03, "Intermediário", G(A03, "Intermediário"), "", com_treino(
    "assert conferir['H2'].value == 8.125 and conferir['H6'].value is None and conferir['H7'].value is None")),
(A03, "Avançado", G(A03, "Avançado"), "", com_treino(
    "assert load_workbook(destino)['Notas']['G15'].value == '=COUNTIF(G2:G13,\">20\")'")),
# ============================================================ 04 juntar e limpar
(A04, "juntar_turmas.py", JUNTAR, "", com_treino("""
assert len(linhas) == 8
texto = (SAIDA / 'todas_as_turmas.csv').read_text(encoding='utf-8-sig').splitlines()
assert texto[1] == '1A;2026001;Ana Souza;8,5;7;9;8;4', texto[1]""")),
(A04, "converter_nota.py", bloco(A04, "def converter_nota"), "", com_treino("""
assert converter_nota('7,5') == (7.5, '') and converter_nota(None)[0] is None
assert converter_nota(11)[1].startswith('fora') and converter_nota('dez')[1].startswith('valor')""")),
(A04, "Básico", G(A04, "Básico"), "", com_treino("assert len(problemas) == 2")),
(A04, "Intermediário", G(A04, "Intermediário"), "", com_treino(
    "assert round(media, 4) == 7.3125", JUNTAR)),
(A04, "Avançado", G(A04, "Avançado"), "", com_treino("assert cabecalhos_iguais(arquivos)")),
# ============================================================ 05 boletim
(A05, "boletim.py", BOLETIM, "", com_treino(f"""
livro = load_workbook(next({SAIDA}.glob('boletim_1A_*.xlsx')))
assert livro.sheetnames == ['Boletim', 'Resumo', 'Problemas']
b = livro['Boletim']
medias = {{r[1]: r[6] for r in b.iter_rows(min_row=2, values_only=True)}}
assert medias['Diego Rocha'] == 4.3 and medias['Elisa Prado'] == 7.3 and medias['Ana Souza'] == 8.1, medias
assert medias['Felipe Torres'] is None and medias['João Pedro Melo'] is None
situacoes = {{r[1]: r[8] for r in b.iter_rows(min_row=2, values_only=True)}}
assert situacoes['Larissa Freitas'] == 'Reprovado' and situacoes['Diego Rocha'] == 'Recuperação'
resumo = dict(r for r in livro['Resumo'].iter_rows(values_only=True) if r[0])
assert resumo['Aprovado'] == 6 and resumo['Média da turma'] == 6.6, resumo
assert livro['Problemas'].max_row == 3
assert arredondar(4.25) == 4.3 and round(4.25, 1) == 4.2
print('boletim ok')""")),
(A05, "Básico", G(A05, "Básico"), "",
 "# === gabarito ===\nassert MEDIA_APROVACAO == 7.0 and MEDIA_RECUPERACAO == 5.0\n"),
(A05, "Básico (efeito)", BOLETIM.replace("MEDIA_APROVACAO = 6.0", "MEDIA_APROVACAO = 7.0")
 .replace("MEDIA_RECUPERACAO = 4.0", "MEDIA_RECUPERACAO = 5.0"), "", com_treino(f"""
b = load_workbook(next({SAIDA}.glob('boletim_1A_*.xlsx')))['Boletim']
s = {{r[1]: r[8] for r in b.iter_rows(min_row=2, values_only=True)}}
assert s['Isabela Costa'] == 'Recuperação' and s['Diego Rocha'] == 'Reprovado' and s['Elisa Prado'] == 'Aprovado', s""")),
(A05, "Intermediário", G(A05, "Intermediário"), "", com_treino(
    "assert [n for n, _ in podio] == ['Carla Mendes', 'Heitor Alves', 'Ana Souza'], podio",
    "import boletim\nboletim.main()", f"# === arquivo: boletim.py ===\n{BOLETIM}\n")),
(A05, "Avançado", G(A05, "Avançado"), "", com_treino(
    f"assert len(list({SAIDA}.glob('boletim_*.xlsx'))) == 3", "", f"# === arquivo: boletim.py ===\n{BOLETIM}\n")),
]
