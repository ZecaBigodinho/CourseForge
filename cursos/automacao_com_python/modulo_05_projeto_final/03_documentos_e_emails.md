# 03 — Documentos e e-mails

> **Curso:** Automação com Python  
> **Módulo:** 05 — Projeto final  
> **Tempo estimado:** 1 h 30 min  

---

## 🎯 Objetivos

Ao final desta aula, você terá:

- O `documentos.py`: **boletim** em Excel e **certificados** em PDF para os aprovados.
- O `emails.py`: um e-mail por aluno com o **resultado**, o **certificado** anexado (para os aprovados), salvo como **rascunho** ou **enviado**.
- Entendido como cada parte reaproveita o que foi feito nos Módulos 02, 03 e 04.

## Pré-requisitos

- [Aula 02](02_pacote_e_dados.md): o `dados.py` e a classe `Aluno`.
- As bibliotecas dos módulos anteriores no ambiente virtual: `openpyxl`, `fpdf2`, `python-dotenv` (e `aiosmtpd` para o servidor de teste).

---

## `documentos.py`

```python title="secretaria/documentos.py"
"""Gera os arquivos: boletim em Excel e certificados em PDF."""
import hashlib
import unicodedata
from collections import Counter
from datetime import date
from pathlib import Path

from fpdf import FPDF
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

from .dados import Aluno

ROXO = (79, 53, 181)
CORES = {"Aprovado": "C6EFCE", "Recuperação": "FFEB9C", "Reprovado": "FFC7CE", "Pendente": "D9D9D9"}
MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho",
         "agosto", "setembro", "outubro", "novembro", "dezembro"]


def nome_de_arquivo(texto: str) -> str:
    sem_acento = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return "".join(c if c.isalnum() else "_" for c in sem_acento.lower()).strip("_")


def gerar_boletim(info: dict, alunos: list[Aluno], pasta: Path) -> Path:
    livro = Workbook()
    aba = livro.active
    aba.title = "Boletim"
    aba.append(["Matrícula", "Nome", "1º bim", "2º bim", "3º bim", "4º bim", "Média", "Frequência", "Situação"])
    for a in alunos:
        aba.append([a.matricula, a.nome, *a.notas, a.media, a.frequencia, a.situacao])
    for celula in aba[1]:
        celula.font = Font(bold=True, color="FFFFFF")
        celula.fill = PatternFill("solid", start_color="4F35B5")
    for linha in aba.iter_rows(min_row=2):
        for celula in linha[2:7]:
            celula.number_format = "0.0"
        linha[7].number_format = "0%"
        linha[8].fill = PatternFill("solid", start_color=CORES[linha[8].value])
    aba.column_dimensions["B"].width = 22
    aba.freeze_panes = "C2"

    resumo = livro.create_sheet("Resumo")
    resumo.append(["Turma", info["Turma"]])
    for situacao, quantidade in Counter(a.situacao for a in alunos).most_common():
        resumo.append([situacao, quantidade])

    problemas = livro.create_sheet("Problemas")
    problemas.append(["Aluno", "Problema"])
    for a in alunos:
        for problema in a.problemas:
            problemas.append([a.nome, problema])
    problemas.column_dimensions["A"].width = 22
    problemas.column_dimensions["B"].width = 36

    destino = pasta / f"boletim_{info['Turma']}.xlsx"
    livro.save(destino)
    return destino


def codigo_de_validacao(matricula: int, turma: str, ano: int) -> str:
    resumo = hashlib.sha256(f"{matricula}|{turma}|{ano}".encode()).hexdigest().upper()
    return f"{resumo[:5]}-{resumo[5:10]}"


def _pagina_certificado(pdf: FPDF, aluno: Aluno, info: dict, codigo: str) -> None:
    hoje = date.today()
    pdf.add_page()
    pdf.set_draw_color(*ROXO)
    pdf.set_line_width(1.5)
    pdf.rect(10, 10, 277, 190)
    pdf.set_y(42)
    pdf.set_font("Helvetica", "B", 32)
    pdf.set_text_color(*ROXO)
    pdf.cell(0, 16, "CERTIFICADO DE APROVAÇÃO", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(30, 30, 30)
    pdf.set_font("Helvetica", "", 15)
    pdf.ln(8)
    pdf.cell(0, 10, "Certificamos que", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "B", 26)
    pdf.cell(0, 16, aluno.nome, align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 15)
    pdf.set_x(40)
    media = f"{aluno.media:.1f}".replace(".", ",")  # 8,1 (vírgula, como no Brasil)
    pdf.multi_cell(217, 9, f"foi aprovado(a) na turma {info['Turma']} do curso {info['Curso']}, "
                           f"ano letivo de {info['Ano']}, com média final {media}.", align="C")
    pdf.ln(12)
    pdf.cell(0, 8, f"Cidade Exemplo, {hoje.day} de {MESES[hoje.month - 1]} de {hoje.year}.", align="C")
    pdf.set_line_width(0.4)
    pdf.line(108, 168, 189, 168)
    pdf.set_xy(108, 170)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(81, 6, info["Responsável"], align="C")
    pdf.set_xy(14, 186)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(110, 110, 110)
    pdf.cell(269, 6, f"Código de validação: {codigo}", align="C")


def gerar_certificados(info: dict, alunos: list[Aluno], pasta: Path) -> list[tuple[Aluno, Path, str]]:
    """Um PDF por aluno aprovado. Devolve [(aluno, arquivo, código)]."""
    emitidos = []
    for aluno in alunos:
        if aluno.situacao != "Aprovado":
            continue
        codigo = codigo_de_validacao(aluno.matricula, info["Turma"], info["Ano"])
        pdf = FPDF(orientation="landscape", format="A4")
        pdf.set_auto_page_break(False)
        _pagina_certificado(pdf, aluno, info, codigo)
        destino = pasta / f"certificado_{nome_de_arquivo(aluno.nome)}.pdf"
        pdf.output(destino)
        emitidos.append((aluno, destino, codigo))
    return emitidos
```

### O que mudou em relação aos módulos anteriores

- **Recebe `Aluno`s prontos.** O boletim não calcula nada: só **escreve** o que o `dados.py` calculou. Se a regra de aprovação mudar, o boletim continua igual.
- **O código de validação** usa matrícula, turma e **ano** (`2026001|1A|2026`): o mesmo aluno, no mesmo ano, recebe sempre o mesmo código.
- **Média com vírgula** no certificado: `f"{aluno.media:.1f}".replace(".", ",")` escreve `7,3`, como no Brasil.
- **`_pagina_certificado`** começa com `_`: é um aviso, por costume do Python, de que a função é de uso **interno** do arquivo. Quem usa o módulo chama `gerar_certificados()`.
- **A linha da assinatura** tem `set_line_width(0.4)` antes: sem isso, ela herdava a espessura da moldura (1,5 mm) e saía grossa demais. Foi o que apareceu na primeira versão, conferindo o PDF.

## `emails.py`

```python title="secretaria/emails.py"
"""E-mails para os alunos: rascunhos (.eml) ou envio pelo servidor do .env."""
import logging
import os
import smtplib
import time
from email.message import EmailMessage
from pathlib import Path

from dotenv import load_dotenv

from .dados import Aluno

log = logging.getLogger("secretaria")
PAUSA_ENTRE_ENVIOS = 2


def montar(aluno: Aluno, info: dict, remetente: str, certificado: Path | None) -> EmailMessage:
    primeiro_nome = aluno.nome.split()[0]
    media = "-" if aluno.media is None else f"{aluno.media:.1f}".replace(".", ",")
    msg = EmailMessage()
    msg["From"] = remetente
    msg["To"] = f"{aluno.nome} <{aluno.email}>"
    msg["Subject"] = f"Turma {info['Turma']}: resultado final de {info['Ano']}"
    texto = (f"Olá, {primeiro_nome}!\n\nSeu resultado final na turma {info['Turma']}:\n\n"
             f"- Média: {media}\n- Frequência: {aluno.frequencia:.0%}\n- Situação: {aluno.situacao}\n")
    if certificado:
        texto += "\nParabéns! Seu certificado de aprovação está no anexo.\n"
    elif aluno.situacao == "Pendente":
        texto += "\nAlguma nota ainda está pendente. Procure a secretaria.\n"
    else:
        texto += "\nProcure a coordenação para saber os próximos passos.\n"
    msg.set_content(texto + f"\n{info['Responsável']}\n")
    if certificado:
        msg.add_attachment(certificado.read_bytes(), maintype="application", subtype="pdf",
                           filename=certificado.name)
    return msg


def configuracao_smtp() -> dict:
    load_dotenv()
    return {
        "servidor": os.getenv("SMTP_SERVIDOR", "localhost"),
        "porta": int(os.getenv("SMTP_PORTA", "8025")),
        "seguranca": os.getenv("SMTP_SEGURANCA", "nenhuma"),
        "usuario": os.getenv("SMTP_USUARIO", ""),
        "senha": os.getenv("SMTP_SENHA", ""),
        "remetente": os.getenv("EMAIL_REMETENTE", "secretaria@example.com"),
    }


def processar(mensagens: list[tuple[Aluno, EmailMessage]], pasta: Path, enviar: bool, config: dict) -> int:
    """Salva rascunhos ou envia. Devolve o número de falhas."""
    if not enviar:
        rascunhos = pasta / "rascunhos"
        rascunhos.mkdir(exist_ok=True)
        for aluno, msg in mensagens:
            (rascunhos / f"{aluno.matricula}.eml").write_bytes(bytes(msg))
            log.info("Rascunho: %s", aluno.email)
        return 0
    falhas = 0
    try:
        servidor = (smtplib.SMTP_SSL if config["seguranca"] == "ssl" else smtplib.SMTP)(
            config["servidor"], config["porta"], timeout=30)
        if config["seguranca"] == "starttls":
            servidor.starttls()
        if config["usuario"]:
            servidor.login(config["usuario"], config["senha"])
    except (OSError, smtplib.SMTPException) as erro:
        log.error("Não consegui conectar a %s:%s: %s", config["servidor"], config["porta"], erro)
        return len(mensagens)
    with servidor:
        for i, (aluno, msg) in enumerate(mensagens):
            try:
                servidor.send_message(msg)
                log.info("Enviado: %s", aluno.email)
            except smtplib.SMTPException as erro:
                falhas += 1
                log.error("Falhou: %s (%s)", aluno.email, erro)
            if i < len(mensagens) - 1:
                time.sleep(PAUSA_ENTRE_ENVIOS)
    return falhas
```

### Detalhes

- **O texto muda conforme a situação:** aprovados recebem "Parabéns!" e o certificado; pendentes são orientados a procurar a secretaria; os demais, a coordenação.
- **`configuracao_smtp()`** lê o `.env` como no [Módulo 04](../modulo_04_email_e_agendamento/03_env_e_configuracao.md), com os mesmos padrões seguros (servidor de teste). O remetente padrão é `secretaria@example.com`.
- **`processar()`** faz o mesmo que o lembrete do Módulo 04: **rascunho** por padrão, ou **envio** com tratamento de erro de conexão, pausa e log. Ele devolve o número de **falhas**, que vira o código de saída.
- **Os rascunhos** são salvos com a **matrícula** no nome (`2026001.eml`), e não com o e-mail: o nome do arquivo fica curto e não expõe o endereço de ninguém numa listagem de pasta.

!!! warning "Quem fica sem e-mail"
    Alunos com e-mail inválido **não** recebem nada. A linha de comando ([aula 04](04_linha_de_comando_e_testes.md)) registra cada um no log como `WARNING`. Na turma de treino, o **Heitor** foi aprovado e tem certificado, mas não vai recebê-lo por e-mail: alguém precisa corrigir a planilha ou entregar em mãos.

---

## ⚠️ Erros comuns

- **Calcular de novo** dentro do boletim ou do e-mail (e chegar a um resultado diferente do `dados.py`).
- **Esquecer o anexo** quando o certificado existe: o `montar()` recebe o caminho, e o `cli.py` passa o certificado certo de cada aluno.
- **Rascunho com e-mail no nome do arquivo** numa pasta compartilhada: expõe endereços.
- **Esquecer o `set_line_width`** depois da moldura: tudo que vier depois sai grosso.

---

## Exercícios

### Básico (fixação)

Mude o assunto dos e-mails para **"Resultado final — Turma 1A (2026)"**. Teste montando o e-mail de um aluno e mostrando o assunto.

<!-- gabarito -->
??? success "Gabarito — Básico"
    No `emails.py`, a linha do assunto fica:

    ```python
    info = {"Turma": "1A", "Ano": 2026}
    assunto = f"Resultado final — Turma {info['Turma']} ({info['Ano']})"
    print(assunto)
    ```

    Ou seja: `msg["Subject"] = f"Resultado final — Turma {info['Turma']} ({info['Ano']})"`. O travessão funciona normalmente em e-mails (o Python codifica o cabeçalho sozinho, [Módulo 04](../modulo_04_email_e_agendamento/01_montar_emails.md)); quem não tem travessão são as fontes padrão do **PDF**.

### Intermediário (aplicação)

Escreva a função `gerar_lista_de_aprovados(info, alunos, pasta)`, no estilo do `documentos.py`, que gera um PDF **A4 em pé** com o título "Aprovados — Turma 1A" e a lista dos aprovados em ordem alfabética, com a média de cada um.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```python
    from pathlib import Path

    from fpdf import FPDF

    from secretaria.dados import ler_turma


    def gerar_lista_de_aprovados(info: dict, alunos: list, pasta: Path) -> Path:
        pdf = FPDF(format="A4")
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 18)
        pdf.cell(0, 12, f"Aprovados - Turma {info['Turma']}", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 12)
        aprovados = sorted((a for a in alunos if a.situacao == "Aprovado"), key=lambda a: a.nome)
        for aluno in aprovados:
            media = f"{aluno.media:.1f}".replace(".", ",")
            pdf.cell(0, 8, f"{aluno.nome} ({media})", new_x="LMARGIN", new_y="NEXT")
        destino = pasta / f"aprovados_{info['Turma']}.pdf"
        pdf.output(destino)
        return destino


    info, alunos = ler_turma(Path("treino_secretaria") / "turma_1A.xlsx")
    pasta = Path("saida")
    pasta.mkdir(exist_ok=True)
    arquivo = gerar_lista_de_aprovados(info, alunos, pasta)
    print(arquivo)
    ```

    Repare no **hífen** no título: o travessão daria erro com a fonte Helvetica ([Módulo 03](../modulo_03_documentos_e_pdfs/02_pdf_com_fpdf2.md#acentos-funcionam-travessao-e-emojis-nao)). A lista: Ana Souza (8,1), Carla Mendes (9,5), Elisa Prado (7,3) e Heitor Alves (8,3).

### Avançado (desafio)

Os alunos em **recuperação** devem receber, no e-mail, as notas dos quatro bimestres para saber onde melhorar. Altere o texto do `montar()` (numa cópia) para incluir as notas **só** nesse caso, com vírgula decimal, e teste com o Bruno.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```python
    from pathlib import Path

    from secretaria.dados import ler_turma
    from secretaria.emails import montar


    def montar_com_notas(aluno, info, remetente, certificado):
        msg = montar(aluno, info, remetente, certificado)
        if aluno.situacao != "Recuperação":
            return msg
        notas = ", ".join(f"{n}º bim: {str(nota).replace('.', ',')}"
                          for n, nota in enumerate(aluno.notas, start=1))
        texto = msg.get_content() + f"\nSuas notas: {notas}.\n"
        msg.set_content(texto)
        return msg


    info, alunos = ler_turma(Path("treino_secretaria") / "turma_1A.xlsx")
    bruno = next(a for a in alunos if a.nome == "Bruno Lima")
    msg = montar_com_notas(bruno, info, "secretaria@example.com", None)
    print(msg.get_content())
    ```

    Em vez de copiar o `montar()` inteiro, a função nova **usa** o `montar()` e só acrescenta a linha das notas: se o texto principal mudar, ela continua funcionando. A última linha do e-mail do Bruno: `Suas notas: 1º bim: 5,0, 2º bim: 6,5, 3º bim: 4,5, 4º bim: 6,0.`

---

## 💡 Resumo

- `documentos.py` **escreve** o que o `dados.py` calculou: boletim (Boletim, Resumo, Problemas) e certificados com código.
- `emails.py` monta um e-mail por aluno, com o certificado dos aprovados; **rascunho** por padrão, envio só quando pedido.
- Funções internas com `_`; conferir o PDF renderizado pega detalhes como a espessura da linha.

## ➡️ Próximo passo

**[04 — Linha de comando e testes](04_linha_de_comando_e_testes.md)**: o `cli.py` que junta tudo e os testes automáticos com pytest.
