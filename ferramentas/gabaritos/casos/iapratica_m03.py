"""Casos de teste do curso IA na prática com Python, Módulo 03 (IA com os seus documentos).

Nenhum caso chama a API: o Gemini é substituído pelo ClienteFalso, ou o programa usa o modo simulado.
O regulamento de treino é criado pelo criar_regulamento.py da aula 01.
Precisa de pypdf, fpdf2, google-genai e python-dotenv (a CI instala).
"""
import re

from extrair import gabarito, texto_aula

M01 = "../ia_na_pratica_com_python/modulo_01_api_de_ia"
MODULO = "../ia_na_pratica_com_python/modulo_03_documentos"
A01, A02, A03, A04, A05 = (
    "01_ler_documentos.md", "02_dividir_em_trechos.md", "03_buscar_trechos.md",
    "04_responder_com_fonte.md", "05_projeto_tira_duvidas.md",
)


def G(aula, nivel):
    return gabarito(MODULO, aula, nivel)


def bloco_titulo(modulo, aula, titulo):
    achados = re.findall(rf'```python title="{re.escape(titulo)}"\n(.*?)```', texto_aula(modulo, aula), re.S)
    assert len(achados) == 1, f"{aula}: esperava 1 bloco {titulo!r}, achei {len(achados)}"
    return achados[0]


ARQUIVOS_AULAS = {
    "erros_ia.py": bloco_titulo(M01, "02_primeira_chamada.md", "erros_ia.py"),
    "cliente_falso.py": bloco_titulo(M01, "02_primeira_chamada.md", "cliente_falso.py"),
    "criar_regulamento.py": bloco_titulo(MODULO, A01, "criar_regulamento.py"),
    "ler_documento.py": bloco_titulo(MODULO, A01, "ler_documento.py"),
    "trechos.py": bloco_titulo(MODULO, A02, "trechos.py"),
    "buscar.py": bloco_titulo(MODULO, A03, "buscar.py"),
    "responder.py": bloco_titulo(MODULO, A04, "responder.py"),
    "tira_duvidas.py": bloco_titulo(MODULO, A05, "tira_duvidas.py"),
}
PERGUNTAS = next(b for b in re.findall(r"```text\n(.*?)```", texto_aula(MODULO, A05), re.S)
                 if b.startswith("pergunta;secao_esperada"))
ARQUIVOS = "".join(f"# === arquivo: {nome} ===\n{codigo}\n" for nome, codigo in ARQUIVOS_AULAS.items())


def com_pasta(verificacao: str = "", preparo: str = "") -> str:
    verificacao = verificacao.strip().removeprefix("# === gabarito ===").strip()
    return (f"{ARQUIVOS}# === arquivo: teste.py ===\nimport os\nfrom pathlib import Path\n"
            f"os.environ.pop('GEMINI_API_KEY', None)\n"
            f"import criar_regulamento\ncriar_regulamento.main()\n"
            f"Path('perguntas_teste.csv').write_text({PERGUNTAS!r}, encoding='utf-8')\n{preparo}\n"
            f"# === gabarito ===\n{verificacao}\n")


TRECHOS = ("from ler_documento import ler_paginas\nfrom trechos import dividir\n"
           "trechos = dividir(ler_paginas(Path('treino_docs') / 'regulamento_escola.pdf'))\n")

GABARITOS = [
# ============================================================ 01
(A01, "regulamento de treino e leitura", "", "", com_pasta("""
from ler_documento import ler_paginas
paginas = ler_paginas(Path('treino_docs/regulamento_escola.pdf'))
assert len(paginas) == 3 and '7h10' in paginas[0] and '8. Biblioteca' in paginas[2]
criar_regulamento.main()  # segunda vez: só avisa""")),
(A01, "Básico", G(A01, "Básico"), "", com_pasta("assert len(paginas) == 3 and 1700 < total < 1900")),
(A01, "Intermediário", G(A01, "Intermediário"), "", com_pasta("assert len(paginas) == 1")),
(A01, "Avançado", G(A01, "Avançado"), "", com_pasta("assert resultado is False")),
# ============================================================ 02
(A02, "dividir: 9 seções com página", "", "", com_pasta(TRECHOS + """
assert [t.titulo[:2] for t in trechos] == ['1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.']
assert [t.pagina for t in trechos] == [1, 1, 1, 2, 2, 2, 3, 3, 3] and '\\n' not in trechos[0].texto""")),
(A02, "Básico", G(A02, "Básico"), "", com_pasta("assert maior == 244 and len(trechos) == 9")),
(A02, "Intermediário", G(A02, "Intermediário"), "", com_pasta("assert len(trechos) == 3 and trechos[1].titulo == '2. Tem armário para alunos?'")),
(A02, "Avançado", G(A02, "Avançado"), "", com_pasta("assert len(partes) == 2 and all(p.endswith('.') for p in partes)")),
# ============================================================ 03
(A03, "buscar: acertos e os dois limites", "", "", com_pasta(TRECHOS + """
from buscar import buscar
assert buscar('Quantos livros posso pegar na biblioteca?', trechos)[0][1].titulo == '8. Biblioteca'
assert buscar('Qual a nota para passar de ano?', trechos) == []
assert buscar('Tem cantina na escola?', trechos)[0][1].titulo == '7. Uniforme'""")),
(A03, "Básico", G(A03, "Básico"), "", com_pasta(
    "assert pergunta == ['livro', 'pegar', 'biblioteca'] and trecho == ['aluno', 'pegar', 'ate', 'livro', 'vez']")),
(A03, "Intermediário", G(A03, "Intermediário"), "", com_pasta("assert [t.titulo for _, t in achados][:2] == ['6. Celular', '7. Uniforme']")),
(A03, "Avançado", G(A03, "Avançado"), "", com_pasta("assert 0 <= acertos <= 5")),
# ============================================================ 04
(A04, "responder: ids inventados e cantina", "", "", com_pasta(TRECHOS + """
import json
from cliente_falso import ClienteFalso
from responder import responder, responder_simulado
r = responder(ClienteFalso(json.dumps({'encontrou': True, 'resposta': 'Até 2 livros.', 'trechos': ['T8', 'T99']})),
              'gemini-3.8-flash', 'Quantos livros posso pegar na biblioteca?', trechos)
assert r['fonte'] == '8. Biblioteca, página 3'
falso = ClienteFalso(json.dumps({'encontrou': False, 'resposta': '', 'trechos': []}))
assert responder(falso, 'gemini-3.8-flash', 'Tem cantina na escola?', trechos)['encontrou'] is False and len(falso.pedidos) == 1
assert responder_simulado('Perdi a prova, o que faço?', trechos)['encontrou'] is False  # limite sem IA, como a aula diz""")),
(A04, "Básico", G(A04, "Básico"), "", com_pasta(
    "assert [r['encontrou'] for r in resultados] == [True, True, False] and 'Laboratório' in resultados[1]['fonte']")),
(A04, "Intermediário", G(A04, "Intermediário"), "", com_pasta(
    "assert [r['encontrou'] for r in resultados] == [True, False, False]")),
(A04, "Avançado", G(A04, "Avançado"), "", com_pasta("assert resultado['encontrou'] is False and len(falso.pedidos) == 0")),
# ============================================================ 05
(A05, "tira_duvidas: avaliação 9 de 11", "", "", com_pasta("""
from tira_duvidas import main
assert main(['treino_docs/regulamento_escola.pdf', '--avaliar', 'perguntas_teste.csv']) == 1
assert main(['nao_existe.pdf']) == 2""")),
(A05, "Básico", G(A05, "Básico"), "", com_pasta("assert codigo == 1")),
(A05, "Intermediário", G(A05, "Intermediário"), "", com_pasta("assert respondidas == 2 and len(registro) == 3")),
(A05, "Avançado", G(A05, "Avançado"), "", com_pasta("assert codigo == 0")),
]
