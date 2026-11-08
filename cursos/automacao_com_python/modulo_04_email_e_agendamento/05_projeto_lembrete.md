# 05 — Projeto do módulo: lembrete semanal

> **Curso:** Automação com Python  
> **Módulo:** 04 — E-mail, agendamento e boas práticas  
> **Tempo estimado:** 2 h  

---

## 🎯 Objetivos

Ao final desta aula, você terá um script que:

- Lê a planilha de **trabalhos pendentes** e **agrupa** por aluno (um e-mail por pessoa, com todos os trabalhos dela).
- **Valida** os e-mails e registra no log quem ficou de fora (vazio ou digitado errado).
- Monta e-mails com **texto e HTML**, destacando os trabalhos **atrasados**, e com **anexo**.
- Tem dois modos: **simulação** (salva rascunhos `.eml`, o padrão) e **envio** (`--enviar`, pelo servidor do `.env`).
- Registra tudo num **log**, trata o **servidor desligado** e devolve um **código de saída** para o Agendador.

## Pré-requisitos

- Aulas [01](01_montar_emails.md) a [04](04_logs_e_agendamento.md) deste módulo, com o `configuracao.py` e o `.env` na pasta.

---

## O script

```python title="lembrete_semanal.py"
"""Lembrete semanal: um e-mail para cada aluno com os trabalhos pendentes.

    python lembrete_semanal.py           # simulação: salva os e-mails como rascunhos .eml
    python lembrete_semanal.py --enviar  # envia pelo servidor configurado no .env
"""
import logging
import re
import smtplib
import sys
import time
from collections import defaultdict
from datetime import date, datetime
from email.message import EmailMessage
from pathlib import Path

from openpyxl import load_workbook

from configuracao import carregar_config, conectar

PASTA = Path("treino_emails")
SAIDA = PASTA / "saida"
ANEXO = PASTA / "orientacoes.txt"
PAUSA_ENTRE_ENVIOS = 2  # segundos: provedores bloqueiam quem envia rápido demais
EMAIL_VALIDO = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

log = logging.getLogger("lembrete")


def configurar_log() -> None:
    """Registra no arquivo logs/lembrete.log e na tela. Só as mensagens deste script."""
    if log.handlers:  # já configurado (main() chamado de novo)
        return
    (PASTA / "logs").mkdir(parents=True, exist_ok=True)
    formato = logging.Formatter("%(asctime)s %(levelname)-7s %(message)s", datefmt="%d/%m/%Y %H:%M:%S")
    for destino in (logging.FileHandler(PASTA / "logs" / "lembrete.log", encoding="utf-8"),
                    logging.StreamHandler(sys.stdout)):
        destino.setFormatter(formato)
        log.addHandler(destino)
    log.setLevel(logging.INFO)


def ler_pendencias(caminho: Path) -> tuple[dict[str, dict], list[str]]:
    """Agrupa as pendências por e-mail. Devolve (alunos, problemas)."""
    alunos, problemas = {}, []
    planilha = load_workbook(caminho, read_only=True)["Pendências"]
    for numero, (nome, email, trabalho, prazo) in enumerate(planilha.iter_rows(min_row=2, values_only=True), start=2):
        email = (email or "").strip()
        if not EMAIL_VALIDO.match(email):
            problemas.append(f"linha {numero}: {nome} sem e-mail válido ({email or 'vazio'})")
            continue
        if isinstance(prazo, datetime):
            prazo = prazo.date()
        aluno = alunos.setdefault(email, {"nome": nome, "trabalhos": []})
        aluno["trabalhos"].append((prazo, trabalho))
    return alunos, problemas


def montar(remetente: str, email: str, aluno: dict, hoje: date) -> EmailMessage:
    primeiro_nome = aluno["nome"].split()[0]
    linhas_texto, linhas_html = [], []
    for prazo, trabalho in sorted(aluno["trabalhos"]):
        situacao = "ATRASADO" if prazo < hoje else f"prazo {prazo:%d/%m}"
        linhas_texto.append(f"- {trabalho} ({situacao})")
        cor = "#9C0006" if prazo < hoje else "#10202A"
        linhas_html.append(f'<li style="color:{cor}">{trabalho} (<strong>{situacao}</strong>)</li>')

    msg = EmailMessage()
    msg["From"] = remetente
    msg["To"] = f"{aluno['nome']} <{email}>"
    quantidade = len(aluno["trabalhos"])
    msg["Subject"] = f"Lembrete: {quantidade} trabalho{'s' if quantidade > 1 else ''} pendente{'s' if quantidade > 1 else ''}"
    msg.set_content(
        f"Olá, {primeiro_nome}!\n\nEstes trabalhos ainda não foram entregues:\n\n"
        + "\n".join(linhas_texto)
        + "\n\nAs orientações estão no anexo. Qualquer dúvida, fale comigo na aula.\n\nAbraço,\nProfessor\n"
    )
    msg.add_alternative(
        f"<p>Olá, <strong>{primeiro_nome}</strong>!</p><p>Estes trabalhos ainda não foram entregues:</p>"
        f"<ul>{''.join(linhas_html)}</ul>"
        "<p>As orientações estão no anexo. Qualquer dúvida, fale comigo na aula.</p><p>Abraço,<br>Professor</p>",
        subtype="html",
    )
    msg.add_attachment(ANEXO.read_bytes(), maintype="text", subtype="plain", filename=ANEXO.name)
    return msg


def main(enviar: bool) -> int:
    configurar_log()
    modo = "ENVIO" if enviar else "SIMULAÇÃO"
    log.info("Início (%s)", modo)
    try:
        config = carregar_config()
        alunos, problemas = ler_pendencias(PASTA / "pendencias.xlsx")
    except Exception as erro:  # qualquer erro de configuração ou de leitura para tudo, com registro
        log.error("Não foi possível começar: %s", erro)
        return 1
    for problema in problemas:
        log.warning(problema)

    hoje = date.today()
    mensagens = [(email, montar(config.remetente, email, aluno, hoje)) for email, aluno in alunos.items()]
    enviados = falhas = 0
    if not enviar:
        rascunhos = SAIDA / "rascunhos"
        rascunhos.mkdir(parents=True, exist_ok=True)
        for email, msg in mensagens:
            (rascunhos / f"{email}.eml").write_bytes(bytes(msg))
            log.info("Rascunho: %s -> %s", email, msg["Subject"])
    else:
        try:
            servidor = conectar(config)
        except (OSError, smtplib.SMTPException) as erro:
            log.error("Não consegui conectar a %s:%d (o servidor está ligado? o .env está certo?): %s",
                      config.servidor, config.porta, erro)
            return 1
        with servidor:
            for i, (email, msg) in enumerate(mensagens):
                try:
                    servidor.send_message(msg)
                    enviados += 1
                    log.info("Enviado: %s -> %s", email, msg["Subject"])
                except smtplib.SMTPException as erro:
                    falhas += 1
                    log.error("Falhou: %s (%s)", email, erro)
                if i < len(mensagens) - 1:
                    time.sleep(PAUSA_ENTRE_ENVIOS)
    log.info("Fim: %d e-mail(s) %s, %d falha(s), %d aluno(s) sem e-mail válido",
             len(mensagens) if not enviar else enviados, "em rascunho" if not enviar else "enviados",
             falhas, len(problemas))
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main(enviar="--enviar" in sys.argv))
```

## Rodando: primeiro a simulação

```text
> python lembrete_semanal.py
08/11/2026 17:48:09 INFO    Início (SIMULAÇÃO)
08/11/2026 17:48:09 WARNING linha 6: Diego Rocha sem e-mail válido (vazio)
08/11/2026 17:48:09 WARNING linha 7: Elisa Prado sem e-mail válido (elisa.prado@example)
08/11/2026 17:48:09 INFO    Rascunho: ana.souza@example.com -> Lembrete: 1 trabalho pendente
08/11/2026 17:48:09 INFO    Rascunho: bruno.lima@example.com -> Lembrete: 2 trabalhos pendentes
08/11/2026 17:48:09 INFO    Rascunho: carla.mendes@example.com -> Lembrete: 1 trabalho pendente
08/11/2026 17:48:09 INFO    Fim: 3 e-mail(s) em rascunho, 0 falha(s), 2 aluno(s) sem e-mail válido
```

Abra o rascunho do Bruno (`treino_emails/saida/rascunhos/bruno.lima@example.com.eml`): **um** e-mail com os **dois** trabalhos, o atrasado primeiro e em vermelho:

```text
Olá, Bruno!

Estes trabalhos ainda não foram entregues:

- Resumo do capítulo 4 (ATRASADO)
- Pesquisa sobre golpes no WhatsApp (prazo 11/11)
```

## Depois o envio (para o servidor de teste)

Com o servidor de teste ligado no outro terminal ([aula 02](02_servidor_de_teste.md#ligando-o-servidor-de-teste)) e o `.env` apontando para ele:

```text
> python lembrete_semanal.py --enviar
... INFO    Início (ENVIO)
... WARNING linha 6: Diego Rocha sem e-mail válido (vazio)
... WARNING linha 7: Elisa Prado sem e-mail válido (elisa.prado@example)
... INFO    Enviado: ana.souza@example.com -> Lembrete: 1 trabalho pendente
... INFO    Enviado: bruno.lima@example.com -> Lembrete: 2 trabalhos pendentes
... INFO    Enviado: carla.mendes@example.com -> Lembrete: 1 trabalho pendente
... INFO    Fim: 3 e-mail(s) enviados, 0 falha(s), 2 aluno(s) sem e-mail válido
```

Os três e-mails aparecem no terminal do servidor, com 2 segundos entre eles.

## Dois problemas que o teste achou

**1. Servidor desligado derrubava o script.** Na primeira versão, a conexão (`conectar(config)`) ficava fora de qualquer `try`. Com o servidor de teste desligado, o script terminava com um `ConnectionRefusedError` e um traceback **na tela**, e o log não registrava nada. Rodando pelo Agendador, ninguém veria. Agora a conexão está num `try` e o log registra:

```text
ERROR   Não consegui conectar a localhost:8025 (o servidor está ligado? o .env está certo?): [WinError 10061] ...
```

e o script termina com **código 1**, que aparece no Agendador.

**2. O log "de outra pessoa" aparecia no nosso.** A primeira versão usava `logging.basicConfig(...)`, que configura o log **de todo o programa**. Resultado: as mensagens internas da biblioteca do servidor de teste (`connection lost`...) apareciam misturadas no `lembrete.log`. A versão final configura **só o log do script** (`logging.getLogger("lembrete")`) e acrescenta os destinos a ele. Regra prática: num script simples, `basicConfig` serve; num script que usa bibliotecas barulhentas ou que vai ser importado, use um log com nome próprio.

## Como ele está organizado

| Parte | Faz |
|---|---|
| `EMAIL_VALIDO` | Expressão regular simples: algo, `@`, algo, `.`, algo. Pega o vazio e o `elisa.prado@example` |
| `ler_pendencias()` | Agrupa por e-mail com `setdefault` e junta os problemas |
| `montar()` | Um `EmailMessage` por aluno, trabalhos em ordem de prazo, singular/plural no assunto |
| `main(enviar)` | Simulação ou envio, pausa entre envios, log e código de saída |
| `configuracao.py` | `.env`, validação e conexão ([aula 03](03_env_e_configuracao.md)) |

!!! tip "Agendando o projeto"
    O `rodar_lembrete.bat` da [aula 04](04_logs_e_agendamento.md#o-bat-um-atalho-para-o-agendador) já chama `lembrete_semanal.py --enviar`. Agende para segunda às 8h **só depois** de rodar a simulação e o envio de teste algumas vezes e de combinar com a turma.

---

## ⚠️ Erros comuns

- **Rodar `--enviar` com o `.env` do Gmail sem ter visto a simulação.**
- **Mandar um e-mail por linha da planilha** (o Bruno receberia dois): agrupe por pessoa.
- **Ignorar os avisos de e-mail inválido**: os alunos sem e-mail **não** foram avisados. Alguém precisa corrigir a planilha (ou avisar pessoalmente).
- **Tirar a pausa entre envios** para "ir mais rápido": provedores bloqueiam.
- **Planilha aberta no Excel enquanto o agendador roda**: em geral a leitura funciona, mas salve e feche antes do horário agendado para o script ler a versão mais nova.

---

## Exercícios

### Básico (fixação)

Mude a pausa entre envios para **5 segundos** e o assunto para começar com **"[Turma 1A]"**. Rode a simulação e confira o assunto nos rascunhos.

<!-- gabarito -->
??? success "Gabarito — Básico"
    A pausa é a constante do começo do arquivo:

    ```python
    PAUSA_ENTRE_ENVIOS = 5  # segundos: provedores bloqueiam quem envia rápido demais
    ```

    E, dentro de `montar()`, o assunto ganha o prefixo:

    ```python
    quantidade = 2
    plural = "s" if quantidade > 1 else ""
    assunto = f"[Turma 1A] Lembrete: {quantidade} trabalho{plural} pendente{plural}"
    print(assunto)
    ```

    Na linha `msg["Subject"] = ...` do script, basta acrescentar `[Turma 1A] ` no começo do texto. O assunto do Bruno fica `[Turma 1A] Lembrete: 2 trabalhos pendentes`.

### Intermediário (aplicação)

Escreva a função `quanto_falta(prazo, hoje)` que devolve o texto da situação: `"ATRASADO há 2 dias"`, `"vence HOJE"`, `"vence amanhã"` ou `"faltam 5 dias"`. Use-a no lugar de `"ATRASADO"` / `"prazo dd/mm"` dentro de `montar()`.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```python
    from datetime import date, timedelta


    def quanto_falta(prazo: date, hoje: date) -> str:
        dias = (prazo - hoje).days
        if dias < 0:
            return f"ATRASADO há {-dias} dia{'s' if -dias > 1 else ''}"
        if dias == 0:
            return "vence HOJE"
        if dias == 1:
            return "vence amanhã"
        return f"faltam {dias} dias"


    hoje = date(2026, 11, 8)
    testes = {d: quanto_falta(hoje + timedelta(days=d), hoje) for d in (-2, -1, 0, 1, 5)}
    for dias, texto in testes.items():
        print(f"{dias:+d} -> {texto}")
    ```

    Subtrair duas datas dá um `timedelta`, e `.days` é o número de dias (negativo se o prazo já passou). Os testes mostram todos os casos: `ATRASADO há 2 dias`, `ATRASADO há 1 dia`, `vence HOJE`, `vence amanhã`, `faltam 5 dias`. No `montar()`, troque a linha do `situacao = ...` por `situacao = quanto_falta(prazo, hoje)`.

### Avançado (desafio)

Além dos lembretes aos alunos, o professor quer receber **um resumo**: um e-mail para `professor@example.com` com a lista de quem foi avisado e de quem ficou **sem e-mail válido**. Escreva a função `montar_resumo(alunos, problemas)` usando as funções do projeto.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```python
    from email.message import EmailMessage
    from pathlib import Path

    from lembrete_semanal import ler_pendencias


    def montar_resumo(alunos: dict, problemas: list[str]) -> EmailMessage:
        avisados = [f"- {a['nome']} ({len(a['trabalhos'])} trabalho(s))" for a in alunos.values()]
        msg = EmailMessage()
        msg["From"] = "professor@example.com"
        msg["To"] = "professor@example.com"
        msg["Subject"] = f"Resumo do lembrete: {len(alunos)} avisados, {len(problemas)} sem e-mail"
        msg.set_content(
            "Avisados:\n" + "\n".join(avisados)
            + "\n\nSem e-mail válido (avisar pessoalmente ou corrigir a planilha):\n"
            + "\n".join(f"- {p}" for p in problemas)
        )
        return msg


    alunos, problemas = ler_pendencias(Path("treino_emails") / "pendencias.xlsx")
    resumo = montar_resumo(alunos, problemas)
    print(resumo["Subject"])
    print(resumo.get_content())
    ```

    Assunto: `Resumo do lembrete: 3 avisados, 2 sem e-mail`. Importar `ler_pendencias` não roda o lembrete, graças ao `if __name__ == "__main__":` do projeto. Para enviar o resumo junto, chame `servidor.send_message(resumo)` no fim do `main()`, dentro do modo de envio.

---

## 💡 Resumo

- **Agrupar** por pessoa, **validar** e-mails e **registrar** quem ficou de fora.
- **Simulação** (rascunhos `.eml`) é o padrão; **envio** só com `--enviar`, pelo servidor do `.env`.
- Conexão dentro de `try`, log com **nome próprio**, **código de saída** para o Agendador.
- Pausa entre envios, um e-mail por pessoa, agendamento só depois de testar.

## ➡️ Próximo passo

**[Módulo 05 — Projeto final](../modulo_05_projeto_final/index.md)**: a **Secretaria automática**, juntando arquivos, planilhas, documentos e e-mails numa ferramenta só.
