"""Casos de teste do curso IA na prática com Python, Módulo 02 (tarefas úteis).

Nenhum caso chama a API: o Gemini é substituído pelo ClienteFalso (Módulo 01, aula 02) ou o
programa usa as regras. Precisa de google-genai, python-dotenv e openpyxl (a CI instala).
"""
import re

from extrair import gabarito, texto_aula

M01 = "../ia_na_pratica_com_python/modulo_01_api_de_ia"
MODULO = "../ia_na_pratica_com_python/modulo_02_tarefas_uteis"
A01, A02, A03, A04, A05 = (
    "01_classificar_mensagens.md", "02_extrair_json.md", "03_reescrever_com_tom.md",
    "04_regras_ou_ia.md", "05_projeto_triagem.md",
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
    "classificar.py": bloco_titulo(MODULO, A01, "classificar.py"),
    "extrair.py": bloco_titulo(MODULO, A02, "extrair.py"),
    "reescrever.py": bloco_titulo(MODULO, A03, "reescrever.py"),
    "regras_ou_ia.py": bloco_titulo(MODULO, A04, "regras_ou_ia.py"),
    "triagem.py": bloco_titulo(MODULO, A05, "triagem.py"),
}
CSV = next(b for b in re.findall(r"```text\n(.*?)```", texto_aula(MODULO, A01), re.S) if b.startswith("id;data;mensagem"))
ARQUIVOS = "".join(f"# === arquivo: {nome} ===\n{codigo}\n" for nome, codigo in ARQUIVOS_AULAS.items())


def com_pasta(verificacao: str = "", preparo: str = "") -> str:
    verificacao = verificacao.strip().removeprefix("# === gabarito ===").strip()
    return (f"{ARQUIVOS}# === arquivo: teste.py ===\nimport os\nfrom pathlib import Path\n"
            f"os.environ.pop('GEMINI_API_KEY', None)\n"
            f"Path('mensagens_exemplo.csv').write_text({CSV!r}, encoding='utf-8')\n{preparo}\n"
            f"# === gabarito ===\n{verificacao}\n")


GABARITOS = [
# ============================================================ 01
(A01, "classificar_simulado acerta as 10 mensagens de treino", "", "", com_pasta("""
import csv
from classificar import classificar_simulado, normalizar
with open('mensagens_exemplo.csv', encoding='utf-8') as arq:
    msgs = [l['mensagem'] for l in csv.DictReader(arq, delimiter=';')]
assert [classificar_simulado(m) for m in msgs] == ['pedido', 'dúvida', 'reclamação', 'elogio', 'pedido', 'dúvida',
                                                  'dúvida', 'reclamação', 'pedido', 'outro']
assert [normalizar(x) for x in ['Reclamação.', ' RECLAMACAO ', 'Dúvida', 'É um pedido', 'elogio!']] == \\
    ['reclamação', 'reclamação', 'dúvida', 'revisar', 'elogio']
assert classificar_simulado('Vi uma promoção de outra padaria e quero que cubram o preço') == 'pedido'""")),
(A01, "Básico", G(A01, "Básico"), "", com_pasta(
    "assert dict(contagem) == {'pedido': 3, 'dúvida': 3, 'reclamação': 2, 'elogio': 1, 'outro': 1}")),
(A01, "Intermediário", G(A01, "Intermediário"), "", com_pasta(
    "assert resultados == ['pedido', 'reclamação', 'revisar', 'elogio']")),
(A01, "Avançado", G(A01, "Avançado"), "", com_pasta(
    "assert classificar.normalizar('Encomenda') == 'encomenda' and classificar.normalizar('encomendas') == 'revisar'")),
# ============================================================ 02
(A02, "extrair_simulado e o erro da dúzia", "", "", com_pasta("""
from datetime import date
from extrair import extrair_simulado
h = date(2026, 11, 8)
assert extrair_simulado('Bom dia! Quero encomendar 2 bolos de fubá para sábado, dia 14/11.', h)[0]['data_entrega'] == date(2026, 11, 14)
assert extrair_simulado('Quero 1 torta de frango pra amanhã', h)[0]['data_entrega'] == date(2026, 11, 9)
erro = extrair_simulado('Quero uma dúzia de pães de queijo para sexta', h)[0]
assert erro['quantidade'] == 1 and erro['data_entrega'] is None  # erra sem perceber, como a aula diz""")),
(A02, "Básico", G(A02, "Básico"), "", com_pasta(
    "assert resultados[0][0] and resultados[1] == (None, 'quantidade estranha: 0') and 'data inválida' in resultados[2][1]")),
(A02, "Intermediário", G(A02, "Intermediário"), "", com_pasta("""
assert resultados[0][0]['quantidade'] == 50
assert resultados[1] == (None, 'a resposta não é um JSON válido')
assert resultados[2][1] == "data inválida: '20/11/2026'"
""")),
(A02, "Avançado", G(A02, "Avançado"), "", com_pasta(
    "assert curto[0]['observacao'] == 'sem açúcar' and longo[0] is None and 'observacao' not in extrair.ESQUEMA['required']")),
# ============================================================ 03
(A03, "reescrever com o cliente falso", "", "", com_pasta("""
from cliente_falso import ClienteFalso
from reescrever import reescrever
texto, problemas = reescrever(ClienteFalso('Olá! Pedimos desculpas, trocamos o sonho com 10% de desconto.'),
                              'gemini-3.8-flash', 'O sonho veio sem recheio', 'vamos trocar o sonho')
assert problemas == ['apareceu preço ou desconto que não estava no rascunho']""")),
(A03, "Básico", G(A03, "Básico"), "", com_pasta("assert all('16h' in t for t in resultados.values())")),
(A03, "Intermediário", G(A03, "Intermediário"), "", com_pasta(
    "assert problemas[0] == [] and 'preço' in problemas[1][0] and problemas[2] == ['longa demais (500 caracteres)'] and problemas[3] == ['resposta vazia']")),
(A03, "Avançado", G(A03, "Avançado"), "", com_pasta("assert certo == set() and errado == {'50'}")),
# ============================================================ 04
(A04, "Básico", G(A04, "Básico"), "", com_pasta("assert respostas['decidir quem ganha uma bolsa'] == 'pessoa'")),
(A04, "Intermediário", G(A04, "Intermediário"), "", com_pasta(
    "assert chamadas == 3 and foram_para_ia[0].startswith('Preciso de 50') and foram_para_ia[2] == 'kkkkk'")),
(A04, "Avançado", G(A04, "Avançado"), "", com_pasta(
    "from decimal import Decimal\nassert total == Decimal('381.00') and sem_preco == ['pão de mel']")),
# ============================================================ 05
(A05, "mascarar", "", "", com_pasta("""
from triagem import mascarar
assert mascarar('Me liga no (11) 98765-4321 ou ana.souza@example.com, CPF 123.456.789-09. Quero 2 bolos dia 14/11.') == \\
    'Me liga no [telefone] ou [e-mail], CPF [CPF]. Quero 2 bolos dia 14/11.'""")),
(A05, "Básico", G(A05, "Básico"), "", com_pasta("assert codigo == 0 and linhas == {'Mensagens': 10, 'Pedidos': 3, 'Revisar': 0}")),
(A05, "Intermediário", G(A05, "Intermediário"), "", com_pasta(
    "assert codigo == 0 and len(falso.pedidos) == 8")),
(A05, "Avançado", G(A05, "Avançado"), "", com_pasta(
    "assert mascarados == ['Meu carro é o [placa], estacionei na frente.', 'A placa é [placa].', 'Quero 2 bolos.']")),
]
