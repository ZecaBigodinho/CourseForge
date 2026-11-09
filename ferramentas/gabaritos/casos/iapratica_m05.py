"""Casos de teste do curso IA na prática com Python, Módulo 05 (Projeto final: Atendente da Padaria).

Nenhum caso chama a API: o Gemini é substituído pelo ClienteFalso, ou o programa usa as regras.
As janelas (CustomTkinter) são testadas com a camada _gui.py. Os testes pytest das aulas rodam aqui também.
Precisa de google-genai, python-dotenv, openpyxl, customtkinter e pytest (a CI instala).
"""
import re

from extrair import gabarito, texto_aula

M01 = "../ia_na_pratica_com_python/modulo_01_api_de_ia"
M02 = "../ia_na_pratica_com_python/modulo_02_tarefas_uteis"
M04 = "../ia_na_pratica_com_python/modulo_04_seguranca_custos_testes"
MODULO = "../ia_na_pratica_com_python/modulo_05_projeto_final"
A01, A02, A03, A04, A05 = (
    "01_planejando_o_atendente.md", "02_encomendas_com_regras.md", "03_registro_e_linha_de_comando.md",
    "04_a_janela.md", "05_entrega_e_certificado.md",
)
P04 = "05_projeto_bateria_de_testes.md"


def G(aula, nivel):
    return gabarito(MODULO, aula, nivel)


def bloco_titulo(modulo, aula, titulo, linguagem="python"):
    achados = re.findall(rf'```{linguagem} title="{re.escape(titulo)}"\n(.*?)```', texto_aula(modulo, aula), re.S)
    assert len(achados) == 1, f"{aula}: esperava 1 bloco {titulo!r}, achei {len(achados)}"
    return achados[0]


def bloco_texto_que_comeca(modulo, aula, inicio):
    return next(b for b in re.findall(r"```text\n(.*?)```", texto_aula(modulo, aula), re.S) if b.startswith(inicio))


# O teste do Módulo 04, como a aula 02 manda atualizar (o resultado ganhou a chave "encomenda")
TESTE_ATENDENTE_M04 = bloco_titulo(M04, P04, "testes/test_atendente.py")
ATUALIZADA = re.search(r"```python\n(    assert atender\(\"Tem coxinha hoje\".*?)\n```", texto_aula(MODULO, A02)).group(1)
ANTIGA = next(l for l in TESTE_ATENDENTE_M04.splitlines() if l.startswith('    assert atender("Tem coxinha hoje"'))
TESTE_ATENDENTE_NOVO = TESTE_ATENDENTE_M04.replace(ANTIGA, ATUALIZADA)
assert TESTE_ATENDENTE_NOVO != TESTE_ATENDENTE_M04

ARQUIVOS_AULAS = {
    "erros_ia.py": bloco_titulo(M01, "02_primeira_chamada.md", "erros_ia.py"),
    "cliente_falso.py": bloco_titulo(M01, "02_primeira_chamada.md", "cliente_falso.py"),
    "classificar.py": bloco_titulo(M02, "01_classificar_mensagens.md", "classificar.py"),
    "extrair.py": bloco_titulo(M02, "02_extrair_json.md", "extrair.py"),
    "privacidade.py": bloco_titulo(M04, "01_dados_pessoais.md", "privacidade.py"),
    "protecao.py": bloco_titulo(M04, "02_prompt_injection.md", "protecao.py"),
    "cliente_seguro.py": bloco_titulo(M04, "03_limites_erros_custos.md", "cliente_seguro.py"),
    "padaria.py": bloco_titulo(M04, P04, "padaria.py"),
    "bateria.py": bloco_titulo(M04, P04, "bateria.py"),
    "testes/conftest.py": bloco_titulo(M04, "04_testes_automaticos.md", "testes/conftest.py"),
    "testes/test_seguranca.py": bloco_titulo(M04, "04_testes_automaticos.md", "testes/test_seguranca.py"),
    "testes/test_atendente.py": TESTE_ATENDENTE_NOVO,
    "encomendas.py": bloco_titulo(MODULO, A02, "encomendas.py"),
    "atendente.py": bloco_titulo(MODULO, A02, "atendente.py"),
    "testes/test_encomendas.py": bloco_titulo(MODULO, A02, "testes/test_encomendas.py"),
    "registro.py": bloco_titulo(MODULO, A03, "registro.py"),
    "pao_quente.py": bloco_titulo(MODULO, A03, "pao_quente.py"),
    "testes/test_registro.py": bloco_titulo(MODULO, A03, "testes/test_registro.py"),
    "janela.py": bloco_titulo(MODULO, A04, "janela.py"),
}
CASOS_CSV = bloco_titulo(M04, P04, "casos_atendente.csv", "text")
MENSAGENS_CSV = bloco_titulo(MODULO, A01, "mensagens_padaria.csv", "text")
NOVOS_CASOS = bloco_texto_que_comeca(MODULO, A05, "14;")
ARQUIVOS = "".join(f"# === arquivo: {nome} ===\n{codigo}\n" for nome, codigo in ARQUIVOS_AULAS.items())

PYTEST = """
import subprocess, sys
def pytest(*alvos):
    r = subprocess.run([sys.executable, '-m', 'pytest', '-q', '-p', 'no:cacheprovider', *alvos],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    print(r.stdout[-3000:], r.stderr[-2000:])
    return r.stdout.strip().splitlines()[-1]
"""


def com_pasta(verificacao: str = "", arquivos_extra: str = "", gui: bool = False) -> str:
    verificacao = verificacao.strip().removeprefix("# === gabarito ===").strip()
    return (f"{ARQUIVOS}{arquivos_extra}\n# === arquivo: teste.py ===\nimport os\nfrom pathlib import Path\n"
            f"os.environ.pop('GEMINI_API_KEY', None)\n"
            f"Path('casos_atendente.csv').write_text({CASOS_CSV!r}, encoding='utf-8')\n"
            f"Path('mensagens_padaria.csv').write_text({MENSAGENS_CSV!r}, encoding='utf-8')\n{PYTEST}\n"
            f"{'import _gui' if gui else ''}\n# === gabarito ===\n{verificacao}\n")


def com_arquivo(aula, nivel, verificacao):
    """Gabaritos que SÃO arquivos (conferir_entrega.py): entram na pasta, e o teste.py os usa."""
    return (aula, nivel, "", "", com_pasta(verificacao, arquivos_extra=G(aula, nivel)))


# Uma "IA" falsa que acerta: classifica pelas regras (e entende a pergunta sem "?"), extrai e responde
IA_ESPERTA = """
import json
import google.genai as genai
import atendente
from classificar import classificar_simulado
from cliente_falso import ClienteFalso
from extrair import extrair_simulado

def esperta(pedido):
    texto = pedido['input'].split('\\n')[1] if pedido['input'].startswith('<mensagem>') else pedido['input']
    if 'response_format' in pedido:
        from datetime import date
        dados, _ = extrair_simulado(texto, date.today())
        if not dados:
            return json.dumps({'produto': '', 'quantidade': 0, 'data_entrega': ''})
        return json.dumps({'produto': dados['produto'], 'quantidade': dados['quantidade'],
                           'data_entrega': dados['data_entrega'].isoformat() if dados['data_entrega'] else ''})
    categoria = 'dúvida' if texto == 'Tem coxinha hoje' else classificar_simulado(texto)
    if 'Responda com UMA palavra' in pedido['system_instruction']:
        return categoria
    return atendente.responder_simulado(texto, categoria)

os.environ['GEMINI_API_KEY'] = 'chave-falsa-para-teste'
genai.Client = lambda *args, **kwargs: ClienteFalso(esperta)
"""

NOVOS = f"Path('casos_atendente.csv').write_text(Path('casos_atendente.csv').read_text(encoding='utf-8') + {NOVOS_CASOS!r}, encoding='utf-8')\n"

GABARITOS = [
# ============================================================ 01
(A01, "Básico", G(A01, "Básico"), "", com_pasta("assert faltando == []")),
(A01, "Intermediário", G(A01, "Intermediário"), "", com_pasta(
    "assert contagem.most_common() == [('pedido', 5), ('dúvida', 2), ('revisar', 2), ('reclamação', 1), ('elogio', 1), ('outro', 1)]")),
# ============================================================ 02
(A02, "encomendas, pedido com IA e o teste atualizado", "", "", com_pasta("""
import json, shutil
from datetime import date
from encomendas import montar_encomenda
from atendente import atender
from cliente_falso import ClienteFalso
e, motivo = montar_encomenda('Quero 20 coxinhas para amanhã', date(2026, 11, 9))
assert e.resumo() == '20 × coxinha para 10/11 (total R$ 140,00)'
assert montar_encomenda('Quero 3 pizzas para amanhã', date(2026, 11, 9)) == (None, 'produto fora do cardápio: pizzas')
# o teste do Módulo 04, sem a atualização, falha como a aula mostra
Path('testes_m04').mkdir()
shutil.copy('testes/conftest.py', 'testes_m04/conftest.py')
Path('testes_m04/test_atendente.py').write_text(""" + repr(TESTE_ATENDENTE_M04) + """, encoding='utf-8')
assert pytest('testes/test_seguranca.py', 'testes_m04/test_atendente.py').startswith('1 failed, 28 passed')
shutil.rmtree('testes_m04')
assert pytest('testes/test_seguranca.py', 'testes/test_atendente.py', 'testes/test_encomendas.py').startswith('40 passed')""")),
(A02, "Básico", G(A02, "Básico"), "", com_pasta(
    "assert [e.resumo() if e else m for e, m in resultados] == ['2 × bolo de cenoura para 14/11 (total R$ 70,00)', "
    "'10 × sonho para 10/11 (total R$ 65,00)', 'produto fora do cardápio: bolo de chocolate', "
    "'quantidade acima de 100: a equipe confirma']")),
(A02, "Intermediário", G(A02, "Intermediário"), "", com_pasta(
    "assert [bool(e) for e, _ in resultados] == [False, True, True]\n"
    "assert resultados[0][1] == 'torta de frango precisa de 2 dias de antecedência'")),
(A02, "Avançado", G(A02, "Avançado"), "", com_pasta(
    "assert saida['encomenda'] is None and saida['revisar'] == \"pedido incompleto: quantidade estranha: 'vinte'\"")),
# ============================================================ 03
(A03, "lote, planilha e pytest: 42 testes", "", "", com_pasta("""
from openpyxl import load_workbook
from pao_quente import main
assert main(['--simulado', 'lote', 'mensagens_padaria.csv']) == 0
livro = load_workbook('atendimentos.xlsx')
assert {a.title: a.max_row - 1 for a in livro} == {'Atendimentos': 12, 'Encomendas': 2, 'Revisar': 5}
motivos = [l[2] for l in livro['Revisar'].iter_rows(min_row=2, values_only=True)]
assert motivos == ['pedido incompleto: sem data de entrega', 'pedido incompleto: produto fora do cardápio: pizzas',
                   'pedido incompleto: quantidade acima de 100: a equipe confirma', 'dado sensível: saúde',
                   'possível prompt injection: ignore, instrucoes']
assert livro['Atendimentos']['C5'].value == 'Quero 2 bolos de fubá, me liga no [telefone]'
assert [l[4] for l in livro['Encomendas'].iter_rows(min_row=2, values_only=True)] == [140, 60]
assert pytest('testes').startswith('42 passed')""")),
(A03, "Básico", G(A03, "Básico"), "", com_pasta(
    "assert codigo == 0 and linhas == {'Atendimentos': 12, 'Encomendas': 2, 'Revisar': 5}")),
(A03, "Intermediário", G(A03, "Intermediário"), "", com_pasta("assert codigo == 0 and canais == ['terminal', 'terminal']")),
(A03, "Avançado", G(A03, "Avançado"), "", com_pasta(
    "assert resumo == 'Atendimentos: pedido 5, dúvida 2, revisar 2, reclamação 1, elogio 1, outro 1\\n"
    "Encomendas: 2, somando R$ 200,00'")),
# ============================================================ 04
(A04, "a janela: histórico, status e planilha", "", "", com_pasta("""
from openpyxl import load_workbook
from janela import JanelaAtendente
app = JanelaAtendente(planilha=Path('janela.xlsx'))
app.mainloop()
_gui.digitar(0, 'Quanto custa a coxinha?'); _gui.clicar('Enviar')
_gui.digitar(0, 'Sou celíaca, tem pão sem glúten?'); _gui.clicar('Enviar')
_gui.clicar('Enviar')   # campo vazio: nada acontece
historico = app.historico.get('1.0', 'end')
assert 'Padaria: Coxinha: R$ 7,00 (unidade).' in historico and historico.count('Cliente:') == 2
_gui.ver('⚠ para revisar: dado sensível: saúde')
assert app.historico._textbox.cget('state') == 'disabled'   # o Text do Tk por dentro do CTkTextbox
canais = [l[1] for l in load_workbook('janela.xlsx')['Atendimentos'].iter_rows(min_row=2, values_only=True)]
assert canais == ['janela', 'janela']""", gui=True)),
(A04, "Básico", G(A04, "Básico"), "", com_pasta("_gui.ver('Horário: de segunda a sábado')", gui=True)),
(A04, "Intermediário", G(A04, "Intermediário"), "", com_pasta("""
_gui.digitar(0, 'Adorei o café!'); _gui.clicar('Enviar')
assert 'Adorei' in app.historico.get('1.0', 'end')
_gui.clicar('Limpar')
assert app.historico.get('1.0', 'end').strip() == ''""", gui=True)),
(A04, "Avançado", G(A04, "Avançado"), "", com_pasta("""
_gui.digitar(0, 'Quero 20 coxinhas para amanhã'); _gui.clicar('Enviar')
_gui.digitar(0, 'Quero 10 sonhos para amanhã'); app.campo._entry.focus_force(); app.update()
app.campo._entry.event_generate('<Return>', when='now'); app.update()   # o Enter
assert app.title() == 'Padaria Pão Quente — encomendas: R$ 205,00', app.title()""", gui=True)),
# ============================================================ 05
(A05, "bateria final: 15 de 16, e 16 de 16 com IA falsa", "", "", com_pasta(NOVOS + IA_ESPERTA + """
from bateria import main
assert main(['casos_atendente.csv']) == 1
assert '15 de 16 casos aprovados' in Path('relatorio_testes.md').read_text(encoding='utf-8')
assert main(['casos_atendente.csv', '--com-ia']) == 0
assert '16 de 16 casos aprovados' in Path('relatorio_testes.md').read_text(encoding='utf-8')""")),
(A05, "Básico", G(A05, "Básico"), "", com_pasta(
    "assert codigo == 1 and '15 de 16 casos aprovados' in Path('relatorio_testes.md').read_text(encoding='utf-8')")),
com_arquivo(A05, "Intermediário", "import conferir_entrega\nassert conferir_entrega.main() == 0"),
(A05, "Avançado", G(A05, "Avançado"), "", com_pasta(
    "assert codigo == 0 and '17 de 17 casos aprovados' in Path('relatorio_testes.md').read_text(encoding='utf-8')")),
]
