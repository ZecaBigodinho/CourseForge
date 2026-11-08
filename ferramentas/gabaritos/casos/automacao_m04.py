"""Casos de teste do curso Automação com Python, Módulo 04 (e-mail, .env, logs e agendamento).

O código vem das aulas. Cada caso roda numa pasta temporária, com os arquivos de treino criados pelo
próprio criar_treino_emails.py da aula 01. Os envios vão para um servidor SMTP de teste (aiosmtpd)
ligado dentro do próprio caso, na porta 8025: nenhum e-mail sai do computador.
Precisa de openpyxl, aiosmtpd e python-dotenv (a CI instala).
"""
import re

from extrair import gabarito, texto_aula

MODULO = "../automacao_com_python/modulo_04_email_e_agendamento"


def G(aula, nivel):
    return gabarito(MODULO, aula, nivel)


def bloco(aula, trecho, linguagem="python"):
    """O bloco de código da aula (fora dos gabaritos) que contém o trecho."""
    texto = re.sub(r'^\?\?\? success "Gabarito.*?(?=^\S)', "", texto_aula(MODULO, aula) + "\n.", flags=re.S | re.M)
    achados = [b for b in re.findall(rf"```{linguagem}[^\n]*\n(.*?)```", texto, re.S) if trecho in b]
    assert len(achados) == 1, f"{aula}: esperava 1 bloco com {trecho!r}, achei {len(achados)}"
    return achados[0]


A01, A02, A03, A04, A05 = (
    "01_montar_emails.md", "02_servidor_de_teste.md", "03_env_e_configuracao.md",
    "04_logs_e_agendamento.md", "05_projeto_lembrete.md",
)

CRIAR = bloco(A01, 'TREINO = Path("treino_emails")')
CONFIG = bloco(A03, "def carregar_config")
LEMBRETE = bloco(A05, "def ler_pendencias")
ENV_EXEMPLO = bloco(A03, "SMTP_SERVIDOR=localhost", "ini")
ARQUIVOS = (f"# === arquivo: configuracao.py ===\n{CONFIG}\n"
            f"# === arquivo: lembrete_semanal.py ===\n{LEMBRETE}\n")

SERVIDOR = '''
from aiosmtpd.controller import Controller


class Guardar:
    def __init__(self):
        self.recebidas = []

    async def handle_DATA(self, server, session, envelope):
        self.recebidas.append(envelope)
        return "250 OK"


caixa = Guardar()
controlador = Controller(caixa, hostname="localhost", port=8025)
controlador.start()
'''


def com_treino(verificacao: str = "", preparo: str = "", servidor: bool = False) -> str:
    """Programa de teste: cria os arquivos de treino (e o servidor, se pedido), roda e confere."""
    verificacao = verificacao.strip().removeprefix("# === gabarito ===").strip()
    fim = "\ncontrolador.stop()" if servidor else ""
    return (f"# === arquivo: criar_treino_emails.py ===\n{CRIAR}\n{ARQUIVOS}"
            f"# === arquivo: teste.py ===\nfrom pathlib import Path\n"
            f"import criar_treino_emails\ncriar_treino_emails.main()\n"
            f"{SERVIDOR if servidor else ''}\n{preparo}\n"
            f"# === gabarito ===\n{verificacao}{fim}\n")


GABARITOS = [
# ============================================================ 01 montar
(A01, "criar_treino_emails.py", CRIAR, "", com_treino("""
from openpyxl import load_workbook
assert load_workbook('treino_emails/pendencias.xlsx')['Pendências'].max_row == 7
criar_treino_emails.main()""")),
(A01, "montar_email.py", bloco(A01, "rascunho_ana.eml"), "", com_treino("""
import email
salvo = email.message_from_bytes(destino.read_bytes(), policy=email.policy.default)
assert salvo['Subject'] == 'Lembrete: Pesquisa sobre golpes no WhatsApp'
assert [p.get_filename() for p in salvo.iter_attachments()] == ['orientacoes.txt']
assert 'Ana' in salvo.get_body(preferencelist=('html',)).get_content()""")),
(A01, "Básico", G(A01, "Básico"), "", com_treino(
    "assert b'=?utf-8?' in destino.read_bytes() and msg['Subject'] == 'Reunião de pais — sábado, 9h'")),
(A01, "Intermediário", G(A01, "Intermediário"), "", com_treino(
    "assert msg['Cc'] == 'professor.auxiliar@example.com' and msg['Reply-To'] == 'coordenacao@example.com'")),
(A01, "Avançado", G(A01, "Avançado"), "", com_treino("assert criados == 5")),
# ============================================================ 02 servidor de teste
(A02, "enviar_teste.py", bloco(A02, "Teste do servidor de e-mail falso"), "", com_treino(
    "assert len(caixa.recebidas) == 1 and caixa.recebidas[0].rcpt_tos == ['ana.souza@example.com']", servidor=True)),
(A02, "Básico", G(A02, "Básico"), "", com_treino(
    "assert enviados == 2 and len(caixa.recebidas) == 2", servidor=True)),
(A02, "Intermediário", G(A02, "Intermediário"), "", com_treino("assert resultado is False")),
(A02, "Avançado", G(A02, "Avançado"), "", com_treino(
    "assert [e.rcpt_tos for e in caixa.recebidas] == [[t] for t in turma]", servidor=True)),
# ============================================================ 03 .env
(A03, "configuracao.py (sem .env: servidor de teste)", CONFIG, "", com_treino(
    "assert config.servidor == 'localhost' and config.porta == 8025 and config.seguranca == 'nenhuma'")),
(A03, "configuracao.py (servidor real sem senha: erro claro)", CONFIG.replace('if __name__ == "__main__":', "if False:"), "",
 com_treino("""
import os
os.environ['SMTP_SEGURANCA'] = 'starttls'
try:
    carregar_config()
    raise SystemExit('deveria recusar servidor real sem usuário e senha')
except ValueError as erro:
    assert 'SMTP_USUARIO' in str(erro)""")),
# O gabarito começa com a linha do .env (bloco ini): o teste usa só a parte em Python
(A03, "Básico", G(A03, "Básico").split("EMAIL_REMETENTE=secretaria@example.com", 1)[1], "", com_treino(
    "assert carregar_config().remetente == 'secretaria@example.com'",
    "Path('.env').write_text('EMAIL_REMETENTE=secretaria@example.com\\n', encoding='utf-8')")),
(A03, "Intermediário", G(A03, "Intermediário"), "", com_treino("assert 'precisa ser um número' in mensagem")),
(A03, "Avançado", G(A03, "Avançado"), "", com_treino(
    "assert faltando == ['EMAIL_REMETENTE', 'SMTP_SEGURANCA', 'SMTP_SENHA', 'SMTP_USUARIO'], faltando",
    f"Path('.env.example').write_text({ENV_EXEMPLO!r}, encoding='utf-8')\n"
    "Path('.env').write_text('SMTP_SERVIDOR=localhost\\nSMTP_PORTA=8025\\n', encoding='utf-8')")),
# ============================================================ 04 logs
(A04, "tarefa_com_log.py", bloco(A04, 'filename="tarefa.log"').replace("sys.exit(main())", "codigo = main()"), "",
 com_treino("""
import logging
logging.shutdown()
texto = Path('tarefa.log').read_text(encoding='utf-8')
assert codigo == 0 and 'A pasta tem 2 itens' in texto and 'Terminou' in texto, texto""")),
(A04, "Básico", G(A04, "Básico").replace("sys.exit(main())", "main()"), "", com_treino("""
import logging
logging.shutdown()
assert 'Pasta cheia: 3 itens' in Path('tarefa.log').read_text(encoding='utf-8')""",
    "Path('treino_emails/saida').mkdir()")),
(A04, "Intermediário", G(A04, "Intermediário"), "", com_treino(
    "assert Path('tarefa.log').read_text(encoding='utf-8').count('Execução de teste') == 3")),
(A04, "Avançado", G(A04, "Avançado"), "", com_treino(
    "assert niveis['WARNING'] == 2 and niveis['INFO'] == 5, niveis",
    "import lembrete_semanal\nlembrete_semanal.main(enviar=False)")),
# ============================================================ 05 projeto
(A05, "lembrete_semanal.py (simulação)", LEMBRETE.replace("sys.exit(main(", "codigo = (main("), "", com_treino("""
rascunhos = sorted(p.name for p in Path('treino_emails/saida/rascunhos').iterdir())
assert codigo == 0 and rascunhos == ['ana.souza@example.com.eml', 'bruno.lima@example.com.eml', 'carla.mendes@example.com.eml']
texto = Path('treino_emails/saida/rascunhos/bruno.lima@example.com.eml').read_text(encoding='utf-8')
assert texto.index('Resumo do cap') < texto.index('Pesquisa sobre') and 'ATRASADO' in texto
print('simulação ok')""")),
(A05, "lembrete_semanal.py --enviar (servidor de teste)", "", "", com_treino("""
import lembrete_semanal
lembrete_semanal.PAUSA_ENTRE_ENVIOS = 0
assert lembrete_semanal.main(enviar=True) == 0
assert sorted(e.rcpt_tos[0] for e in caixa.recebidas) == ['ana.souza@example.com', 'bruno.lima@example.com', 'carla.mendes@example.com']
log = Path('treino_emails/logs/lembrete.log').read_text(encoding='utf-8')
assert 'Enviado: bruno.lima@example.com' in log and 'connection lost' not in log  # só o log do script
print('envio ok')""", servidor=True)),
(A05, "lembrete_semanal.py --enviar (servidor desligado)", "", "", com_treino("""
import os
os.environ['SMTP_PORTA'] = '8099'
import lembrete_semanal
assert lembrete_semanal.main(enviar=True) == 1
assert 'Não consegui conectar a localhost:8099' in Path('treino_emails/logs/lembrete.log').read_text(encoding='utf-8')
print('servidor desligado vira erro no log, sem traceback')""")),
(A05, "Básico", G(A05, "Básico"), "", com_treino("assert assunto == '[Turma 1A] Lembrete: 2 trabalhos pendentes'")),
(A05, "Intermediário", G(A05, "Intermediário"), "", com_treino(
    "assert list(testes.values()) == ['ATRASADO há 2 dias', 'ATRASADO há 1 dia', 'vence HOJE', 'vence amanhã', 'faltam 5 dias']")),
(A05, "Avançado", G(A05, "Avançado"), "", com_treino(
    "assert resumo['Subject'] == 'Resumo do lembrete: 3 avisados, 2 sem e-mail' and 'Diego Rocha' in resumo.get_content()")),
]
