"""Casos de teste do curso IA na prática com Python, Módulo 01 (API de IA).

Nenhum caso chama a API de verdade: o Gemini é substituído pelo ClienteFalso da aula 02 (ou o
programa usa o motor simulado). Assim os testes não precisam de chave, internet nem cota.
Precisa de google-genai e python-dotenv (a CI instala).
"""
import re

from extrair import gabarito, texto_aula

MODULO = "../ia_na_pratica_com_python/modulo_01_api_de_ia"
A01, A02, A03, A04, A05 = (
    "01_o_que_e_uma_api_de_ia.md", "02_primeira_chamada.md", "03_instrucoes_e_ajustes.md",
    "04_conversa_e_motores.md", "05_projeto_resumidor.md",
)


def G(aula, nivel):
    return gabarito(MODULO, aula, nivel)


def bloco_titulo(aula, titulo, linguagem="python"):
    texto = texto_aula(MODULO, aula)
    padrao = rf'```{linguagem} title="{re.escape(titulo)}"\n(.*?)```' if titulo else rf"```{linguagem}\n(.*?)```"
    achados = re.findall(padrao, texto, re.S)
    assert len(achados) == 1, f"{aula}: esperava 1 bloco {titulo!r}, achei {len(achados)}"
    return achados[0]


ARQUIVOS_AULAS = {
    "erros_ia.py": bloco_titulo(A02, "erros_ia.py"),
    "cliente_falso.py": bloco_titulo(A02, "cliente_falso.py"),
    "primeira_chamada.py": bloco_titulo(A02, "primeira_chamada.py"),
    "comparar_instrucoes.py": bloco_titulo(A03, "comparar_instrucoes.py"),
    "motores.py": bloco_titulo(A04, "motores.py"),
    "conversa.py": bloco_titulo(A04, "conversa.py"),
    "resumidor.py": bloco_titulo(A05, "resumidor.py"),
}
# O texto de exemplo é o bloco ```text da aula 05 que começa com "A Padaria"
TEXTO = next(b for b in re.findall(r"```text\n(.*?)```", texto_aula(MODULO, A05), re.S)
             if b.startswith("A Padaria"))
ARQUIVOS = "".join(f"# === arquivo: {nome} ===\n{codigo}\n" for nome, codigo in ARQUIVOS_AULAS.items())


def com_pasta(verificacao: str = "", preparo: str = "") -> str:
    """Programa de teste com os arquivos das aulas e o texto de exemplo, sem .env (caminho sem chave)."""
    verificacao = verificacao.strip().removeprefix("# === gabarito ===").strip()
    return (f"{ARQUIVOS}# === arquivo: teste.py ===\nimport os\nfrom pathlib import Path\n"
            f"os.environ.pop('GEMINI_API_KEY', None)\n"
            f"Path('texto_exemplo.txt').write_text({TEXTO!r}, encoding='utf-8')\n{preparo}\n"
            f"# === gabarito ===\n{verificacao}\n")


COM_FALSO = """
import google.genai as genai
from cliente_falso import ClienteFalso
os.environ['GEMINI_API_KEY'] = 'chave-falsa-para-teste'
"""

GABARITOS = [
# ============================================================ 01
(A01, "Básico", G(A01, "Básico"), "", com_pasta("assert estimativa == 16")),
(A01, "Intermediário", G(A01, "Intermediário"), "", com_pasta("assert caminho == 'Sem chave: motor simulado'")),
# ============================================================ 02
(A02, "primeira_chamada.py (com o cliente falso)", "", "", com_pasta("""
import runpy
falso = ClienteFalso("Uma API é uma porta entre programas.")
genai.Client = lambda *a, **k: falso
runpy.run_path('primeira_chamada.py', run_name='__main__')
assert falso.pedidos[0]['model'] == 'gemini-3.8-flash' and 'API' in falso.pedidos[0]['input']""", COM_FALSO)),
(A02, "primeira_chamada.py (limite 429 vira mensagem e saída 1)", "", "", com_pasta("""
import runpy
class Erro429(Exception):
    status_code = 429
genai.Client = lambda *a, **k: ClienteFalso(erro=Erro429('RESOURCE_EXHAUSTED'))
try:
    runpy.run_path('primeira_chamada.py', run_name='__main__')
    raise AssertionError('deveria sair com erro')
except SystemExit as saida:
    assert saida.code == 1""", COM_FALSO)),
(A02, "primeira_chamada.py (sem chave)", "", "", com_pasta("""
import runpy
try:
    runpy.run_path('primeira_chamada.py', run_name='__main__')
except SystemExit as saida:
    assert saida.code == 1""")),
(A02, "Básico", G(A02, "Básico"), "", com_pasta("assert resposta.usage.total_tokens > 0")),
(A02, "Intermediário", G(A02, "Intermediário"), "", com_pasta(
    "assert 'chave' in mensagens[0] and 'limite' in mensagens[1] and 'internet' in mensagens[2] and 'ValueError' in mensagens[3]")),
(A02, "Avançado", G(A02, "Avançado"), "", com_pasta(
    "assert ok[0] == 'Resposta.' and falha[0] is None and 'internet' in falha[1]")),
# ============================================================ 03
(A03, "Básico", G(A03, "Básico"), "", com_pasta("assert '9º ano' in pedido['system_instruction'] and pedido['input'].startswith('Como')")),
(A03, "Intermediário", G(A03, "Intermediário"), "", com_pasta(
    "assert estilos == ['formal', 'formal', 'descontraído', 'descontraído'] and len(falso.pedidos) == 4")),
(A03, "Avançado", G(A03, "Avançado"), "", com_pasta("assert all(resultados[t] == esperado for t, esperado in exemplos.items())")),
# ============================================================ 04
(A04, "Básico", G(A04, "Básico"), "", com_pasta("assert ids == [None, 'falso-1', None]")),
(A04, "Intermediário", G(A04, "Intermediário"), "", com_pasta(
    "assert resumos[2].startswith('A Padaria Pão Quente abriu em 2019') and curto == 'Uma frase só.'")),
(A04, "Avançado", G(A04, "Avançado"), "", com_pasta("assert motor.tokens_usados == 3")),
(A04, "conversa.py sem chave (motor simulado)", "", "/nova\nOutra pergunta.\n/sair\n", com_pasta("""
import runpy
runpy.run_path('conversa.py', run_name='__main__')""")),
# ============================================================ 05
(A05, "resumidor.py (simulado, arquivo inexistente)", "", "", com_pasta("""
from resumidor import main
assert main(['texto_exemplo.txt']) == 0
assert Path('texto_exemplo_resumo.txt').read_text(encoding='utf-8').startswith('A Padaria Pão Quente abriu em 2019')
assert main(['nao_existe.txt']) == 2
Path('vazio.txt').write_text('', encoding='utf-8')
assert main(['vazio.txt']) == 2""")),
(A05, "Básico", G(A05, "Básico"), "", com_pasta("assert codigo == 0 and resumo.count('.') == 3")),
(A05, "Intermediário", G(A05, "Intermediário"), "", com_pasta(
    "assert codigo == 0 and pedido['input'].startswith('Resuma em no máximo 2 frases:') and 'resume textos' in pedido['system_instruction']\n"
    "assert pedido['generation_config'] == {'thinking_level': 'low'}")),
(A05, "Avançado", G(A05, "Avançado"), "", com_pasta(
    "assert resumidos == 2 and not list(pasta.glob('*_resumo_resumo.txt'))")),
]
