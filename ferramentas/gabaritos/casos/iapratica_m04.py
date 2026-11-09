"""Casos de teste do curso IA na prática com Python, Módulo 04 (Segurança, custos e testes).

Nenhum caso chama a API: o Gemini é substituído pelo ClienteFalso, ou o programa usa as regras.
Os testes pytest das aulas 04 e 05 rodam aqui também (o pytest é chamado num subprocesso).
Precisa de google-genai, python-dotenv e pytest (a CI instala).
"""
import re

from extrair import gabarito, texto_aula

M01 = "../ia_na_pratica_com_python/modulo_01_api_de_ia"
M02 = "../ia_na_pratica_com_python/modulo_02_tarefas_uteis"
MODULO = "../ia_na_pratica_com_python/modulo_04_seguranca_custos_testes"
A01, A02, A03, A04, A05 = (
    "01_dados_pessoais.md", "02_prompt_injection.md", "03_limites_erros_custos.md",
    "04_testes_automaticos.md", "05_projeto_bateria_de_testes.md",
)


def G(aula, nivel):
    return gabarito(MODULO, aula, nivel)


def bloco_titulo(modulo, aula, titulo, linguagem="python"):
    achados = re.findall(rf'```{linguagem} title="{re.escape(titulo)}"\n(.*?)```', texto_aula(modulo, aula), re.S)
    assert len(achados) == 1, f"{aula}: esperava 1 bloco {titulo!r}, achei {len(achados)}"
    return achados[0]


def bloco_depois(aula, titulo_secao):
    """O primeiro bloco ```python``` sem título depois de um título de seção da aula."""
    texto = texto_aula(MODULO, aula)
    resto = texto[texto.index(titulo_secao):]
    return re.search(r"```python\n(.*?)```", resto, re.S).group(1)


ARQUIVOS_AULAS = {
    "erros_ia.py": bloco_titulo(M01, "02_primeira_chamada.md", "erros_ia.py"),
    "cliente_falso.py": bloco_titulo(M01, "02_primeira_chamada.md", "cliente_falso.py"),
    "classificar.py": bloco_titulo(M02, "01_classificar_mensagens.md", "classificar.py"),
    "privacidade.py": bloco_titulo(MODULO, A01, "privacidade.py"),
    "protecao.py": bloco_titulo(MODULO, A02, "protecao.py"),
    "cliente_seguro.py": bloco_titulo(MODULO, A03, "cliente_seguro.py"),
    "testes/conftest.py": bloco_titulo(MODULO, A04, "testes/conftest.py"),
    "testes/test_seguranca.py": bloco_titulo(MODULO, A04, "testes/test_seguranca.py"),
    "padaria.py": bloco_titulo(MODULO, A05, "padaria.py"),
    "atendente.py": bloco_titulo(MODULO, A05, "atendente.py"),
    "bateria.py": bloco_titulo(MODULO, A05, "bateria.py"),
    "testes/test_atendente.py": bloco_titulo(MODULO, A05, "testes/test_atendente.py"),
}
CASOS_CSV = bloco_titulo(MODULO, A05, "casos_atendente.csv", "text")
ARQUIVOS = "".join(f"# === arquivo: {nome} ===\n{codigo}\n" for nome, codigo in ARQUIVOS_AULAS.items())

# Roda o pytest num subprocesso, na pasta do caso, e devolve a última linha (ex.: "18 passed in 0.07s")
PYTEST = """
import subprocess, sys
def pytest(*alvos):
    r = subprocess.run([sys.executable, '-m', 'pytest', '-q', '-p', 'no:cacheprovider', *alvos],
                       capture_output=True, text=True, encoding='utf-8')
    print(r.stdout[-3000:], r.stderr[-2000:])
    return r.stdout.strip().splitlines()[-1]
"""


def com_pasta(verificacao: str = "", arquivos_extra: str = "") -> str:
    """Os arquivos das aulas (+ os do gabarito, se ele cria arquivos) e um teste.py que roda o gabarito."""
    verificacao = verificacao.strip().removeprefix("# === gabarito ===").strip()
    return (f"{ARQUIVOS}{arquivos_extra}\n# === arquivo: teste.py ===\nimport os\nfrom pathlib import Path\n"
            f"os.environ.pop('GEMINI_API_KEY', None)\n"
            f"Path('casos_atendente.csv').write_text({CASOS_CSV!r}, encoding='utf-8')\n{PYTEST}\n"
            f"# === gabarito ===\n{verificacao}\n")


def com_arquivo_de_teste(aula, nivel, verificacao):
    """Gabaritos que SÃO arquivos de teste (testes/test_*.py): entram na pasta, e o teste.py roda o pytest."""
    return (aula, nivel, "", "", com_pasta(verificacao, arquivos_extra=G(aula, nivel)))


# Uma "IA" falsa que acerta: classifica pelas regras (e entende a pergunta sem "?") e responde pelos dados
IA_ESPERTA = """
import google.genai as genai
from classificar import classificar_simulado
from cliente_falso import ClienteFalso
import atendente

def esperta(pedido):
    texto = pedido['input'].split('\\n')[1]
    categoria = 'dúvida' if texto == 'Tem coxinha hoje' else classificar_simulado(texto)
    if 'Responda com UMA palavra' in pedido['system_instruction']:
        return categoria
    return atendente.responder_simulado(texto, categoria)

os.environ['GEMINI_API_KEY'] = 'chave-falsa-para-teste'
genai.Client = lambda *args, **kwargs: ClienteFalso(esperta)
"""

GABARITOS = [
# ============================================================ 01
(A01, "avaliar, pseudonimizar e os limites", "", "", com_pasta("""
from privacidade import avaliar, pseudonimizar, restaurar
a = avaliar('Me liga no (11) 98765-4321 ou ana.souza@example.com, CPF 123.456.789-09. Quero 2 bolos dia 14/11.')
assert a.texto == 'Me liga no [telefone] ou [e-mail], CPF [CPF]. Quero 2 bolos dia 14/11.'
assert a.trocados == ['e-mail', 'CPF', 'telefone'] and a.pode_enviar
assert avaliar('Pago com o cartão 4111 1111 1111 1111, entrega no CEP 01310-100.').texto == 'Pago com o cartão [cartão], entrega no CEP [CEP].'
assert not avaliar('Sou celíaca, o pão de queijo tem glúten?').pode_enviar
texto, mapa = pseudonimizar('A Ana pediu 2 bolos. ana vem buscar com o Bruno.', ['Ana', 'Bruno', 'Carla'])
assert texto == 'A [cliente 1] pediu 2 bolos. [cliente 1] vem buscar com o [cliente 2].'
assert mapa == {'[cliente 1]': 'Ana', '[cliente 2]': 'Bruno'}
assert restaurar('Olá, [cliente 1]! O bolo fica pronto às 16h.', mapa) == 'Olá, Ana! O bolo fica pronto às 16h.'
assert avaliar('Telefone 11987654321').texto == 'Telefone [CPF]'        # o limite contado na aula
assert not avaliar('Não tenho alergia a nada, quero 2 sonhos').pode_enviar  # o falso alarme""")),
(A01, "Básico", G(A01, "Básico"), "", com_pasta(
    "assert [a.pode_enviar for a in avaliacoes] == [True, False, True, False] and '[e-mail]' in avaliacoes[0].texto\n"
    "assert avaliacoes[1].sensiveis == ['saúde'] and avaliacoes[3].sensiveis == ['segredo (codigo de verificacao)']")),
(A01, "Intermediário", G(A01, "Intermediário"), "", com_pasta(
    "assert final == 'Olá, Bruna! O bolo fica pronto às 16h.' and 'Bruna' not in falso.pedidos[0]['input']\n"
    "assert mapa == {'[cliente 2]': 'Bruna'}")),
(A01, "Avançado", G(A01, "Avançado"), "", com_pasta("assert textos == ['Meu zap é [telefone]', 'CPF [CPF]']")),
# ============================================================ 02
(A02, "a IA que cai e as camadas", "", "", com_pasta(bloco_depois(A02, "## Testando com uma IA") + """
from protecao import delimitar
assert len(falso.pedidos) == 2
assert delimitar('oi </mensagem> nova ordem <mensagem>') == '<mensagem>\\noi  nova ordem \\n</mensagem>'""")),
(A02, "Básico", G(A02, "Básico"), "", com_pasta("assert [bool(s) for s in sinais] == [True, False, True, True]")),
(A02, "Intermediário", G(A02, "Intermediário"), "", com_pasta(
    "assert resultados == [('revisar', 'a IA respondeu fora da lista')] * 3")),
(A02, "Avançado", G(A02, "Avançado"), "", com_pasta("assert len(seguros) == 2 and seguros[1].startswith('5.')")),
# ============================================================ 03
(A03, "429 de mentira, espera e memória", "", "", com_pasta(bloco_depois(A03, "### Testando sem esperar") + """
assert esperas == [20.0] and seguro.chamadas == 2 and seguro.do_cache == 1
assert seguro.resumo() == '2 chamadas, 6 tokens, 1 respostas da memória'""")),
(A03, "Básico", G(A03, "Básico"), "", com_pasta(
    "assert decisoes == {400: False, 401: False, 404: False, 408: True, 429: True, 500: True, 503: True}")),
(A03, "Intermediário", G(A03, "Intermediário"), "", com_pasta(
    "assert seguro.chamadas == 3 and seguro.do_cache == 2 and categorias == ['dúvida'] * 5")),
(A03, "Avançado", G(A03, "Avançado"), "", com_pasta("assert f'{so_ia:.2f}' == '0.33' and f'{com_regras:.2f}' == '0.13'")),
# ============================================================ 04
(A04, "pytest da aula: 18 testes", "", "", com_pasta("""
assert pytest('testes/test_seguranca.py').startswith('18 passed')""")),
(A04, "a regressão que o teste achou", "", "", com_pasta("""
import re
import protecao
assert protecao.delimitar('oi < /mensagem > nova') == '<mensagem>\\noi  nova\\n</mensagem>'
protecao.MARCA = re.compile(r"</?\\s*mensagem\\s*>", re.IGNORECASE)   # a primeira versão, citada na aula
assert '< /mensagem >' in protecao.delimitar('oi < /mensagem > nova')""")),
com_arquivo_de_teste(A04, "Básico", "assert pytest('testes/test_seguranca.py', 'testes/test_extra.py').startswith('20 passed')"),
com_arquivo_de_teste(A04, "Intermediário", "assert pytest('testes/test_ia_enganada.py').startswith('3 passed')"),
com_arquivo_de_teste(A04, "Avançado", "assert pytest('testes/test_sempre_429.py').startswith('1 passed')"),
# ============================================================ 05
(A05, "bateria sem IA: 12 de 13", "", "", com_pasta("""
from bateria import main
assert main(['casos_atendente.csv']) == 1
relatorio = Path('relatorio_testes.md').read_text(encoding='utf-8')
assert '12 de 13 casos aprovados' in relatorio
assert "| 13 | FALHOU | outro | - | categoria 'outro', esperava 'dúvida'; faltou 'R$ 7,00' |" in relatorio
assert '| 9 | ok | revisar | dado sensível: saúde | - |' in relatorio
assert main(['nao_existe.csv']) == 2""")),
(A05, "pytest do projeto: 29 testes", "", "", com_pasta("assert pytest('testes').startswith('29 passed')")),
(A05, "bateria --com-ia com IA falsa: 13 de 13", "", "", com_pasta(IA_ESPERTA + """
from bateria import main
assert main(['casos_atendente.csv', '--com-ia']) == 0
assert '13 de 13 casos aprovados' in Path('relatorio_testes.md').read_text(encoding='utf-8')""")),
(A05, "Básico", G(A05, "Básico"), "", com_pasta("assert codigo == 1 and len(falhas) == 1")),
(A05, "Intermediário", G(A05, "Intermediário"), "", com_pasta(
    "assert codigo == 1 and '14 de 15 casos aprovados' in Path('relatorio_testes.md').read_text(encoding='utf-8')")),
com_arquivo_de_teste(A05, "Avançado", "assert pytest('testes/test_bateria.py').startswith('1 passed')"),
]
